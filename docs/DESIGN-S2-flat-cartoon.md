# S2 · Flat cartoon

The skin the owner chose for this project. It comes from his "Electricity Game Sampler" (2026-11-07), where the same level card was drawn in three skins: S1 pixel, **S2 flat cartoon**, S3 technical.

The sampler described S2 as: friendly and bright, phone-game feel, easiest to make approachable for non-technical people later.

`design-reference.html` in this folder renders the original card.

## What the source defines

S2 exists as one level card. Everything in this section is taken from it unchanged.

### Colors

| Role in the card | Value |
| --- | --- |
| Card background (cream) | `#FFF1D6` |
| Ink: text, outlines, hard shadow | `#2B2B2B` |
| Primary: heading and main button (orange) | `#FF6B35` |
| Pill background (cyan) | `#38B6D6` |
| Hearts (pink) | `#FF3E6C` |
| Progress fill (green) | `#8BD346` |
| Icon fill (yellow) | `#FFD23F` |
| Progress track, text on button and pill | `#FFFFFF` |

### Type

- Family: **Fredoka**, weights 500 and 700.
- Heading: 26px, weight 700, line-height 1.1, orange.
- Body: 15px, weight 500.
- Button label: 17px, weight 700.

### Shape and depth

- Every element has a solid ink outline: 3px on the card, 2px on pill, progress bar and button. The icon uses a 4px stroke with round joins.
- Depth is a hard offset shadow with no blur: `0 8px 0` ink on the card, `0 4px 0` ink on the button.
- Card radius 26px. Pill, bar and button are fully rounded (`999px`).
- Fills are flat. No gradients, no blur, no soft shadows.

### Source CSS

```css
.skin{border-radius:14px;padding:18px;display:grid;gap:12px;min-height:280px}
.sk-top{display:flex;justify-content:space-between;align-items:center}
.sk-bar{height:12px;border-radius:999px;overflow:hidden}
.sk-bar i{display:block;height:100%}

.skin-cartoon{background:#FFF1D6;color:#2B2B2B;font-family:"Fredoka",var(--body);border:3px solid #2B2B2B;border-radius:26px;box-shadow:0 8px 0 #2B2B2B}
.skin-cartoon h4{font-size:26px;font-weight:700;color:#FF6B35;line-height:1.1}
.skin-cartoon p{font-size:15px;font-weight:500}
.skin-cartoon .sk-top{font-weight:700;color:#2B2B2B}
.skin-cartoon .sk-top .pill{background:#38B6D6;color:#fff;border-radius:999px;padding:4px 12px;border:2px solid #2B2B2B}
.skin-cartoon .sk-hearts{color:#FF3E6C;font-size:20px}
.skin-cartoon .sk-bar{background:#fff;border:2px solid #2B2B2B;height:16px}
.skin-cartoon .sk-bar i{background:#8BD346}
.skin-cartoon button{font-family:inherit;font-weight:700;font-size:17px;background:#FF6B35;color:#fff;border:2px solid #2B2B2B;border-radius:999px;padding:10px 24px;box-shadow:0 4px 0 #2B2B2B;width:max-content}
```

Icon: `<path d="M38 4 16 36h14l-4 24 22-34H34z" fill="#FFD23F" stroke="#2B2B2B" stroke-width="4" stroke-linejoin="round"/>` in a 64×64 viewBox. It is a lightning bolt, which belongs to the electricity topic. This project needs its own icons in the same style.

## What the source does not define

One card is not a design system. These are open, and the owner has not decided any of them.

- **Page background.** The card is cream, but the page it sits on was the sampler's own neutral grey.
- **Dark mode.** S2 was drawn in light only.
- **States.** Hover, pressed, focus, disabled, selected, correct, wrong and locked are not drawn.
- **Hebrew type.** The card was in English. Fredoka's Google Fonts family lists Hebrew support; confirm the Hebrew glyphs and the 500 and 700 weights render before relying on it.
- **Dense content.** Nothing shows how a glossary, a long paragraph, a 16-step grid or a 38-node graph looks in this style.
- **Motion.**

## Contrast: fix before shipping

Computed WCAG contrast ratios for the source pairings. Normal text needs 4.5:1; large text (24px, or 18.66px bold) and UI graphics need 3:1.

| Pairing | Colors | Ratio |
| --- | --- | --- |
| Ink on cream | `#2B2B2B` on `#FFF1D6` | 12.68:1 |
| Orange heading on cream | `#FF6B35` on `#FFF1D6` | 2.54:1 |
| White label on orange button | `#FFFFFF` on `#FF6B35` | 2.84:1 |
| White label on cyan pill | `#FFFFFF` on `#38B6D6` | 2.38:1 |
| Pink hearts on cream | `#FF3E6C` on `#FFF1D6` | 3.05:1 |
| Ink on orange | `#2B2B2B` on `#FF6B35` | 4.99:1 |
| Ink on cyan | `#2B2B2B` on `#38B6D6` | 5.95:1 |
| Ink on green | `#2B2B2B` on `#8BD346` | 7.76:1 |
| Ink on yellow | `#2B2B2B` on `#FFD23F` | 9.81:1 |
| Ink on pink | `#2B2B2B` on `#FF3E6C` | 4.15:1 |

Three source pairings fail even the large-text threshold: the orange heading, the white button label and the white pill label. This is a learning tool that people read for a long time, so it matters. The simplest fix that keeps the look is ink text on the colored fills (all pass except ink on pink at normal size) and ink or a darker orange for headings on cream. Raise this with the owner; it changes the look he approved.

## Suggested mapping to this project

Suggestions only. Nothing here was approved.

### Shared

- Wrap each unit of content (lesson card, challenge, genre card) in the cartoon card: cream fill, 3px ink outline, 26px radius, `0 8px 0` hard shadow.
- Primary action (play, start challenge, next level): the orange pill button with the `0 4px 0` shadow. On press, move it down 4px and drop the shadow, so it reads as a physical button.
- Level number and counters: the cyan pill.
- Stars: yellow fill with an ink outline. The prototypes use `★☆` text characters.
- Correct and wrong: green and pink fills with ink outline, and keep the ✓ and ✗ marks so color is never the only signal.
- Keep RTL: `dir="rtl"`, logical properties, and LTR isolation for English names.

### Trance School

- The level strip becomes a row of level cards with the pill, stars and a locked state. The sampler's progression section showed a map with a path between units; a path through the seven levels would fit.
- The sound "machine" is a dark panel today. In S2 it could be a white or cream panel with ink outline, where lit steps use green and cyan and the playing step gets a thick ink ring.
- Progress toward the next level can use the outlined progress bar from the card.

### Trance Family Tree

- The four families need four distinct fills. One option from the S2 palette: psy line green `#8BD346`, club line cyan `#38B6D6`, left-the-family orange `#FF6B35`, roots a neutral (white or a darker cream), all with ink text.
- The prototypes also give each family a marker shape (circle, square, diamond, triangle). Keep them, so the families do not depend on color alone.
- Genre chips become small outlined cards with a `0 4px 0` shadow. The selected chip can drop its shadow and take a thicker outline.
- Lineage curves: ink at low opacity by default, full ink at 3px when highlighted.
- 38 outlined, shadowed chips plus 76 curves will be busy. Check the tree at phone width early; this is the part most likely to need a calmer variant of the style.
