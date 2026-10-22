# Literature and idea provenance

I use APA 7 references and verified locators in the thesis. These entries retain the findings of the preliminary literature review. No new literature retrieval occurred during ACT-0001 or ACT-0002. Bibliographic verification and full-text review are distinct; publication years are retained.

## LIT-001 Modular arithmetic optimisation

Zelenetsky, A. S., & Klyucharev, P. G. (2024). Modular arithmetic optimization in Kyber KEM. *Journal of Computer Virology and Hacking Techniques, 20*, 857–865. https://doi.org/10.1007/s11416-024-00537-x

- Inspected: publisher abstract/accessible preview in the earlier review; full experimental configuration not reviewed.
- Context: wider arithmetic reduces modular reductions; the authors report maximum speedups of 1.41 times for key generation, 1.58 for encapsulation and 1.83 for decapsulation.
- Project relationship: motivation for EXP-002 and the research question. These are literature results, not project forecasts.
- Attribution boundary: exact EXP-001/EXP-003/EXP-005/EXP-006 proposals arose from the source analysis; do not attribute those rearrangements to this paper without checking its full text.
- Outstanding: review the full paper through legitimate access before claiming faithful replication or citing its detailed protocol; add verified page/section locators.

## LIT-002 Final ML-KEM standard

National Institute of Standards and Technology. (2024). *Module-lattice-based key-encapsulation mechanism standard* (FIPS PUB 203). https://doi.org/10.6028/NIST.FIPS.203

- Inspected: official publication landing page in the earlier review.
- Relationship: terminology and algorithm context. Final-standard conformance of the pinned implementation has not been established.
- Outstanding: inspect the applicable standard text and errata for any conformance claim; the landing page alone is insufficient.

## LIT-003 Experimental software

pq-crystals. (n.d.). *Kyber* (Commit 3edd5af5991927164edd4aacebfcbee00b8064e7) [Computer software]. GitHub. https://github.com/pq-crystals/kyber/tree/3edd5af5991927164edd4aacebfcbee00b8064e7

- Inspected: local pinned source and provenance; upstream README in the earlier review.
- Relationship: EXP-000 and every implementation comparison. ACT-0012 traced EXP-005's error-vector consumer and conservative forward-NTT/addition bounds directly through indcpa.c, polyvec.c, poly.c, ntt.c, reduce.c, params.h and cbd.c; no new external literature was retrieved for that local-source argument.
- ACT-0014: I traced EXP-006's keygen-only wide-dot output through poly_tomont, raw-error addition and the retained final public-key reduction. The proposal preserves general dot/inverse caller contracts. Its bounds/counts are local-source reasoning, not a result taken from an unreviewed publication.
- Reproduction: preserve pinned source, project/harness revisions, build commands and binary hashes.

## LIT-004 Statistical timing evidence

Reparaz, O. (n.d.). *dudect* [Computer software]. GitHub. https://github.com/oreparaz/dudect

