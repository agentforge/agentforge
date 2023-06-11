import React, { createContext, useContext, useRef, useEffect, useState } from 'react';

interface VideoProviderContextValue {
  playVideo: (videoSrc: string) => void;
  setIdleVideoSource: (videoSrc: string) => void;
  isStreaming: boolean;
  idleVideoRef: React.RefObject<HTMLVideoElement>;
  streamVideoRef: React.RefObject<HTMLVideoElement>;
}

const VideoProviderContext = createContext<VideoProviderContextValue | undefined>(undefined);

export const useVideo = () => {
  const context = useContext(VideoProviderContext);
  if (!context) {
    throw new Error('useVideo must be used within a VideoProvider');
  }
  return context;
};

interface VideoProviderProps {
  children: React.ReactNode;
  defaultIdleVideoSource: string;
}

export const VideoProvider: React.FC<VideoProviderProps> = ({ children, defaultIdleVideoSource }) => {
  const idleVideoRef = useRef<HTMLVideoElement>(null);
  const streamVideoRef = useRef<HTMLVideoElement>(null);
  const [isStreaming, setIsStreaming] = useState(false);

  const playVideo = (videoSrc: string) => {
    if (idleVideoRef.current && streamVideoRef.current) {
      idleVideoRef.current.pause();
      streamVideoRef.current.src = videoSrc;
      streamVideoRef.current.play();
      setIsStreaming(true);
    }
  };

  const setIdleVideoSource = (videoSrc: string) => {
    if (idleVideoRef.current) {
      idleVideoRef.current.src = videoSrc;
    }
  };

  useEffect(() => {
    const streamVideo = streamVideoRef.current;
    if (streamVideo) {
      streamVideo.addEventListener('ended', () => {
        setIsStreaming(false);
        if (idleVideoRef.current) {
          idleVideoRef.current.play();
        }
      });
    }
  }, []);

  return (
    <VideoProviderContext.Provider value={{ playVideo, setIdleVideoSource, isStreaming, idleVideoRef, streamVideoRef }}>
      {children}
    </VideoProviderContext.Provider>
  );
};
