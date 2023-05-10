// VideoComponent.tsx
import React, { useRef, useEffect } from 'react';
import { useVideoProvider } from '@/components/shared/context/videoprovidercontext'

const VideoComponent: React.FC = () => {
  const { videoARef, videoBRef, switchVideo, playVideo, pauseVideo, isPlaying } = useVideoProvider();

  const handleTimeUpdate = (videoRef: React.RefObject<HTMLVideoElement>) => {
    if (!videoRef.current) return;
    const timeRemaining = videoRef.current.duration - videoRef.current.currentTime;
    if (timeRemaining < 0.1) {
      switchVideo('/videos/default.mp4');
    }
  };

  // Initialize first video
  useEffect(() => {
    console.log("switching video");
    switchVideo('/videos/default.mp4');
  }, []);

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
