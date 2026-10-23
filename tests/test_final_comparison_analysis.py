#!/usr/bin/env python3
"""Protect matching, effect definitions and complete order coverage."""
import copy
import itertools
import sys
import unittest
from unittest.mock import patch
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
import analyse_final_comparison as analysis
import run_final_comparison as runner

def fixture():
    return [dict(parameter_set=f"Kyber{k}",operation=op,block=b,variant=v,samples=1000,
                 fixture_seed=b,position=i+1,median_ns=([100,1000][b-1] * factor))
            for k,op,b in itertools.product(analysis.PARAMETERS,("keygen","encap","decap"),(1,2))
            for i,(v,factor) in enumerate((("baseline",1),("exp003",[.8,.6][b-1]),("exp005",.5)))]

class AnalysisTests(unittest.TestCase):
    def test_matched_effect_not_ratio_of_medians(self):
        pairs,rows=analysis.derive(fixture(),2,1)
        row=next(r for r in rows if r["reference"]=="baseline" and r["candidate"]=="exp003")
        self.assertAlmostEqual(row["median_paired_improvement_pct"],30)
        self.assertNotAlmostEqual(100*(1-row["candidate_median_of_medians_ns"]/row["reference_median_of_medians_ns"]),30)
        self.assertEqual(len(pairs),54);self.assertEqual(len(rows),27)
    def test_reject_bad_matching_and_coverage(self):
        rows=fixture()
        for changed in (rows[:-1],rows+[rows[0]]):
            with self.assertRaises(ValueError):analysis.derive(changed,2,1)
        for key,value in (("fixture_seed",9),("samples",999),("median_ns",0)):
            changed=copy.deepcopy(rows);changed[1][key]=value
            with self.assertRaises(ValueError):analysis.derive(changed,2,1)
    def test_session_units_and_rejected_duplicates(self):
        manifests=[];tables=[]
        for session,effect in enumerate((10.0,0.0,-4.0),1):
            m=dict(session=session,protocol={},source_file_sha256={},support_file_sha256={},compiler={},build_flags=[],tool_sha256={})
            _,table=analysis.derive(fixture(),2,session)
            for row in table:row["median_paired_improvement_pct"]=effect
            manifests.append(m);tables.append(table)
        def read(index):return manifests[index],tables[index]
        with patch.object(analysis,"read_run",side_effect=read):
            _,_,combined=analysis.combine([0,1,2])
            self.assertEqual(combined[0]["median_session_improvement_pct"],0)
            self.assertEqual(combined[0]["positive_sessions"],1)
            self.assertEqual(combined[0]["negative_sessions"],1)
            with self.assertRaises(ValueError):analysis.combine([0,0,2])
            manifests[2]["compiler"]={"sha256":"changed"}
            with self.assertRaises(ValueError):analysis.combine([0,1,2])
    def test_balanced_order_and_disjoint_seeds(self):
        p=runner.load_protocol();all_seeds=[]
        for session in (1,2,3):
            all_seeds.extend(p["session_seeds"][session-1]+b-1 for b in range(1,13))
            for k in analysis.PARAMETERS:
                orders=[tuple(runner.order_for_block(p,session,b,k)) for b in range(1,13)]
                for permutation in itertools.permutations(analysis.VARIANTS):self.assertEqual(orders.count(permutation),2)
                for v in analysis.VARIANTS:
                    for position in range(3):self.assertEqual(sum(order[position]==v for order in orders),4)
        self.assertEqual(len(set(all_seeds)),36)
if __name__=="__main__":unittest.main()
