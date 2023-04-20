import React from 'react';

export type MessageProps = {
  id: string;
  author_type: string;
  author: string;
  text: string;
  error: boolean;
};

const Message: React.FC<MessageProps> = ({ id, author_type, author, text }) => {
  // Return component JSX with ref attributes
  return (
    <li key={id} className={author_type}>
      {author}: {text}
    </li>
  );
};

export default Message;
