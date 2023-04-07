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

interface HomeProps {}

const Home: React.FC<HomeProps> = () => {

  // TODO: make dynamic, temporary until we can source these from the API
  // CONSTANTS
  const avatars = ["default", "makhno", "fdr"];
  const modelConfigs = ["creative", "logical", "moderate"];
  const models = ["alpaca-lora-7b"];
  const videoSrc = "/videos/default.mp4";

  // useState values
  const [messages, setMessages] = useState<MessageProps[]>([]);
  const [textAreaValue, setTextAreaValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  //useRefs
  const avatarDropdownRef = useRef<HTMLSelectElement>(null);
  const heroVideoRef = useRef<HTMLVideoElement>(null);
  const sendMessageRef = useRef<HTMLButtonElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const maxNewTokensRef = useRef<HTMLInputElement>(null);
  const ttsCheckboxRef = useRef<HTMLInputElement>(null);
  const streamingCheckboxRef = useRef<HTMLInputElement>(null);
  const nameInputRef = useRef<HTMLInputElement>(null);
  const aiInputRef = useRef<HTMLInputElement>(null);
  const lipsyncCheckboxRef = useRef<HTMLInputElement>(null);
  const chatHistoryRef = useRef<HTMLUListElement>(null);

  const avatarRef = useRef<HTMLSelectElement>(null);
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
    // setMessages([...messages, newMessage]);
    // Wrap setMessages in a Promise and use await to ensure sequential execution
      await new Promise<void>((resolve) => {
        setMessages((prevMessages) => {
          resolve();
          clearTextarea()
          return [...prevMessages, newMessage];
        });
      });
  }

  // API Functions
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
      addMessage(response.data.choices[0]["text"], author, 'ai');

    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  const getTTS = async () => {

  };

  // Getter/Setter Functions
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

  // useEffect Function
  useEffect(() => {

    if (messages.length > 0) {
      // Scroll to the bottom of chat-history element
      if (chatHistoryRef.current) {
        chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
      }
    }
    const updateMaxTokensValue = () => {
      const slider = maxNewTokensRef.current;
      if (slider !== null) {
        document.getElementById('max_new_tokens_value')!.textContent = slider.value;
      }
    };

    const getAvatar = () => {
      const avatar = avatarDropdownRef.current?.value;
      return avatar;
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

    // More change events
    if (avatarDropdownRef.current && heroVideoRef.current) {
      avatarDropdownRef.current.addEventListener('change', () => {
        const selectedAvatar = getAvatar();
        if (heroVideoRef.current) {
          heroVideoRef.current.src = '/videos/' + selectedAvatar + '.mp4';
        }
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
  }, [messages]);
  
  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.code === 'Enter') {
      e.preventDefault()
      getCompletion();
    }
  };

  return (
    <div>
      <div className="row">
        <div className="col-2 main-control">
        <div className="control-panel container">
          <h2>Control Panel</h2>

          <div className="form-group">
            <Button id="reset-history" className="btn-main">Reset History</Button>
          </div>
          <div className="form-group">
            <h5>Name</h5>
            <input 
              id="name-input"
              type="text"
              className="form-control"
              defaultValue="User"
              ref={nameInputRef}
            />
          </div>
          <div className="form-group">
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
          <div id="hero-video-wrapper"><video id="hero-video" src={videoSrc} autoPlay loop></video></div>
          <div className="custom-control custom-checkbox">
            <input type="checkbox" id="tts" className="custom-control-input" ref={ttsCheckboxRef} defaultChecked />
            <label htmlFor="tts" className="custom-control-label">
              TTS
            </label>
          </div>
          <div className="custom-control custom-checkbox">
            <input type="checkbox" id="lipsync" className="custom-control-input" ref={lipsyncCheckboxRef} defaultChecked />
            <label htmlFor="lipsync" className="custom-control-label">
              LipSync
            </label>
          </div>
          <div className="custom-control custom-checkbox">
            <input type="checkbox" id="streaming" className="custom-control-input" ref={streamingCheckboxRef} />
            <label htmlFor="streaming" className="custom-control-label">
              Streaming
            </label>
          </div>
          <div className="slider-container">
            <label htmlFor="max_new_tokens">Max New Tokens</label>
            <input
              ref={maxNewTokensRef}
              type="range"
              id="max_new_tokens"
              className="custom-range"
              min="1"
              max="2048"
            />
            <span id="max_new_tokens_value"></span>
          </div>
          <div className="dropdown-container">
            <label>Avatars</label>
            <select className="custom-select" id="avatar-dropdown" ref={avatarRef}>
              {avatars.map((avatar) => (
                <option key={avatar} value={avatar}>
                  {avatar}
                </option>
              ))}
            </select>
          </div>
          <div className="dropdown-container">
            <label htmlFor="model-config">Model Config</label>
            <select className="custom-select" id="model-config" ref={modelConfigInputRef}>
              {modelConfigs.map((config) => (
                <option key={config} value={config}>
                  {config}
                </option>
              ))}
            </select>
          </div>
          <div className="dropdown-container">
            <label htmlFor="model">Model</label>
            <select className="custom-select" id="model" ref={modelKeyInputRef}>
              {models.map((model) => (
                <option key={model} value={model}>
                  {model}
                </option>
              ))}
            </select>
          </div>
        </div>
        </div>
        <div className="col-8 interaction">
          <div style={{ marginTop: '32px', width: '100%', height: '100%' }}>
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
        <div className="col-2 secondary-control">
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
