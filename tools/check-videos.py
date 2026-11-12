"""Check that every real track has a YouTube ID that still exists and allows embedding.

Usage: python3 tools/check-videos.py
Reads assets/videos.js, asks YouTube's oEmbed endpoint about each ID, and lists
tracks with no ID. Run it now and then: videos get removed or have embedding turned off.
Exit code 1 when something needs attention. Needs network access.
"""
import json, pathlib, re, sys, time, urllib.error, urllib.parse, urllib.request

root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "assets" / "videos.js").read_text(encoding="utf-8")
videos = json.loads(re.search(r"window\.TRANCE_VIDEOS\s*=\s*(\{.*\});", src, re.S).group(1))

# Every track the pages ask for: the tree's dataset plus the School's real-track lists.
data = json.loads((root / "data" / "trance-data.json").read_text(encoding="utf-8"))
wanted = {f"{g['track']['artist']} — {g['track']['title']}" for g in data["genres"] if g["track"]}
for g in data["genres"]:
    for p in (g.get("pioneers") or []) + (g.get("today") or []):
        if p.get("track"):  # a pioneer without a recording has track: null
            wanted.add(f"{p['track']['artist']} — {p['track']['title']}")
school = (root / "prototypes" / "trance-school.html").read_text(encoding="utf-8")
for line in re.findall(r"real: \[(.*)\] \}", school):
    for a, t in re.findall(r"\['((?:[^'\\]|\\.)*)', '((?:[^'\\]|\\.)*)', '(?:[^'\\]|\\.)*'\]", line):
        a, t = a.replace("\\'", "'"), t.replace("\\'", "'")
        wanted.add(f"{a} — {t}" if t else a)

problems = [f"no video: {k}" for k in sorted(wanted - videos.keys())]
for key, v in videos.items():
    url = "https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(f"https://www.youtube.com/watch?v={v['id']}")
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            json.load(r)
    except urllib.error.HTTPError as e:
        reason = {401: "embedding disabled", 403: "embedding disabled", 404: "video gone"}.get(e.code, f"HTTP {e.code}")
        problems.append(f"{reason}: {key} ({v['id']})")
    time.sleep(0.3)

print("\n".join(problems) if problems else f"ok: {len(videos)} videos, all embeddable; {len(wanted)} tracks covered")
sys.exit(1 if problems else 0)
