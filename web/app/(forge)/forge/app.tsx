'use client';
import { v4 as uuidv4 } from 'uuid';
import React, { useEffect, useRef, useState, KeyboardEvent } from 'react';
import api, { api_url } from '@/components/shared/api';
import { ReflectionProps } from '@/components/shared/reflection';
import ErrorMessage from '@/components/shared/error';
// import { getConfiguration, Configuration } from '../../components/shared/Configure';
// import AudioRecorder from '../../components/shared/AudioRecorder';
// import useStateWithCallback from './useStateWithCallback';
import SwirlIcon from './mind-icon.svg';
import CheckboxElement from '@/components/shared/checkbox';
import SliderElement from '@/components/shared/slider';
import SelectElement from '@/components/shared/select';
import ChatWidget from '@/components/shared/chatwidget';
import ButtonComponent from '@/components/shared/button';
import { useCheckboxState } from '@/components/shared/context/checkboxstatecontext';
import { useSelectState } from '@/components/shared/context/selectstatecontext';
import { useSliderState } from '@/components/shared/context/sliderstatecontext';
import { useLanguageModelConfig } from '@/components/shared/context/languagemodelconfigcontext';
import VideoComponent from '@/components/shared/video';

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

  const [userConfiguration, setUserConfiguration] = useState<Configuration>({
    username: '',
    email: '',
    logged_in: false,
  });

  //Config Refs
  const avatarRef = useRef<HTMLSelectElement>(null);
  const thoughtHistoryRef = useRef<HTMLUListElement>(null);
  // useState values
  const [reflections, setReflections] = useState<ReflectionProps[]>([]);

  const { setLanguageModelConfig } = useLanguageModelConfig();

  const heroVideoWrapperRef = useRef<HTMLDivElement | null>(null);

  // err handling
  const [errorState, setErrorState] = useState(false);
  const [errorValue, setErrorValue] = useState('');

  const fullScreen = () => {
    // if (!heroVideoWrapperRef.current || !chatHistoryRef.current) {
    //   return;
    // }
  
    // const chatHistoryRect = chatHistoryRef.current.getBoundingClientRect();
    // heroVideoWrapperRef.current.style.position = 'absolute';
    // heroVideoWrapperRef.current.style.width = `${chatHistoryRect.width}px`;
    // heroVideoWrapperRef.current.style.height = `${chatHistoryRect.height}px`;
    // heroVideoWrapperRef.current.style.left = `${chatHistoryRect.left}px`;
    // heroVideoWrapperRef.current.style.top = `${chatHistoryRect.top}px`; 
  }

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
  // const appendMessage = (newText: string) => {
  //   if (streamingCheckboxRef.current?.checked) {
  //     setMessages((prevMessages) => {
  //       const lastIndex = prevMessages.length - 1;
  //       const lastMessage = prevMessages[lastIndex];
  //       if (lastMessage != undefined) {
  //         const updatedMessage = { ...lastMessage, text: lastMessage.text + newText };
  //         return [...prevMessages.slice(0, lastIndex), updatedMessage];
  //       }
  //       return prevMessages;
  //     });
  //   }
  // };

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

  // useEffect to initialize the languageModelConfig on first render
  useEffect(() => {
    setLanguageModelConfig('human_name', userConfiguration.username || 'Human');
    setLanguageModelConfig('robot_name', names[getAvatar()] || 'Sam');
    setLanguageModelConfig('speech', false);
    setLanguageModelConfig('lipsync', false);
    setLanguageModelConfig('streaming', false);
    setLanguageModelConfig('max_new_tokens', 512);
    setLanguageModelConfig('avatar', getAvatar());
    setLanguageModelConfig('generation_config', modelConfigs[0]);
    setLanguageModelConfig('model_key', models[0]);
    setLanguageModelConfig('prompt', '');
  }, []);


  // Setup streaming listener
  useEffect(() => {
    // SSE Event Listener for streaming messages and more
    const eventSource = new EventSource(`${api_url}/stream`);

    // eventSource.onmessage = (e: MessageEvent) => {
    //   appendMessage(JSON.parse(e.data).next);
    // };

    // eventSource.addEventListener('stream_completion', (e: MessageEvent) => {
    //   appendMessage(JSON.parse(e.data).next);
    // });

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

  // Setup the Configuration Interface
  useEffect(() => {
    // Avatar change event
    if (avatarRef.current) {
      avatarRef.current.addEventListener('change', () => {
        const selectedAvatar = getAvatar();
        playVideo(undefined, '/videos/' + selectedAvatar + '.mp4');
      });
    }
  }, []);

  useEffect(() => {
    // Add resize event listener (use a method instead of @resizeVideo)
    window.addEventListener('resize', handleResize);

    // Cleanup event listeners on unmount
    return () => {
      // Remove all event listeners here TODO
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <>
    <main className="flex min-h-screen w-full flex-col py-32">
      <div className='fixed top-0 w-full z-30 transition-all'>
        <div className="md:block md:w-2/12">
          <div className="container mx-auto">
            <VideoComponent/>
            <div className="flex mt-3">
              <div className="w-1/2">
                <CheckboxElement label={"Speech"} id="speech" defaultVal={false} />
              </div>
              <div className="w-1/2">
                <CheckboxElement label={"Video"} id="lipsync" defaultVal={false}  />
              </div>
              <div className="w-1/2">
                <CheckboxElement label={"Streaming"} id="streaming" defaultVal={false} />
              </div>
            </div>
            <div className='flex w-full'>
              <SliderElement defaultValue={512} max={2048} step={1} ariaLabel="Max New Tokens" width="200px" sliderId="tokens" />
            </div>
          </div>
          <div className='flex w-full mt-3'>
            <SelectElement options={avatars} id="avatar" label="Avatar" defaultVal="caretaker" />
          </div>
          <div className='flex w-full mt-3'>
            <SelectElement options={ modelConfigs } id="generation_config" label="Prompt Config" defaultVal="logical" />
          </div>
          <div className='flex w-full mt-3'>
            <SelectElement options={models} id="model_key" label="Model" defaultVal="alpaca-lora-7b" />
          </div>
          {/* <div className='flex w-full mt-3'>
            <ButtonComponent text="Expand Video" onClick={fullScreen} />
          </div>   */}
        </div>
        <div className="w-full md:w-8/12">
          <div className="px-18%">
            <ChatWidget />
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