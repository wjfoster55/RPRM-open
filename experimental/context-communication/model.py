"""NEWLY PROPOSED finite question selection under a fixed truthful bit law."""

HYPOTHESES = ("00", "01", "10", "11")
MAX_HISTORY = 32
SCHEMA = "context-communication/v1"


def bit(value, name):
    if type(value) is not int or value not in (0, 1):
        raise ValueError(f"{name} must be a plain integer bit, excluding booleans")
    return value


def hypothesis(value):
    if type(value) is not str or value not in HYPOTHESES:
        raise ValueError("hypothesis must be one of 00, 01, 10, 11")
    return value


def admit_hypotheses(values):
    if type(values) not in (tuple, list) or len(values) > 4:
        raise ValueError("hypotheses must be a list/tuple of at most four IDs")
    clean = tuple(hypothesis(value) for value in values)
    if len(set(clean)) != len(clean):
        raise ValueError("duplicate hypothesis ID")
    return tuple(sorted(clean))


def answer(rule, context):
    """ID ab denotes the fixed response a at context0 and b at context1."""
    rule = hypothesis(rule)
    context = bit(context, "context")
    return int(rule[context])


def admit_history(history):
    """Copy the admitted records, retaining order and duplicate occurrences."""
    if type(history) not in (tuple, list) or len(history) > MAX_HISTORY:
        raise ValueError("history must be a list/tuple of at most 32 records")
    clean = []
    for record in history:
        if type(record) is not dict or set(record) != {"context", "answer"}:
            raise ValueError("record keys must be exactly context and answer")
        clean.append({"context": bit(record["context"], "context"),
                      "answer": bit(record["answer"], "answer")})
    return clean


def _tag(values):
    return "NONE" if not values else "ONE" if len(values) == 1 else "MANY"


def fiber(history):
    """The complete subset of four fixed rules compatible with every record."""
    clean = admit_history(history)
    candidates = [h for h in HYPOTHESES
                  if all(answer(h, row["context"]) == row["answer"] for row in clean)]
    return {"disposition": _tag(candidates), "hypotheses": candidates}


def predictions(history, context):
    """Complete possible response set; an inconsistent source gives NONE."""
    context = bit(context, "context")
    candidates = fiber(history)["hypotheses"]
    values = sorted({answer(h, context) for h in candidates})
    return {"disposition": _tag(values), "values": values}


def append_answer(history, context, response):
    """Return a new history even when its valid bit answer causes contradiction."""
    clean = admit_history(history)
    context = bit(context, "context")
    response = bit(response, "answer")
    if len(clean) == MAX_HISTORY:
        raise ValueError("history capacity reached; no observation was discarded")
    return [*clean, {"context": context, "answer": response}]


def minimax(candidates):
    """Minimize worst surviving cardinality for one unit-cost binary question.

    This is one-step worst-case selection, with no prior probabilities.
    All optimal informative questions are retained; the numeric tie break
    chooses the smaller context solely for a deterministic example policy.
    """
    candidates = admit_hypotheses(candidates)
    if not candidates:
        return {"status": "INCONSISTENT", "hypotheses": [], "questions": [],
                "choice_fiber": {"disposition": "NONE", "contexts": []},
                "chosen_context": None, "worst_case_size": None,
                "reason": "No admitted rule remains; the fixed model supplies no next-question guarantee."}
    questions = []
    for context in (0, 1):
        branches = [{"answer": value, "hypotheses": [h for h in candidates if answer(h, context) == value]}
                    for value in (0, 1)]
        questions.append({"context": context, "branches": branches,
                          "worst_case_size": max(len(branch["hypotheses"]) for branch in branches)})
    best_score = min(question["worst_case_size"] for question in questions)
    best = [question["context"] for question in questions
            if question["worst_case_size"] == best_score and best_score < len(candidates)]
    return {"status": "ASK" if best else "IDENTIFIED", "hypotheses": list(candidates),
            "questions": questions, "choice_fiber": {"disposition": _tag(best), "contexts": best},
            "chosen_context": best[0] if best else None, "worst_case_size": best_score,
            "reason": "Minimize the maximum compatible-rule count; choose the smaller context on a tie."
                      if best else "One admitted rule remains; this identification is conditional on model membership."}


def analyze(history):
    clean = admit_history(history)
    result = fiber(clean)
    conflicts = [{"context": left["context"], "occurrences": [i, j]}
                 for i, left in enumerate(clean) for j, right in enumerate(clean)
                 if i < j and left["context"] == right["context"] and left["answer"] != right["answer"]]
    return {"schema": SCHEMA, "history": clean, "fiber": result,
            "predictions": [{"context": context, **predictions(clean, context)} for context in (0, 1)],
            "selection": minimax(result["hypotheses"]), "conflicts": conflicts}
