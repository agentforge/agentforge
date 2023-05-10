// SpeechComponent.tsx

import React, { useRef } from 'react';
import api_url from './api';
import { AvatarData } from './context/avatarcontextprovider';

interface SpeechComponentProps {
  lastResponseRef: React.MutableRefObject<string>;
  currentAvatar:  React.MutableRefObject<AvatarData | undefined>;
}

const SpeechComponent: React.FC<SpeechComponentProps> = ({ lastResponseRef, currentAvatar }) => {
  const audioPlayerRef = useRef<HTMLAudioElement>(null);

  React.useEffect(() => {
    if (lastResponseRef.current) {
      playAudio(lastResponseRef.current, currentAvatar.current);
    }
  }, [lastResponseRef.current]);


  const fetchAudio = async (text: string, avatar: AvatarData | undefined): Promise<Blob> => {
    if (!avatar) {
      throw new Error('Avatar must be set to call TTS API');
    }
    const request = {
      "prompt": text,
      "avatar": avatar.avatar,
    };

    // TODO: Going around TS server to API, we need to use a token to authenticate
    const response = await fetch(`${api_url}/v1/tts`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error('Failed to fetch audio');
    }

    return await response.blob();
  };

  const playAudio = async (text: string, avatar: AvatarData | undefined) => {
    try {
      const audioBlob = await fetchAudio(text, avatar);
      const audioUrl = URL.createObjectURL(audioBlob);

      if (audioPlayerRef.current) {
        audioPlayerRef.current.src = audioUrl;
        audioPlayerRef.current.play();
      }
    } catch (error) {
      console.error('Error fetching audio:', error);
    }
  };

  return (
    <div>
      <audio ref={audioPlayerRef} />
    </div>
  );
};

export default SpeechComponent;
