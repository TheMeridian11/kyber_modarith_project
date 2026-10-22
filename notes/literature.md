# Literature and idea provenance

Use APA 7 references and verified locators in the thesis. These entries seed the record from the 29 September 2026 review. No new literature retrieval occurred in the 22 October setup session. Bibliographic verification and full-text review are distinct.

## LIT-001 Modular arithmetic optimisation

Zelenetsky, A. S., & Klyucharev, P. G. (2024). Modular arithmetic optimization in Kyber KEM. *Journal of Computer Virology and Hacking Techniques, 20*, 857–865. https://doi.org/10.1007/s11416-024-00537-x

- Inspected: publisher abstract/accessible preview in the earlier review; full experimental configuration not reviewed.
- Context: wider arithmetic reduces modular reductions; the authors report maximum speedups of 1.41 times for key generation, 1.58 for encapsulation and 1.83 for decapsulation.
- Project relationship: motivation for EXP-002 and the research question. These are literature results, not project forecasts.
- Attribution boundary: exact EXP-001/EXP-003 proposals arose from our source analysis; do not attribute those rearrangements to this paper without checking its full text.
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

## New-source fields

- Literature ID and verified APA 7 reference:
- DOI/stable URL and version:
- Review date and scope: abstract/full text/code:
- Claim supported in our own words:
- Verified page/section/code locator:
- Linked experiments:
- Platform/protocol differences from our study:
- Unverified claims and outstanding checks:
