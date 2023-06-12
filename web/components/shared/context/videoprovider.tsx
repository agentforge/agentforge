import React, { createContext, useContext, useRef, useState, useEffect } from 'react';

interface VideoProviderContextValue {
  videoRef: React.RefObject<HTMLVideoElement>;
  playVideo: (videoSrc: string) => void;
  setIdleVideoSource: (videoSrc: string) => void;
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
  const videoRef = useRef<HTMLVideoElement>(null);
  const [idleVideoSource, setIdleVideoSource] = useState(defaultIdleVideoSource);

  const playVideo = (videoSrc: string) => {
    if (videoRef.current) {
      videoRef.current.src = videoSrc;
      videoRef.current.play();
    }
  };

  useEffect(() => {
    const videoElement = videoRef.current;
    if (videoElement) {
      videoElement.addEventListener('ended', () => {
        if (videoRef.current) {
          videoRef.current.src = idleVideoSource;
          videoRef.current.play();
        }
      });
    }
    return () => {
      if (videoElement) {
        videoElement.removeEventListener('ended', () => {});
      }
    };
  }, [idleVideoSource]);

  // // Initialize first video
  useEffect(() => {
    console.log(defaultIdleVideoSource);
    setIdleVideoSource(defaultIdleVideoSource);
    if (videoRef.current) {
      videoRef.current.muted = false;
    }
  }, []);


  return (
    <VideoProviderContext.Provider
      value={{
        videoRef,
        playVideo,
        setIdleVideoSource,
      }}
    >
      {children}
    </VideoProviderContext.Provider>
  );
};
