"""Finite synthetic B0b experiment, NOT a product importer or resource sandbox."""
from decimal import Decimal, InvalidOperation
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import struct
import sys

import rfc8785

SAFE = 2**53 - 1
LIMITS = {"artifact": 1024**2, "suite": 5 * 1024**2, "bundle": 25 * 1024**2}
MESSAGES = {"E_JSON": "Invalid JSON input.", "E_LIMIT": "Input limit exceeded.",
            "E_SCALAR": "Invalid Scalar type.", "E_INTERNAL": "Internal research error."}


class Rejected(Exception):
    pass


def reject(code="E_JSON"):
    raise Rejected(code)


def diagnostic(code):
    return {"code": code, "location": {"kind": "input", "input": "suite", "pointer": ""},
            "message": MESSAGES[code]}


def number(token, integer):
    # Decimal construction is exact; no arithmetic governed by context precision.
    exact = Decimal(token)
    if exact == exact.to_integral_value() and exact.copy_abs() > SAFE:
        reject()
    if integer:
        return int(token)
    value = float(token)
    if not math.isfinite(value) or (value == 0 and exact != 0):
        reject()
    if value.is_integer() and abs(value) > SAFE:
        reject()
    return value


def object_pairs(pairs):
    result = {}
    for key, value in pairs:
        key.encode("utf-8", errors="strict")
        if key in result:
            reject()
        result[key] = value
    return result


def unicode_values(value):
    if type(value) is str:
        value.encode("utf-8", errors="strict")
    elif type(value) is list:
        for child in value:
            unicode_values(child)
    elif type(value) is dict:
        for child in value.values():
            unicode_values(child)


def parse(raw, byte_limit=LIMITS["suite"], scalar=False):
    if type(raw) is not bytes:
        reject()
    if len(raw) > byte_limit:
        reject("E_LIMIT")
    text = raw.decode("utf-8", errors="strict")
    # Count containers before recursive decoding; JSON decoder validates grammar.
    depth = 0
    quoted = escaped = False
    for char in text:
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in "[{":
            depth += 1
            if depth > 32:
                reject("E_LIMIT")
        elif char in "]}":
            depth -= 1
    value = json.loads(text, object_pairs_hook=object_pairs,
                       parse_int=lambda t: number(t, True),
                       parse_float=lambda t: number(t, False), parse_constant=lambda _: reject())
    unicode_values(value)
    if scalar and type(value) not in (str, bool, type(None), int):
        reject("E_SCALAR")
    return value


