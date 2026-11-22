# B1c: exact standalone archive inspection

Status: in-progress acquisition/static-inspection checkpoint; **runtime tests have not run**.
2026-11-22; GPT-6 Astra (`gpt-6-astra`) / OpenCode, original persistent worker.
[Issue #28](https://github.com/Himanshu-singh04/releaselens/issues/28), fixed A1–A6;
[founder assent](https://github.com/Himanshu-singh04/releaselens/pull/27#issuecomment-7078081060)
to the [complete permission](https://github.com/Himanshu-singh04/releaselens/pull/27#issuecomment-7077984175).
Base `c2d56ef6ec90ba5121cf9d486cd3e0b382a9c22f`; start 10:56:13 UTC, stop by 12:56:13 UTC.

## Exact scope and trust

Only release 20261110 / ID 441136779, asset 733713948:
`cpython-3.14.10+20261110-aarch64-apple-darwin-install_only.tar.gz`, 27,109,898 bytes,
SHA-256 `42031ed5f0d38777335252c8c77d64708c8010dd67c128246bdec25000672666`.
Inspection-only trust: published GitHub metadata/hash over verified TLS, not an independent
attestation, PSF signature/notarization or runtime adoption. Prior .pkg trust does not transfer.
Up to three official support documents plus exact metadata recheck; <=100 MB response bodies.
At most three manually inspected HTTPS asset redirects, hosts exactly github.com or
release-assets.githubusercontent.com; no credentials/retries/unrestricted redirects.
Signed query values stay out of public records. Changed identity/bytes/hash stops acquisition.

Validate archive members as untrusted data before extraction: <=20,000 members, <=2 GiB
total task allocation including archive/extraction/scratch/logs; reject escaping paths/links,
special files, conflicting duplicates and unsafe link-order effects. No target invocation,
imports, pip, install/startup code, admin/system/PATH/service/trust change or binary patch.

## Evidence and pending gates

Fresh cache `/Volumes/AIWorkspace/caches/releaselens/b1c-standalone-inspection/`;
ignored raw evidence `/Volumes/AIWorkspace/projects/releaselens/artifacts/b1c/`.
A1 authority/base/prior-head checks passed; host/tool/space preflight pending. A2 metadata/
acquisition, A3 safety/extraction, A4 static findings and A5 later-phase recommendation pending.
A6 early attributed checkpoint; final checks, preservation, attribution/CI and literal Sourcery
will be recorded in PR timeline. Stop for independent review before any execution request.

#25/#27, stopped records and all prior evidence remain preserved. B1a-I1 remains open;
D1–D4 unadopted; M0/M1–M4/privacy/customer storage/deadline gates open. Original oracle-before-
execution, 96-new/105-legacy/two-run requirements remain future scope, not tests run here.
