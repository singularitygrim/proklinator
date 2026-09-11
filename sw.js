/* ПРОКЛИНАТОР — light service worker, v20.6.
   Caches the app shell so the page opens without a network. Nothing the user types is ever cached: answers, nick,
   history and settings live in localStorage only; this worker only sees GET requests for the app's own files
   (plus the two pinned jsDelivr libraries the page loads with SRI).
   - navigations: network first (a fresh index.html whenever online), the cached shell after a short timeout / offline
   - same-origin assets (app.js?v=…, fonts, icons, hero, manifest): cache first, refreshed in the background
   - pinned CDN libraries (three / anime): cached on the first successful fetch so the ritual keeps its effects offline;
     the page still verifies their integrity hashes on every load
   Bump VERSION (and APP_JS) with every release: the new worker installs a fresh cache and drops the old one on activate.
   Every failure is soft — a blocked or failed worker leaves the app exactly as it was without one. */
"use strict";

const VERSION = "v20.6";
const CACHE = "proklinator-" + VERSION;
const APP_JS = "app.js?v=20.6";
const NAV_TIMEOUT = 4000;

// The folder sw.js lives in is the app root; index.html is served at the folder URL (Vercel cleanUrls).
const BASE = new URL("./", self.location.href).href;
const SHELL_URL = BASE;

// Without these two the app cannot start offline — the install fails (and is retried next visit) if either is missing.
const REQUIRED = ["./", "./" + APP_JS];
// Best effort: a missing icon or font must not fail the install.
const OPTIONAL = [
  "./manifest.webmanifest",
  "./hero-altar.jpg",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/maskable-512.png",
  "./icons/apple-touch-icon.png",
  // v20.2 art: the portrait altar (splash + intro) and the four avatar presets — best effort like the rest of this list
  "./assets/splash/altar-9x16.jpg",
  "./assets/avatars/hood.png",
  "./assets/avatars/seal.png",
  "./assets/avatars/raven.png",
  "./assets/avatars/pack-3.png",
  // v20.5 ritual FX sprites (Kenney CC0, recoloured) and the splash paper grain — the ritual runs without them (procedural glow), so best effort too
  "./assets/fx/ember-01.png",
  "./assets/fx/ember-02.png",
  "./assets/fx/spark-01.png",
  "./assets/fx/ash-01.png",
  "./assets/fx/smoke-01.png",
  "./assets/fx/smoke-02.png",
  "./assets/fx/crack-01.png",
  "./assets/fx/sigil-glow.png",
  "./assets/splash/paper-grain.jpg",
  "./fonts/playfair-display-cyrillic.woff2",
  "./fonts/playfair-display-latin.woff2",
  "./fonts/playfair-display-italic-cyrillic.woff2",
  "./fonts/playfair-display-italic-latin.woff2"
];
const CDN = [
  "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js",
  "https://cdn.jsdelivr.net/npm/animejs@3.2.2/lib/anime.min.js"
];

const noop = function(){};

self.addEventListener("install", function(event){
  event.waitUntil(
    caches.open(CACHE).then(function(cache){
      return cache.addAll(REQUIRED).then(function(){
        return Promise.all(OPTIONAL.concat(CDN).map(function(u){ return cache.add(u).catch(noop); }));
      });
    }).then(function(){ return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function(event){
  event.waitUntil(
    caches.keys().then(function(keys){
      return Promise.all(keys
        .filter(function(k){ return k.indexOf("proklinator-") === 0 && k !== CACHE; })
        .map(function(k){ return caches.delete(k); }));
    }).then(function(){ return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function(event){
  const req = event.request;
  if(req.method !== "GET") return;
  let url;
  try{ url = new URL(req.url); }catch(e){ return; }
  const sameOrigin = url.origin === self.location.origin;
  if(req.mode === "navigate"){
    if(sameOrigin) event.respondWith(navigate(req, url));
    return;
  }
  if(sameOrigin){
    if(url.href.indexOf(BASE) !== 0) return;   // outside the app folder — not ours to cache
    event.respondWith(cacheFirst(req, true));
    return;
  }
  if(CDN.indexOf(url.href) >= 0) event.respondWith(cacheFirst(req, false));
});

function isShell(url){
  const path = url.origin + url.pathname;
  return path === SHELL_URL || path === SHELL_URL + "index.html";
}

// Network first. The cached shell answers only for the app page itself, and only when the network is slow,
// down or answering with a server error; any other path inside the folder is left to the network as-is.
async function navigate(req, url){
  const cache = await caches.open(CACHE);
  const shell = isShell(url);
  const network = fetch(req).then(function(res){
    if(shell && res && res.ok && res.type === "basic") cache.put(SHELL_URL, res.clone()).catch(noop);
    return res;
  });
  network.catch(noop);   // the race below may abandon this promise — keep its rejection handled
  if(!shell) return network.catch(function(){ return Response.error(); });
  const cached = await cache.match(SHELL_URL, { ignoreVary: true });
  if(!cached) return network;   // first visit: nothing to fall back to; the browser shows its own offline page on failure
  const timer = new Promise(function(resolve){ setTimeout(resolve, NAV_TIMEOUT, null); });
  const res = await Promise.race([network.catch(function(){ return null; }), timer]);
  if(!res) return cached;
  return (res.status >= 500) ? cached : res;
}

// Cache first. `revalidate` (same-origin assets) refreshes the entry in the background after serving it;
// the pinned CDN files are immutable by URL and are never re-fetched once cached.
async function cacheFirst(req, revalidate){
  const cache = await caches.open(CACHE);
  const cached = await cache.match(req, { ignoreVary: true });
  if(cached && !revalidate) return cached;
  const network = fetch(req).then(function(res){
    if(res && res.ok && (res.type === "basic" || res.type === "cors")) cache.put(req, res.clone()).catch(noop);
    return res;
  });
  if(cached){ network.catch(noop); return cached; }
  try{ return await network; }catch(e){ return Response.error(); }
}
