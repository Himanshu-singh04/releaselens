# B1b: isolated exact-runtime feasibility

Status: **bounded assessment complete; no practical route established within the unchanged limits**.
2026-11-22; original GPT-6 Astra (`gpt-6-astra`) / OpenCode worker.
[Issue #26](https://github.com/Himanshu-singh04/releaselens/issues/26), fixed A1–A6;
[founder assent](https://github.com/Himanshu-singh04/releaselens/pull/25#issuecomment-7077759962)
was “ok proceedc” to the sole bounded feasibility request.
Base `c2d56ef6ec90ba5121cf9d486cd3e0b382a9c22f`; start 10:24:38 UTC, stop by 11:24:38 UTC.
Initial conservative stop: 10:26:11 UTC; record written 10:26:44 UTC. Same-task correction
resumed at 10:33:26 UTC under [B1b-R1](https://github.com/Himanshu-singh04/releaselens/pull/27#issuecomment-7077859464),
without resetting the deadline. Earlier commit `99b729a0e3e52bf763b0434acbdde738842ac55a`
and stopped evidence remain unchanged. The 404 was a source gap, not a mandatory whole-task
stop or reason for new founder permission to finish this assessment; that earlier claim was wrong.

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

## Source ledger: four slots used, three documents received

Retrieved 2026-11-22 with existing curl, verified HTTPS, no redirect/retry options.
Four distinct requests including the failed S3; two candidates; no search calls or retries.
Repository/issue authority and prior reviewed evidence are separate from this public-source cap.

| ID / primary URL | Version scope, locator and observed evidence |
| --- | --- |
| S1: [Python release](https://www.python.org/downloads/release/python-31410/) | 3.14.10; Files/XZ source row: URL, 23.1 MB displayed, SHA-256, Sigstore/SPDX links. HTTP 200, TLS result 0, 46,491 bytes. Saved row analyzed in R1; no linked artifact fetched. |
| S2: [CPython configuration](https://docs.python.org/release/3.14.10/using/configure.html) | Versioned 3.14.10 URL; §§3.1–3.1.1, 3.3.6, 3.3.10, 3.3.13, 3.4.2–3.4.3 and `--disable-gil`. HTTP 200, TLS result 0, 193,273 bytes. Relevant saved sections fully analyzed in R1; forward-looking 3.15/3.16 notes are not applied to this target. |
| S3 attempted: [standalone README](https://raw.githubusercontent.com/astral-sh/python-build-standalone/main/README.rst) | Moving main, no verified version scope: **HTTP 404, curl exit 56**, TLS result 0, zero body bytes. Requested filename was not established as valid. This proves a failed URL, not absence of the project or exact distribution. |
| S4: [standalone release API](https://api.github.com/repos/astral-sh/python-build-standalone/releases/latest) | Retrieved once at 10:33:26–28 UTC in R1: HTTP 200, TLS result 0, 2,098,375 bytes. Release `20261110`, ID 441136779; `assets` entry ID 733713948 and release `body` analyzed below. Latest is a moving query; saved response fixes the observation. |

S4 was planned but unsent at the original stop; B1b-R1 expressly allowed that distinct request.
No retry of S3, corrected README filename, alternate transport or fifth source. No provider/
quota/transport error occurred; the HTTP 404 and overly broad local stop interpretation remain
disclosed. The source budget is exhausted, not extended by this correction.

## C1 — official source, private non-framework prefix

Exact published source: `https://www.python.org/ftp/python/3.14.10/Python-3.14.10.tar.xz`,
SHA-256 `de414a57119abef52784d8993e341d53aed635fc2b05c2607d9f98a2c5b72032`, displayed **23.1 MB**.
S1 links that URL plus `.sigstore` and `.spdx.json`; neither fetched. This is a new artifact,
not the approved .pkg. Published hash/provenance is not a local hash or signature verification.
Prior packet records PSF v2 and incorporated notices; exact source/build dependency-license
closure remains uninspected. No compiled binary would inherit the .pkg's PSF signature result.

S2 supplies affirmative isolation evidence, stronger than the earlier note acknowledged:
- §3.3.13 / `--enable-framework`: “Create a Python.framework rather than a traditional Unix
  install”; default **no**. A traditional non-framework build is documented, not package relocation.
- §3.3.6 / `--prefix`: architecture-independent files go to PREFIX; `--exec-prefix` defaults
  to PREFIX for architecture-dependent files. Explicit private prefix avoids default `/usr/local`.
- `--disable-gil` enables free-threading and defines `Py_GIL_DISABLED`; omit it for the intended
  standard build. §3.3.13 documents universal2 including arm64; it does not prove a native
  compiler invocation here emits arm64. Native arm64 build/SDK and final GIL identity need verification.
- §3.3.10: shared libpython defaults **no**; §3.4.2 describes static libpython linked into
  the executable. This avoids a shared Python framework design, not all dynamic dependencies.
- §3.3.6: `--with-ensurepip=no` suppresses automatic ensurepip during installation; default
  is upgrade. §3.4.3.6 says `make install` builds and installs: it is execution, not inert copying.

Proposed final prefix: `/Volumes/AIWorkspace/caches/releaselens/b1b-runtime/source-prefix/`,
with sibling source/build/scratch directories. Install at that final prefix; do not assume
later relocation. Use only its explicit interpreter path, no activation or PATH/profile links.
The design needs no shared Current, Applications, receipts, service or trust writes; actual
build/install scripts and output/linkage would still need inspection. No admin action is
intended if existing tools and writable private paths suffice; neither condition was probed.

Practical constraints: S2 §3.1 requires C11, IEEE 754/NaN and threads. §3.1.1 requires headers/
libraries for optional modules and says missing modules are reported by configure/make.
Examples material to later validation: zlib for ensurepip; OpenSSL for ssl (hashlib has bundled
fallbacks); decimal has a pure-Python fallback without libmpdec. These are documented behaviors,
not authorization to silently accept a reduced stdlib. Compiler/SDK/make, module inventory,
linked dependencies and bootstrap wheel versions/licenses are unknown on this host.
No PGO/LTO/JIT, tool installation or dependency acquisition is proposed as an implicit fallback.
The compressed source alone appears below 100 MB; exact bytes, expanded/build/venv peaks and
dependency downloads are not established within **2 GiB per device / <100 MB transfer**.
Private-prefix configuration is supported; practical fit at $0 with existing tools is unproved.

## C2 — exact standalone archive

S4 lists `cpython-3.14.10+20261110-aarch64-apple-darwin-install_only.tar.gz`, asset **733713948**,
**27,109,898 bytes**, digest **`sha256:42031ed5f0d38777335252c8c77d64708c8010dd67c128246bdec25000672666`**.
Exact URL: `https://github.com/astral-sh/python-build-standalone/releases/download/20261110/cpython-3.14.10%2B20261110-aarch64-apple-darwin-install_only.tar.gz`.
Release ID 441136779, published 2026-11-11T01:51:17Z, draft/prerelease false, immutable true;
target_commitish `9244801782b78e4c4afc5c82a4524aa2101d3298`. These are API fields, not build attestations.
The filename identifies a macOS aarch64 candidate; separately named freethreaded assets support
interpreting this as the standard candidate, but actual architecture/GIL/build identity is untested.

Proposed location: private `b1b-runtime/standalone/` beneath the cache above, explicit executable,
no shared installer, PATH/service/trust edits. An install-only archive could avoid local compiler
and admin requirements **if** it supports that location and needs no external libraries/helpers.
S4 supplies neither relocation/support instructions nor exact dependency/license inventory;
an archive name and extraction alone prove neither. Release notes mention pip 26.3, setuptools
84.2.1, zlib 1.4 and other updates, not this asset's complete inventory or approved bootstrap.
PSF .pkg signature/Gatekeeper results do not apply; asset signing/notarization is unverified.
Compressed bytes fit <100 MB (27,119,138 including the retained wheel); expanded/staging/venv
peak within 2 GiB is unknown. GitHub download redirect/host behavior was not requested/observed;
the original exact-host/no-redirect acquisition policy cannot silently be widened. No new tool
or paid service is assumed; failure to use existing extraction/inspection tools would stop.

For both candidates, the retained rfc8785 0.1.4 wheel identity remains the packet's exact
9,240-byte file, SHA-256 `520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48`.
B1a observed a pure wheel with optional-only dependencies; complete license/source review,
bootstrap-tool identity and target compatibility remain pending. No new wheel request/import.
Existing Homebrew, shared .pkg relocation, containers and other paths were not added as candidates.

## Decision and next permission boundary

**No practical route established under the unchanged envelope; neither is shown infeasible.**
C1 has the strongest documented isolation design and exact official source identity, but lacks
existing-tool/module/space fit. C2 has a concrete exact-version asset and attractive transfer
size, but lacks relocation, dependency/license and trust evidence. Neither is selected/adopted
as an approved runtime. This conclusion follows those specific gaps, not the S3 404. B1a-I1 stays open.

No new founder assent was needed for this R1 document correction. Future acquisition/build/
execution is a different boundary: the original permission names the .pkg, not either artifact
above. Any such proposal must separately authorize the chosen exact bytes/provenance checks,
read-only tool/capacity preflight, archive/script/license/dependency inspection and proposed
private paths before execution. C1 additionally needs compiler/SDK/module identities and a
bounded source-build budget; C2 needs supported relocation/linkage and download-host/trust
disposition. Missing bootstrap identity or any new dependency cannot be silently substituted.
No execution-ready assent request or automatic follow-on study is issued from this assessment.
Unapproved tools/dependencies, wrong arm64/GIL/version, excess transfer/space/time, shared-state
writes or actual provider/quota/transport errors remain stops, without retries or trust repair.
The original oracle-before-execution requirement, 96-new-check/105-historical-control split,
two-run cap and unqualified product/privacy/deadline gates remain; no harness is prepared.

## Evidence and delivery

Raw requests/headers, successful bodies, text views and historical stop record remain under
ignored `artifacts/b1b/`. The original 13-entry manifest remains
`3b23d32542648db78e80ac43ff4734df09b9de9375ea66049697b79b567b9b7d`; new R1 evidence/manifest is
separate under `artifacts/b1b/r1/`. Its analysis record preserves exact S1/S4 metadata and limits.
B1a's 63-entry manifest remains `3e315c25babd13e574580539a07b8a24bc555fa1c28606e97414a547fac3a655`.
No artifact acquisition, extraction, build/install, target/host experiment or settings change.
A1 authority/exact target preserved; A2 four-slot evidence analysis complete with stated gaps;
A3 effects/tool/budget assessment distinguishes design from unverified practical fit; A4 returns
no established path; A5 corrects the continuation boundary and preserves separate execution
permission; A6 checks/preservation/attribution/exact-head CI and literal Sourcery are recorded
in the PR. B1b-R1 awaits coordinator verification; no worker resolution/approval/merge.
