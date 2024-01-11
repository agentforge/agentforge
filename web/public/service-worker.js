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
    body: eventData.message || 'No message included.',
    icon: '/path/to/icon.png',
    vibrate: [100, 50, 100],
    data: {
      url: eventData.url || '/path/to/url',
    },
    actions: [
      {
        action: 'open-url',
        title: 'Open URL',
      },
    ],
  };

  self.registration.showNotification(eventData.title || 'Default Title', options);
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

//import { Novu } from "@novu/node";

//const novu = new Novu(process.env.NOVU_API_KEY || '');

// interface NotificationData {
//   notification: string;
//   // Add other fields as needed based on your actual notification payload
// }

// const handleNotification = (data: NotificationData) => {

//   // Perform actions based on the received notification
//   try {
//     novu.trigger("schedule", {
//         to: {
//           subscriberId: process.env.NOVU_SUB_ID || '',
//         },
//         payload: {
//           description: "Test notification",
//         },
//       });
//   console.log('Received notification: ', data.notification);
// } catch (error) {
//   console.log('Service Worker error: ', error);
//     };
// }