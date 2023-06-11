'use client';
import React from 'react';
import ChatWidget from '@/components/shared/chatwidget';

interface ChatProps {
  params: Record<string, any>;
}

const Chat: React.FC<ChatProps> = ({ params }) => {
  return (
    <>
    <div className="md:block w-full h-full md:w-8/12">
        <ChatWidget id={ params.id } />
    </div>
    </>
)};

export default Chat;