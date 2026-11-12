# Trance learning project

Two Hebrew (RTL) learning pages about trance music. They were built as prototypes in a Claude chat on 2026-11-12 and handed over here to be reskinned and developed further.

The owner is a web developer learning the subject from zero. The pages teach him first; later they are meant to become a game that teaches other people.

## Status

Both pages are reskinned in **S2 flat cartoon** (2026-11-12). Spec: `docs/DESIGN-S2-flat-cartoon.md`. Every shared component, in every state, is on `docs/s2-sheet.html`.

Decisions the owner made on 2026-11-12:

1. **Stack:** stays vanilla HTML/CSS/JS, no build step. Whether it later becomes a content pack for the Vite + React + TS learning-game engine is still open.
2. **Dark mode:** none. S2 is light only.
3. **Structure:** two pages that share `assets/` (skin, palette picker, video player). The School's last level links to the tree with a relative link.
4. **English:** not now. Hebrew only.
5. **Contrast:** text on any colored fill is ink, never white. Headings are ink with a primary-color marker behind them. This departs from the source card, where white text on orange and cyan failed WCAG.
6. **Palette:** the viewer picks one of three: UV (default), Laser, S2 original. Shapes stay S2 in all three.
7. **Real tracks:** embedded YouTube players that load only when clicked, with a search link kept as a fallback.

## How the owner works

- Give a short, high-level plan before any non-trivial task and wait for a go-ahead. Small fixes do not need one.
- Never choose a stack, framework or tool for him. Recommend with reasons, then wait.
- Code, comments and docs in English. The learning content itself is Hebrew.
- Push back when something he asks for is wrong or there is a better way, and flag risks he may not see.
- Small change: give only the changed part and where it goes. Wide change: the full file.

## What is in the folder

| Path | What it is |
| --- | --- |
| `prototypes/trance-school.html` | Trance School. Seven game-like levels teaching the basics from zero. |
| `prototypes/trance-family-tree.html` | Trance Family Tree. 38 genres across 5 eras with lineage and per-era quizzes. Generated file, do not edit by hand. |
| `data/trance-data.json` | The dataset behind the tree: 38 genres, 76 parent links, 5 eras, 4 families. |
| `tools/tree-template.html` | Source of the tree page (markup, CSS, JS) with a `/*__DATA__*/` marker. |
| `tools/build-tree.py` | Validates the dataset and rebuilds the tree page. Run `python3 tools/build-tree.py`. |
| `assets/s2.css` | The S2 skin: role-named color tokens, the three palettes, and shared components (card, button, pill, bar, stars, answer, slider, video). |
| `assets/s2-palette.js` | The palette picker. Fills any `[data-palette-picker]` element and saves the choice in localStorage under `trance-palette`. |
| `assets/s2-video.js` | `S2Video.player({artist, title, note})`: a thumbnail that becomes a youtube-nocookie player when clicked, plus a search link. |
| `assets/videos.js` | YouTube IDs for the real tracks, keyed `"Artist — Title"`. Shared by both pages. |
| `tools/check-videos.py` | Checks that every track has an ID and that each ID still exists and allows embedding. Needs network access. |
| `docs/s2-sheet.html` | Component sheet: all S2 components in all states, a palette switcher, and a live contrast table. Check a new palette here. |
| `.claude/launch.json` | Local static server (`python3 -m http.server 8765`) for the browser pane. |
| `docs/DESIGN-S2-flat-cartoon.md` | The skin spec. |
| `docs/design-reference.html` | The original S2 card, rendered, plus an unapproved Hebrew adaptation sketch. |
| `docs/SOURCES.md` | Sources used for the history content. |

Both pages link `../assets/`, so they are no longer single files: publishing one as an artifact means attaching those files too. Fredoka loads from Google Fonts. Serve the folder over HTTP (`python3 -m http.server 8765`, then open `/prototypes/…`). YouTube refuses embeds on `file://` pages, so there the player opens YouTube in a new tab instead.

RTL rules:
- Everything that represents time or order runs right to left, like the text: the level 5 timeline (opening on the right), the beat grid (step 1 next to the labels on the right), the beat counter, the BPM slider and its scale (100 on the right). Do not force these to LTR.
- Only English names, numbers and media icons (the play triangle) stay LTR.
- Number ranges such as `125–135` display reversed inside RTL text. Each page's `h()` helper wraps them in an LTR isolate (`isoRanges`), for both `text` and string children; keep that when you add text.

## Trance School: how it works

One file, one IIFE. The parts, in order:

- **Sound engine.** Web Audio API, no samples. `I` holds the instruments (kick, hat, clap, bass, pad, pluck, lead, acid, stab, blip, riser). `playStep(cfg, info, t, dur)` plays one 16th-note step from a config object such as `{ bpm: 138, kick: FOUR, hat: OFF, bass: 'offbeat', arp: 'minor' }`. `start(run)` and `stop()` drive a look-ahead scheduler; only one thing plays at a time. A run is either a loop (`cfg`), a fixed number of bars (`bars`), or a song (`song`, a list of sections).
- **`transport(cls, label, makeRun)`** builds a play/stop button bound to one run.
- **`SK`** holds the style sketches (house, techno, trance, prog, upl, goa, fullon, dark, hitech). **`STYLES`** describes the six styles of level 7. **`SONG`** and **`BLOCKS`** define the 18-bar arrangement of level 5.
- **`TOYS[n]`** builds the interactive "machine" for level n.
- **`CHALLENGES[n]()`** returns three questions. `mcq()` makes a text question, `listen()` makes a question answered by playing clips.
- **`LEVELS`** holds the lesson text, glossary terms and real tracks (`real: [[artist, title, note]]`, played through `S2Video`).
- **State** lives in localStorage under `trance-school-v1`: `{ unlocked, stars, openAll, current }`. Two correct answers out of three unlock the next level.
- `TREE_URL` is the relative link `trance-family-tree.html`.
- When a real track starts, `s2video:play` stops the synth, so only one thing plays at a time.

