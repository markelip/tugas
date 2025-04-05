self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open("farouq-cache").then((cache) =>
      cache.addAll(["/", "/static/style.css", "/static/icon-192.png"])
    )
  );
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((res) => res || fetch(event.request))
  );
});
