'use client'
import { ModeToggle } from '@/components/ui/mode-toggle'
import { Button } from '@/components/ui/button'
import {
  NovuProvider,
  PopoverNotificationCenter,
  NotificationBell,
  INotificationBellProps,
} from "@novu/notification-center";
import { useEffect, useState } from 'react';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Input } from '@/components/ui/input'; 
import DOMPurify from 'dompurify';

export default function Home() {
  const [createEventName, setcreateEventName] = useState('');
  const [createIntervalValue, setcreateIntervalValue] = useState(0);
  const [deleteEventName, setdeleteEventName] = useState('');
  const [updateEventName, setupdateEventName] = useState('');
  const [updateIntervalValue, setupdateIntervalValue] = useState(0);
  const [subscribeEventName, setsubscribeEventName] = useState('');
  const [unsubscribeEventName, setunsubscribeEventName] = useState('');
  const [scheduleData, setScheduleData] = useState<ScheduleItem[]>([]);

  interface ScheduleItem {
    _id: string;
    event_name: string;
    interval: number;
    subscribe?: number;
  }

  const apiBaseUrl = 'http://localhost:8000/events'; // Replace with FastAPI backend URL

  const validateEventName = (eventName: string): boolean => {
    // Check if the input is not empty and has a reasonable length
    const sanitizedEventName = DOMPurify.sanitize(eventName);
    return sanitizedEventName.trim() !== '' && sanitizedEventName.length <= 50;
  };

  const normalizeEventName = (eventName: string): string => {
    // Trim leading and trailing whitespaces, replace spaces with dashes, and convert to lowercase
    return eventName.trim().replace(/\s+/g, '-').toLowerCase();
  };
  

  const handleCreateSchedule = async () => {
    try {
      // Validate and normalize the event name
      if (!validateEventName(createEventName)) {
        console.error('Invalid event name');
        // Optionally, display an error message to the user
        return;
      }

      const normalizedEventName = normalizeEventName(createEventName);

      // Use the normalized event name in the payload
      const payload = {
        //user: '1',                            // TO DO: add user identifier?
        event_name: normalizedEventName,
        interval: createIntervalValue,
      };
  
      const response = await fetch('http://localhost:8000/events/v1/create-schedule', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
  
      if (!response.ok) {
        // Handle non-successful responses
        const errorData = await response.json();
        console.error('API Error:', errorData.detail);
        throw new Error(`API Error: ${response.status} - ${response.statusText}`);
      }
  
      const result = await response.json();
      //Debugging
      //console.log('Created Schedule:', result);
    } catch (error) {
      console.error('API Error:', error);
    }
  };

  const handleViewSchedule = async () => {
    try {
      const response = await fetch('http://localhost:8000/events/v1/view-schedule', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        }
      });
      if (!response.ok) {
        const errorData = await response.json();
        console.error('API Error:', errorData.detail);
        throw new Error(`API Error: ${response.status} - ${response.statusText}`);
      }
      const result = await response.json();
      console.log('View schedule:', result);
      setScheduleData(Array.isArray(result) ? (result as ScheduleItem[]) : []);
    } catch (error) {
      console.error('API Error:', error);
    }
  };

  const handleDeleteSchedule = async () => {
    try {
      if (!validateEventName(deleteEventName)) {
        console.error('Invalid event name');
        // Optionally, display an error message to the user
        return;
      }

      const payload = {
        event_name: normalizeEventName(deleteEventName),
      }
  
      const response = await fetch(`${apiBaseUrl}/v1/delete-schedule`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw errorData || 'Error deleting schedule';
      }
      return response.json();
    } catch (error) {
      throw error || 'Error deleting schedule';
    }
  };

  const handleUpdateSchedule = async () => {
    try {
      if (!validateEventName(updateEventName)) {
        console.error('Invalid event name');
        // Optionally, display an error message to the user
        return;
      }

      const payload = {
        event_name: normalizeEventName(updateEventName),
        interval: updateIntervalValue
      }
  
      const response = await fetch(`${apiBaseUrl}/v1/update-schedule`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw errorData || 'Error updating schedule';
      }
      return response.json();
    } catch (error) {
      throw error || 'Error updating schedule';
    }
  }

  const handleSubscribeSchedule = async () => {
    try {
      if (!validateEventName(subscribeEventName)) {
        console.error('Invalid event name');
        // Optionally, display an error message to the user
        return;
      }

      const payload = {
        event_name: normalizeEventName(subscribeEventName),
      }
      const response = await fetch(`${apiBaseUrl}/v1/subscribe-schedule`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw errorData || 'Error subscribing to schedule';
      }
      return response.json();
    } catch (error) {
      throw error || 'Error subscribing to schedule';
    }
  };

  const handleUnSubscribeSchedule = async () => {
    try {
      if (!validateEventName(unsubscribeEventName)) {
        console.error('Invalid event name');
        // Optionally, display an error message to the user
        return;
      }

      const payload = {
        event_name: normalizeEventName(unsubscribeEventName),
      }
      const response = await fetch(`${apiBaseUrl}/v1/unsubscribe-schedule`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw errorData || 'Error unsubscribing schedule';
      }
      return response.json();
    } catch (error) {
      throw error || 'Error unsubscribing from schedule';
    }
  };
  
  function urlBase64ToUint8Array(base64String: string) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
      .replace(/\-/g, '+')
      .replace(/_/g, '/');
  
    const rawData = window.atob(base64);
    const buffer = new Uint8Array(rawData.length);
  
    for (let i = 0; i < rawData.length; ++i) {
      buffer[i] = rawData.charCodeAt(i);
    }
  
    return buffer;
  }
  
  // Private key for push subscription
  const publicApplicationServerKey = "BPZjhYmoa74hrffBOS0flp3Sk_EcLuSFFww7iJ8HNFZe6JVx6tshoBQKT4GOZOxgBq81qqLAjEu9JKBwamCEELY";

  const sendSubscriptionToServer = async (subscription: PushSubscription) => {
    try {
      // Send the subscription details to server
      const response = await fetch('http://localhost:8000/events/v1/subscribe-notifications', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(subscription),
      });
      //debugging
      //console.log('response: ', response)
      if (!response.ok) {
        console.error('Failed to send subscription to the server');
      }
    } catch (error) {
      console.error('Error sending subscription to server:', error);
    }
  };

