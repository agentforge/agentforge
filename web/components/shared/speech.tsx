// SpeechComponent.tsx

import React, { useRef } from 'react';
import { AvatarData } from './context/avatarcontextprovider';
import { useAudio } from './context/audioprovider';

interface SpeechComponentProps {
  lastResponseRef: React.MutableRefObject<string>;
  currentAvatar:  React.MutableRefObject<AvatarData | undefined>;
}

const SpeechComponent: React.FC<SpeechComponentProps> = ({ lastResponseRef, currentAvatar }) => {
  const audioPlayerRef = useRef<HTMLAudioElement>(null);

  return (
    <div>
      <audio ref={audioPlayerRef} />
    </div>
  );
};

export default SpeechComponent;
