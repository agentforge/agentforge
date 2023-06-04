'use client';
// VideoComponent.tsx
import React, { useEffect } from 'react';
import { useVideo } from '@/components/shared/context/videoprovider'
import { useModelProfileConfig } from '@/components/shared/context/modelprofileconfig';
import { useAvatarProvider } from '@/components/shared/context/avatarcontextprovider';

const VideoComponent: React.FC = () => {
  const { videoARef, videoBRef, switchVideo, playVideo, pauseVideo, isPlaying } = useVideo();
  const { modelProfileConfigs } = useModelProfileConfig();
  const { getAvatarData } = useAvatarProvider();

  const getVideoRef = () => {
    const av_id = modelProfileConfigs["avatar"] as string;
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

  // // Initialize first video
  useEffect(() => {
    switchVideo(`/videos/${getVideoRef()}`);
  }, [modelProfileConfigs]);

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
