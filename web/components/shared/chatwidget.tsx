// ChatWidget.tsx
import * as React from 'react';
import { useChatWidgetState, ChatWidgetStateProvider } from '@/components/shared/context/chatwidgetstatecontext';
import { ArrowRightIcon } from '@radix-ui/react-icons';
import ProgressSpinner from '@/components/shared/progressspinner';
import SpeechComponent from './speech';
import { useModelProfileConfig } from '@/components/shared/context/modelprofileconfig';
import { useAvatarProvider, AvatarData } from '@/components/shared/context/avatarcontextprovider';
import { useVideo } from '@/components/shared/context/videoprovider';
import AudioRecorder from '@/components/shared/audiorecorder';
import { MessageProps } from '@/components/shared/message';
import { v4 as uuidv4 } from 'uuid';

export interface ChatWidgetProps {
  id: string
}

export const ChatWidget: React.FC<ChatWidgetProps> = ({ id }) =>  {
  const { messages, setMessages, textAreaValue, setTextAreaValue } = useChatWidgetState();
  const chatContainerRef = React.useRef<HTMLUListElement>(null);
  const [isLoading, setIsLoading] = React.useState(false);
  const responseSpeechRef = React.useRef<string>('');
  const currentMessageIndex = React.useRef<number | null>(null);

  const currentAvatar = React.useRef<AvatarData>();
  const { playVideo } = useVideo();
  var streamingSetup = false;
  var audioStreamingSetup = false;

  // When loading state changes scroll to the bottom of the chat container
  React.useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [isLoading]);

  //Streaming event listener
  const addStreamingMessage = () => {
    let eventSource: EventSource;

    // Set up the stream
    if (!streamingSetup) { 
      streamingSetup = true;

      eventSource = new EventSource('/api/stream/');

      // Handle incoming chunks
      eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
    
        if (currentMessageIndex.current === null) {
          currentMessageIndex.current = -1;    // Prevent race condition
          setMessages((prevMessages) => {
            currentMessageIndex.current = prevMessages.length; // Store the index of the new message
            const newMessage = {
              id: uuidv4(),
              author_type: 'default',
              author: "Almanac",
              text: data.message,
              error: false,
            };
            return [...prevMessages, newMessage];
          });
        } else {
          // Update the current message
          setMessages((prevMessages) => {
            // Update the current message
            if (currentMessageIndex.current) {
              if (data.message == "<|endoftext|>") {
                // Message complete
                currentMessageIndex.current = null;
              } else { 
                const updatedMessage = {...prevMessages[currentMessageIndex.current]};
                updatedMessage.text += data.message;
  
                // Create a new array with the updated message
                const updatedMessages = prevMessages.map((message, index) => 
                  index === currentMessageIndex.current ? updatedMessage : message
                );
                return updatedMessages;
              }
      
            }
            return prevMessages;
          });
        }
      }
    };
  
    // Clean up the stream when done
    return () => {
      console.log("DONE?");
      eventSource.close();
      currentMessageIndex.current = null; // Reset the current message index
    };
  };
    let audioQueue:any = [];
    let audioPlaying = false;
    
    const addAudioStreamingMessage = () => {
      let audioEventSource: EventSource;
    
      // Set up the stream
      if (!audioStreamingSetup) { 
        audioStreamingSetup = true;
    
        audioEventSource = new EventSource('/api/audio/');
    
        audioEventSource.onmessage = (event) => {
          const data = JSON.parse(event.data);
          console.log(data)
          if (data.message) {
            const buffer = Buffer.from(data.message, 'base64');
            const decodedAudioData = Buffer.from(data.message, 'base64');
            console.log(decodedAudioData)
            // Create a Blob from the Uint8Array with the correct MIME type
            const blob = new Blob([decodedAudioData], { type: 'audio/wav' });
      
            // Create an object URL for the Blob
            const objectURL = URL.createObjectURL(blob);
      
            // Create an Audio element and add it to the queue
            const audioElement = new Audio();
            console.log(audioElement);
            audioElement.src = objectURL;
            audioQueue.push(audioElement);
      
            // If there is no audio currently playing, start playing
            if (!audioPlaying) {
              playNextAudio();
            }
          }
        }
      };
  
      // Function to play the next audio in the queue
      const playNextAudio = () => {
        if (audioQueue.length > 0) {
          const audioElement = audioQueue.shift();
          audioPlaying = true;
          audioElement.onended = () => {
            audioPlaying = false;
            playNextAudio();  // Play the next audio when the current one ends
          };
          audioElement.play();
        }
      };
  
    // Clean up the stream when done
    return () => {
      audioEventSource.close();
    };
  };

  React.useEffect(() => {
    addStreamingMessage();
  }, []); // Empty dependency array ensures this runs only once

  React.useEffect(() => {
    addAudioStreamingMessage();
  }, []); // Empty dependency array ensures this runs only once

  const handleTextAreaChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setTextAreaValue(event.target.value);
  };

  const addMessage = async (
    message: string | undefined,
    author: string | undefined,
    author_type: string | undefined,
    error: boolean,
  ) => {

    if (author == null) {
      console.error('ERROR: Must set author.');
      return;
    }
    if (message == null) {
      console.error('ERROR: Must set message.');
      return;
    }
    if (author_type == null) {
      console.error('ERROR: Must set author_type.');
      return;
    }
  
    // Create new message
    const newMessage: MessageProps = {
      id: uuidv4(),
      author_type: author_type, //'human',
      author: author,
      text: message,
      error: error,
    };
  
    // Wrap setMessages in a Promise and use await to ensure sequential execution
    await new Promise<void>((resolve) => {
      setMessages((prevMessages: any) => {
        resolve();
        setTextAreaValue(''); // Clear text area
        return [...prevMessages, newMessage];
      });
    });
  };

  // Handles completion API call after user enters a prompt and clicks the send button or enter key
  const complete = async () => {

    // set is loading, hitting API now
    setIsLoading(true);

    const mergedObject = {
      id: id,
      prompt: textAreaValue,
    };
    // Add the Human message //TODO: Get the name of the human from the user
    addMessage(mergedObject.prompt, 'Human', 'human', false);
    if (currentMessageIndex.current) { 
      currentMessageIndex.current += 1;
    }
    // Scroll to the top of the chat container after human message is added
    const res = await fetch('/api/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(mergedObject),
    });
    const data = await res.json();
    setIsLoading(false);

    // if (data.error_type) { 
    //   // TODO: Replace with a proper modal
    //   alert(data.error_message);
    //   return;
    // }
    // // TODO More robust error handling
    // const completion = data.data?.choices?.[0].text
    // if (data.video) {
    //   const buffer = Buffer.from(data.video, 'base64'); // Assume that data.video contains the base64 encoded MP4 data
    //   const decodedVideoData = Buffer.from(data.video, 'base64');

    //   // Create a Blob from the Uint8Array with the correct MIME type
    //   const blob = new Blob([decodedVideoData], { type: 'video/mp4' });

    //   // Create an object URL for the Blob
    //   const objectURL = URL.createObjectURL(blob);
      
    //   playVideo(objectURL);

    // }

    if (data.data.audio) {
      const buffer = Buffer.from(data.data.audio, 'base64');
      const decodedAudioData = Buffer.from(data.data.audio, 'base64');
      console.log(decodedAudioData)
      // Create a Blob from the Uint8Array with the correct MIME type
      const blob = new Blob([decodedAudioData], { type: 'audio/wav' });

      // Create an object URL for the Blob
      const objectURL = URL.createObjectURL(blob);

      // Create an Audio element and play the audio
      const audioElement = new Audio();
      console.log(audioElement);
      audioElement.src = objectURL;
      audioElement.play();

    }
    // if (completion) { 
    //   addMessage(completion, "Almanac", 'default', false);
    // }

    // Handle the result, update the state, etc.
    // setIsLoading(false);
  }

  // Handles completion API call after user enters a prompt and clicks the send button
  const useCompletion = async () => {
    complete();
  };

  const useEnterKey = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (!isLoading && e.code === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      complete();
    }
  };

  return (
    <ChatWidgetStateProvider>
      <div className="chat-widget">
        <ul className="no-bullets chat-history" ref={chatContainerRef} style={{ minWidth: '720px', maxHeight: '500px', overflowY: 'scroll', overflowX: 'hidden' }}>
          {messages.map((message) => (
            <li key={message.id} className={message.author_type}>
              <div>
                {message.author}:{' '}
                <span dangerouslySetInnerHTML={{ __html: message.text }}></span>
              </div>
            </li>
          ))}
        </ul>
        <div id="chat-input" className="flex">
          <div className="w-3/4">
            <textarea
              onChange={handleTextAreaChange}
              value={textAreaValue}
              id="user-input"
              className="form-control bg-blackA5 shadow-blackA9 inline-flex w-full appearance-none items-center justify-center rounded-[4px] px-[10px] text-[15px] leading-none text-white shadow-[0_0_0_1px] outline-none focus:shadow-[0_0_0_2px_black]"
              rows={4}
              style={{ width: '100%' }}
              onKeyDown={useEnterKey}
            ></textarea>
          </div>
          <div className="w-1/4">
            {isLoading ? (
              <div className="m-4">
                <ProgressSpinner />
              </div>
            ) : (
              <button id="send-message" className="btn-main m-4" onClick={useCompletion} style={{ padding: '0px' }}>
                <ArrowRightIcon />
              </button>
              )}
            <AudioRecorder />
            <SpeechComponent lastResponseRef={responseSpeechRef} currentAvatar={currentAvatar} />
          </div>
        </div>
      </div>
    </ChatWidgetStateProvider>
  );
};

export default ChatWidget;