- Inspected in ACT-0014: author-maintained repository README, its discussion of input classes/testing limits, and the [author's methodological discussion](https://www.reparaz.net/oscar/misc/dudect.html). This is repository/author-page review, not full-paper review.
- Relationship: the required focused implementation-security assessment will compare timing classes separately from throughput measurements. No leakage test has been executed in this project yet.
- Limitation: no detected difference within a tested budget is not a constant-time proof; compiler, platform and chosen secret classes matter. I will pin a tool revision and commit the protocol after a sensitivity pilot.
- Publication trail: the repository links the DATE 2017 paper by Oscar Reparaz, Josep Balasch and Ingrid Verbauwhede. The ePrint PDF retrieval at https://eprint.iacr.org/2016/1123.pdf returned HTTP 403 during ACT-0014. I do not claim to have read its full text.
- Outstanding: verify complete APA publication details and exact paper locators through legitimate access before using its detailed methods in the thesis. The practical tool choice here is supported by the inspected primary repository/author discussion.

## LIT-005 Compiler instrumentation scope

Free Software Foundation. (n.d.). *Program instrumentation options*. In *Using the GNU Compiler Collection (GCC 13.3.0)*. https://gcc.gnu.org/onlinedocs/gcc-13.3.0/gcc/Instrumentation-Options.html

- Inspected in ACT-0010: the official entries for signed-integer-overflow instrumentation/integer promotions and stack-protector variants. This was a targeted documentation check, not a review of the entire manual.
- Relationship: EXP-003/EXP-005 explicit narrowing bounds cannot be replaced by a passing UBSan run. GCC describes overflow checks in terms of promoted arithmetic and gives an example where a small signed object's increment is not an overflow of that promoted arithmetic.
- Stack context: protection selection can depend on local arrays/actual stack allocation. This supports interpretation of the EXP-002 observation, while the actual presence/absence of its canary comes from the saved assembly.
- Scope: compiler documentation supports the interpretation of these checks; it does not validate the cryptographic implementation or prove constant-time behaviour.

## LIT-006 Dynamic secret-flow checking

Valgrind Developers. (n.d.). *Memcheck: A memory error detector*. In *Valgrind user manual*. https://valgrind.org/docs/manual/mc-manual.html

Related primary demonstration: https://github.com/agl/ctgrind

- Inspected in ACT-0014: Memcheck section 4.2.2 on uninitialised-value uses and origin diagnostics; the ctgrind author's repository description of marking secrets and detecting their use in branches/addresses.
- Relationship: planned dynamic checks complement generated-code inspection and timing measurements. I will classify public/secret values, mark only secret operands, inspect reports and retain the exercised-path limits. A generic undefined-value warning needs diagnosis; it is not automatically a cryptographic vulnerability.
- Implementation decision: prefer supported installed Memcheck interfaces after inspecting the pinned headers rather than assuming an old ctgrind patch works. Tool installation, interface verification, harness sensitivity and actual checks remain pending.
- Scope: this technique does not certify all paths, hardware instruction timing, physical leakage or exhaustive memory safety. Public-matrix rejection branches require correct public-input classification.

## LIT-007 Performance profiling considered and excluded

Intel Corporation. (n.d.). *Hotspots analysis*. In *Intel VTune Profiler user guide* (Version 2025.4). https://www.intel.com/content/www/us/en/docs/vtune-profiler/user-guide/2025-4/basic-hotspots-analysis.html

- Inspected in ACT-0014: official Hotspots documentation, [collection-method documentation](https://www.intel.com/content/www/us/en/docs/vtune-profiler/user-guide/2025-4/collect.html), and [release/system requirements](https://www.intel.com/content/www/us/en/developer/articles/release-notes/vtune-profiler/current.html).
- Scope decision in ACT-0015: I excluded VTune from the remaining practical work at my request. I retain this earlier primary-source review as provenance, not a pending installation/profiling task. Existing raw CSV timing results support primary performance analysis.
- Constraints: software and hardware sampling have different collection requirements/overheads. WSL support does not establish which hardware events this local setup exposes. Check actual availability before relying on profiler metrics.
- Security boundary: hotspot/CPU measurements do not compare secret-input timing classes and do not replace the required leakage assessment. Keep profiling runs separate from primary normal-build timings.

## ACT-0016 tool-interface verification

I inspected the official Memcheck manual (sections 4.2.2 and 4.7) and the actual Ubuntu valgrind 1:3.22.0-0ubuntu3 package headers. In usr/include/valgrind/memcheck.h, VALGRIND_MAKE_MEM_UNDEFINED and VALGRIND_MAKE_MEM_DEFINED map to Memcheck client requests; valgrind.h supplies RUNNING_ON_VALGRIND. I inspected the emitted XML protocol 4, error kinds UninitCondition/UninitValue, completion states, origin stacks and occurrence counts in real positive-control executions. Exact package/header/runtime hashes and retained reports are in [ACT-0016 support evidence](evidence/ACT-0016/secret-flow-support-smoke.json). This is interface/source and local execution evidence, not a new whole-program proof or a full-text paper review. [Official manual](https://valgrind.org/docs/manual/mc-manual.html).

The [EXP-007 protocol](experiments/EXP-007-secret-flow.md) makes my use of undefined-value propagation explicit and distinguishes defined twins from marked secrets. Dynamic dependency checks and statistical timing tests answer complementary questions; numerical leakage-test budgets and a pinned dudect revision remain to be prepared. I do not claim that throughput plots or quiet Memcheck reports establish absence of every side channel.

## New-source fields

- Literature ID and verified APA 7 reference:
- DOI/stable URL and version:
- Review activity ID and scope: abstract/full text/code:
- Claim supported in my own words:
- Verified page/section/code locator:
- Linked experiments:
- Platform/protocol differences from my study:
- Unverified claims and outstanding checks:
