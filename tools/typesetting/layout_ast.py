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
    receipt = {"inline_math_breaks": [], "table_widths": [], "figures": [], "compact_table_space": []}

    def walk(node):
        if isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, dict):
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
            for val in node.values():
                walk(val)

    walk(result)
    blocks, output, i = result["blocks"], [], 0
    while i < len(blocks):
        block = blocks[i]
        if block.get("t") == "Table":
            header = plain(block["c"][3])
            content = plain(block)
            rule_comparison = header.startswith("Neighborhood") and "Color-conjugate rule 135" in content
            escape_comparison = header.startswith("Complete supplied graph") and "Indefinite continuation" in header
            if rule_comparison or escape_comparison:
                # Reserve the measured compact table's space before longtable starts.
                # This changes pagination only; table nodes and cells are retained.
                output.append(raw(r"\Needspace{10\baselineskip}"))
                receipt["compact_table_space"].append({"header": header, "reserved_baselines": 10, "treatment": "Keep the short comparison together; verify in the rendered successor."})
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