// Function to unregister the service worker and unsubscribe from push notifications
const unSubscribeNotifications = async () => {
  if (typeof window !== 'undefined') { // Check if running on the client-side
    try {
      // Get the existing service worker registration
      const registration = await navigator.serviceWorker.ready;

      // Retrieve the push subscription
      const subscription = await registration.pushManager.getSubscription();
      //debugging
      //console.log(subscription)

      if (!subscription) {
        console.log('No push manager subscription found');
      }

      // Unsubscribe from push notifications
      const successful = await subscription?.unsubscribe();
      console.log('push manager unsubscribe success', successful);

      // Unregister the service worker
      await registration.unregister();
      console.log('Service Worker unregistered successfully');

      // Handle service removal or any other logic here
      try {
        // Assuming you have an API endpoint for removing subscriptions
        const response = await fetch('http://localhost:8000/events/v1/unsubscribe-notifications', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(subscription),
        });

        if (response.ok) {
          localStorage.setItem('hasUnsubscribed', 'true');
          alert('You unsubscribed successfully!');
          return true;
        } else {
          console.error('Failed to remove subscription from the server');
          return false;
        }
      } catch (error) {
        console.error('Error while removing subscription:', error);
        return false;
      }
    } catch (error) {
      // Handle registration errors
      console.error('Service Worker registration failed:', error);
      return false;
    }
  }
};

async function registerServiceWorker() {
  if ('serviceWorker' in navigator) {
    try {
      // Check if a service worker is already registered
      const registration = await navigator.serviceWorker.getRegistration();

      if (!!registration) {
        console.log('Service worker is already registered:', registration);
        return;
      }

      // If no service worker is registered, proceed with registration
      const newRegistration = await navigator.serviceWorker.register('/service-worker.js');
      console.log('Service Worker registered with scope:', newRegistration.scope);

      await navigator.serviceWorker.ready;
      console.log('Service worker is active');

      if ('PushManager' in window) {
        const existingSubscription = await newRegistration.pushManager.getSubscription();

        if (!existingSubscription) {
          const newSubscription = await newRegistration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: publicApplicationServerKey,
          });
          
          //debugging
          //console.log('Received push subscription:', JSON.stringify(newSubscription));
          await sendSubscriptionToServer(newSubscription);
        } else {
          console.log('Subscription already exists:', JSON.stringify(existingSubscription));
        }
      } else {
        console.warn('Push notifications are not supported in this browser.');
      }
    } catch (error) {
      console.error('Service Worker registration failed:', error);
    }
  } else {
    console.warn('Service Worker is not supported in this browser.');
  }
}


