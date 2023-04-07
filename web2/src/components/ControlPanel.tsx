import React, { useEffect, useRef } from 'react';
import { Button } from 'react-bootstrap';

interface ControlPanelProps {
  avatars: string[];
  modelConfigs: string[];
  models: string[];
}

const ControlPanel: React.FC<ControlPanelProps> = ({ avatars, modelConfigs, models }) => {

const avatarDropdownRef = useRef<HTMLSelectElement>(null);
  const heroVideoRef = useRef<HTMLVideoElement>(null);
  const sendMessageRef = useRef<HTMLButtonElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const maxNewTokensRef = useRef<HTMLInputElement>(null);
  const ttsCheckboxRef = useRef<HTMLInputElement>(null);
  const streamingCheckboxRef = useRef<HTMLInputElement>(null);
  const nameInputRef = useRef<HTMLInputElement>(null);
  const lipsyncCheckboxRef = useRef<HTMLInputElement>(null);

  const avatarRef = useRef<HTMLSelectElement>(null);
  const modelConfigInputRef = useRef<HTMLSelectElement>(null);
  const modelKeyInputRef = useRef<HTMLSelectElement>(null);

  const videoSrc = "/videos/default.mp4";
  

  const getConfigValues = () => {
    const configs = {
      human_name: nameInputRef.current?.value || "",
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

  useEffect(() => {
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

    // Set change events
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

    if (textareaRef.current) {
      textareaRef.current.addEventListener('keydown', (e) => {
        if (e.keyCode === 13 && e.shiftKey) {
          if (textareaRef.current) {
            textareaRef.current.value += '\n';
            e.preventDefault();
          }
        }
        if (e.keyCode === 13 && !e.shiftKey) {
          // Call sendMessage function here
          e.preventDefault();
        }
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
      const chatHistory = document.querySelector('.chat-history') as HTMLElement;
      const chatHistoryRect = chatHistory.getBoundingClientRect();
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
  }, []);

  return (
    <div className="control-panel container">
      <h2>Control Panel</h2>

      <div className="form-group">
        <Button id="reset-history" className="btn-main">Reset History</Button>
      </div>
      <div className="form-group">
        <h5>Name</h5>
        <input id="name-input" type="text" className="form-control" defaultValue="User" />
      </div>
      <div className="form-group">
        <h5>Robot Name</h5>
        <input
          id="robot-name-input"
          type="text"
          className="form-control"
          defaultValue="Robot"
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
  );
};

export default ControlPanel;
