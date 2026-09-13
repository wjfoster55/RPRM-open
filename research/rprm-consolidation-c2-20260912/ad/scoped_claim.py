"""AD1 development specimen: exact, immutable-snapshot aggregate reuse."""
from collections import Counter
from dataclasses import asdict, dataclass, field
from hashlib import sha256
import json
from pathlib import Path

DOMAIN = frozenset((-1, 0, 1, 5, 8))
MAX_ROWS = 4


class AdmissionError(ValueError):
    pass


class EvidenceError(ValueError):
    pass


def validate(rows):
    if not isinstance(rows, list) or len(rows) > MAX_ROWS:
        raise AdmissionError("expected at most four rows")
    seen = set()
    for row in rows:
        if not isinstance(row, list) or len(row) != 2:
            raise AdmissionError("expected [occurrence_id,value]")
        key, value = row
        if not isinstance(key, str) or not key or key in seen:
            raise AdmissionError("occurrence IDs must be unique nonempty strings")
        if type(value) is not int or value not in DOMAIN:
            raise AdmissionError("value outside strict integer domain; NULL excluded")
        seen.add(key)
    return rows


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


@dataclass
class Metrics:
    source_read_attempts: int = 0
    source_reads: int = 0
    source_bytes: int = 0
    decoded_rows: int = 0
    aggregate_recomputations: int = 0
    cache_hits: int = 0


@dataclass(frozen=True)
class Claim:
    source_relative: str
    source_sha256: str
    value_bag: tuple
    aggregate_pair: tuple
    statement: str = "S=sum(occurrences); D=sum(distinct values); compare S=D"
    quantifier: str = "this admitted immutable source snapshot"
    domain: str = "0..4 rows, unique nonempty string IDs, values {-1,0,1,5,8}; no NULL"
    evidence: str = "validated source and exact finite integer calculation; hash binds bytes only"
    receiver: tuple = ("aggregate_pair", "equality", "distinct_value_condition")
    omitted: tuple = ("row order", "occurrence-ID/value assignment")
    reopen: str = "read source_relative, verify source_sha256, validate rows"
    boundary: str = "needed missing/altered source => OPEN; unknown operation => OPEN_NEW_CONTRACT"


class SourceAccess:
    """Shared mechanics, not aggregate/conditional/cache decisions."""
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.metrics = Metrics()

    def read(self, relative, expected_hash=None):
        target = (self.root / relative).resolve()
        if not target.is_relative_to(self.root):
            raise AdmissionError("source route escapes supplied root")
        self.metrics.source_read_attempts += 1
        try:
            raw = target.read_bytes()
        except OSError as error:
            raise EvidenceError("backing unavailable") from error
        self.metrics.source_reads += 1
        self.metrics.source_bytes += len(raw)
        digest = sha256(raw).hexdigest()
        if expected_hash is not None and digest != expected_hash:
            raise EvidenceError("backing bytes differ from the saved snapshot")
        try:
            rows = validate(json.loads(raw))
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise AdmissionError("malformed source JSON") from error
        self.metrics.decoded_rows += len(rows)
        return rows, digest


class ScopedStore(SourceAccess):
    def __init__(self, root):
        super().__init__(root)
        self.cache = {}
        self.claims = []

    def calculate(self, bag):
        self.metrics.aggregate_recomputations += 1
        return sum(bag), sum(set(bag))

    def promote(self, relative):
        rows, digest = self.read(relative)
        bag = tuple(sorted(value for _, value in rows))
        if bag in self.cache:
            self.metrics.cache_hits += 1
        else:
            self.cache[bag] = self.calculate(bag)
        claim = Claim(relative, digest, bag, self.cache[bag])
        self.claims.append(claim)
        return claim

    def hot(self, claim):
        return {"status": "ONE", "value": list(claim.aggregate_pair),
                "equal": claim.aggregate_pair[0] == claim.aggregate_pair[1]}

    def conditional(self, claim):
        if len(claim.value_bag) != len(set(claim.value_bag)):
            return {"status": "REJECT_ASSUMPTION"}
        return {"status": "ONE", "value": True}

    def universal(self):
        return {"status": "REJECT", "counterexample": [["P", 5], ["Q", 5]],
                "value": list(self.calculate((5, 5)))}

    def lookup(self, claim, query_id):
        try:
            rows, _ = self.read(claim.source_relative, claim.source_sha256)
        except (EvidenceError, AdmissionError) as error:
            return {"status": "OPEN", "reason": str(error)}
        matches = [value for key, value in rows if key == query_id]
        return {"status": "ONE", "value": matches[0]} if matches else {"status": "NONE"}

    def unsupported(self):
        return {"status": "OPEN_NEW_CONTRACT"}

    def retained(self):
        return {"records": [asdict(c) for c in self.claims],
                "cache": [{"bag": k, "pair": v} for k, v in self.cache.items()]}


class OrdinaryCache(SourceAccess):
    """Conventional typed memoization, same source and query access."""
    def __init__(self, root):
        super().__init__(root)
        self.memo = {}
        self.records = []

    def calculate(self, frequencies):
        self.metrics.aggregate_recomputations += 1
        total = 0
        distinct = 0
        for value, count in frequencies:
            total += value * count
            distinct += value
        return total, distinct

    def promote(self, relative):
        rows, digest = self.read(relative)
        key = tuple(sorted(Counter(row[1] for row in rows).items()))
        if key not in self.memo:
            self.memo[key] = self.calculate(key)
        else:
            self.metrics.cache_hits += 1
        record = {"path": relative, "hash": digest, "frequencies": key,
                  "pair": self.memo[key], "scope": "immutable admitted snapshot"}
        self.records.append(record)
        return record

    def hot(self, record):
        left, right = record["pair"]
        return {"status": "ONE", "value": [left, right], "equal": left == right}

    def conditional(self, record):
        for _, multiplicity in record["frequencies"]:
            if multiplicity > 1:
                return {"status": "REJECT_ASSUMPTION"}
        return {"status": "ONE", "value": True}

    def universal(self):
        witness = ((5, 2),)
        return {"status": "REJECT", "counterexample": [["P", 5], ["Q", 5]],
                "value": list(self.calculate(witness))}

    def lookup(self, record, query_id):
        try:
            rows, _ = self.read(record["path"], record["hash"])
        except (EvidenceError, AdmissionError) as error:
            return {"status": "OPEN", "reason": str(error)}
        for key, value in rows:
            if key == query_id:
                return {"status": "ONE", "value": value}
        return {"status": "NONE"}

    def unsupported(self):
        return {"status": "OPEN_NEW_CONTRACT"}

    def retained(self):
        return {"records": self.records,
                "cache": [{"frequencies": k, "pair": v} for k, v in self.memo.items()]}