function registerNotificationPermissions() {
  if (Notification.permission === 'default') {
    Notification.requestPermission().then((permission) => {
      if (permission === 'granted') {
        console.log('Notification permission granted');
        registerServiceWorker();
      } else {
        console.warn('Notification permission denied');
      }
    });
  } else if (Notification.permission === 'granted') {
    console.log('Notification permission already granted');
    registerServiceWorker();
  } else {
    console.warn('Service Worker registration skipped because notifications are not allowed or Service Worker is not supported.');
  }
}

  useEffect(() => {
    // asks user permission to display push notifications,
    // then checks for and registers service-worker and
    // PushManager
    registerNotificationPermissions();
  }, []);

  
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
          <AlertDialog>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle>Enable notifications?</AlertDialogTitle>
                <AlertDialogDescription>
                Stay up-to-date with important updates and events by enabling notifications. 
                We'll send you timely alerts to keep you informed and connected. 
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter>
                <AlertDialogCancel>No</AlertDialogCancel>
                <AlertDialogAction>Yes</AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>

      <NovuProvider
      //Subscriber ID is in NOVU subscribers dashboard
      // TO DO: Store sub ID and app ID in env var
      
      //subscriberId={process.env.NOVU_SUB_ID || ''}
        subscriberId='123456789'
      //applicationIdentifier={process.env.NOVU_APP_ID || ''}
        applicationIdentifier='H8H2BBYuflb8'
      >
        <PopoverNotificationCenter colorScheme={'light'}>
          {({ unseenCount }) => (
            <>
              <NotificationBell unseenCount={unseenCount} />
            </>
          )}
        </PopoverNotificationCenter>
      </NovuProvider>

      <div>
      <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', marginBottom: 10, alignItems: 'center' }}>
        {/* Create Schedule */}
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <Input
            type="text"
            placeholder="Event Name"
            value={createEventName}
            onChange={(e) => setcreateEventName(e.target.value)}
          />
          <Input
            type="number"
            placeholder="Interval"
            value={createIntervalValue}
            onChange={(e) => setcreateIntervalValue(parseInt(e.target.value))}
          />
          <Button onClick={handleCreateSchedule}>
            Create Schedule
          </Button>
        </div>

        {/* Delete Schedule */}
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <Input
            type="text"
            placeholder="Event Name"
            value={deleteEventName}
            onChange={(e) => setdeleteEventName(normalizeEventName(e.target.value))}
          />
          <Button onClick={handleDeleteSchedule}>
            Delete schedule
          </Button>
        </div>

        {/* Display the schedule */}
        <AlertDialog>
          <AlertDialogTrigger>
            {/* View Schedule */}
            <Button onClick={handleViewSchedule}>
              View Schedule
            </Button>
          </AlertDialogTrigger>

          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>Schedule</AlertDialogTitle>
            </AlertDialogHeader>
            <AlertDialogDescription>
            {scheduleData && scheduleData.length > 0 ? (
              scheduleData.map((schedule) => (
                <p key={schedule._id}>{JSON.stringify(schedule)}</p>
              ))
            ) : (
              <p>No schedule data available.</p>
            )}
            </AlertDialogDescription>
            <AlertDialogFooter>
              <AlertDialogCancel>Close</AlertDialogCancel>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog>
        
        {/* Update Schedule */}
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <Input
            type="text"
            placeholder="Event Name"
            value={updateEventName}
            onChange={(e) => setupdateEventName(e.target.value)}
          />
          <Input
            type="number"
            placeholder="Interval"
            value={updateIntervalValue}
            onChange={(e) => setupdateIntervalValue(parseInt(e.target.value))}
          />
          <Button onClick={handleUpdateSchedule}>
            Update schedule
          </Button>
        </div>

        {/* Subscribe Schedule */}
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <Input
            type="text"
            placeholder="Event Name"
            value={subscribeEventName}
            onChange={(e) => setsubscribeEventName(normalizeEventName(e.target.value))}
          />
          <Button onClick={handleSubscribeSchedule}>
            Subscribe schedule
          </Button>
        </div>

        {/* Unsubscribe Schedule */}
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <Input
            type="text"
            placeholder="Event Name"
            value={unsubscribeEventName}
            onChange={(e) => setunsubscribeEventName(normalizeEventName(e.target.value))}
          />
          <Button onClick={handleUnSubscribeSchedule}>
            Unsubscribe schedule
          </Button>
        </div>
      </div>
    </div>

      {/* Notification Buttons */}
      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
        <Button onClick={() => registerNotificationPermissions()}>
          register notifications
        </Button>
        <Button onClick={() => unSubscribeNotifications()}>
          unregister notifications
        </Button>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
      <ModeToggle />
      </div>
    </main>
  )
}
