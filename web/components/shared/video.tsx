'use client';
// VideoComponent.tsx
import React, { useEffect } from 'react';
import { useVideo } from '@/components/shared/context/videoprovider'
import { useModelProfileConfig } from '@/components/shared/context/modelprofileconfig';
import { useAvatarProvider } from '@/components/shared/context/avatarcontextprovider';

const VideoComponent: React.FC = () => {
  const { playVideo, setIdleVideoSource } = useVideo();
  const { modelProfileConfigs } = useModelProfileConfig();
  const { getAvatarData } = useAvatarProvider();
  const { isStreaming, idleVideoRef, streamVideoRef } = useVideo();

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
      playVideo(`/videos/${getVideoRef()}`);
    }
  };

  // // Initialize first video
  useEffect(() => {
    setIdleVideoSource(`/videos/${getVideoRef()}`);
  }, []);

  return (
    <div className="video-container">
      <video ref={idleVideoRef} loop autoPlay className="video"></video>
      <video ref={streamVideoRef} className={`video ${isStreaming ? 'active' : ''}`}></video>
    </div>
  );
};

export default VideoComponent;
