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
  const currentAvatar = React.useRef<AvatarData>();
  const { playVideo } = useVideo();

  // When loading state changes scroll to the bottom of the chat container
  React.useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [isLoading]);

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
      console.log('ERROR: Must set author.');
      return;
    }
    if (message == null) {
      console.log('ERROR: Must set message.');
      return;
    }
    if (author_type == null) {
      console.log('ERROR: Must set author_type.');
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

    // Scroll to the top of the chat container after human message is added
    const res = await fetch('/api/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(mergedObject),
    });
    const data = await res.json();

    if (data.error_type) { 
      // TODO: Replace with a proper modal
      alert(data.error_message);
      setIsLoading(false);
      return;
    }
    const completion = data.choices[0].text
    console.log(data)
    if (data.video) {
      const buffer = Buffer.from(data.video, 'base64'); // Assume that data.video contains the base64 encoded MP4 data
      const decodedVideoData = Buffer.from(data.video, 'base64');

      // Create a Blob from the Uint8Array with the correct MIME type
      const blob = new Blob([decodedVideoData], { type: 'video/mp4' });

      // Create an object URL for the Blob
      const objectURL = URL.createObjectURL(blob);
      
      playVideo(objectURL);

    }
    else if (data.audio) {
      const buffer = Buffer.from(data.audio, 'base64');
      const decodedAudioData = Buffer.from(data.audio, 'base64');

      // Create a Blob from the Uint8Array with the correct MIME type
      const blob = new Blob([decodedAudioData], { type: 'audio/wav' });

      // Create an object URL for the Blob
      const objectURL = URL.createObjectURL(blob);

      // Create an Audio element and play the audio
      const audioElement = new Audio();
      audioElement.src = objectURL;
      audioElement.play();

    }
    addMessage(completion, "Sam", 'default', false);

    // Handle the result, update the state, etc.
    setIsLoading(false);
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
        <ul className="no-bullets chat-history" ref={chatContainerRef}>
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
              className="form-control"
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
