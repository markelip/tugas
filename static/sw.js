self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open("botfarouq").then((cache) => {
      return cache.addAll(["/", "/static/icons/favicon-96x96.png"]);
    })
  );
});

self.addEventListener("fetch", (e) => {
  e.respondWith(
    caches.match(e.request).then((response) => response || fetch(e.request))
  );
});
