// VideoProviderContext.tsx
import React, { createContext, useContext, useEffect, useState, useRef } from 'react';
import { AvatarData } from '@/components/shared/context/avatarcontextprovider'
import { api_url } from '@/components/shared/api';

interface VideoProviderContextValue {
  videoARef: React.RefObject<HTMLVideoElement>;
  videoBRef: React.RefObject<HTMLVideoElement>;
  playVideo: (text: string, avatar: AvatarData | undefined) => Promise<Blob>
  renderVideo: (blob: Blob | undefined, videoSrc: string | undefined, defaultUrl: string) => void;
  pauseVideo: (videoRef: React.RefObject<HTMLVideoElement>) => void;
  switchVideo: (videoSrc: string) => void;
  isPlaying: boolean;
}

const VideoProviderContext = createContext<VideoProviderContextValue | undefined>(undefined);

export const useVideo = () => {
  const context = useContext(VideoProviderContext);
  if (!context) {
    throw new Error('useVideoProvider must be used within a VideoProvider');
  }
  return context;
};

interface VideoProviderProps {
  children: React.ReactNode;
}

export const VideoProvider: React.FC<VideoProviderProps> = ({ children }) => {
  const videoARef = useRef<HTMLVideoElement>(null);
  const videoBRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [currentVideo, setCurrentVideo] = useState<'videoA' | 'videoB'>('videoA');

  const playVideo = async (text: string, avatar: AvatarData | undefined) => {
    if (!avatar) {
      throw new Error('Avatar must be set to call TTS API');
    }
    const request = {
      "prompt": text,
      "avatar": avatar.avatar,
      "lipsync": true,
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
    renderVideo(blob, undefined, avatar.mp4);
  }

  // Play a video from blob or url -- setup the non-active video, load it, and play it.
  // Switch the reference to this video
  const renderVideo = async (blob: Blob | undefined, videoSrc: string | undefined, defaultUrl: string) => {
    const nextVideoRef = currentVideo === 'videoA' ? videoBRef : videoARef;
    const currentVideoRef = currentVideo === 'videoA' ? videoARef : videoBRef;

    const nextVideo = nextVideoRef.current;
    if (nextVideo) {
      if (videoSrc == undefined) {
        if (blob == undefined) {
          console.log('err: Must select url or blob.');
          return;
        }
        const videoUrl = URL.createObjectURL(blob);
        if (!nextVideo.src.includes(videoUrl)) {
          nextVideo.src = videoUrl;
        }
      } else {
        if (!nextVideo.src.includes(videoSrc)) {
          nextVideo.src = videoSrc;
        }
      }
      const playWhenLoaded = () => {
        if (currentVideoRef.current != null) {
          nextVideo.play();
          nextVideo.style.display = 'block';

          // // Hide prev video
          currentVideoRef.current.style.display = 'none';

          if (!currentVideoRef.current.src.includes(defaultUrl)) {
            currentVideoRef.current.src = defaultUrl;
          }
          currentVideoRef.current.pause();
          nextVideo.removeEventListener('canplaythrough', playWhenLoaded);
        }
      };
      nextVideo.addEventListener('canplaythrough', playWhenLoaded);
    }
  };

  const pauseVideo = (videoRef: React.RefObject<HTMLVideoElement>) => {
    if (videoRef.current) {
      videoRef.current.pause();
      setIsPlaying(false);
    }
  };

  // Switches between two video contexts for smooth transitions between
  // Video states allowing us to load tts videos and then discreetly reload loops
  const switchVideo = (videoSrc: string) => {
    setCurrentVideo((prevVideo) => (prevVideo === 'videoA' ? 'videoB' : 'videoA'));
    if (currentVideo === 'videoA') {
      if (videoARef.current) {
        if (!videoARef.current.src.includes(videoSrc)) {
          videoARef.current.src = videoSrc;
        }
        videoARef.current.currentTime = 0.1;

        const playWhenLoaded = () => {
          if (videoARef.current != null && videoBRef.current != null) {
            videoARef.current.style.display = 'block';
            videoARef.current.play();

            // Perform your specific action here
            videoBRef.current.style.display = 'none';
            // Manually loop the video
            videoBRef.current.currentTime = 0.1;
            if (!videoBRef.current.src.includes(videoSrc)) {
              videoBRef.current.src = videoSrc;
            }
            videoBRef.current.pause();
            videoARef.current.removeEventListener('canplaythrough', playWhenLoaded);
          }
        };
        videoARef.current.addEventListener('canplaythrough', playWhenLoaded);
      }
    } else {
      if (videoBRef.current) {
        if (!videoBRef.current.src.includes(videoSrc)) {
          videoBRef.current.src = videoSrc;
        }
        videoBRef.current.currentTime = 0.1;
        const playWhenLoaded = () => {
          if (videoBRef.current != null && videoARef.current != null) {
            videoBRef.current.style.display = 'block';
            videoBRef.current.play();

            // Perform your specific action here
            videoARef.current.style.display = 'none';
            // Manually loop the video
            videoARef.current.currentTime = 0.1;
            if (!videoARef.current.src.includes(videoSrc)) {
              videoARef.current.src = videoSrc;
            }
            videoARef.current.pause();
            videoBRef.current.removeEventListener('canplaythrough', playWhenLoaded);
          }
        };
        videoBRef.current.addEventListener('canplaythrough', playWhenLoaded);
      }
    }
  };

  useEffect(() => {
    const videoRefs = [videoARef, videoBRef];

    const handleEnded = (video: HTMLVideoElement) => {
      video.currentTime = 0;
      video.play();
    };

    for (const videoRef of videoRefs) {
      if (!videoRef.current) continue;
      const video = videoRef.current;

      if (isPlaying) {
        video.play();
        video.addEventListener('ended', () => handleEnded(video));
      } else {
        video.pause();
      }

      return () => {
        video.removeEventListener('ended', () => handleEnded(video));
      };
    }
  }, [videoARef, videoBRef, isPlaying]);

  return (
    <VideoProviderContext.Provider value={{ videoARef, videoBRef, switchVideo, playVideo, pauseVideo, isPlaying }}>
      {children}
    </VideoProviderContext.Provider>
  );
};
