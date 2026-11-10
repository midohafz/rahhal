self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open('rahhal-store').then((cache) => cache.addAll([
      './',
      './index.html',
      './sitemap.xml'
    ])),
  );
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((response) => response || fetch(e.request)),
  );
});
