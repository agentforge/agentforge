// AudioRecorder.tsx

import React, { useState, useRef, useContext } from 'react';
// import { pipeline } from '@xenova/transformers';
import { AudioRecorderContext } from '@/components/shared/context/audioprovider';

const AudioRecorder: React.FC = () => {
    const [isRecording, setIsRecording] = useState(false);
    const mediaRecorder = useRef<MediaRecorder | null>(null);
    const audioChunks = useRef<Blob[]>([]);

    const { setTranscription } = useContext(AudioRecorderContext);

    const handleStartRecording = async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder.current = new MediaRecorder(stream);
        mediaRecorder.current.ondataavailable = (event) => {
            audioChunks.current.push(event.data);
        };
        mediaRecorder.current.onstop = handleTranscription;
        mediaRecorder.current.start();
        setIsRecording(true);
    };

    const handleStopRecording = () => {
        if (mediaRecorder.current) {
            mediaRecorder.current.stop();
            setIsRecording(false);
        }
    };

    const handleTranscription = async () => {
        const audioBlob = new Blob(audioChunks.current, { type: 'audio/wav' });
        const transcriber = await pipeline('automatic-speech-recognition', 'Xenova/whisper-tiny.en');
        const output = await transcriber(audioBlob);
        setTranscription(output.text);
    };

    return (
        <button onClick={isRecording ? handleStopRecording : handleStartRecording}>
            {isRecording ? 'Stop Recording' : 'Start Recording'}
        </button>
    );
};

export default AudioRecorder;
