'use client'
import { ModeToggle } from '@/components/mode-toggle'
import { Button } from '@/components/ui/button'
import Image from 'next/image'
import {
  NovuProvider,
  PopoverNotificationCenter,
  NotificationBell,
  INotificationBellProps,
} from "@novu/notification-center";
import { Novu } from "@novu/node";
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
    validation_logic: string;
    subscribe?: number;
  }

  const apiBaseUrl = 'http://localhost:8000/events'; // Replace with FastAPI backend URL

  const validateEventName = (eventName: string): boolean => {
    // Check if the input is not empty and has a reasonable length
    return eventName.trim() !== '' && eventName.length <= 50;
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
      console.log('Created Schedule:', result);
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
      console.log('response: ', response)
      if (!response.ok) {
        console.error('Failed to send subscription to the server');
      }
    } catch (error) {
      console.error('Error sending subscription to server:', error);
    }
  };

  async function unregisterServiceWorker() {
    if ('serviceWorker' in navigator) {
      try {
        const swRegistration = await navigator.serviceWorker.ready;
        await swRegistration.unregister();
        console.log('Service Worker successfully unregistered');

        if (Notification.permission === 'granted') {
          try {
            const permission = Notification.requestPermission();
            console.log(`Notification permission requested: ${permission}`);
          } catch (err) {
            console.error('Error occurred attempting to request Notification permission:', err);
          }
        }
      } catch (err) {
        console.error('Error occurred attempting to unregister Service Worker:', err);
      }
    }
  }

  const registerServiceWorker = async () => {
    if ('serviceWorker' in navigator) {
      try {
        const registration = await navigator.serviceWorker.register('/service-worker.js');
        console.log('Service Worker registered with scope:', registration.scope);
        
        await navigator.serviceWorker.ready; // Wait for the service worker to become active
        console.log('Service worker is active')

        // Check if pushManager is supported
        if ('PushManager' in window) {
          // Get the push subscription
          const subscription = await registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: publicApplicationServerKey,
          });
  
          console.log("Received push subscription: ", JSON.stringify(subscription));
  
          // Send the subscription to the server
          await sendSubscriptionToServer(subscription);
        } else {
          console.warn('Push notifications are not supported in this browser.');
        }
      } catch (error) {
        console.error('Service Worker registration failed:', error);
      }
    } else {
      console.warn('Service Worker is not supported in this browser.');
    }
  };  

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
      console.warn('Notification permission already granted');
    } else {
      console.warn('Service Worker registration skipped because notifications are not allowed or Service Worker is not supported.');
    }
  }

  useEffect(() => {
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
        subscriberId={process.env.NOVU_SUB_ID || ''}
        applicationIdentifier={process.env.NOVU_APP_ID || ''}
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
      {/* <div style={{ display: 'flex', justifyContent: 'space-between' }}>
        <Button onClick={() => registerNotificationPermissions()}>
          register notifications
        </Button>
        <Button onClick={() => unregisterServiceWorker()}>
          unregister notifications
        </Button>
      </div> */}
      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
      <ModeToggle />
      </div>
    </main>
  )
}