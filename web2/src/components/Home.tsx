import React, { useEffect, useRef, useState, KeyboardEvent } from 'react';
import { Button } from 'react-bootstrap';
import ControlPanel from './ControlPanel';
import Agent from './Agent';
import Gutter from './Gutter';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRocket, faEllipsisH } from '@fortawesome/free-solid-svg-icons';
import axios from 'axios';
import config from "../config/config";
import Message, {MessageProps} from './Message'
import { v4 as uuidv4 } from 'uuid';
import useStateWithCallback from './useStateWithCallback'

interface HomeProps {}

const Home: React.FC<HomeProps> = () => {

  // TODO: make dynamic, temporary until we can source these from the API
  // CONSTANTS
  const avatars = ["default", "makhno", "fdr"];
  const modelConfigs = ["creative", "logical", "moderate"];
  const models = ["alpaca-lora-7b"];
  const videoSrc = "/videos/default.mp4";
  interface VideoMap {
    [key: string]: string;
  }
  const videos: VideoMap = {
    default: '/videos/default.mp4',
    makhno: '/videos/makhno.mp4',
    fdr: '/videos/fdr.mp4',
  };
  

  // useState values
  const [messages, setMessages] = useStateWithCallback<MessageProps[]>([], () => {
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  });
  const [textAreaValue, setTextAreaValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentVideo, setCurrentVideo] = useState<'videoA' | 'videoB'>('videoA');


  //Config Refs
  const avatarRef = useRef<HTMLSelectElement>(null);
  const maxNewTokensRef = useRef<HTMLInputElement>(null);
  const ttsCheckboxRef = useRef<HTMLInputElement>(null);
  const streamingCheckboxRef = useRef<HTMLInputElement>(null);
  const nameInputRef = useRef<HTMLInputElement>(null);
  const aiInputRef = useRef<HTMLInputElement>(null);
  const lipsyncCheckboxRef = useRef<HTMLInputElement>(null);

  // Video refs
  const videoARef = useRef<HTMLVideoElement>(null);
  const videoBRef = useRef<HTMLVideoElement>(null);

  // Text Refs
  const sendMessageRef = useRef<HTMLButtonElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const chatHistoryRef = useRef<HTMLUListElement>(null);

  const modelConfigInputRef = useRef<HTMLSelectElement>(null);
  const modelKeyInputRef = useRef<HTMLSelectElement>(null);

  // Change Events
  const handleTextAreaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setTextAreaValue(e.target.value);
  };

  const clearTextarea = () => {
    if (textareaRef.current) {
      setTextAreaValue('');
      textareaRef.current.value = '';
      // textAreaValue = '';
    }
  };

  const addMessage = async (prompt: string | undefined, author: string | undefined, author_type: string | undefined) => {
    // Validations
    if(author == null){
      console.log("ERROR: Must set author.")
      return
    }
    if(prompt == null){
      console.log("ERROR: Must set prompt.")
      return
    }
    if(author_type == null){
      console.log("ERROR: Must set author_type.")
      return      
    }

    // Create new message
    const newMessage: MessageProps = {
      id: uuidv4(),
      author_type: author_type, //'human',
      author: author,
      text: prompt,
    };

    // Wrap setMessages in a Promise and use await to ensure sequential execution
    await new Promise<void>((resolve) => {
      setMessages((prevMessages: any) => {
        resolve();
        clearTextarea();
        return [...prevMessages, newMessage];
      });
    });
  }

  // LLM Completion API Functions
  const getCompletion = async () => {
    var prompt = textareaRef.current?.value
    if(prompt == null){
      return 
    }
    const data = {
      prompt: prompt,
      config: getConfigValues()
    };
    try {
      // Create a human message
      var author = nameInputRef.current?.value;
      addMessage(prompt, author, 'human');

      // Get completion
      setIsLoading(true)
      const response = await axios.post(`${config.host}:${config.port}/v1/completions`, data);
      
      // Create an AI message
      var author = aiInputRef.current?.value;
      const output = response.data.choices[0]["text"];
      addMessage(output, author, 'ai');
      getTTS(output);

    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  // Calls TTS API
  const getTTS = async (prompt: string) => {
    const data = {
      prompt: prompt,
      config: getConfigValues()
    };
    const response = await axios.post(`${config.host}:${config.port}/v1/tts`, data, {
      responseType: 'blob',
    });
    console.log(response)
    playVideo(response.data, undefined);
  };

  // Getter/Setter Functions for all user configuration variables
  // present on this screen
  const getConfigValues = () => {
    const configs = {
      human_name: nameInputRef.current?.value || "",
      robot_name: aiInputRef.current?.value || "",
      tts: ttsCheckboxRef.current?.checked || false,
      lipsync: lipsyncCheckboxRef.current?.checked || false,
      streaming: streamingCheckboxRef.current?.checked || false,
      max_new_tokens: parseInt(maxNewTokensRef.current?.value || "0", 10),
      avatar: avatarRef.current?.value || "",
      generation_config: modelConfigInputRef.current?.value || "",
      model_key: modelKeyInputRef.current?.value || "",
    };
  
    return configs;
  };

  // Get the current avatar dropdown value
  const getAvatar = () => {
    var avatar = avatarRef.current?.value;
    if(avatar == null){
      avatar = "default"
    }
    return avatar;
  };

  // Switches between two video contexts for smooth transitions between
  // Video states allowing us to load tts videos and then discreetly reload loops
  const switchVideo = () => {
    setCurrentVideo((prevVideo) => (prevVideo === 'videoA' ? 'videoB' : 'videoA'));
    if (currentVideo === 'videoA') {
      if (videoARef.current) {
        console.log(currentVideo)
        const avatar = getAvatar();
        if(!videoARef.current.src.includes(videos[avatar])){
          videoARef.current.src = videos[avatar];
        }
        videoARef.current.currentTime = .1;
        // videoARef.current.play();
        // videoARef.current.style.display = 'block';

        const playWhenLoaded = () => {
          if(videoARef.current != null && videoBRef.current != null){
            videoARef.current.style.display = 'block';
            videoARef.current.play();

            // Perform your specific action here
            videoBRef.current.style.display = 'none';
            // Manually loop the video
            videoBRef.current.currentTime = .1;
            if(!videoBRef.current.src.includes(videos[avatar])){
              videoBRef.current.src = videos[avatar];
            }
            videoBRef.current.pause()
            videoARef.current.removeEventListener('canplaythrough', playWhenLoaded);
          }
        };
        videoARef.current.addEventListener('canplaythrough', playWhenLoaded);
      }
    } else {
      if (videoBRef.current) {
        console.log(currentVideo)
        const avatar = getAvatar();
        if(!videoBRef.current.src.includes(videos[avatar])){
          videoBRef.current.src = videos[avatar];
        }
        videoBRef.current.currentTime = .1;
        const playWhenLoaded = () => {
          if(videoBRef.current != null && videoARef.current != null){
            videoBRef.current.style.display = 'block';
            videoBRef.current.play();

            // Perform your specific action here
            videoARef.current.style.display = 'none';
            // Manually loop the video
            videoARef.current.currentTime = .1;
            if(!videoARef.current.src.includes(videos[avatar])){
              videoARef.current.src = videos[avatar];
            }
            videoARef.current.pause()
            videoBRef.current.removeEventListener('canplaythrough', playWhenLoaded);
          }
        };
        videoBRef.current.addEventListener('canplaythrough', playWhenLoaded);
        // videoBRef.current.play();
        // videoBRef.current.style.display = 'block';
      }
    }
  };

  const handleTimeUpdate = (videoRef: React.RefObject<HTMLVideoElement>) => {
    if(videoRef.current){
      const timeRemaining = videoRef.current.duration - videoRef.current.currentTime;
      if (timeRemaining < 0.1) {
        // videoRef.current.play();
        console.log("TIME UP SWITCHING")
        switchVideo();
      }
    }
  };

  // Play a video from blob or url -- setup the non-active video, load it, and play it.
  // Switch the reference to this video
  const playVideo = async (blob: Blob | undefined, url: string | undefined) => {
    const nextVideoRef = currentVideo === 'videoA' ? videoBRef : videoARef;
    const currentVideoRef = currentVideo === 'videoA' ? videoARef : videoBRef;

    const nextVideo = nextVideoRef.current;
    if (nextVideo) {
      if(url == undefined){
        if(blob == undefined) {
          console.log("err: Must select url or blob.")
          return
        }
        const videoUrl = URL.createObjectURL(blob);
        if(!nextVideo.src.includes(videoUrl)){
          nextVideo.src = videoUrl;
        }
      } else {
        if(!nextVideo.src.includes(url)){
          nextVideo.src = url;
        }
      }
      const playWhenLoaded = () => {
          if(currentVideoRef.current != null){
            // nextVideo.currentTime = .1;
            nextVideo.play();
            nextVideo.style.display = 'block';
            
            // // Hide prev video
            currentVideoRef.current.style.display = 'none';
            // currentVideoRef.current.currentTime = .1;
            const selectedAvatar = getAvatar();
            const defaultUrl = '/videos/' + selectedAvatar + '.mp4';

            if(!currentVideoRef.current.src.includes(defaultUrl)){
              currentVideoRef.current.src = defaultUrl;
            }
            currentVideoRef.current.pause()
            // setCurrentVideo((prevVideo) => (prevVideo === 'videoA' ? 'videoB' : 'videoA'));
            // switchVideo();
            nextVideo.removeEventListener('canplaythrough', playWhenLoaded);
          }
      };
      nextVideo.addEventListener('canplaythrough', playWhenLoaded);
      // await nextVideo.play();
      // nextVideo.style.display = 'block';
      // switchVideo();
    }
  };

  // useEffect Function
  useEffect(() => {

    //Update max tokens
    const updateMaxTokensValue = () => {
      const slider = maxNewTokensRef.current;
      if (slider !== null) {
        document.getElementById('max_new_tokens_value')!.textContent = slider.value;
      }
    };

    const updateStates = () => {
      const ttsChecked = ttsCheckboxRef.current?.checked;
      const streamingChecked = streamingCheckboxRef.current?.checked;

      const lipsyncCheckbox = document.getElementById("lipsync") as HTMLInputElement;

      if (ttsChecked) {
        if (streamingChecked) {
          lipsyncCheckbox.checked = false;
          lipsyncCheckbox.disabled = true;
        } else {
          lipsyncCheckbox.checked = true;
          lipsyncCheckbox.disabled = false;
        }
      } else {
        lipsyncCheckbox.checked = false;
        lipsyncCheckbox.disabled = true;
      }
    };

    // Avatar change event
    if (avatarRef.current) {
      avatarRef.current.addEventListener('change', () => {
        const selectedAvatar = getAvatar();
        playVideo(undefined, '/videos/' + selectedAvatar + '.mp4')
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

    if (ttsCheckboxRef.current && streamingCheckboxRef.current) {
      ttsCheckboxRef.current.addEventListener('change', (e) => {
        console.log('change');
        e.preventDefault();
        updateStates();
      });

      streamingCheckboxRef.current.addEventListener('change', (e) => {
        console.log('change');
        e.preventDefault();
        updateStates();
      });
    }

    // Add resize event listener (use a method instead of @resizeVideo)
    window.addEventListener('resize', () => {
      const video = document.getElementById('hero-video') as HTMLVideoElement;
      const videoWrapper = document.getElementById('hero-video-wrapper') as HTMLElement;
      // const chatHistory = document.querySelector('.chat-history') as HTMLElement;
      // const chatHistoryRect = chatHistory.getBoundingClientRect();
      const userInput = document.getElementById('user-input') as HTMLElement;
      const userInputRect = userInput.getBoundingClientRect();
      const distanceFromTop = userInputRect.top;
    
      if (videoWrapper.style.position === 'absolute') {
        videoWrapper.style.top = '0';
        videoWrapper.style.left = userInputRect.left + 'px';
        video.style.width = userInputRect.width + 'px';
        video.style.height = distanceFromTop + 'px';
      }
    });

    // Cleanup event listeners on unmount
    return () => {
      // Remove all event listeners here TODO
    };
  }, [messages, currentVideo]);

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.code === 'Enter') {
      e.preventDefault();
      getCompletion();
    }
  };

  // // Changes the source of the video
  // const handleVideoEnded = () => {
  //   var avatar = getAvatar()
  //   const defaultVideoUrl = videos[avatar];
  //   if (heroVideoRef.current) {
  //     // console.log("heroVideoRef.current.src")
  //     // console.log(heroVideoRef.current.src)

  //     // console.log("defaultVideoUrl")
  //     // console.log(defaultVideoUrl)
  //     if(!heroVideoRef.current.src.includes(defaultVideoUrl)){
  //       console.log(defaultVideoUrl)
  //       heroVideoRef.current.src = defaultVideoUrl;
  //     }
  //     console.log(heroVideoRef.current.currentTime)
  //     // Manually loop the video
  //     // heroVideoRef.current.currentTime = 0;
  //     // heroVideoRef.current.play();
  //   }
  // };

  return (
    <div>
      <div className="row">
        <div className="col-2 main-control d-none d-md-block">
        <div className="control-panel container">
          <h2>Control Panel</h2>

          {/* <div className="form-group">
            <Button id="reset-history" className="btn-main">Reset History</Button>
          </div> */}
          <div className="form-group config-row">
            <h5>Name</h5>
            <input 
              id="name-input"
              type="text"
              className="form-control"
              defaultValue="User"
              ref={nameInputRef}
            />
          </div>
          <div className="form-group config-row">
            <h5>Robot Name</h5>
            <input
              id="robot-name-input"
              type="text"
              className="form-control"
              defaultValue="Robot"
              ref={aiInputRef}
            />
          </div>
          {/* Add your video implementation */}
          <div id="hero-video-wrapper">
            <div style={{ position: 'relative' }}>
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
            {/* <video
              id="hero-video"
              src={videoSrc}
              ref={heroVideoRef}
              preload="auto"
              autoPlay
            ></video> */}
          </div>
          <div className="row form-group">
            <div className="custom-control custom-checkbox col-md-6">
              <input type="checkbox" id="tts" className="custom-control-input" ref={ttsCheckboxRef} defaultChecked />
              <label htmlFor="tts" className="custom-control-label">
                Speech
              </label>
            </div>
            <div className="custom-control custom-checkbox col-md-6">
              <input type="checkbox" id="lipsync" className="custom-control-input" ref={lipsyncCheckboxRef} defaultChecked />
              <label htmlFor="lipsync" className="custom-control-label">
                Video
              </label>
            </div>
            <div className="custom-control custom-checkbox col-md-6">
              <input type="checkbox" id="streaming" className="custom-control-input" ref={streamingCheckboxRef} />
              <label htmlFor="streaming" className="custom-control-label">
                Streaming
              </label>
            </div>
          </div>
          <div className="slider-container">
            <label htmlFor="max_new_tokens">Max New Tokens</label>
            <div className="row config-row justify-content-md-center" >
              <input
                ref={maxNewTokensRef}
                type="range"
                id="max_new_tokens"
                className="custom-range col-8"
                min="1"
                max="2048"
                defaultValue="1024"
              />
              <span id="max_new_tokens_value" className="col-2">1024</span>
            </div>
          </div>
          <div className="row config-row">
            <div className="form-group">
              <label htmlFor="avatar-dropdown" className="col-md-6">Avatar</label>
              <select className="custom-select col-md-6 float-end" id="avatar-dropdown" ref={avatarRef}>
                {avatars.map((avatar) => (
                  <option key={avatar} value={avatar}>
                    {avatar}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div className="row config-row">
            <div className="form-group">
              <label htmlFor="model-config" className="col-md-6">Personality</label>
              <select className="custom-select col-md-6 float-end" id="model-config" ref={modelConfigInputRef}>
                {modelConfigs.map((config) => (
                  <option key={config} value={config}>
                    {config}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div className="row config-row">
            <div className="form-group">
              <label htmlFor="model" className="col-md-6">Model</label>
              <select className="custom-select col-md-6 float-end" id="model" ref={modelKeyInputRef}>
                {models.map((model) => (
                  <option key={model} value={model}>
                    {model}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
        </div>
        <div className="sm-col-12 md-col-8 interaction">
          <div className="main-control">
            <div style={{ paddingLeft: '18%', paddingRight: '18%' }}>
              <div className="chat-widget">
                <ul
                  ref={chatHistoryRef}
                  className="no-bullets chat-history"
                  style={{ maxHeight: '500px', overflow: 'scroll' }}
                >
                  {messages.map((message, _) => (
                      <li key={message.id} className={message.author_type}>
                        {message.author}: {message.text}
                      </li>
                      // <Message id={message.id} author_type={message.author_type} author={message.author} text={message.text} />
                    ))}

                </ul>
                <div id="chat-input" className="row">
                  <div className="col-9">
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
                  <div className="col-3">
                    <Button id="send-message" className="btn btn-main" onClick={getCompletion}>
                    {isLoading ? (
                      <FontAwesomeIcon icon={faEllipsisH} className="animated-ellipsis" />
                    ) : (
                      <FontAwesomeIcon icon={faRocket} />
                    )}
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="col-2 secondary-control d-none d-md-block">
          <div className="container">
            <ul
              className="thought-history"
              style={{ maxHeight: '500px', overflow: 'scroll', fontSize: '10px' }}
            ></ul>
          </div>
        </div>  
      </div>
    </div>
  );
};

export default Home;