def convert(raw, byte_limit=LIMITS["suite"], scalar=False, dumps=rfc8785.dumps):
    """Only this boundary emits diagnostics; never serialize exception text or input keys."""
    try:
        value = parse(raw, byte_limit, scalar)
        return {"canonical": dumps(value), "type": type(value).__name__}
    except Rejected as error:
        return {"diagnostic": diagnostic(error.args[0])}
    except (ValueError, UnicodeError, InvalidOperation, OverflowError):
        return {"diagnostic": diagnostic("E_JSON")}
    except Exception:
        return {"diagnostic": diagnostic("E_INTERNAL")}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    corpus = Path(__file__).resolve().parents[2] / "fixtures/b0b/vectors.json"
    fixtures = json.loads(corpus.read_text(encoding="utf-8"))
    rows = []

    def record(identifier, ok, observed, **details):
        rows.append({"id": identifier, "pass": bool(ok), "observed": observed, **details})

    def check_bytes(identifier, raw, expected=None, error=None, expected_type=None, **kwargs):
        calls = []

        def spy(value):
            calls.append(type(value).__name__)
            return rfc8785.dumps(value)

        result = convert(raw, dumps=spy, **kwargs)
        if error:
            ok = result == {"diagnostic": diagnostic(error)} and not calls
            record(identifier, ok, result.get("diagnostic", {}).get("code", "ACCEPT"),
                   candidate_calls=len(calls))
        else:
            actual = result.get("canonical")
            ok = actual == expected and sha(actual or b"") == sha(expected)
            if expected_type:
                ok = ok and result.get("type") == expected_type
            record(identifier, ok, "ACCEPT" if actual is not None else "REJECT",
                   raw_sha256=sha(raw), canonical_sha256=sha(actual) if actual is not None else None,
                   expected_sha256=sha(expected), parsed_type=result.get("type"))

    for case in fixtures["bytes"]:
        raw = bytes.fromhex(case["hex"]) if "hex" in case else case["text"].encode("utf-8")
        check_bytes(case["id"], raw, case.get("canon", "").encode("utf-8"), case.get("error"),
                    case.get("type"), scalar=case.get("scalar", False))

    for identifier, bits, expected in fixtures["binary64"]:
        value = struct.unpack(">d", bytes.fromhex(bits))[0]
        try:
            actual = rfc8785.dumps(value)
            ok = expected is not None and actual == expected.encode("ascii")
            record(identifier, ok, actual.decode("ascii"), canonical_sha256=sha(actual),
                   expected_sha256=sha(expected.encode("ascii")) if expected else None,
                   product_domain="reject" if value.is_integer() and abs(value) > SAFE else "accept")
        except rfc8785.CanonicalizationError:
            record(identifier, expected is None, "REJECT", product_domain="reject")

    sample = fixtures["rfc_sample"]
    # This isolated normative path intentionally does not apply narrower product N1.
    actual = rfc8785.dumps(json.loads(sample["text"]))
    expected = bytes.fromhex(sample["canonical_hex"])
    record("RFC-sample", actual == expected and sha(actual) == sha(expected), "JCS",
           canonical_sha256=sha(actual), expected_sha256=sha(expected))
    check_bytes("RFC-sample-product", sample["text"].encode(), error="E_JSON")

    # Compact recipes specify independent inclusive-boundary expectations, not golden output.
    for label, limit in LIMITS.items():
        for delta in (-1, 0, 1):
            raw = b"0" + b" " * (limit + delta - 1)
            check_bytes(f"bytes-{label}-{delta:+}", raw, b"0",
                        "E_LIMIT" if delta > 0 else None, byte_limit=limit)
    for label, opening, closing in (("array", b"[", b"]"), ("object", b'{"a":', b"}")):
        for depth in (31, 32, 33):
            raw = opening * depth + b"0" + closing * depth
            check_bytes(f"depth-{label}-{depth}", raw, raw, "E_LIMIT" if depth > 32 else None)
    check_bytes("utf8-byte-limit", '"é"'.encode(), error="E_LIMIT", byte_limit=3)
    check_bytes("utf8-byte-exact", '"é"'.encode(), '"é"'.encode(), byte_limit=4)

    # Expected default-Python counterexamples remain tests, not corrections to expectations.
    record("default-duplicate", json.loads('{"a":1,"\\u0061":2}') == {"a": 2}, "last-key-wins")
    record("default-NaN", math.isnan(json.loads("NaN")), "accepts-NaN")
    record("default-surrogate", json.loads('"\\ud800"') == "\ud800", "accepts-surrogate")
    record("default-float", json.dumps([1.0, -0.0, 1e-6], separators=(",", ":")) ==
           "[1.0,-0.0,1e-06]", "non-JCS-number-spelling")
    record("default-order", sorted(["😀", "דּ"]) == ["דּ", "😀"], "non-UTF16-order")
    record("default-rounding", json.loads("9007199254740993e0") == 9007199254740992.0,
           "original-integer-lost")
    record("exact-type", True == 1 and type(parse(b"true")) is bool and type(parse(b"1")) is int,
           "types-distinct-despite-Python-equality")
    a, b = b'{"a":1,"b":2}', b' { "b":2, "\\u0061":1 } '
    record("semantic-hash", sha(a) != sha(b) and sha(convert(a)["canonical"]) ==
           sha(convert(b)["canonical"]), "different-raw-equal-canonical")
    record("array-hash", sha(convert(b"[1,2]")["canonical"]) !=
           sha(convert(b"[2,1]")["canonical"]), "array-order-significant")
    record("unicode-hash", sha(convert('"é"'.encode())["canonical"]) !=
           sha(convert('"é"'.encode())["canonical"]), "no-normalization")
    # Simulate a candidate error containing secrets; require the whole fixed diagnostic.
    for exception in (ValueError, RuntimeError):
        def faulty(_):
            raise exception("SYNTHETIC_SECRET_B0B raw exception /private/path")
        code = "E_JSON" if exception is ValueError else "E_INTERNAL"
        result = convert(b"null", dumps=faulty)
        record("diagnostic-" + exception.__name__, result == {"diagnostic": diagnostic(code)}, code)

    assert len({r["id"] for r in rows}) == len(rows)
    report = {"python": sys.version, "executable": sys.executable,
              "candidate_version": rfc8785.__version__, "candidate_path": rfc8785.__file__,
              "inventory": sorted((d.metadata["Name"], d.version) for d in importlib.metadata.distributions()),
              "corpus_sha256": sha(corpus.read_bytes()), "cases": rows,
              "passed": sum(r["pass"] for r in rows), "total": len(rows)}
    print(json.dumps(report, indent=2, ensure_ascii=True))
    return 0 if report["passed"] == report["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
