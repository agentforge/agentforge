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
    
    const handleCanPlayThrough = () => {
        if (videoRef.current) {
            videoRef.current.play();
        }
    };
    
    const handleEnded = () => {
        if (videoRef.current) {
            videoRef.current.src = idleVideoSource;
            // Remove the play() call here, because we want to wait for canplaythrough
        }
    };

    if (videoElement) {
        // Listen for the canplaythrough event to know when we can safely play the video
        videoElement.addEventListener('canplaythrough', handleCanPlayThrough);

        // Listen for the ended event to know when to change the source
        videoElement.addEventListener('ended', handleEnded);
    }

    // Clean up the event listeners when the component unmounts
    return () => {
        if (videoElement) {
            videoElement.removeEventListener('canplaythrough', handleCanPlayThrough);
            videoElement.removeEventListener('ended', handleEnded);
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
