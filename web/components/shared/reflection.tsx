import React from 'react';

export type ReflectionProps = {
  id: string;
  text: string;
  type: string;
};

const Message: React.FC<ReflectionProps> = ({ id, text, type }) => {
  // Return component JSX with ref attributes
  return (
    <li key={id} className={type}>
      Test: <b>{type}: </b> {text}
    </li>
  );
};

export default Message;
