// AvatarProviderContext.tsx
import React, { createContext, useContext, useEffect, useState } from 'react';

export interface AvatarData {
  avatar: string;
  mp4: string;
  prompt_context: {
    context: string;
    name: string;
  };
  speaker_idx?: number;
  speaker_wav?: string;
}

type AvatarMapping = {
  [key: string]: AvatarData;
};

interface AvatarProviderContextValue {
  avatars: AvatarMapping;
  getAvatarData: (key: string) => AvatarData | undefined;
}

const AvatarProviderContext = createContext<AvatarProviderContextValue | undefined>(undefined);

export const useAvatarProvider = () => {
  const context = useContext(AvatarProviderContext);
  if (!context) {
    throw new Error('useAvatarProvider must be used within an AvatarProvider');
  }
  return context;
};

interface AvatarProviderProps {
  children: React.ReactNode;
}

export const AvatarProvider: React.FC<AvatarProviderProps> = ({ children }) => {
  const [avatars, setAvatars] = useState<AvatarMapping>({});

  const getAvatarData = (key: string): AvatarData | undefined => {
    return avatars[key];
  };

  useEffect(() => {
    const fetchAvatars = async () => {
      try {
        const response = await fetch('/api/avatars'); // replace with your API endpoint
        const data: AvatarMapping = await response.json();
        setAvatars(data);
      } catch (error) {
        console.error('Error fetching avatars:', error);
      }
    };

    fetchAvatars();
  }, []);

  return (
    <AvatarProviderContext.Provider value={{ avatars, getAvatarData }}>
      {children}
    </AvatarProviderContext.Provider>
  );
};
