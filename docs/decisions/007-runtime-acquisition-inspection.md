# B1a first phase: runtime acquisition and inspection

Status: **BLOCKED before founder-admin installation**; artifact verification passed,
but mandatory shared-framework-link effects lack complete service-impact evidence.
2026-11-22; GPT-6 Astra (`gpt-6-astra`) / OpenCode, original persistent worker.
[Issue #24](https://github.com/Himanshu-singh04/releaselens/issues/24), first phase A1–A3/A6 only.
Base: `c2d56ef6ec90ba5121cf9d486cd3e0b382a9c22f`, accepted PR #23.
Start 08:50:27 UTC; two-hour stop 10:50:27 UTC.
Acquisition/inspection stopped at 08:56:45 UTC; remaining work is evidence/checkpoint delivery.

## Authority and scope

Founder replied “ok proceed” to the concrete acquisition/validation sequence:
[authorization](https://github.com/Himanshu-singh04/releaselens/pull/23#issuecomment-7076756051),
[original briefing](https://github.com/Himanshu-singh04/releaselens/pull/23#issuecomment-7075826705).
The immutable [243-line packet](006-runtime-validation-scope.md) supplies exact artifacts,
paths, caps and stop conditions. Its earlier permission-pending wording is historical.
This dispatch permits preflight, exact acquisition and native/static inspection only.
Founder alone may install after coordinator verifies the evidence; no install command,
target/package execution, venv, bootstrap or empirical harness is prepared or run here.

## Preflight observations

Read-only capture at 08:52:06 UTC: macOS 27.2.1 / build 26B131, arm64, Apple M2.
Available space: Mac framework filesystem 26,267,521,024 bytes; pendrive cache filesystem
121,435,594,752 bytes. Both exceed the proposed 2 GiB working allowance; no space was reclaimed.
`/Library/Frameworks/Python.framework/Versions/3.14` and `/Applications/Python 3.14` are absent.
Existing `Versions/Current` points to `3.13`; framework Headers/Python/Resources use Current.
Existing `/usr/local/bin/python3` and versioned 3.13 links resolve to explicit 3.13 paths.
PythonT 3.13 links also exist; no changes to either framework or those links were performed.
Python receipt inventory contains Framework, Applications, UnixTools and Documentation 3.13.

Selected launch-agent declarations were read without recording environment values:
- `local.portfolio.opencode-projects` names the explicit 3.13 framework interpreter.
- `com.sidehustle.control` names `/opt/homebrew/opt/python@3.14/bin/python3.14`.
These are declarations, not proof of loaded-process or transitive dependency behavior.
No service-wrapper/portfolio records were read. The Homebrew declaration is not an acquired,
executed, qualified or substituted target; the approved python.org target path remains absent.
Current consumers beyond these declarations remain unknown. This matters because the mandatory
payload below changes Current even when shell/profile/UNIX-link components are disabled.

## Exact acquisition and native verification

Only the packet's [Python release](https://www.python.org/downloads/release/python-31410/)
and [version-specific PyPI metadata](https://pypi.org/pypi/rfc8785/0.1.4/json) were rechecked.
Both returned HTTP 200 with curl TLS verification result 0 on 2026-11-22 at 08:52:35 UTC.
Metadata responses were 46,491 and 5,468 bytes; saved headers/bodies retain the source record.
Their actual artifact URLs/checksums match the approved packet after HTML-text extraction.

| Artifact in approved cache | Acquisition UTC | Bytes | Locally computed SHA-256 |
| --- | --- | --- | --- |
| python-3.14.10-macos11.pkg | 08:53:50–08:54:08 | 76,018,440 | `286c7018aa2730f6747ca433dccdc2b31be45f078a9ea0ffa44d5f06368fd2d7` |
| rfc8785-0.1.4-py3-none-any.whl | 08:54:08–08:54:09 | 9,240 | `520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48` |

Exact URLs are the immutable packet's S1/S3 artifact URLs, also retained in request records.
Each artifact returned HTTP 200, unchanged effective URL and TLS verification result 0.
Total artifact transfer **76,027,680 bytes**, below 100,000,000; four HTTP requests total,
including metadata, with no redirects followed, retries, fallback hosts or additional acquisitions.
Existing curl used `-q --fail --silent --show-error --proto '=https'`, no `-L`, no insecure
option; connection timeout 20 seconds, metadata/artifact maximum time 60/180 seconds,
and response-size caps. Exact argument arrays, exit codes and timestamps are outside Git.
Both stdlib SHA-256 and native `shasum -a 256` agree with the approved hashes.

`pkgutil --check-signature` exited 0: Apple-issued Developer ID Installer certificate,
**Python Software Foundation (BMM5U3QVKW)**; trusted notarization; trusted timestamp
2026-10-25 21:35:03 UTC. Full leaf/intermediate/root chain and fingerprints are retained.
`spctl --assess --type install --verbose=4` exited 0, **accepted**, source **Notarized Developer ID**.
OS-managed verification was permitted; no trust settings or certificate stores were changed.
No Sigstore verifier or additional package was downloaded. Native acceptance is not product validation.

## Static package inspection and concrete blocker

`pkgutil --expand` exited 0; package contents remain under cache `pkg-expanded/`.
Distribution XML, PackageInfo, the framework postinstall and BOMs were inspected as data.
No installer was launched and no package script, interpreter or wheel code was executed.
No choice-evaluation command or modified/repacked installer was prepared.

Distribution lines 20–22 make `org.python.Python.PythonFramework-3.14` selected=true,
enabled=false: the standard framework cannot be deselected. Its PackageInfo installs to
`/Library/Frameworks/Python.framework`, auth=root, overwrite-permissions=true, with a
124045 installKBytes estimate and 7935 payload entries (installer metadata, not measured install).
Its BOM explicitly contains `./Versions/Current` as a symlink to **3.14**, plus root
Headers/Python/Resources links through Current. The current link instead targets **3.13**.
This is an unavoidable shared-link change in the inspected standard component, not a change
confined to the new version directory and not prevented by omitting UNIX command-line links.

The framework postinstall lines 9–27 would invoke target Python/compileall four times,
including optimized bytecode; lines 29–31 would recursively chgrp admin, enable group writes
in the new framework version, then remove group-write on venv/scripts. These are inspected
future installer effects, **not commands run here**. The script ends with exit 0; a future
installer exit alone would not replace post-install verification of these effects.

Inspection-derived choices below are **not a ready-to-run installation instruction**:

| Exact choice suffix after org.python.Python. | Required disposition / inspected reason |
| --- | --- |
| PythonFramework-3.14 | Mandatory; shared Current effect blocks readiness until service impact is resolved. |
| PythonApplications-3.14 | Omit; optional GUI resources under /Applications. |
| PythonUnixTools-3.14 | Disable; payload install-location /usr/local/bin would affect global command links. |
| PythonDocumentation-3.14 | Omit; optional documentation, with its own postinstall. |
| PythonProfileChanges-3.14 | Disable; Distribution start_selected=true; profile updater. |
| PythonInstallPip-3.14 | Disable; Distribution start_selected=true; pip install/upgrade script-only component. |
| PythonTFramework-3.14 | Disable; optional separate free-threaded framework, start_selected=false. |

**Blocker B1a-I1:** complete shared-link/service impact has not been established. The inspected
launch declarations alone cannot prove that wrappers, subprocesses or other consumers avoid
Current. The approved packet requires stopping before installation when that impact is uncertain.
No package patch, shared-link restoration, alternate runtime, broader portfolio read or extra
probe is used to get past this gate. Coordinator must resolve that specific dependency evidence
within authority before presenting founder-admin steps; no founder installation is requested now.

Before any later installation, refresh target absence, receipts, shared links, service bindings
and capacity against this record. After an authorized install, reconcile exact target files,
Current/root links, receipts, unchanged UNIX/profile/service state and all installer script effects.
That future inventory cannot be supplied by this phase. No automatic rollback/repair is authorized.

Wheel ZIP inspection found seven regular members: two Python sources, py.typed, LICENSE,
WHEEL, METADATA and RECORD; no .pth, entry point, native binary, install script or path traversal.
Metadata says purelib, py3-none-any, version 0.1.4, Python >=3.8 and optional-only dependencies.
LICENSE is retained (SHA-256 `0d542e0c8804e39aa7f37eb00da5a762149dc682d7829451287e11b938e94594`).
No wheel import occurred. Complete source/license audit and remaining package scripts/notices
were not finished after the blocker; no complete dependency/license closure is claimed.

## Evidence, inspection errors and pending criteria

Cache: `/Volumes/AIWorkspace/caches/releaselens/b1a-runtime/`; raw evidence:
`/Volumes/AIWorkspace/projects/releaselens/artifacts/b1a/`, under the unchanged ignore rule.
All invoked acquisition/native inspection commands exited 0. Three local inspection-wrapper
assumptions failed; their corrections use already saved data, never repeated acquisition/native commands:
1. Raw HTML literal checksum search failed because span/wbr tags split the checksum. Actual
   checksum text and acquired bytes match. `metadata-stop.json` retains the preliminary false flag;
   `metadata-comparison.json` records its correction, not an upstream mismatch or source retry.
2. Signature wording guard expected a different macOS phrase. Native exit 0 and PSF/notary output
   were retained; `signature-guard-correction.json` records the wording error. Gatekeeper ran once.
3. Inventory wrapper assumed every PackageInfo has payload. Script-only pip has none; the
   AttributeError is recorded in `inventory-guard-correction.json`; absent payload is now null.
   Six BOM captures were retained; the remaining profile-only component BOM was not inspected.

`preflight.json` retains native OS/CPU/receipt commands and selected service declarations.
`*.request.json` plus headers/bodies retain each of the four exact HTTPS transactions.
`artifact-shasum.json`, `pkg-signature.json`, `gatekeeper.json`, `pkg-expand.json`,
`*.bom.json`, `package-inventory.json` and `wheel-inspection.json` retain native/static findings.
`phase-stop.json` records the blocker and 21 unchanged preflight path/link checks after inspection.
`evidence-manifest.json` hashes 63 retained entries, including expanded package material;
regular bytes 156,944,283, allocated bytes 167,948,288 before the manifest itself, below 2 GiB.
Manifest SHA-256: `3e315c25babd13e574580539a07b8a24bc555fa1c28606e97414a547fac3a655`.
No system installation bytes were written; logs/artifacts are retained without cleanup.

| Criterion | First-phase disposition |
| --- | --- |
| A1 | Base/authority, OS/CPU/capacity, target absence, links/receipts and selected declarations captured; complete service impact unresolved. |
| A2 | Exact acquisition/hash/native signature/Gatekeeper passed; static inspection identified blocker; remaining script/payload/license review incomplete. |
| A3 | BLOCKED by mandatory shared-link change plus uncertain consumer impact; no installer launch or ready-to-run founder steps. |
| A4 | Pending founder installation reconciliation and coordinator continuation; no target imports/venv/bootstrap. |
| A5 | Pending later independent expectation review; no empirical harness prepared or executed. |
| A6 | Early draft and blocker checkpoint; exact-head existing checks, preservation, attribution/CI and literal Sourcery recorded in PR timeline. |

Accepted B1 source definitions remain unchanged; no encoding/product implementation follows.
D1–D4 remain unadopted; M0/M1–M4 open. Customer/private-storage/native/deadline gates stay open.
Stopped for independent review of the concrete blocker, without approval/merge/self-dispatch.
