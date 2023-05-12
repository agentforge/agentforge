// VideoComponent.tsx
import React, { useRef, useEffect } from 'react';
import { useVideo } from '@/components/shared/context/videoprovider'
import { useLanguageModelConfig } from '@/components/shared/context/languagemodelconfigcontext';
import { useAvatarProvider } from '@/components/shared/context/avatarcontextprovider';

const VideoComponent: React.FC = () => {
  const { videoARef, videoBRef, switchVideo, playVideo, pauseVideo, isPlaying } = useVideo();
  const { languageModelConfigs } = useLanguageModelConfig();
  const { getAvatarData } = useAvatarProvider();

  const getVideoRef = () => {
    const av_id = languageModelConfigs["avatar"] as string;
    const avatarData = getAvatarData(av_id);
    if (!avatarData) return "default.mp4";
    return avatarData["mp4"];
  }

  const handleTimeUpdate = (videoRef: React.RefObject<HTMLVideoElement>) => {
    if (!videoRef.current) return;
    const timeRemaining = videoRef.current.duration - videoRef.current.currentTime;
    if (timeRemaining < 0.1) {
      switchVideo(`/videos/${getVideoRef()}`);
    }
  };

  // Initialize first video
  useEffect(() => {
    switchVideo(`/videos/${getVideoRef()}`);
  }, [languageModelConfigs]);

  return (
    <div id="hero-video-wrapper">
      <div className="relative">
        <video
          id="videoA"
          className="hero-video"
          ref={videoARef}
          preload="auto"
          autoPlay={isPlaying}
          style={{ display: 'none' }}
          onTimeUpdate={() => handleTimeUpdate(videoARef)}
        />
        <video
          id="videoB"
          className="hero-video"
          ref={videoBRef}
          preload="auto"
          autoPlay={isPlaying}
          style={{ display: 'none' }}
          onTimeUpdate={() => handleTimeUpdate(videoBRef)}
        />
      </div>
    </div>
  );
};

export default VideoComponent;
