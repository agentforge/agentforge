//notifications background service worker
let mainPageClient;

self.addEventListener('connect', (event) => {
  mainPageClient = event.source;
});

self.addEventListener('message', (event) => {
  // Handle the message from the backend
  const eventData = event.data;
});

self.addEventListener('push', (event) => {
  const eventData = event.data.text();

  console.log('Received push event:', eventData);

  const options = {
    body: event.data || 'No data included.',
    icon: '/path/to/icon.png',
    vibrate: [100, 50, 100],
    data: {
      url: event.url || '/path/to/url',
    },
    actions: [
      {
        action: 'open-url',
        title: 'Open URL',
      },
    ],
  };

  event.waitUntil(self.registration.showNotification(eventData, options));

  //self.registration.showNotification(eventData.title || 'Default Title', options);
});

self.addEventListener('notificationclick', (event) => {
  // Handle notification click if needed
  event.notification.close();
  // Add logic to navigate or perform an action on notification click
});

function sendMessageToMainPage(message) {
  if (mainPageClient) {
    mainPageClient.postMessage(message);
  }
}