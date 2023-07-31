import React, { createContext, useContext, useRef, useState, useEffect } from 'react';

interface VideoProviderContextValue {
  videoRef: React.RefObject<HTMLVideoElement>;
  playVideo: (videoSrc: string) => void;
  setIdleVideoSource: (videoSrc: string) => void;
  playCurrentIdleVideo: () => void;
  stopPlaying: () => void;
  setOnVideoEnd: (callback: () => void) => void;
  onVideoEnd: (() => void) | null;
  videoPlaying: React.RefObject<boolean>;
  idleVideoSource: string;
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
  const [onVideoEnd, setOnVideoEnd] = useState<(() => void) | null>(null);
  var videoPlaying = useRef(false);

  const stopPlaying = () => { 
    videoPlaying.current = false;
  }

  const playVideo = (videoSrc: string) => {
    if (videoRef.current) {
      videoRef.current.src = videoSrc;
      videoRef.current.autoplay = false; // Disable autoplay
      videoPlaying.current = true; 
      videoRef.current.play().catch(error => {
        console.log('Error occurred while playing video:', error);
      });
    }
  };

  const setIdleVideoSourceVideo = (videoSrc: string) => {
    if (videoRef.current) {
      videoRef.current.src = videoSrc;
      videoRef.current.play().catch(error => {
        console.log('Error occurred while playing video:', error);
      });
      videoPlaying.current = false; 
    }
  };

  const playCurrentIdleVideo = () => {
    if (videoRef.current) {
      videoRef.current.src = idleVideoSource;
      videoRef.current.loop = true; 
      videoRef.current.muted = true; 
      videoRef.current.play().catch(error => {
        console.log('Error occurred while playing video:', error);
      });
      videoPlaying.current = false; 
    }
  };

  useEffect(() => {
    const videoElement = videoRef.current;
    
    const handleCanPlayThrough = () => {
        if (videoRef.current) {
            videoRef.current.play();
        }
    };

    if (videoElement) {
        videoElement.addEventListener('canplaythrough', handleCanPlayThrough);
    }

    return () => {
        if (videoElement) {
            videoElement.removeEventListener('canplaythrough', handleCanPlayThrough);
        }
    };
}, [idleVideoSource]);

  useEffect(() => {
    setIdleVideoSourceVideo(defaultIdleVideoSource);
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
        playCurrentIdleVideo, // Add this line
        setOnVideoEnd,
        stopPlaying,
        onVideoEnd,
        videoPlaying,
        idleVideoSource,
      }}
    >
      {children}
    </VideoProviderContext.Provider>
  );
};
