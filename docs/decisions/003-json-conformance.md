# B0b JSON/JCS conformance experiment

Status: **105/105 finite controls pass; candidate GO for continued evaluation on the
tested CPython 3.13.4 only; product implementation NO-GO.** Date: 2026-11-19.
GPT-6 Astra (`gpt-6-astra`) / OpenCode, registered ReleaseLens worker; no subagents.

Acceptance update: [PR #15](https://github.com/Himanshu-singh04/releaselens/pull/15) merged
at `b271ec1f19f3f4a67ef9dd2279af129334c322b1`; [main CI](https://github.com/Himanshu-singh04/releaselens/actions/runs/44673491213)
passed. This accepts finite research, not N1–N4, runtime qualification or implementation.
The integration/review-state wording below is historical. [B0c](004-mvp-decision.md)
collects proposed decisions; D1–D4 and E1 remain unaccepted/unauthorized respectively.

## Scope and independent expectations

[Issue #14](https://github.com/Himanshu-singh04/releaselens/issues/14) preserves A1–A6.
Original founder instruction: “ok proceed with the further tasks”. Coordinator authorized
this independent research from approved main `1bfa0576aabfbb17a9a625a513a1d7dea6079eb3`
while B0a awaited review. The original delivery preserved B0a without incorporating it.
One byte-parser experiment, reviewed synthetic expectations and this decision record;
no product importer, evaluator, storage publication or native bridge.

Integration update: accepted main `f9b47649ea75b53daf2beff480e60ad8a1ca39a7`
([B0a PR #13](https://github.com/Himanshu-singh04/releaselens/pull/13)) is merged into
this research branch without rewriting its history. The accepted storage record and R1
correction are inherited unchanged. [Coordinator verification](https://github.com/Himanshu-singh04/releaselens/pull/15#issuecomment-7006095738)
met A1–A6 at original B0b head `f6456bb85ac3aed5a1f811c45933726c0ee10649`;
the integrated head requires fresh review. Corpus, helpers, pins and prior captures
are unchanged. Observations and pending-review language below retain their original
delivery context. N1–N4 and D1–D4 remain unaccepted; E1, product implementation and
target/storage changes remain unauthorized. Integration check evidence is in PR #15.

The [contract](../evidence-contract.md) requires UTF-8 JSON, unique **decoded** object
keys, valid Unicode, finite binary64 fractions, safe integers (±9007199254740991), and
exact-type Scalars (string, bool, null, safe integer). Bool is not an integer despite
Python subclass/equality behavior. Raw file bytes, parsed values, canonical UTF-8 bytes
and SHA-256 digests are four distinct things. Whitespace/escape variants can have
different raw hashes but equal semantic hashes; array order and Unicode normalization
differences remain significant. Hash equality is not authenticity.

The finite [corpus](../../fixtures/b0b/vectors.json) was specified **before candidate
execution**. Binary64 bit patterns/output strings are transcribed from
[RFC8785 Appendix B](https://www.rfc-editor.org/rfc/rfc8785.html#appendix-B), including
all 26 rows (NaN/infinity are errors). Other labelled expectations derive from
§3.1, §3.2.1–4 and the contract, not a library-generated golden file. RFC §3.2.4's
sample is represented by its literal published hex bytes. The coordinator independently
corroborated the RFC transcription and reviewed expectations at the original head linked above;
that verification does not accept N1–N4 as product policy or approve the integrated head.

## Proposed numeric and boundary decisions (unaccepted)

- **N1:** apply the safe-integer bound to the exact mathematical decimal token,
  including exponent/dot forms, before binary64 conversion; also reject any rounded
  binary64 integral value outside the safe range. Ordinary nonintegral binary64
  rounding remains allowed. Lexical-only integer checking would admit `1e30` and
  `9007199254740993e0`; checking only rounded values loses original-token evidence.
- **N2:** preserve lexical numeric type: integer grammar → exact Python int;
  dot/exponent grammar → float, even `1.0`/`1e0`. Scalar accepts only exact int,
  not integral float or bool-as-int coercion. Alternative: normalize all mathematical
  integers to int; contract does not resolve this spelling/Scalar distinction.
- **N3:** reject nonzero tokens that underflow to binary64 zero; accept nonzero
  subnormal rounding and signed zero (JCS emits `0`). Alternative: allow silent
  underflow as ordinary binary64 rounding. Contract does not explicitly choose.
- **N4:** nesting counts open object/array containers: root container depth 1,
  primitive depth 0, maximum 32 inclusive. Byte limits are inclusive over exact raw
  UTF-8 bytes including whitespace. Reject UTF-8 BOM rather than silently stripping it.
  These operational interpretations need approval; requirements themselves are unchanged.

The experiment exercises these proposals, not an accepted product numeric policy.
Suite 5 MiB, bundle 25 MiB and artifact 1 MiB bounds receive boundary controls.
The 20 MiB aggregate decoded-artifact limit, schema/count/unknown-field validation,
60-second deadline, streaming I/O and memory enforcement are outside this parser experiment.

## Acquisition and execution record

Candidate `rfc8785==0.1.4` is not a product dependency. Installed Python observed:
`/Library/Frameworks/Python.framework/Versions/3.13/bin/python3`, version
`3.13.4 (v3.13.4:8a526ec7cbe, Jun 3 2025, 21:14:54) [Clang 16.0.0 (clang-1600.0.26.6)]`.
Proposed CPython 3.14.10 remains uninstalled/unverified. Host pip 26.1.2 was observed,
but the final installation uses the interpreter's **bundled pip 25.1.1** without
installing pip into the venv. Bundled installer wheel SHA-256:
`2913a38a2abf4ea6b64ab507bd9e967f3b53dc1ede74b01b0931e1ce548751af`.
It is existing interpreter tooling, not a downloaded dependency or a newly authenticated
Python distribution. Every run prints the actual bundled wheel identity; other Python
installations may bundle another installer and are separate observations.
Distribution Pythons may instead provide their installer wheel in the interpreter's
`sysconfig` `WHEEL_PKG_DIR`; the helper uses that configured directory when present,
requiring exactly one pip wheel and recording its name/hash. No installer is downloaded.

Primary metadata retrieved 2026-11-19 from
[version-specific PyPI JSON](https://pypi.org/pypi/rfc8785/0.1.4/json), corroborated
against the downloaded archive before execution:

| Property | Observed |
| --- | --- |
| Artifact | `rfc8785-0.1.4-py3-none-any.whl`, 9240 bytes |
| SHA-256 | `520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48` |
| Exact upstream URL | `https://files.pythonhosted.org/packages/4d/78/119878110660b2ad709888c8a1614fce7e2fab39080ab960656dc8605bf6/rfc8785-0.1.4-py3-none-any.whl` |
| External acquisition location | `/Volumes/AIWorkspace/caches/releaselens/` |
| Wheel metadata | Name `rfc8785`, version `0.1.4`, Python `>=3.8`, purelib, `py3-none-any`, generator flit 3.9.0 (not run here) |
| License | Apache-2.0; complete `rfc8785-0.1.4.dist-info/LICENSE` read; SHA-256 `0d542e0c8804e39aa7f37eb00da5a762149dc682d7829451287e11b938e94594` |
| Mandatory dependency closure | None; final venv distribution inventory is exactly `rfc8785 0.1.4` |
| Unselected optional extras | dev: `rfc8785[doc,test,lint]`, `build`; doc: `pdoc`; lint: `ruff ~=0.3`, `mypy >=1.0`, `interrogate`; test: `pytest`, `pytest-cov`, `coverage`. None acquired/installed. |
| Archive contents | `__init__.py`, `_impl.py`, `py.typed`; dist-info LICENSE, WHEEL, METADATA, RECORD. No `.pth`, entry points, `.data/scripts`, native binary or build hook. Source read before import. |
| Installed code hashes | `__init__.py`: `fa44927afd547caf7547247078bcf28863d1e69caf116d258c532b3f20ffd154`; `_impl.py`: `c25bc3a046528482d53bee3487b837f31dd9c05f33e8f13288c7aab320932cec` |
| Fixture SHA-256 | `cec1d004789a52cf49cccb451d4c88b004e4f036eade9bf1cac67f3e4c87ea3f` (independent expectation checkpoint `7a426fd`) |

The first download attempt using Python urllib failed certificate-chain verification
before acquisition. TLS-verifying curl succeeded; no trust-store change or TLS bypass.
The first exploratory fresh venv used standard venv/ensurepip and contained pip 25.1.1
plus rfc8785 0.1.4; it passed 105/105. The final helper instead creates a **no-pip venv**
and runs the existing bundled pip wheel in-process with `-I -B`, avoiding ensurepip's
child interpreter flag propagation. Final fresh run `artifacts/b0b/run2` passed
105/105 and `pip check`; it contained only rfc8785 0.1.4. No expectation was changed
to conceal a mismatch. Neither local experiment had a failing case.

Final observed executable: `artifacts/b0b/run2/.venv/bin/python` under this checkout;
imported candidate: `artifacts/b0b/run2/.venv/lib/python3.13/site-packages/rfc8785/__init__.py`.
The helper compares every wheel member except pip-rewritten RECORD to installed bytes
**before import**. Version metadata alone is not integrity evidence. These checks establish
equality to the verified wheel in that fresh environment at that time, **not arbitrary
installed-tree authentication**, provenance signatures, OS/runtime trust, absence of extra
files, protection against concurrent same-user mutation, or secure evidence ingestion.
Pip-generated metadata is outside the wheel-member equality claim.

## Reproduction, isolation and maintenance

Run from the repository root with the installed interpreter above. Acquire only the
exact URL above when the approved cache lacks it; no network is needed thereafter.
The helper verifies filename/size/hash/metadata/license before executing candidate code.
Choose a **new, nonexistent** task path; it refuses to reuse an existing environment.

```sh
python3 -I -B research/b0b/offline.py /Volumes/AIWorkspace/caches/releaselens/rfc8785-0.1.4-py3-none-any.whl artifacts/b0b/reproduce
artifacts/b0b/reproduce/.venv/bin/python -I -B research/b0b/experiment.py
node research/b0b/node_oracle.js
```

The first command reports installation/inventory to stderr and all per-case observations,
raw/canonical/expected hashes, fixture digest, interpreter and import location to stdout.
Its exact install options are `--isolated --disable-pip-version-check install --no-index
--find-links WHEEL_DIRECTORY --only-binary=:all: --require-hashes --no-deps --no-compile
--no-cache-dir -r research/b0b/requirements.txt`. No pip install-script-disable switch is
assumed: the authenticated wheel has no install/startup scripts or entry points, and
wheel-only/no-deps excludes sdists/build hooks/extras. The installer itself necessarily runs.
HOME, XDG config/cache, TMP/TEMP/TMPDIR are task-local; pip config is disabled with
`PIP_CONFIG_FILE=/dev/null`, environment is rebuilt, and Python runs isolated/without
bytecode generation. No system package/runtime installation, shared pip cache or runtime
upgrade. Artifacts/venvs/logs remain ignored outside Git.

[Scoped Dependabot](../../.github/dependabot.yml) watches only `/research/b0b` weekly
for Python updates. A proposed update is a review signal, not permission to alter the
frozen experiment: the hash, artifact checks, license/dependency review and decision
record must be updated explicitly. Expected vectors change only with independent source
evidence, never merely to match new output. The reviewed manifest includes no extras.
[CI](../../.github/workflows/ci.yml) downloads only the exact candidate URL, verifies it
with the same offline helper and runs the bounded corpus inside the existing five-minute
foundation job. Runner Python/tooling identities are emitted per run; CI is a portability
smoke check, not qualification of the proposed target or every Python version.

## Experiment mechanics and observations

[experiment.py](../../research/b0b/experiment.py) is a small stdlib adapter around the
candidate. It checks byte length before decoding, strict UTF-8 before JSON, and container
depth before recursive decoding. JSON object-pair hooks reject decoded duplicates before
building that object's dict; number hooks retain exact decimal token values before
binary64 conversion. Invalid Unicode keys/values are rejected before canonicalization.
The decoder is still responsible for JSON grammar. It operates on already allocated
bytes and builds an in-memory tree: these checks are not streaming or memory guarantees.
Exact type checks prevent float-as-Scalar and bool-as-int coercion; no schema is implemented.

Every negative byte/limit/Scalar case asserts its whole fixed Diagnostic and **zero
candidate calls**. The error boundary never copies input keys, values, exception text or
paths; its location is the fixed root input pointer. Synthetic duplicate-key/malformed
secret cases and injected ValueError/RuntimeError verify non-leaking descriptions.
Locations always use `suite` in this research harness; this is not product input routing.
Canonical bytes are compared directly to independent expectations and their SHA-256s;
the displayed hashes are computed from expected bytes, not independent cryptographic
test vectors. Literal byte comparison is the actual canonicalization oracle.

Boundary recipes are finite source fixtures in the runner: 1/5/25 MiB raw JSON containing
`0` plus whitespace at limit−1, limit, limit+1; object/array nesting 31/32/33; and a
four-byte UTF-8 JSON string `"é"` against limits 3/4. They expand in memory, avoiding
multi-megabyte committed fixtures. Quoted brackets/escapes ensure depth scanning ignores
string contents. No measured peak RSS, adversarial complexity or deadline guarantee follows.

### Per-case observed verdicts

All **105** rows below passed on the final local run. ACCEPT means exact expected bytes
and hash equality; E_* means the expected fixed rejection and zero candidate calls.
B* test the serializer directly on exact binary64 bits; they do not bypass product
policy in the byte-adapter path. B05–09 and B12–17 are valid JCS values rejected by N1;
B10/11 are nonfinite and invalid JCS. All other B* are inside the proposed JSON domain.

| Case | Observed (expected) |
| --- | --- |
| P01 | ACCEPT: literals/array order |
| P02 | ACCEPT: nested object sorting |
| P03 | ACCEPT: UTF-16 order |
| P04 | ACCEPT: escaping |
| P05 | ACCEPT: no Unicode normalization |
| P06 | ACCEPT: safe integer endpoints |
| P07 | ACCEPT: safe exponent |
| P08 | E_JSON: unsafe positive integer |
| P09 | E_JSON: unsafe negative integer |
| P10 | E_JSON: unsafe exponent before rounding |
| P11 | E_JSON: fraction rounding to unsafe integer |
| P12 | E_JSON: large integral exponent |
| P13 | E_JSON: positive overflow |
| P14 | E_JSON: negative overflow |
| P15 | E_JSON: positive underflow to zero |
| P16 | E_JSON: negative underflow to zero |
| P17 | ACCEPT: nonzero subnormals |
| P18 | ACCEPT: signed zero → 0 |
| P19 | ACCEPT: small exponents/rounding |
| P20 | E_JSON: escaped duplicate |
| P21 | E_JSON: astral duplicate |
| P22 | E_JSON: nested duplicate |
| P23 | E_JSON: high surrogate |
| P24 | E_JSON: low surrogate key |
| P25 | E_JSON: overlong UTF-8 |
| P26 | E_JSON: encoded surrogate |
| P27 | E_JSON: truncated UTF-8 |
| P28 | E_JSON: BOM |
| P29 | E_JSON: NaN |
| P30 | E_JSON: infinity |
| P31 | E_JSON: negative infinity |
| P32 | E_JSON: leading zero |
| P33 | E_JSON: trailing input |
| P34 | ACCEPT: quoted bracket/escape depth control |
| P35 | ACCEPT: exact bool Scalar |
| P36 | ACCEPT: exact int Scalar |
| P37 | E_SCALAR: float spelling |
| P38 | E_SCALAR: exponent spelling |
| P39 | ACCEPT: null Scalar |
| P40 | ACCEPT: string Scalar |
| P41 | E_SCALAR: container |
| P42 | E_JSON: synthetic secret key absent from Diagnostic |
| P43 | E_JSON: synthetic secret value absent from Diagnostic |
| P44 | E_JSON: negative unsafe exponent |
| P45 | E_JSON: unsafe dot form |
| P46 | ACCEPT: binary64 0.1 |
| P47 | ACCEPT: numeric-looking keys lexical order |
| P48 | ACCEPT: empty/prefix key order |
| B01 | `0` |
| B02 | `0` |
| B03 | `5e-324` |
| B04 | `-5e-324` |
| B05 | `1.7976931348623157e+308` |
| B06 | `-1.7976931348623157e+308` |
| B07 | `9007199254740992` |
| B08 | `-9007199254740992` |
| B09 | `295147905179352830000` |
| B10 | REJECT: NaN |
| B11 | REJECT: infinity |
| B12 | `9.999999999999997e+22` |
| B13 | `1e+23` |
| B14 | `1.0000000000000001e+23` |
| B15 | `999999999999999700000` |
| B16 | `999999999999999900000` |
| B17 | `1e+21` |
| B18 | `9.999999999999997e-7` |
| B19 | `0.000001` |
| B20 | `333333333.3333332` |
| B21 | `333333333.33333325` |
| B22 | `333333333.3333333` |
| B23 | `333333333.3333334` |
| B24 | `333333333.33333343` |
| B25 | `-0.0000033333333333333333` |
| B26 | `1424953923781206.2` |
| RFC-sample | Exact published §3.2.4 hex and hash match |
| RFC-sample-product | E_JSON: N1 rejects 1e30 |
| bytes-artifact--1 | ACCEPT |
| bytes-artifact-+0 | ACCEPT |
| bytes-artifact-+1 | E_LIMIT |
| bytes-suite--1 | ACCEPT |
| bytes-suite-+0 | ACCEPT |
| bytes-suite-+1 | E_LIMIT |
| bytes-bundle--1 | ACCEPT |
| bytes-bundle-+0 | ACCEPT |
| bytes-bundle-+1 | E_LIMIT |
| depth-array-31 | ACCEPT |
| depth-array-32 | ACCEPT |
| depth-array-33 | E_LIMIT |
| depth-object-31 | ACCEPT |
| depth-object-32 | ACCEPT |
| depth-object-33 | E_LIMIT |
| utf8-byte-limit | E_LIMIT at 3 bytes |
| utf8-byte-exact | ACCEPT at 4 bytes |
| default-duplicate | Python keeps last key (information lost) |
| default-NaN | Python accepts NaN |
| default-surrogate | Python accepts lone surrogate |
| default-float | Python emits `[1.0,-0.0,1e-06]` |
| default-order | Python codepoint order differs from UTF-16 |
| default-rounding | Python loses original integer in exponent token |
| exact-type | bool/int remain distinct despite Python equality |
| semantic-hash | Different raw bytes, equal canonical hashes |
| array-hash | Reordering changes semantic hash |
| unicode-hash | Composed/decomposed strings retain different hashes |
| diagnostic-ValueError | Fixed E_JSON; injected secret/raw exception absent |
| diagnostic-RuntimeError | Fixed E_INTERNAL; injected secret/raw exception absent |

Optional [Node oracle](../../research/b0b/node_oracle.js) ran using
`/opt/homebrew/bin/node`, **v26.13.0**: all 24 finite B* serialization agreements,
two expected nonfinite→null counterexamples, 14 shared P* primitive/array agreements,
and three controls passed. P01/P04/P05/P06/P07/P17/P18/P19/P34/P35/P36/P39/P40/P46
agree; the other controls show UTF-16 native sorting, numeric-looking object keys
remaining non-JCS ordered, and duplicate loss in JSON.parse. JSON.stringify neither
validates duplicate keys nor implements JCS recursive property sorting and emits null
for NaN/infinity. It is corroboration, never the source of expected vectors.

## Verdict, acceptance and remaining gates

**GO for further candidate evaluation on this tested installed CPython 3.13.4**, with
the proposed adapter; **NO-GO for product adoption/implementation**. Candidate alone
is a serializer: it cannot recover duplicate keys or unsafe numeric tokens already
lost by a default parser. Its int input range is narrower than its binary64 input
range; Appendix B must be tested with exact floats, not arbitrarily large Python ints.
No claim covers all binary64 bit patterns, all Unicode, hostile resource consumption,
secure ingestion, product correctness/support, performance or M0 completion.

| Acceptance | Local result / limitation |
| --- | --- |
| A1 | Met as research: unchanged rules recorded; N1–N4 explicitly proposed/unaccepted. No schema importer. |
| A2 | Met locally: independent 26 RFC number rows, 48 raw-byte rows, literal RFC hex and finite boundary recipes; independent coordinator expectation review pending. |
| A3 | Met locally: 105 controls, byte/hash comparisons, pre-canonicalization rejection, Python/Node counterexamples and fixed diagnostic checks. |
| A4 | Met locally: verified wheel/license/closure, fresh offline install, pre-import installed-member comparison and scoped maintenance; arbitrary installed-tree authentication unclaimed. |
| A5 | Met as bounded verdict: per-case observations above; uninstalled target and product gates unverified. |
| A6 | Local research, repository, 25 policy tests, actionlint and full-diff checks passed; final CI evidence recorded in the issue-linked PR; independent coordinator review pending. |

Smallest next recommendation: coordinator reproduces the fresh offline command and
independently checks RFC transcription, policy proposals and reject-before-loss controls.
Target-Python validation requires separate authorization; no system installation follows
from this GO. Native/storage/privacy/publication/durability/deadline and remaining B0
build/runtime gates stay open. No B0a file or assumption is needed for this experiment.

Local verification commands: `python3 scripts/check_repository.py` (tracked text/links
passed); `python3 -m unittest discover -s scripts -p 'test_*.py'` (25 passed);
`/Volumes/AIWorkspace/caches/actionlint/1.7.12/actionlint -shellcheck= -pyflakes=`
(exit 0); `git diff --check origin/main` (exit 0). Final fresh-offline command above
passed 105/105; Node command passed all stated secondary controls. Compared run1/run2
case records: identical; all 105 IDs have document rows. B0a ref was
`a1c4e0b705b37cba8e016dd473fabeeddb6b8f6c` at that initial delivery, when its document
was absent from the B0b branch; the integration update above supersedes that branch-state observation.
No target-Python, native, storage, deadline, product, peak-memory or comprehensive
binary64 test ran. PR records preserve acquisition/CI failures and their corrections.
Initial new-code CI run `44488237702` failed before candidate installation: Ubuntu's
Python provides pip outside `ensurepip/_bundled`. The helper was corrected to use
`WHEEL_PKG_DIR` where configured; this changes installer discovery, not corpus expectations.
The corrected helper's fresh local `artifacts/b0b/run3` rerun passed 105/105,
pip check and installed-member equality with the same installer/candidate inventory.
