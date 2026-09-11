# ATTRIBUTIONS

Third-party material shipped with ПРОКЛИНАТОР, and the provenance of everything else in this repository.

Кратко: сторонние компоненты — значки Lucide (ISC), шрифт Playfair Display (OFL) и две библиотеки с jsDelivr (MIT).
Аватары, алтарь, герой, PWA-иконки и все тексты — собственные. Сторонних брендовых наборов (логотипов платформ, соцсетей, компаний) в приложении нет.

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
- `assets/splash/altar-9x16.png`, `hero-altar.jpg` (and the copy in `docs/`) — the altar: splash, intro gate, hero image and link preview. In-house / staff artwork.
- `icons/icon-192.png`, `icon-512.png`, `maskable-512.png`, `apple-touch-icon.png` — PWA icons: the app's own crown-in-a-ring sigil. In-house.
- Inline decorative SVG (`ICO.sig` wax seal, `ICO.crownGold`, the 03:00 clock art) and the poster / OG cards painted on canvas at run time — in-house.
- All copy — Freya's shell and intro texts, Tyr's legal texts, the sin catalogue and verdicts — in-house.

## Deliberately absent

- No third-party brand kits: no platform, social-network, messenger or company logos and no trademarked glyphs. Sharing goes through the Web Share API (or copy / download) with plain links; contact rows are text links.
- No stock-photo or clip-art libraries, no icon fonts, no remote font services.

## Scope

This file covers third-party material only. Application code, copy and the in-house assets listed above are the publisher's own work (publisher: Singularity, as shown in «О приложении») and are not covered by the licenses quoted here.

When adding a Lucide icon, copy the file verbatim from `lucide-static@0.469.0` (keep its license header) and list it above; if a newer Lucide version is adopted, update the version here and in the file headers together.

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
