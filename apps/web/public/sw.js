/**
 * Service Worker for Python OOP Journey
 * 
 * Features:
 * - Cache static assets (Next.js build files)
 * - Cache curriculum.json
 * - Network-first for API calls
 * - Background sync for pending operations
 * - Push notifications (optional)
 */

const CACHE_NAME = 'oop-journey-v1';
const STATIC_CACHE = 'oop-journey-static-v1';
const API_CACHE = 'oop-journey-api-v1';

// Assets to cache on install
const STATIC_ASSETS = [
  '/',
  '/offline',
  '/curriculum.json',
  '/manifest.json',
  '/favicon.ico',
];

// API routes to cache with network-first strategy
const API_ROUTES = [
  '/api/curriculum/',
];

// Skip waiting and claim clients immediately
self.addEventListener('install', (event) => {
  console.log('[SW] Installing...');
  
  event.waitUntil(
    Promise.all([
      // Skip waiting to activate immediately
      self.skipWaiting(),
      
      // Cache static assets
      caches.open(STATIC_CACHE).then((cache) => {
        console.log('[SW] Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      }),
    ])
  );
});

// Activate and clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating...');
  
  event.waitUntil(
    Promise.all([
      // Claim clients immediately
      self.clients.claim(),
      
      // Clean up old caches
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((name) => {
              return name.startsWith('oop-journey-') && 
                     name !== STATIC_CACHE && 
                     name !== API_CACHE;
            })
            .map((name) => {
              console.log('[SW] Deleting old cache:', name);
              return caches.delete(name);
            })
        );
      }),
    ])
  );
});

// Fetch event - handle caching strategies
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests for cache handling (except for same-origin)
  if (request.method !== 'GET' && url.origin === self.location.origin) {
    return;
  }

  // Handle API requests
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(handleAPIRequest(request));
    return;
  }

  // Handle Next.js static files (_next/static)
  if (url.pathname.startsWith('/_next/static/')) {
    event.respondWith(handleStaticRequest(request));
    return;
  }

  // Handle curriculum.json
  if (url.pathname === '/curriculum.json') {
    event.respondWith(handleCurriculumRequest(request));
    return;
  }

  // Handle other requests with network-first strategy
  event.respondWith(handleNetworkFirst(request));
});

/**
 * Handle API requests with network-first strategy
 */
async function handleAPIRequest(request) {
  try {
    // Try network first
    const networkResponse = await fetch(request);
    
    // Cache successful GET responses
    if (request.method === 'GET' && networkResponse.ok) {
      const cache = await caches.open(API_CACHE);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('[SW] API request failed, trying cache:', request.url);
    
    // Try to return cached response
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Return offline response
    return new Response(
      JSON.stringify({ 
        error: 'You are offline. This data is not available.',
        offline: true 
      }),
      {
        status: 503,
        headers: { 'Content-Type': 'application/json' },
      }
    );
  }
}

/**
 * Handle static assets with cache-first strategy
 */
async function handleStaticRequest(request) {
  const cachedResponse = await caches.match(request);
  
  if (cachedResponse) {
    return cachedResponse;
  }
  
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(STATIC_CACHE);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('[SW] Static request failed:', request.url);
    throw error;
  }
}

/**
 * Handle curriculum.json with stale-while-revalidate strategy
 */
async function handleCurriculumRequest(request) {
  const cache = await caches.open(STATIC_CACHE);
  const cachedResponse = await cache.match(request);
  
  // Return cached version immediately if available
  const fetchPromise = fetch(request).then((networkResponse) => {
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  }).catch((error) => {
    console.log('[SW] Curriculum fetch failed, using cache');
    return cachedResponse;
  });
  
  return cachedResponse || fetchPromise;
}

/**
 * Handle generic requests with network-first strategy
 */
async function handleNetworkFirst(request) {
  try {
    const networkResponse = await fetch(request);
    
    // Cache successful HTML responses for offline browsing
    if (networkResponse.ok && request.headers.get('accept')?.includes('text/html')) {
      const cache = await caches.open(STATIC_CACHE);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
  } catch (error) {
    console.log('[SW] Network request failed, trying cache:', request.url);
    
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Return offline page for HTML requests
    if (request.headers.get('accept')?.includes('text/html')) {
      return caches.match('/offline');
    }
    
    throw error;
  }
}

// ==================== Background Sync ====================

self.addEventListener('sync', (event) => {
  console.log('[SW] Background sync event:', event.tag);
  
  if (event.tag === 'sync-pending-operations') {
    event.waitUntil(syncPendingOperations());
  }
});

/**
 * Sync pending operations via the sync engine
 */
async function syncPendingOperations() {
  try {
    // Notify all clients to trigger sync
    const clients = await self.clients.matchAll({ type: 'window' });
    clients.forEach((client) => {
      client.postMessage({
        type: 'SYNC_PENDING_OPERATIONS',
      });
    });
    
    console.log('[SW] Triggered sync for pending operations');
  } catch (error) {
    console.error('[SW] Background sync failed:', error);
  }
}

// ==================== Push Notifications ====================

self.addEventListener('push', (event) => {
  console.log('[SW] Push event received:', event);
  
  if (!event.data) {
    return;
  }
  
  const data = event.data.json();
  const options = {
    body: data.body || 'New notification from Python OOP Journey',
    icon: '/icon-192x192.png',
    badge: '/badge-72x72.png',
    tag: data.tag || 'default',
    requireInteraction: data.requireInteraction || false,
    actions: data.actions || [],
    data: data.data || {},
  };
  
  event.waitUntil(
    self.registration.showNotification(
      data.title || 'Python OOP Journey',
      options
    )
  );
});

self.addEventListener('notificationclick', (event) => {
  console.log('[SW] Notification clicked:', event);
  
  event.notification.close();
  
  const urlToOpen = event.notification.data?.url || '/';
  
  event.waitUntil(
    self.clients.matchAll({ type: 'window' }).then((clients) => {
      // Focus existing window if open
      for (const client of clients) {
        if (client.url === urlToOpen && 'focus' in client) {
          return client.focus();
        }
      }
      
      // Open new window
      if (self.clients.openWindow) {
        return self.clients.openWindow(urlToOpen);
      }
    })
  );
});

// ==================== Message Handling ====================

self.addEventListener('message', (event) => {
  console.log('[SW] Message received:', event.data);
  
  switch (event.data?.type) {
    case 'SKIP_WAITING':
      self.skipWaiting();
      break;
      
    case 'CACHE_CURRICULUM':
      cacheCurriculum(event.data.curriculum);
      break;
      
    case 'CLEAR_CACHE':
      clearAllCaches();
      break;
      
    default:
      break;
  }
});

/**
 * Cache curriculum data
 */
async function cacheCurriculum(curriculum) {
  const cache = await caches.open(STATIC_CACHE);
  const response = new Response(JSON.stringify(curriculum), {
    headers: { 'Content-Type': 'application/json' },
  });
  await cache.put('/curriculum.json', response);
  console.log('[SW] Curriculum cached');
}

/**
 * Clear all caches
 */
async function clearAllCaches() {
  const cacheNames = await caches.keys();
  await Promise.all(
    cacheNames
      .filter((name) => name.startsWith('oop-journey-'))
      .map((name) => caches.delete(name))
  );
  console.log('[SW] All caches cleared');
}
