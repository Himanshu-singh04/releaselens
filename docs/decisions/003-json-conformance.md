# B0b JSON/JCS conformance experiment

Status: research in progress; no product approval. Date: 2026-11-19.
GPT-6 Astra (`gpt-6-astra`) / OpenCode, registered ReleaseLens worker; no subagents.

## Scope and independent expectations

[Issue #14](https://github.com/Himanshu-singh04/releaselens/issues/14) preserves A1–A6.
Original founder instruction: “ok proceed with the further tasks”. Coordinator authorized
this independent research from approved main `1bfa0576aabfbb17a9a625a513a1d7dea6079eb3`
while B0a awaits review. The B0a branch/PR is preserved; this work does not incorporate it.
One byte-parser experiment, reviewed synthetic expectations and this decision record;
no product importer, evaluator, storage publication or native bridge.

The [contract](../evidence-contract.md) requires UTF-8 JSON, unique **decoded** object
keys, valid Unicode, finite binary64 fractions, safe integers (±9007199254740991), and
exact-type Scalars (string, bool, null, safe integer). Bool is not an integer despite
Python subclass/equality behavior. Raw file bytes, parsed values, canonical UTF-8 bytes
and SHA-256 digests are four distinct things. Whitespace/escape variants can have
different raw hashes but equal semantic hashes; array order and Unicode normalization
differences remain significant. Hash equality is not authenticity.

The finite [corpus](../../fixtures/b0b/vectors.json) is specified **before candidate
execution**. Binary64 bit patterns/output strings are transcribed from
[RFC8785 Appendix B](https://www.rfc-editor.org/rfc/rfc8785.html#appendix-B), including
all 26 rows (NaN/infinity are errors). Other labelled expectations derive from
§3.1, §3.2.1–4 and the contract, not a library-generated golden file. RFC §3.2.4's
sample is represented by its literal published hex bytes. Coordinator independently
reviews transcription and expectations; these are author-reviewed, not yet independently approved.

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

Pending verified wheel acquisition and execution. Candidate `rfc8785==0.1.4` is not
a product dependency. Installed Python observed: `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3`,
CPython 3.13.4, Clang 16.0.0; proposed CPython 3.14.10 remains uninstalled/unverified.
Host pip 26.1.2; Node `/opt/homebrew/bin/node` v26.13.0 may be a secondary serializer
oracle only. No full-JCS claim for `JSON.stringify`.
