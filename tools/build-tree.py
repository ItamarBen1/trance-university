"""Validate data/trance-data.json and rebuild prototypes/trance-family-tree.html.

Usage: python3 tools/build-tree.py
The tree page is a single self-contained file: the template with the dataset inlined as JSON.
"""
import json, pathlib, sys

root = pathlib.Path(__file__).resolve().parent.parent
data = json.loads((root / "data" / "trance-data.json").read_text(encoding="utf-8"))

ids = [g["id"] for g in data["genres"]]
by = {g["id"]: g for g in data["genres"]}
eras = {e["id"]: e for e in data["eras"]}
fams = {f["id"] for f in data["families"]}
problems = []
if len(ids) != len(set(ids)):
    problems.append("duplicate ids")
for g in data["genres"]:
    e = eras[g["era"]]
    if not (e["from"] <= g["year"] <= (e["to"] or 9999)):
        problems.append(f"{g['id']}: year {g['year']} outside era {e['id']}")
    if g["family"] not in fams:
        problems.append(f"{g['id']}: unknown family")
    for p in g["parents"]:
        if p not in by:
            problems.append(f"{g['id']}: missing parent {p}")
        elif by[p]["year"] > g["year"]:
            problems.append(f"{g['id']}: parent {p} is younger")
        elif by[p]["era"] > g["era"]:
            problems.append(f"{g['id']}: parent {p} is in a later era")
    for k in ("name_he", "name_en", "origin_he", "story_he", "sound_he"):
        if not g.get(k):
            problems.append(f"{g['id']}: empty {k}")
    if not g["artists"]:
        problems.append(f"{g['id']}: no artists")
    # Optional: pioneers (who started it) and today (who leads it now), max 3 each.
    for kind in ("pioneers", "today"):
        people = g.get(kind) or []
        if len(people) > 3:
            problems.append(f"{g['id']}: more than 3 {kind}")
        for p in people:
            who = f"{g['id']}/{kind}/{p.get('name', '?')}"
            t = p.get("track") or {}
            if not p.get("name") or not p.get("role_he"):
                problems.append(f"{who}: missing name or role_he")
            # A pioneer may have no track (e.g. a DJ who never released records): track is null then.
            if p.get("track") is not None and (not t.get("artist") or not t.get("title") or not isinstance(t.get("year"), int)):
                problems.append(f"{who}: track needs artist, title and an integer year")
            if not p.get("sources") or not all(str(u).startswith("http") for u in p["sources"]):
                problems.append(f"{who}: needs at least one source URL")
    if g.get("today") is not None and len(g["today"]) < 3 and not g.get("today_note_he"):
        problems.append(f"{g['id']}: fewer than 3 'today' artists needs a today_note_he")

def ancestors(i, seen=None):
    seen = seen if seen is not None else set()
    for p in by[i]["parents"]:
        if p not in seen:
            seen.add(p)
            ancestors(p, seen)
    return seen

for i in ids:
    if i in ancestors(i):
        problems.append(f"{i}: cycle")

if problems:
    print("\n".join(problems))
    sys.exit(1)

payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
tpl = (root / "tools" / "tree-template.html").read_text(encoding="utf-8")
assert "/*__DATA__*/" in tpl, "data marker missing from template"
fragment = tpl.replace("/*__DATA__*/", payload)
head, body = fragment.split('<div class="wrap"', 1)
page = (
    '<!doctype html>\n<html lang="he" dir="rtl">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
    '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
    + head + '</head>\n<body>\n<div class="wrap"' + body + '\n</body>\n</html>\n'
)
out = root / "prototypes" / "trance-family-tree.html"
out.write_text(page, encoding="utf-8")
edges = sum(len(g["parents"]) for g in data["genres"])
print(f"ok: {len(ids)} genres, {edges} parent links -> {out.relative_to(root)}")
