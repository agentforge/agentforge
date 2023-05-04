'use client';

import React, { useEffect, useRef, useState, KeyboardEvent } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { SpinnerIcon, ArrowRightIcon } from '@radix-ui/react-icons';

import api, { api_url } from '@/components/shared/api';
import { MessageProps } from '@/components/shared/message';
import { ReflectionProps } from '@/components/shared/reflection';
import ErrorMessage from '@/components/shared/error';
// import { getConfiguration, Configuration } from '../../components/shared/Configure';
// import AudioRecorder from '../../components/shared/AudioRecorder';
// import useStateWithCallback from './useStateWithCallback';
import SwirlIcon from './mind-icon.svg';
import CheckboxElement from '@/components/shared/checkbox';
import SliderElement from '@/components/shared/slider';
import SelectElement from '@/components/shared/select';
import { useCheckboxState } from '@/components/shared/context/checkboxcontext';

interface ForgeProps {}

const Forge: React.FC<ForgeProps> = () => {
  // TODO: make dynamic, temporary until we can source these from the API
  // CONSTANTS
  const avatars = ['caretaker', 'default', 'makhno', 'fdr', 'sankara'];
  const modelConfigs = ['logical', 'creative', 'moderate'];
  const models = [
    'alpaca-lora-7b',
    'alpaca-lora-13b',
    'dolly-v1-6b',
    'dolly-v2-12b',
    'pythia-6.9b-gpt4all-pretrain',
    'vicuna-7b',
  ];
  interface StringMap {
    [key: string]: string;
  }
  const videos: StringMap = {
    default: '/videos/default.mp4',
    caretaker: '/videos/default.mp4',
    makhno: '/videos/makhno.mp4',
    fdr: '/videos/fdr.mp4',
    sankara: '/videos/sankara.mp4',
  };
  const names: StringMap = {
    default: 'Sam',
    caretaker: 'Sam',
    makhno: 'Nestor Makhno',
    sankara: 'Thomas Sankara',
    fdr: 'Franklin D. Roosevelt',
  };

  const [textAreaValue, setTextAreaValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentVideo, setCurrentVideo] = useState<'videoA' | 'videoB'>('videoA');
  const [userConfiguration, setUserConfiguration] = useState<Configuration>({
    username: '',
    email: '',
    logged_in: false,
  });

  //Config Refs
  const avatarRef = useRef<HTMLSelectElement>(null);
  const maxNewTokensRef = useRef<HTMLInputElement>(null);
  // const ttsCheckboxRef = useRef<HTMLButtonElement>(null);
  const { checkboxState } = useCheckboxState();

  const handleClick = () => {
    console.log('Checkbox checked:', checkboxState);
  };

  const streamingCheckboxRef = useRef<HTMLInputElement>(null);
  const lipsyncCheckboxRef = useRef<HTMLInputElement>(null);

  // Video refs
  const videoARef = useRef<HTMLVideoElement>(null);
  const videoBRef = useRef<HTMLVideoElement>(null);

  // Text Refs
  const sendMessageRef = useRef<HTMLButtonElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const chatHistoryRef = useRef<HTMLUListElement>(null);
  const thoughtHistoryRef = useRef<HTMLUListElement>(null);

  const modelConfigInputRef = useRef<HTMLSelectElement>(null);
  const modelKeyInputRef = useRef<HTMLSelectElement>(null);

  // useState values
  const [messages, setMessages] = useState<MessageProps[]>([]);
  const [reflections, setReflections] = useState<ReflectionProps[]>([]);

  // Change Events
  const handleTextAreaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setTextAreaValue(e.target.value);
  };

  // err handling
  const [errorState, setErrorState] = useState(false);
  const [errorValue, setErrorValue] = useState('');

  const clearTextarea = () => {
    if (textareaRef.current) {
      setTextAreaValue('');
      textareaRef.current.value = '';
      // textAreaValue = '';
    }
  };

  const handleResize = () => {
    const video = document.getElementById('hero-video') as HTMLVideoElement;
    const videoWrapper = document.getElementById('hero-video-wrapper') as HTMLElement;
    // const chatHistory = document.querySelector('.chat-history') as HTMLElement;
    // const chatHistoryRect = chatHistory.getBoundingClientRect();
    const userInput = document.getElementById('user-input') as HTMLElement;
    if (userInput) {
      const userInputRect = userInput.getBoundingClientRect();
      const distanceFromTop = userInputRect.top;
      if (videoWrapper.style.position === 'absolute') {
        videoWrapper.style.top = '0';
        videoWrapper.style.left = userInputRect.left + 'px';
        video.style.width = userInputRect.width + 'px';
        video.style.height = distanceFromTop + 'px';
      }
    }
  };

  const addMessage = async (
    prompt: string | undefined,
    author: string | undefined,
    author_type: string | undefined,
    error: boolean,
  ) => {
    if (author == null) {
      console.log('ERROR: Must set author.');
      return;
    }
    if (prompt == null) {
      console.log('ERROR: Must set prompt.');
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
      text: prompt,
      error: error,
    };

    // Wrap setMessages in a Promise and use await to ensure sequential execution
    await new Promise<void>((resolve) => {
      setMessages((prevMessages: any) => {
        resolve();
        clearTextarea();
        return [...prevMessages, newMessage];
      });
    });
  };

  const closeError = () => {
    setErrorState(false);
    setErrorValue('');
  };

  const openError = (error: any) => {
    setErrorState(true);
    setErrorValue(error);
  };
  const errMessage = async (error: string) => {
    openError(`You have encountered a problem. Please contact support. Error message ${error}`);
  };

  // Append a string to the latest message for streaming
  const appendMessage = (newText: string) => {
    if (streamingCheckboxRef.current?.checked) {
      setMessages((prevMessages) => {
        const lastIndex = prevMessages.length - 1;
        const lastMessage = prevMessages[lastIndex];
        if (lastMessage != undefined) {
          const updatedMessage = { ...lastMessage, text: lastMessage.text + newText };
          return [...prevMessages.slice(0, lastIndex), updatedMessage];
        }
        return prevMessages;
      });
    }
  };

  // Add a reflection to the list of reflections in the UX
  const addReflection = async (text: string | undefined, type: string | undefined) => {
    if (text == null) {
      console.log('ERROR: Must set text.');
      return;
    }
    if (type == null) {
      console.log('ERROR: Must set type.');
      return;
    }
    // Create new message
    const newReflection: ReflectionProps = {
      id: uuidv4(),
      type: type,
      text: text,
    };
    // Append a string to the latest message for streaming
    await new Promise<void>((resolve) => {
      setReflections((prevReflections: any) => {
        return [...prevReflections, newReflection];
      });
    });
  };

  // Get the current avatar dropdown value
  const getAvatar = () => {
    let avatar = avatarRef.current?.value;
    if (avatar == null) {
      avatar = 'default';
    }
    return avatar;
  };

  // Getter/Setter Functions for all user configuration variables
  // present on this screen
  const getLanguageModelConfig = () => {
    const configs = {
      human_name: userConfiguration.username || '',
      robot_name: names[getAvatar()] || '',
      tts: ttsCheckboxRef.current?.checked || false,
      lipsync: lipsyncCheckboxRef.current?.checked || false,
      streaming: streamingCheckboxRef.current?.checked || false,
      max_new_tokens: parseInt(maxNewTokensRef.current?.value || '0', 10),
      avatar: avatarRef.current?.value || '',
      generation_config: modelConfigInputRef.current?.value || '',
      model_key: modelKeyInputRef.current?.value || '',
      prompt: '',
    };

    return configs;
  };

  // Play a video from blob or url -- setup the non-active video, load it, and play it.
  // Switch the reference to this video
  const playVideo = async (blob: Blob | undefined, url: string | undefined) => {
    const nextVideoRef = currentVideo === 'videoA' ? videoBRef : videoARef;
    const currentVideoRef = currentVideo === 'videoA' ? videoARef : videoBRef;

    const nextVideo = nextVideoRef.current;
    if (nextVideo) {
      if (url == undefined) {
        if (blob == undefined) {
          console.log('err: Must select url or blob.');
          return;
        }
        const videoUrl = URL.createObjectURL(blob);
        if (!nextVideo.src.includes(videoUrl)) {
          nextVideo.src = videoUrl;
        }
      } else {
        if (!nextVideo.src.includes(url)) {
          nextVideo.src = url;
        }
      }
      const playWhenLoaded = () => {
        if (currentVideoRef.current != null) {
          nextVideo.play();
          nextVideo.style.display = 'block';

          // // Hide prev video
          currentVideoRef.current.style.display = 'none';
          const selectedAvatar = getAvatar();
          const defaultUrl = videos[selectedAvatar];

          if (!currentVideoRef.current.src.includes(defaultUrl)) {
            currentVideoRef.current.src = defaultUrl;
          }
          currentVideoRef.current.pause();
          nextVideo.removeEventListener('canplaythrough', playWhenLoaded);
        }
      };
      nextVideo.addEventListener('canplaythrough', playWhenLoaded);
    }
  };

  // Calls TTS API
  const getTTS = async (prompt: string) => {
    const data = getLanguageModelConfig();
    data['prompt'] = prompt;
    await fetch(`/v1/tts`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/octet-stream',
      },
      body: JSON.stringify(data),
    })
      .then((res) => res.json())
      .then((data: any) => {
        playVideo(data(), undefined);
        setIsLoading(false);
      });
  };

  // LLM Completion API Functions
  const getCompletion = async () => {
    const prompt = textareaRef.current?.value;
    const data = getLanguageModelConfig();
    if (prompt == null) {
      return;
    }
    data['prompt'] = prompt;
    try {
      // Get authors
      const author = userConfiguration.username;
      const aiAuthor = names[getAvatar()];

      // Create a human message
      addMessage(prompt, author, 'human', false);

      // If we are streaming append an empty message for the streamed output
      console.log(data['streaming']);
      if (data['streaming']) {
        addMessage('', aiAuthor, 'ai', false);
      }

      // Get completion
      
      data['prompt'] = prompt;
      await fetch(`/v1/completions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/octet-stream',
        },
        body: JSON.stringify(data),
      })
        .then((res) => res.json())
        .then((response: any) => {
          if (response.data.error) {
            errMessage(response.data.error);
            setIsLoading(false);
            return;
          }
          const output = response.data.choices[0]['text'];
    
          if (!data['streaming']) {
            // Create an AI message
            addMessage(output, aiAuthor, 'ai', false);
          }
    
          if (data['tts']) {
            getTTS(output);
          } else {
            setIsLoading(false);
          }
        });
      } catch (error: any) {
          // Check for react failure
          setIsLoading(false);
          errMessage(error);
          console.error('Error sending message:', error);
        }
      };

  // Switches between two video contexts for smooth transitions between
  // Video states allowing us to load tts videos and then discreetly reload loops
  const switchVideo = () => {
    setCurrentVideo((prevVideo) => (prevVideo === 'videoA' ? 'videoB' : 'videoA'));
    if (currentVideo === 'videoA') {
      if (videoARef.current) {
        const avatar = getAvatar();
        if (!videoARef.current.src.includes(videos[avatar])) {
          videoARef.current.src = videos[avatar];
        }
        videoARef.current.currentTime = 0.1;

        const playWhenLoaded = () => {
          if (videoARef.current != null && videoBRef.current != null) {
            videoARef.current.style.display = 'block';
            videoARef.current.play();

            // Perform your specific action here
            videoBRef.current.style.display = 'none';
            // Manually loop the video
            videoBRef.current.currentTime = 0.1;
            if (!videoBRef.current.src.includes(videos[avatar])) {
              videoBRef.current.src = videos[avatar];
            }
            videoBRef.current.pause();
            videoARef.current.removeEventListener('canplaythrough', playWhenLoaded);
          }
        };
        videoARef.current.addEventListener('canplaythrough', playWhenLoaded);
      }
    } else {
      if (videoBRef.current) {
        const avatar = getAvatar();
        if (!videoBRef.current.src.includes(videos[avatar])) {
          videoBRef.current.src = videos[avatar];
        }
        videoBRef.current.currentTime = 0.1;
        const playWhenLoaded = () => {
          if (videoBRef.current != null && videoARef.current != null) {
            videoBRef.current.style.display = 'block';
            videoBRef.current.play();

            // Perform your specific action here
            videoARef.current.style.display = 'none';
            // Manually loop the video
            videoARef.current.currentTime = 0.1;
            if (!videoARef.current.src.includes(videos[avatar])) {
              videoARef.current.src = videos[avatar];
            }
            videoARef.current.pause();
            videoBRef.current.removeEventListener('canplaythrough', playWhenLoaded);
          }
        };
        videoBRef.current.addEventListener('canplaythrough', playWhenLoaded);
      }
    }
  };

  const handleTimeUpdate = (videoRef: React.RefObject<HTMLVideoElement>) => {
    if (videoRef.current) {
      const timeRemaining = videoRef.current.duration - videoRef.current.currentTime;
      if (timeRemaining < 0.1) {
        // videoRef.current.play();
        switchVideo();
      }
    }
  };

  // Setup streaming listener
  useEffect(() => {
    // SSE Event Listener for streaming messages and more
    const eventSource = new EventSource(`${api_url}stream`);

    eventSource.onmessage = (e: MessageEvent) => {
      appendMessage(JSON.parse(e.data).next);
    };

    eventSource.addEventListener('stream_completion', (e: MessageEvent) => {
      appendMessage(JSON.parse(e.data).next);
    });

    eventSource.addEventListener('reflection', (e: MessageEvent) => {
      const reflect = JSON.parse(e.data).reflection.choices[0].text;
      addReflection(reflect, 'Reflection');
    });

    eventSource.addEventListener('observation', (e: MessageEvent) => {
      const reflect = JSON.parse(e.data).observation.choices[0].text;
      addReflection(reflect, 'Observation');
    });

    // Cleanup function to close the event source when the component is unmounted
    return () => {
      eventSource.close();
    };
  }, []); // Pass an empty dependency array to run the effect only once

  // Set user configuration if uninitialized
  // useEffect(() => {
  //   if (userConfiguration.username === '' && userConfiguration.email === '') {
  //     const res = getConfiguration();
  //     res.then((data: Configuration) => {
  //       setUserConfiguration(data);
  //     });
  //   }
  // }, []); // Pass an empty dependency array to run the effect only once

  // Setup the Configuration Interface
  useEffect(() => {
    //Update max tokens
    const updateMaxTokensValue = () => {
      const slider = maxNewTokensRef.current;
      if (slider !== null) {
        document.getElementById('max_new_tokens_value')!.textContent = slider.value;
      }
    };

    // Avatar change event
    if (avatarRef.current) {
      avatarRef.current.addEventListener('change', () => {
        const selectedAvatar = getAvatar();
        playVideo(undefined, '/videos/' + selectedAvatar + '.mp4');
      });
    }

    if (sendMessageRef.current) {
      sendMessageRef.current.addEventListener('click', (event) => {
        // Call sendMessage function here
        event.preventDefault();
      });
    }

    if (maxNewTokensRef.current) {
      maxNewTokensRef.current.addEventListener('input', updateMaxTokensValue);
      maxNewTokensRef.current.addEventListener('change', updateMaxTokensValue);
    }
  }, []); // Pass an empty dependency array to run the effect only once

  useEffect(() => {
    // Add resize event listener (use a method instead of @resizeVideo)
    window.addEventListener('resize', handleResize);

    // Cleanup event listeners on unmount
    return () => {
      // Remove all event listeners here TODO
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.code === 'Enter') {
      e.preventDefault();
      getCompletion();
    }
  };

  return (
    <>
    <main className="flex min-h-screen w-full flex-col py-32">
    <div className='fixed top-0 w-full z-30 transition-all'>
      <div className="md:block md:w-2/12">
        <div className="container mx-auto">
          <div id="hero-video-wrapper">
            <div className="relative">
              <video
                id="videoA"
                className="hero-video"
                ref={videoARef}
                preload="auto"
                autoPlay
                style={{ display: 'none' }}
                onTimeUpdate={() => handleTimeUpdate(videoARef)}
              />
              <video
                id="videoB"
                className="hero-video"
                ref={videoBRef}
                preload="auto"
                autoPlay
                style={{ display: 'none' }}
                onTimeUpdate={() => handleTimeUpdate(videoBRef)}
              />
            </div>
          </div>
          <div className="flex mt-3">
            <div className="w-1/2">
                  <CheckboxElement label={"Speech"} id="speech" />
              {/* <input type="checkbox" id="tts" className="form-checkbox" ref={ttsCheckboxRef} defaultChecked />
              <label htmlFor="tts" className="ml-2">
                Speech
              </label> */}
            </div>
              <div className="w-1/2">
              <CheckboxElement label={"Video"} id="lipsync" />

              {/* <input
                type="checkbox"
                id="lipsync"
                className="form-checkbox"
                ref={lipsyncCheckboxRef}
                defaultChecked
              />
              <label htmlFor="lipsync" className="ml-2">
                Video
              </label> */}
            </div>
              <div className="w-1/2">
              <CheckboxElement label={"Streaming"} id="streaming" />

              {/* <input
                defaultChecked
                type="checkbox"
                id="streaming"
                className="form-checkbox"
                ref={streamingCheckboxRef}
              />
              <label htmlFor="streaming" className="ml-2">
                Streaming
              </label> */}
            </div>
          </div>
              <div className='flex m-4'>
                <div className='mt-3'>
                  <SliderElement defaultValue={512} max={2048} step={1} ariaLabel="Max New Tokens" width="200px" />
                </div>
                <span id="max_new_tokens_value" className="w-2/12">
                  512
                </span>
            </div>
            </div>
            <div className='flex w-full'>
              <SelectElement options={avatars} id="avatar-dropdown" label="Avatar" defaultVal="caretaker" />
            </div>
            <div className='flex w-full'>
              <SelectElement options={ modelConfigs } id="model-config" label="Prompt Config" defaultVal="logical" />
            </div>
            <div className='flex w-full'>
              <SelectElement options={models} id="model" label="Model" defaultVal="alpaca-lora-7b" />
            </div>
            {/* <div className="flex">
              <div className="w-1/2">
                <label htmlFor="avatar-dropdown">Avatar</label>
              </div>
              <div className="w-1/2">
                <select className="form-select float-right" id="avatar-dropdown" ref={avatarRef}>
                  {avatars.map((avatar) => (
                    <option key={avatar} value={avatar}>
                      {avatar}
                    </option>
                  ))}
                </select>
              </div>
            </div> */}
          {/* <div className="flex">
            <div className="w-1/2">
              <label htmlFor="model-config">Personality</label>
            </div>
            <div className="w-1/2">
              <select className="form-select float-right" id="model-config" ref={modelConfigInputRef}>
                {modelConfigs.map((config) => (
                  <option key={config} value={config}>
                    {config}
                  </option>
                ))}
              </select>
            </div>
          </div>
            <div className="flex">
            <div className="w-full">
            <select className="form-select float-right" id="model" ref={modelKeyInputRef}>
              {models.map((model) => (
                <option key={model} value={model}>
                  {model}
                </option>
              ))}
            </select>
          </div>
        </div> */}
    </div>
    <div className="w-full md:w-8/12">
      <div className="px-18%">
        <div className="chat-widget">
          <ul
            ref={chatHistoryRef}
            className="no-bullets chat-history"
            style={{ maxHeight: '500px', overflow: 'scroll' }}
          >
            {messages.map((message, _) => (
              <li key={message.id} className={message.author_type}>
                <div>
                  {message.author}: <span dangerouslySetInnerHTML={{ __html: message.text }}></span>
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
                ref={textareaRef}
                onKeyDown={handleKeyDown}
              ></textarea>
            </div>
            <div className="w-1/4">
            <button
              id="send-message"
              className="btn-main"
              onClick={getCompletion}
              style={{ padding: '0px' }}
            >
              {
                isLoading ? (
                  <SpinnerIcon className="swirling-icon" />
                ) : (
                  <ArrowRightIcon />
                )}
            </button>
              {/* <AudioRecorder /> */}
            </div>
          </div>
        </div>
        <div>
          <ErrorMessage errorState={errorState} errorValue={errorValue} closeError={closeError} />
        </div>
      </div>
    </div>
    <div className="md:block md:w-2/12">
      <div className="container mx-auto">
        <ul
          ref={thoughtHistoryRef}
          className="thought-history"
          style={{ maxHeight: '500px', overflow: 'scroll', fontSize: '10px' }}
        >
          {reflections.map((reflection, index) => (
            <li key={index}>
              <b>{reflection.type}: </b> {reflection.text}
            </li>
          ))}
        </ul>
      </div>
    </div>
  </div>
  </main >
  </>
)};

export default Forge;