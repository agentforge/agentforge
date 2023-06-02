// ChatWidget.tsx
import * as React from 'react';
import { useChatWidgetState, ChatWidgetStateProvider } from '@/components/shared/context/chatwidgetstatecontext';
import { ArrowRightIcon } from '@radix-ui/react-icons';
import ProgressSpinner from '@/components/shared/progressspinner';
import SpeechComponent from './speech';
import { useLanguageModelConfig } from '@/components/shared/context/languagemodelconfigcontext';
import { useAvatarProvider, AvatarData } from '@/components/shared/context/avatarcontextprovider';
import { useVideo } from '@/components/shared/context/videoprovider';
import { useAudio } from '@/components/shared/context/audioprovider';
import { MessageProps } from '@/components/shared/message';
import { v4 as uuidv4 } from 'uuid';

export interface ChatWidgetProps {
  id: string
}

export const ChatWidget: React.FC<ChatWidgetProps> = ({ id }) =>  {
  const languageModelConfig = useLanguageModelConfig();
  const { getAvatarData } = useAvatarProvider();
  const { messages, setMessages, textAreaValue, setTextAreaValue } = useChatWidgetState();
  const chatContainerRef = React.useRef<HTMLUListElement>(null);
  const [isLoading, setIsLoading] = React.useState(false);
  const responseSpeechRef = React.useRef<string>('');
  const responseVideoRef = React.useRef<string>('');
  const currentAvatar = React.useRef<AvatarData>();
  const { playVideo } = useVideo();
  const { playAudio } = useAudio();

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
    const mergedObject = {
      id: id,
      prompt: textAreaValue,
    };

    // Add the Human message //TODO: Get the name of the human from the user
    addMessage(mergedObject.prompt, 'Human', 'human', false);

    // set is loading, hitting API now
    setIsLoading(true);
    // Scroll to the top of the chat container after human message is added
    const res = await fetch('/api/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(mergedObject),
    });
    const data = await res.json();
    const av_id = languageModelConfig.languageModelConfigs["avatar"] as string;
    // TODO: USE MODEL CONFIG
    // if (av_id != currentAvatar.current?.avatar) {
    //   const avatarData = getAvatarData(av_id);
    //   if (!avatarData) {
    //     return; // TODO: handle error
    //   }
    //   currentAvatar.current = avatarData;
    // }
    const completion = data.choices[0].text
    const tts = languageModelConfig.languageModelConfigs["speech"] as boolean;
    const lipsync = languageModelConfig.languageModelConfigs["lipsync"] as boolean;
    if (tts&& !lipsync) {
      // responseSpeechRef.current = completion;
      playAudio(completion, currentAvatar.current);
    } else if (tts && lipsync) {
      playVideo(completion, currentAvatar.current);
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
    if (e.code === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      complete();
    }
  };

  // ... Your existing component JSX ...
  return (
    <ChatWidgetStateProvider>
      <div className="chat-widget">
        <ul className="no-bullets chat-history" ref={chatContainerRef} style={{ maxHeight: '500px', overflow: 'scroll' }}>
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
            {/* <AudioRecorder /> */}
            <SpeechComponent lastResponseRef={responseSpeechRef} currentAvatar={currentAvatar} />
          </div>
        </div>
      </div>
    </ChatWidgetStateProvider>
  );
};

export default ChatWidget;