The seven levels: tempo and BPM, four-on-the-floor, the bassline (offbeat vs rolling), melody layers (pad, arpeggio, lead, acid), track structure, what makes it trance (vs house and techno), and telling styles apart by ear.

## Trance Family Tree: how it works

- The page reads the dataset from an inline `<script type="application/json" id="trance-data">` block.
- Five era bands are stacked top to bottom, so time flows down. Inside an era, a genre sits one row below its latest parent from the same era.
- Lineage curves are SVG paths computed from the DOM positions of the genre chips and redrawn on resize.
- Selecting a genre highlights its ancestors and descendants and opens a detail card (sticky side panel on wide screens, inline under the era on narrow ones).
- Six quiz generators (`sound`, `origin`, `parent`, `artist`, `track`, `first`) build five questions per era from the dataset. Distractors are chosen to exclude a genre's own ancestors and descendants.

### Dataset schema

Each genre: `id`, `name_he`, `name_en`, `era` (1 to 5), `year` (approximate), `family` (`roots`, `club`, `psy`, `out`), `origin_he`, `parents` (ids of direct sources), `story_he`, `sound_he`, `bpm` (string or null), `artists`, `track` (`{artist, title, year}` or null), `disputed_he` (string or null).

Since 2026-11-12 each genre also has `pioneers` and `today`: up to 3 artists each, `{name, role_he, track: {artist, title, year} | null, sources: [url]}`, plus `today_note_he` (string or null) when `today` has fewer than 3. Pioneers founded the style; `today` are artists with 2024–2026 evidence (charts, festival lineups, label releases). A pioneer without a recording (the Goa beach DJs) has `track: null`. Every artist must have a source URL. Their videos live in `assets/videos.js` like all others.

`build-tree.py` checks: unique ids, every parent exists, no parent is younger than its child or in a later era, no cycles, year inside the era's range, no empty text fields, and for pioneers/today: max 3, name and role_he present, complete track or null, at least one source URL, `today_note_he` when `today` has fewer than 3.

## Content rules

- Hebrew text, with the English term in parentheses on first use: `ארפג' (Arpeggio)`.
- Artist, label and track names stay in English and are rendered LTR inside RTL text (the `.ltr` class).
- Explain every term before using it. The reader has no musical background.
- Contested origins are marked, not smoothed over. Keep every `disputed_he` note.
- Real tracks play through click-to-load YouTube embeds (`assets/videos.js`). Keep the search link under each one, because videos get removed. When you add a track, add its ID and run `python3 tools/check-videos.py`.
- The synthesized sound demonstrates a principle (tempo, bass pattern, structure). It is not meant to sound like a finished production.
- Parent links list only direct sources. They are a deliberate simplification.

## Known gaps

- Nobody has listened to the synthesized sketches. The code ran without errors, but how each sketch actually sounds is unchecked. Level 7 is the most likely to need tuning: Goa vs full-on and dark vs hi-tech differ only subtly.
- Some landmark tracks and artist lists come from model knowledge, not from the sources in `docs/SOURCES.md`. Examples: Marco V, "Simulated"; Armin van Buuren, "Ping Pong"; the artists listed for forest and hi-tech. Verify any fact before building game questions on it.
- The least certain entries are the years for tech trance and hi-tech, and Russia as the origin of hi-tech. Both carry a `disputed_he` note.
- Fredoka's Hebrew subset was checked at weights 500 and 700 and renders.
- Video IDs were found by search and checked through oEmbed for existence and embedding. Their choice of upload (official, remaster, fan upload) was not reviewed by a person.
- Sensient, "Pressure Optimal" (the `zenonesque` track) does not appear on YouTube under that title, so the title is probably wrong. It has no video and shows only the search link. Check the dataset entry.
- Video choices worth a second look: Age of Love uses the 1990 original vocal mix (`FrCAEibKMR4`), but the 1992 Jam & Spoon "Watch Out For Stella" mix (`-ubrhlYVv2k`) is the famous one. Kindzadza, which has no title in level 7, plays "Quantime" (alternatives: "Cristal Inside" `Rh4V7H0gnAY`, "Intergalactic Boom" `_SVzmqHPVFI`). Kraftwerk is a 3:20 remaster (fan upload of the original: `kv8_EZrNhpY`). A Split-Second "Flesh" is the 7-inch edit (12-inch: `-FDy-RVeI-A`). X-Dream "Radio" is a low-view Topic upload that may not be the right track.
- Progress is stored per browser only.
- **iPhone audio (fixed 2026-11-12, not yet confirmed on a real iPhone).** A tester got no sound in levels 5–7 on the first version. The synthesis is fine: every sketch in levels 5–7 measures real output in Chrome. The cause was `ensureCtx()`, which only resumed a `'suspended'` context. iOS Safari puts the context into `'interrupted'` after switching apps (the tester was chatting in WhatsApp between level 4 and 5), so every later play stayed silent. Now an interrupted or closed context is rebuilt inside the tap, any other non-running state is resumed, and `navigator.audioSession.type = 'playback'` lets audio play with the silent switch on (Safari 17+).

## What was verified

- After the S2 reskin, both pages were rendered at desktop and phone widths with no horizontal overflow and no console errors, in all three palettes.
- School: every control in every level was clicked and every challenge completed several times.
- Tree: each era's quiz was run 15 times before the reskin and 4 times after it; every run produced five questions with four distinct options and exactly one correct answer.
