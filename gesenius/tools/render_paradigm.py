"""Render a verb paradigm (paradigms.py) as two Typst tables, one per printed
page of the original spread, each with its own row labels."""
from convert import esc, tstr


def form_cell(cell) -> str:
    if cell is None:
        return None  # covered by a rowspan above
    text, _, span = cell.partition("|")
    rowspan = int(span) if span else 1
    if text == "—":
        body = ""
    elif text.startswith("~"):
        body = f"#text(fill: muted, style: \"italic\")[{esc(text[1:])}];"
    else:
        parts = []
        for f in text.split(", "):
            star = f.endswith("*")
            parts.append(f"#pform({tstr(f.rstrip('*'))}, {str(star).lower()});")
        body = "#box[" + ", ".join(parts) + "];"
    if rowspan > 1:
        return f"table.cell(rowspan: {rowspan}, align: center + horizon)[{body}]"
    return f"[{body}]"


def label(row) -> tuple[str, str]:
    sect, num, pers, gen = row[:4]
    a = " ".join(x for x in (sect, num) if x)
    b = " ".join(x for x in (pers.rstrip("."), gen.rstrip(".")) if x)
    return (f"#emph[{esc(a)}];" if a else "", f"{esc(b.split(' ')[0])} #emph[{esc(b.split(' ')[1])}];" if " " in b else esc(b))


def table(half: dict, caption: str) -> str:
    ncols = sum(n for _, n in half["group"])
    header = ["[]", "[]"] + [
        f"table.cell(colspan: {n}, align: center)[#text(fill: primary, weight: \"bold\")[{esc(name)}]]"
        for name, n in half["group"]]
    cells = []
    for row in half["rows"]:
        if row == "rule":
            cells.append(f"table.hline(stroke: 0.6pt + primary)")
            continue
        a, b = label(row)
        if row[0].startswith("Shortened") and all(c == "—" for c in row[4]):
            cells.append(f"table.cell(colspan: {2 + ncols})[{a}]")
            continue
        if row[0].startswith("Shortened"):
            cells.append(f"table.cell(colspan: 2)[#box[{a}]]")
        else:
            cells += [f"[{a}]", f"[{b}]"]
        for c in row[4]:
            r = form_cell(c)
            if r is not None:
                cells.append(r)
    return (f"#ptable({tstr(caption)}, {ncols}, ("
            + ", ".join(header) + "), (" + ", ".join(cells) + ",));\n")


def paradigm(p: dict) -> str:
    out = [f"#parhead({tstr(p['id'])}, {tstr(p['title'])});\n"]
    lp, rp = p["printed_pages"]
    out.append(f"#origpage({tstr(lp)});")
    out.append(table(p["left"], "Qal · Niphʿal · Piʿēl"))
    out.append("#pagebreak(weak: true)\n")
    out.append(f"#origpage({tstr(rp)});")
    out.append(table(p["right"], "Puʿal · Hiphʿîl · Hophʿal · Hithpaʿēl"))
    return "\n".join(out)
