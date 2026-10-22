# Literature and idea provenance

I use APA 7 references and verified locators in the thesis. These entries retain the findings of the preliminary literature review. No new literature retrieval occurred during ACT-0001 or ACT-0002. Bibliographic verification and full-text review are distinct; publication years are retained.

## LIT-001 Modular arithmetic optimisation

Zelenetsky, A. S., & Klyucharev, P. G. (2024). Modular arithmetic optimization in Kyber KEM. *Journal of Computer Virology and Hacking Techniques, 20*, 857–865. https://doi.org/10.1007/s11416-024-00537-x

- Inspected: publisher abstract/accessible preview in the earlier review; full experimental configuration not reviewed.
- Context: wider arithmetic reduces modular reductions; the authors report maximum speedups of 1.41 times for key generation, 1.58 for encapsulation and 1.83 for decapsulation.
- Project relationship: motivation for EXP-002 and the research question. These are literature results, not project forecasts.
- Attribution boundary: exact EXP-001/EXP-003 proposals arose from the source analysis; do not attribute those rearrangements to this paper without checking its full text.
- Outstanding: review the full paper through legitimate access before claiming faithful replication or citing its detailed protocol; add verified page/section locators.

## LIT-002 Final ML-KEM standard

National Institute of Standards and Technology. (2024). *Module-lattice-based key-encapsulation mechanism standard* (FIPS PUB 203). https://doi.org/10.6028/NIST.FIPS.203

- Inspected: official publication landing page in the earlier review.
- Relationship: terminology and algorithm context. Final-standard conformance of the pinned implementation has not been established.
- Outstanding: inspect the applicable standard text and errata for any conformance claim; the landing page alone is insufficient.

## LIT-003 Experimental software

pq-crystals. (n.d.). *Kyber* (Commit 3edd5af5991927164edd4aacebfcbee00b8064e7) [Computer software]. GitHub. https://github.com/pq-crystals/kyber/tree/3edd5af5991927164edd4aacebfcbee00b8064e7

- Inspected: local pinned source and provenance; upstream README in the earlier review.
- Relationship: EXP-000 and every implementation comparison.
- Reproduction: preserve pinned source, project/harness revisions, build commands and binary hashes.

## LIT-004 Statistical timing evidence

Source: https://github.com/oreparaz/dudect

- Inspected: authors' repository README in the earlier review.
- Relationship: possible focused timing-behaviour checks; none has been performed here.
- Limitation: failure to detect leakage is not a constant-time proof.
- Outstanding: verify complete APA publication metadata for the associated DATE 2017 paper before adding its thesis reference.

## LIT-005 Compiler instrumentation scope

Free Software Foundation. (n.d.). *Program instrumentation options*. In *Using the GNU Compiler Collection (GCC 13.3.0)*. https://gcc.gnu.org/onlinedocs/gcc-13.3.0/gcc/Instrumentation-Options.html

- Inspected in ACT-0010: the official entries for signed-integer-overflow instrumentation/integer promotions and stack-protector variants. This was a targeted documentation check, not a review of the entire manual.
- Relationship: EXP-003's explicit narrowing bounds cannot be replaced by a passing UBSan run. GCC describes overflow checks in terms of promoted arithmetic and gives an example where a small signed object's increment is not an overflow of that promoted arithmetic.
- Stack context: protection selection can depend on local arrays/actual stack allocation. This supports interpretation of the EXP-002 observation, while the actual presence/absence of its canary comes from the saved assembly.
- Scope: compiler documentation supports the interpretation of these checks; it does not validate the cryptographic implementation or prove constant-time behaviour.

## New-source fields

- Literature ID and verified APA 7 reference:
- DOI/stable URL and version:
- Review activity ID and scope: abstract/full text/code:
- Claim supported in my own words:
- Verified page/section/code locator:
- Linked experiments:
- Platform/protocol differences from my study:
- Unverified claims and outstanding checks:
