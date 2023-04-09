import React, { useState } from 'react';
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMicrophone, faStopCircle } from '@fortawesome/free-solid-svg-icons';

const AudioRecorder: React.FC = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
  const [audioChunks, setAudioChunks] = useState<Blob[]>([]);

  const processAudioBlob = async (audioBlob: Blob) => {
    // Send the axios POST request
    const formData = new FormData();
    formData.append('audio', audioBlob);
    const response = await axios.post('/v1/whisper', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    // Display or process the generated_text
    console.log(response.data.generated_text);
  };

  const startRecording = async () => {
    setIsRecording(true);

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);

      recorder.addEventListener('dataavailable', (event: BlobEvent) => {
        setAudioChunks((prevChunks) => [...prevChunks, event.data]);
      });

      recorder.addEventListener('stop', () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        // Process the audioBlob after recording stops
        processAudioBlob(audioBlob);
      });

      recorder.start();
      setMediaRecorder(recorder);
    } catch (error) {
      console.error('Error while accessing the microphone:', error);
      setIsRecording(false);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
    }
    setIsRecording(false);
  };

  return (
    <div style={{ marginTop: '10px' }}>
      <button className="btn btn-main btn-primary" onClick={isRecording ? stopRecording : startRecording}>
        <FontAwesomeIcon icon={isRecording ? faStopCircle : faMicrophone} />
      </button>
    </div>
  );
};

export default AudioRecorder;
