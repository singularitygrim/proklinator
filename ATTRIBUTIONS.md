# ATTRIBUTIONS

Third-party material shipped with ПРОКЛИНАТОР, and the provenance of everything else in this repository.

Кратко: сторонние компоненты — значки Lucide (ISC), спрайты частиц Kenney (CC0), бумажная текстура ambientCG (CC0), шрифт Playfair Display (OFL) и две библиотеки с jsDelivr (MIT).
Аватары, алтарь, герой, PWA-иконки, рисунки пустых состояний, рунные кольца ритуала и все тексты — собственные. Сторонних брендовых наборов (логотипов платформ, соцсетей, компаний) в приложении нет.

Only permissive licenses are admitted: CC0, ISC, MIT, OFL. Every third-party binary is regenerated from a pinned, SHA-256-checked download by `tools/build_assets.py`, so its provenance can be replayed.

## Icons — Lucide (ISC)

- Source: [Lucide Icons](https://lucide.dev), npm package `lucide-static` **v0.469.0**
  (repository: https://github.com/lucide-icons/lucide).
- License: **ISC** — full text at the end of this file.
  Copyright (c) for portions of Lucide are held by Cole Bemis 2013-2022 as part of Feather (MIT).
  All other copyright (c) for Lucide are held by Lucide Contributors 2022.
- Files shipped verbatim from the package — each carries the header `<!-- @license lucide-static v0.469.0 - ISC -->`:
  - `assets/icons/categories/` (v20.3) — the eight category glyphs:
    `users.svg`, `briefcase.svg`, `heart-crack.svg`, `graduation-cap.svg`, `home.svg` (Lucide's `house`, the icon formerly named `home`; only the file name differs), `smartphone.svg`, `zap.svg`, `globe.svg`.
    Mapped in `app.js` (`ICO`) to the category ids `people`, `work`, `relations`, `study`, `home`, `tech`, `situations`, `world`.
  - `assets/icons/` (v20.2):
    `clock.svg`, `crown.svg`, `layout-grid.svg`, `lock.svg`, `lucide-flame.svg`, `lucide-heart.svg`, `moon.svg`, `share-2.svg`, `shield-check.svg`, `sparkles.svg`, `user.svg`.
- Inline icons in `app.js` / `index.html` (`ICO`, `ICONS`, tab bar, intro) and the remaining `assets/icons/*.svg` are drawn in-house in the Lucide style (24-unit grid, `stroke="currentColor"`, round caps and joins). Where their geometry is reused or adapted from Lucide it is covered by the same ISC notice. The only deliberate deviation is the stroke width (1.8 instead of Lucide's 2) so the whole set reads as one weight.
- The icons are self-hosted; nothing is loaded from Lucide's servers.

## Particle sprites — Kenney (CC0 1.0 Universal)

- Source: [Kenney Particle Pack](https://kenney.nl/assets/particle-pack) v1.1 and [Kenney Smoke Particles](https://kenney.nl/assets/smoke-particles) by Kenney Vleugels (Kenney.nl);
  filter templates in the Particle Pack credited by the author to Indigo Ray, Craig Nisbet, Zoltan Erdokovy, Heliagon, ThreeDee, Killst4r and Tim2501.
- License: **CC0 1.0 Universal** (public domain dedication) — https://creativecommons.org/publicdomain/zero/1.0/ . Credit is not required; given here anyway.
  The pack's own `License.txt` ships as [`assets/fx/LICENSE-kenney.txt`](assets/fx/LICENSE-kenney.txt).
- Pinned downloads (SHA-256 in `tools/build_assets.py`): `kenney_particle-pack.zip` `b631d4b0…1d8958`, `kenney_smoke-particles.zip` `97a1d09c…a1e1c9`.
- Files in `assets/fx/` (v20.5) are downscaled, **recoloured** derivatives (blood / ember / ash / smoke ramps baked in by `tools/build_assets.py fx`):

  | file | source sprite | role in the ritual |
  | --- | --- | --- |
  | `ember-02.png` | Particle Pack `circle_05` | rising embers |
  | `ember-01.png` | Particle Pack `scorch_02` | crackling motes |
  | `spark-01.png` | Particle Pack `star_07` | spark burst at the stamp |
  | `ash-01.png` | Particle Pack `dirt_01` | drifting soot |
  | `smoke-01.png` | Particle Pack `smoke_08` | smoke off the rim |
  | `smoke-02.png` | Smoke Particles `blackSmoke12` | smoke off the rim |
  | `crack-01.png` | Particle Pack `spark_05` | lightning cracks («Апокалипсис») |
  | `sigil-glow.png` | Particle Pack `light_02` | glow under the altar disc |

- The rune rings, heptagram, dial and crown of the ritual disc are **not** Kenney: they are drawn at run time on a canvas by `app.js` (`runeRing`) — in-house, decorative glyphs with no real inscription.

## Paper grain — ambientCG Paper001 (CC0 1.0 Universal)

- Source: [ambientCG — Paper 001](https://ambientcg.com/a/Paper001), 1K JPG set (`Paper001_1K-JPG.zip`, SHA-256 `5be094ff…7a0013`), published by ambientCG (Lennart Demes).
- License: **CC0 1.0 Universal** — https://creativecommons.org/publicdomain/zero/1.0/ (all ambientCG assets are released under CC0).
- `assets/splash/paper-grain.jpg` (v20.5) is the colour map high-passed to neutral grey and downscaled by `tools/build_assets.py grain`; it is the only file derived from it and is used at 6 % opacity over the splash.

## Font — Playfair Display (SIL OFL 1.1)

- `fonts/playfair-display-*.woff2` — self-hosted subsets (latin, cyrillic, italic).
- Copyright 2017 The Playfair Display Project Authors (https://github.com/clauseggers/Playfair-Display), with Reserved Font Name "Playfair Display".
- Licensed under the **SIL Open Font License, Version 1.1** — full text in [`fonts/OFL.txt`](fonts/OFL.txt).

## Runtime libraries (not bundled — loaded from jsDelivr with pinned versions and SRI)

- **three.js** 0.160.0 — MIT License, © 2010-2024 three.js authors — `https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js`
- **anime.js** 3.2.2 — MIT License, © Julian Garnier — `https://cdn.jsdelivr.net/npm/animejs@3.2.2/lib/anime.min.js`

No copies of these libraries live in the repository; the browser fetches them with the integrity hashes in `index.html`, and the service worker caches them after the first successful load.

## In-house artwork and assets (no third-party sources)

- `assets/avatars/hood.png`, `seal.png`, `raven.png`, `pack-3.png` — profile avatar presets (v20.2). In-house / staff artwork made for ПРОКЛИНАТОР.
- `hero-altar.jpg` (and the copy in `docs/`) — the altar: hero image and link preview. In-house / staff artwork.
- `assets/splash/altar-9x16.jpg` (v20.5) — the same altar as a true 9:16 frame (1080×1920): a centre-safe cover crop of `hero-altar.jpg` produced by `tools/build_assets.py altar`. No other source.
- `icons/icon-512.png` — the app's own crown-in-a-ring sigil, the in-house master. `icon-192.png`, `apple-touch-icon.png`, `maskable-512.png` are derived from it by `tools/build_assets.py icons` (v20.5); nothing third-party.
- `assets/empty/quiet-candle.svg`, `hollow-heart.svg`, `unlit-altar.svg`, `cold-ash.svg` (v20.5) — empty-state illustrations, drawn in-house in the Lucide stroke style; the same markup is inlined as `EMPTY_ART` in `app.js`.
- Inline decorative SVG (`ICO.crownGold`, the 03:00 clock art, the static ritual sigil in `index.html`), the run-time rune rings of the ritual (`runeRing` in `app.js`) and the poster / OG cards painted on canvas at run time — in-house.
- All copy — Freya's shell and intro texts, Tyr's legal texts, the sin catalogue and verdicts — in-house.

## Deliberately absent

- No third-party brand kits: no platform, social-network, messenger or company logos and no trademarked glyphs. Sharing goes through the Web Share API (or copy / download) with plain links; contact rows are text links.
- No stock-photo or clip-art libraries, no icon fonts, no remote font services.

## Scope

This file covers third-party material only. Application code, copy and the in-house assets listed above are the publisher's own work (publisher: Singularity, as shown in «О приложении») and are not covered by the licenses quoted here.

When adding a Lucide icon, copy the file verbatim from `lucide-static@0.469.0` (keep its license header) and list it above; if a newer Lucide version is adopted, update the version here and in the file headers together.
When adding a sprite or texture, add it to `tools/build_assets.py` (source, pinned hash, ramp) rather than committing a hand-edited file, and list it in the table above. Licenses other than CC0 / ISC / MIT / OFL are not admitted.

---

## ISC License (Lucide) — verbatim

```
ISC License

Copyright (c) for portions of Lucide are held by Cole Bemis 2013-2022 as part of Feather (MIT). All other copyright (c) for Lucide are held by Lucide Contributors 2022.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
```
