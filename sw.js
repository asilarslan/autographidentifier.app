// The site no longer uses a service worker. The old one served index.html
// cache-first, so returning visitors never saw updates. This version removes
// the old caches and unregisters itself.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(names => Promise.all(names.map(name => caches.delete(name))))
      .then(() => self.registration.unregister())
  );
});
