"""Numerical oracle and corrupt-stream checks for the security analysis."""
import json,math,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import analyse_timing_leakage as a
class AnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory(prefix='kyber-welch-');cls.base=Path(cls.temp.name)
        cls.exe=cls.base/'reference'
        subprocess.run(['gcc','-O2',str(ROOT/'tests/check_welch_reference.c'),'-lm','-o',str(cls.exe)],check=True,capture_output=True)
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()
    def stream(self,fn):
        rows=[a.RECORD.pack(*fn(i)) for i in range(6000)]
        p=self.base/'raw.bin';p.write_bytes(b'KTL00801'+b''.join(rows));return p
    def test_pinned_numerical_oracle(self):
        for shift in (0,17,1000000):
            x=[float(100+shift+(i*13)%19) for i in range(937)]
            y=[float(103+shift+(i*7)%23) for i in range(1103)]
            for second in (False,True):
                mean=sum(x+y)/(len(x)+len(y));xx=[(v-mean)**2 for v in x] if second else x;yy=[(v-mean)**2 for v in y] if second else y
                text=''.join(f'{c} {v:.17g}\n' for c,arr in enumerate((xx,yy)) for v in arr)
                ref=float(subprocess.run([str(self.exe)],input=text,text=True,capture_output=True,check=True).stdout)
                self.assertTrue(math.isclose(a.welch(xx,yy)['t'],ref,rel_tol=1e-7,abs_tol=1e-7))
    def test_known_signal_and_constant_cases(self):
        p=self.stream(lambda i:(100+(i&1)*100+(i//2)%7,0,0,i&1));m=a.analyse(p,4000,100);self.assertTrue(m['adequate'] and m['flag'])
        self.assertEqual(a.welch([1]*20,[1]*20)['t'],0)
        self.assertTrue(a.welch([1]*20,[2]*20)['flag'])
        self.assertIsNone(a.welch([1]*20,[2]*20)['t'])
    def test_truncation_class_and_balance_rejected(self):
        p=self.stream(lambda i:(100+(i//2)%7,0,0,i&1));p.write_bytes(p.read_bytes()[:-1])
        with self.assertRaises(ValueError):a.analyse(p,4000,100)
        p=self.stream(lambda i:(100,0,0,2 if i==20 else i&1))
        with self.assertRaises(ValueError):a.analyse(p,4000,100)
        p=self.stream(lambda i:(100,0,0,0))
        with self.assertRaises(ValueError):a.analyse(p,4000,100)
    def test_migration_and_invalid_duration_preserved(self):
        p=self.stream(lambda i:(0 if i==3000 else 100+(i//2)%7,0,1 if i==4000 else 0,i&1));m=a.analyse(p,4000,100)
        self.assertEqual(m['excluded_indices'],[3000,4000]);self.assertTrue(m['adequate'])
        p=self.stream(lambda i:(100+(i//2)%7,0,1 if 2000<=i<2200 else 0,i&1));self.assertFalse(a.analyse(p,4000,100)['adequate'])
if __name__=='__main__':unittest.main()
