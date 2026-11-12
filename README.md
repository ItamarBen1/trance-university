# Trance learning

Two Hebrew learning pages about trance music, packaged for Claude Code.

**Live:** https://itamarben1.github.io/trance-university/ (GitHub Pages, deploys on every push to `main`).

- `prototypes/trance-school.html`: seven game-like levels that teach the basics from zero.
- `prototypes/trance-family-tree.html`: 38 genres, where each came from and what it led to.

Both pages use the S2 flat cartoon skin from `assets/`. No build step is needed, but serve the folder over HTTP so the YouTube players work:

```
python3 -m http.server 8765
```

Then open http://localhost:8765/prototypes/trance-school.html. The component sheet is at `/docs/s2-sheet.html`.

## Rebuild the tree after editing the data

```
python3 tools/build-tree.py
```

It validates `data/trance-data.json` and regenerates `prototypes/trance-family-tree.html`.

## Check the YouTube videos

```
python3 tools/check-videos.py
```

It flags tracks without a video ID and IDs that were removed or no longer allow embedding. IDs live in `assets/videos.js`.
