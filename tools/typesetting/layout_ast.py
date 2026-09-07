"""Presentation-only Pandoc AST changes; source mathematics stays recoverable."""
import copy


def plain(node):
    if isinstance(node, list):
        return "".join(plain(x) for x in node)
    if not isinstance(node, dict):
        return ""
    if node.get("t") in ("Str", "Code", "Math"):
        return node["c"] if node["t"] == "Str" else node["c"][1]
    if node.get("t") in ("Space", "SoftBreak", "LineBreak"):
        return " "
    return plain(node.get("c", []))


def inline_breaks(value):
    result, depth = [], 0
    for i, char in enumerate(value):
        escaped = i > 0 and value[i-1] == "\\"
        if char == "{" and not escaped:
            depth += 1
        elif char == "}" and not escaped:
            depth -= 1
        result.append(char)
        if char == "," and not escaped and depth == 0:
            result.append(r"\allowbreak ")
    return "".join(result)


def raw(value):
    return {"t": "RawBlock", "c": ["latex", value]}


def transform(ast):
    result = copy.deepcopy(ast)
    receipt = {"inline_math_breaks": [], "table_widths": [], "figures": [], "compact_table_space": [], "page_guards": [], "qed_spacing": [], "inline_math_keeps": []}

    def walk(node):
        if isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, dict):
            if node.get("t") == "Para":
                c = node["c"]
                if len(c) >= 2 and c[-2].get("t") == "Space" and (
                    (c[-1].get("t") == "Math" and c[-1]["c"][1] == r"\square")
                    or (c[-1].get("t") == "Str" and c[-1]["c"] == "∎")
                ):
                    receipt["qed_spacing"].append({"paragraph": plain(c), "treatment": "Nonbreaking space before the proof-ending symbol."})
                    c[-2] = {"t": "RawInline", "c": ["latex", r"\nobreakspace{}"]}
            if node.get("t") == "Math" and node["c"][0]["t"] == "InlineMath":
                old = node["c"][1]
                new = inline_breaks(old)
                if old != new:
                    assert new.replace(r"\allowbreak ", "") == old
                    node["c"][1] = new
                    receipt["inline_math_breaks"].append({"before": old, "after": new})
            if node.get("t") == "Table":
                c = node["c"]
                header = plain(c[3])
                if "Meaning in this manuscript" in header and len(c[2]) == 3:
                    for col, width in zip(c[2], [.23, .60, .17]):
                        col[1] = {"t": "ColWidth", "c": width}
                    receipt["table_widths"].append({"header": header, "widths": [.23, .60, .17]})
                if "Continuous-scan" in header and "Purpose" in header and len(c[2]) == 8:
                    widths = [.13, .09, .11, .09, .12, .14, .11, .21]
                    for col, width in zip(c[2], widths):
                        col[1] = {"t": "ColWidth", "c": width}
                    receipt["table_widths"].append({"header": header, "widths": widths})
                if header.startswith("Manuscript result family") and len(c[2]) == 3:
                    widths = [.24, .34, .42]
                    for col, width in zip(c[2], widths):
                        col[1] = {"t": "ColWidth", "c": width}
                    receipt["table_widths"].append({"header": header, "widths": widths})
            for val in node.values():
                walk(val)

    walk(result)
    blocks, output, i = result["blocks"], [], 0
    # These two short equalities crossed a page turn in the reviewed output.
    # Keep each existing Math node in a text box; its equation bytes are unchanged.
    keep_math = {r"\varepsilon\lambda\gamma^3=x+y\omega", "x=m+(n+1)(M-m)/2"}
    for block in blocks:
        if block.get("t") != "Para":
            continue
        inlines = []
        for node in block["c"]:
            if node.get("t") == "Math" and node["c"][1] in keep_math:
                inlines.extend([{"t": "RawInline", "c": ["latex", r"\mbox{"]}, node, {"t": "RawInline", "c": ["latex", "}"]}])
                receipt["inline_math_keeps"].append(node["c"][1])
            else:
                inlines.append(node)
        block["c"] = inlines
    # Move each space reservation before the introduction (and its heading,
    # when adjacent). Reserving after that text can strand it on the prior page.
    reservations = {}
    table_lines = {"Neighborhood": 10, "Complete supplied graph": 10,
                   "Operation or lossy description": 25, "StepOrbit": 17,
                   "Row t": 19, "FunctionLower integer": 11,
                   "WordComplete path": 13, "Work category": 13}
    for table_i, block in enumerate(blocks):
        if block.get("t") != "Table":
            continue
        header = plain(block["c"][3])
        lines = next((n for prefix,n in table_lines.items() if header.startswith(prefix)), 5)
        start = table_i
        if start and blocks[start-1].get("t") == "Para":
            start -= 1
            lines += max(2, (len(plain(blocks[start]))+69)//70)
        if start and blocks[start-1].get("t") == "Header":
            start -= 1
            lines += 3
        reservations[start] = max(reservations.get(start, 0), lines)
        receipt["compact_table_space"].append({"header": header, "reserved_baselines": lines, "treatment": "Reserve space before the table introduction and any adjacent heading; inspect actual pagination."})
    closing_groups = {"III.5.5. A timing adapter and its precise receiver": 32,
                      "Standard models and computational constructions": 9,
                      "Proposition II.2.4": 22,
                      "For the independent unrestricted route,": 20,
                      "For each row, the proved normalized or raw monotonicity": 9}
    for block_i, block in enumerate(blocks):
        if block.get("t") not in ("Header", "Para"):
            continue
        text = plain(block)
        for prefix, lines in closing_groups.items():
            if text.startswith(prefix):
                reservations[block_i] = max(reservations.get(block_i, 0), lines)
                receipt["page_guards"].append({"target": prefix, "reserved_baselines": lines, "treatment": "Keep the short closing argument or paired endpoint calculation together."})
    while i < len(blocks):
        block = blocks[i]
        previous = blocks[i-1] if i else None
        if i in reservations:
            output.append(raw(r"\Needspace{" + str(reservations[i]) + r"\baselineskip}"))
        display = block.get("t") == "Para" and any(x.get("t") == "Math" and x["c"][0]["t"] == "DisplayMath" for x in block["c"])
        if display and previous and previous.get("t") == "Para":
            output.append(raw(r"\nopagebreak[4]"))
            receipt["page_guards"].append({"target": plain(block), "treatment": "Keep display with the preceding paragraph's last lines."})
        if block.get("t") == "Header" and block["c"][0] >= 4 and i not in reservations:
            output.append(raw(r"\Needspace{7\baselineskip}"))
            receipt["page_guards"].append({"target": plain(block), "treatment": "Reserve seven lines for a subsection heading and its opening."})
        if block.get("t") == "Para" and plain(block).startswith(("Theorem ", "Proposition ", "Lemma ", "Corollary ")) and not (previous and previous.get("t") == "Header") and i not in reservations:
            output.append(raw(r"\Needspace{6\baselineskip}"))
            receipt["page_guards"].append({"target": plain(block)[:150], "treatment": "Reserve six lines for a statement opening."})
        if block.get("t") == "Table":
            header = plain(block["c"][3])
            if previous and previous.get("t") == "Para":
                output.append(raw(r"\nopagebreak[4]"))
                receipt["page_guards"].append({"target": header, "treatment": "Keep table opening with its introduction."})
        if block.get("t") != "Figure":
            output.append(block)
            i += 1
            continue
        inner = block["c"][2]
        assert len(inner) == 1 and inner[0]["t"] in ("Plain", "Para")
        images = inner[0]["c"]
        assert len(images) == 1 and images[0]["t"] == "Image"
        caption = blocks[i+1]
        assert caption["t"] == "Para" and plain(caption).startswith("Figure"), plain(caption)
        # Alt text remains on the Image node; the written source caption is printed once.
        output.extend([
            raw(r"\par\addvspace{8pt}\noindent\begin{minipage}{\linewidth}\centering"),
            {"t": "Para", "c": images},
            raw(r"\par\vspace{4pt}\raggedright\fontsize{9}{11.7}\selectfont"),
            caption,
            raw(r"\end{minipage}\par\addvspace{8pt}"),
        ])
        receipt["figures"].append({"target": images[0]["c"][2][0], "caption": plain(caption), "treatment": "Nonfloating image and its supplied caption, kept together; no generated second caption."})
        i += 2
    result["blocks"] = output
    return result, receipt
