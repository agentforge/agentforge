// AudioProvider.tsx

import React, { createContext, useContext, useState } from 'react';
import api_url from '@/components/shared/api';
import { AvatarData } from '@/components/shared/context/avatarcontextprovider';

interface AudioProviderContextValue {
  playAudio: (text: string, avatar: AvatarData | undefined) => void;
}

interface AudioProviderProps {
  children: React.ReactNode;
}

const AudioProviderContext = createContext<AudioProviderContextValue>({
  playAudio: () => {},
});

export const AudioProvider: React.FC<AudioProviderProps> = ({ children }) => {
  const [audio, setAudio] = useState<HTMLAudioElement | null>(null);

  const fetchAudio = async (text: string, avatar: AvatarData | undefined): Promise<HTMLAudioElement> => {
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

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    return new Audio(url);
  };

  const playAudio = async (text: string, avatar: AvatarData | undefined) => {
    try {
      const newAudio = await fetchAudio(text, avatar);

      if (audio) {
        audio.pause();
      }
  
      newAudio.play();
      setAudio(newAudio);

    } catch (error) {
      console.error('Error fetching audio:', error);
    }
  };

  const value: AudioProviderContextValue = {
    playAudio,
  };

  return (
    <AudioProviderContext.Provider value={value}>
      {children}
    </AudioProviderContext.Provider>
  );
};

export const useAudio = () => {
  return useContext(AudioProviderContext);
};
