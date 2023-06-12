// AudioRecorderContext.tsx

import React, { createContext, useState, ReactNode } from 'react';

interface AudioRecorderContextProps {
    transcription: string;
    setTranscription: React.Dispatch<React.SetStateAction<string>>;
}

export const AudioRecorderContext = createContext<AudioRecorderContextProps>({
    transcription: '',
    setTranscription: () => {},
});

interface AudioRecorderProviderProps {
    children: ReactNode;
}

export const AudioRecorderProvider: React.FC<AudioRecorderProviderProps> = ({ children }) => {
    const [transcription, setTranscription] = useState('');

    return (
        <AudioRecorderContext.Provider value={{ transcription, setTranscription }}>
            {children}
        </AudioRecorderContext.Provider>
    );
};
