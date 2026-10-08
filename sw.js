const CACHE_NAME = 'puratto-tokai-v175';
const RUNTIME_CACHE = 'puratto-tokai-runtime-v175';

const FILES = [
  './',
  './index.html',
  './new-pan.html',
  './ramen.html',
  './panrush.html',
  './autumn-rush.html',
  './manifest.webmanifest',
  './data/static-catalog.json',
  './aichi-top10.json',
  './puratto-tokai-mobile.png',
  './puratto-tokai-pc.png',
  './icon-192.png',
  './icon-512.png'
];

self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(FILES))
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => key !== CACHE_NAME && key !== RUNTIME_CACHE)
          .map(key => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  const sameOrigin = url.origin === self.location.origin;

  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req)
        .then(response => {
          if (response && response.ok) {
            const copy = response.clone();
            caches.open(RUNTIME_CACHE).then(cache => cache.put(req, copy));
          }
          return response;
        })
        .catch(async () =>
          (await caches.match(req, {ignoreSearch:true})) ||
          (await caches.match('./index.html')) ||
          (await caches.match('./'))
        )
    );
    return;
  }

  if (sameOrigin) {
    event.respondWith(
      caches.match(req, {ignoreSearch:true}).then(async cached => {
        if (cached) return cached;
        try {
          const response = await fetch(req);
          if (response && response.ok) {
            const copy = response.clone();
            caches.open(RUNTIME_CACHE).then(cache => cache.put(req, copy));
          }
          return response;
        } catch (e) {
          return new Response('', {status: 503, statusText: 'Offline'});
        }
      })
    );
    return;
  }

  event.respondWith(fetch(req));
});
