# B1b: isolated exact-runtime feasibility

Status: **no established practical route; incomplete assessment stopped on source-access error**.
2026-11-22; original GPT-6 Astra (`gpt-6-astra`) / OpenCode worker.
[Issue #26](https://github.com/Himanshu-singh04/releaselens/issues/26), fixed A1–A6;
[founder assent](https://github.com/Himanshu-singh04/releaselens/pull/25#issuecomment-7077759962)
was “ok proceedc” to the sole bounded feasibility request.
Base `c2d56ef6ec90ba5121cf9d486cd3e0b382a9c22f`; start 10:24:38 UTC, stop by 11:24:38 UTC.
Research stopped on the third request at 10:26:11 UTC; stop record written 10:26:44 UTC.

## Scope and preserved blocker

Assess CPython **3.14.10, standard GIL, arm64**, with **rfc8785 0.1.4**, $0 new spend.
At most four primary public documents and two concrete isolated paths; stop when supported.
Only document/metadata retrieval: no artifact acquisition/extraction, build, installation,
runtime/tool experiment, host probe, service/PATH/trust change or substituted pin.
Two candidates considered: official source built for a private non-framework prefix, and
Astral python-build-standalone for the exact target. Neither is approved or qualified.

[B1a coordinator review](https://github.com/Himanshu-singh04/releaselens/pull/25#issuecomment-7076949825)
confirmed the correct stop, not completion. Mandatory official .pkg payload changes shared
Current from 3.13 to 3.14; uninspected/dynamic consumer impact remains unknown. No denied
Docker-helper read is retried. Existing Homebrew 3.14.9 is not the target.
Pending #25 head `506d735252747c8a9d84e12e1c4db07cd7a8a9e8`, its note, cache and raw evidence
remain on the preserved ref; the pending note is not brought onto this branch.

The [accepted packet](006-runtime-validation-scope.md), [contract](../evidence-contract.md)
and [testing](../testing.md) retain their policy/oracle authority. D1–D4 remain unadopted;
M0/M1–M4, privacy/customer storage and the 60-second terminal deadline gates remain open.

## Source ledger and mandatory stop

Retrieved 2026-11-22 with existing curl, verified HTTPS, no redirect/retry options.
Three requests attempted, two documents received; no search snippets or fourth source.
Repository/issue authority and prior reviewed evidence are separate from this public-source cap.

| ID / primary URL | Version scope, locator and observed evidence |
| --- | --- |
| S1: [Python release](https://www.python.org/downloads/release/python-31410/) | 3.14.10; heading and Source release/Files rows name `Python-3.14.10.tar.xz` and `Python-3.14.10.tgz`. HTTP 200, TLS result 0, 46,491 bytes. Published source availability, not acquisition or build qualification. |
| S2: [CPython configuration](https://docs.python.org/release/3.14.10/using/configure.html) | 3.14.10; Build Requirements names a C11 compiler; installation options include `--prefix`, with example `--prefix="$HOME/.local/"`; optional-module and GIL configuration sections exist. HTTP 200, TLS result 0, 193,273 bytes. Only preliminary locators examined before stop; no complete dependency/configuration review. |
| S3 attempted: [standalone README](https://raw.githubusercontent.com/astral-sh/python-build-standalone/main/README.rst) | Moving main, no verified version scope: **HTTP 404, curl exit 56**, TLS result 0, zero body bytes. Requested filename was not established as valid. This proves a failed URL, not absence of the project or exact distribution. |

The third request failed at 10:26:11 UTC. The planned fourth request, release metadata at
`https://api.github.com/repos/astral-sh/python-build-standalone/releases/latest`, was never
sent. No corrected filename, alternate URL/transport or additional source was tried.
The no-retry stop applies even if the failed filename might be correctable. Remaining
public-document analysis was not completed; nothing below promotes a missing fact to support.

## Candidate assessment and effects still requiring evidence

**C1 — official source, private non-framework prefix.** S1 identifies exact-version source
at `https://www.python.org/ftp/python/3.14.10/Python-3.14.10.tar.xz`; no source bytes acquired,
hash/signature verified or source archive license/dependency inventory inspected here.
Prior packet records PSF licensing with incorporated notices, not this build's complete closure.
S2's prefix option supports investigating a private destination, not a completed non-framework
recipe or relocatability guarantee. C11 compiler availability, SDK/tool versions, selected
dependencies, standard-GIL/arm64 configuration and linked-library identity remain unverified.
No developer-tool availability probe, build, configure or interpreter invocation occurred.

Proposed future location, not created: `/Volumes/AIWorkspace/caches/releaselens/b1b-runtime/`,
with separate source/build/private-prefix subdirectories and explicit interpreter path.
Intent: install directly to the final prefix without shared framework, PATH, service or trust
writes; no later relocation assumed. Admin-free operation would depend on already available
tools and writable locations, neither established here. New tools/dependency downloads are
not approved. Source/build/network/space needs cannot yet be bounded within the original
<100 MB transfer and 2 GiB per-device allowances; build time and $0 feasibility are unknown.
Thus C1 is a documented starting point, **not an execution-ready recommendation**.

**C2 — exact standalone distribution.** The project-specific source failed before supporting
facts were obtained. No exact 3.14.10 standard-GIL Apple Silicon asset URL, digest, size,
release identity, signing, license/dependency closure or relocation/support claim verified.
Proposed destination would be a separate subtree of the same private cache, using an explicit
path. Build/tool/admin/network/space needs and shared-link/PATH/service/trust effects remain
unknown; do not assume archive extraction means supported isolation. A third-party artifact
would require separate selection/authorization even if its upstream version matched.

For both candidates, the retained rfc8785 0.1.4 wheel identity remains the packet's exact
9,240-byte file, SHA-256 `520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48`.
B1a observed a pure wheel with optional-only dependencies; complete license/source review,
bootstrap-tool identity and target compatibility remain pending. No new wheel request/import.
Existing Homebrew, shared .pkg relocation, containers and other paths were not added as candidates.

## Decision, next boundary and delivery

**No established route from this interrupted assessment.** This is not proof that either
candidate is infeasible. Exact source availability alone does not establish a practical
isolated build; the standalone path lacks the required primary evidence. B1a-I1 stays open.
No acquisition/install/build permission packet is ready. Any resumption of the stopped
assessment requires separate authorization; none is requested or dispatched automatically.
Any later execution also needs explicit artifact/tool/dependency identities, paths, network/
space/time limits and shared-state effects. Missing identity/closure, unapproved dependencies,
budget overrun, shared-state writes or provider/quota/transport error must stop that work.
The original oracle-before-execution requirement, 96-new-check/105-historical-control split,
two-run cap and unqualified product/privacy/deadline gates remain; no harness is prepared.

Raw requests/headers, successful bodies, preliminary text views and stop record are retained
under ignored `artifacts/b1b/`; the PR records their manifest hash and exact command outcomes.
B1a's 63-entry manifest remains `3e315c25babd13e574580539a07b8a24bc555fa1c28606e97414a547fac3a655`.
No artifact acquisition, extraction, build/install, target/host experiment or settings change.
A1 authority/exact target established; A2 evidence and A3 effects analysis partial; A4 returns
no established path; A5 preserves the next permission boundary; A6 checkpoint checks/attribution/
exact-head CI and literal Sourcery are recorded in the PR. Independent review remains pending.
