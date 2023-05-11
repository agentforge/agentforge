import React from 'react';

interface ButtonComponentProps {
  text: string;
  onClick: () => void;
}

const ButtonComponent: React.FC<ButtonComponentProps> = ({ text, onClick }) => {
  return (
    <button className="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded" onClick={onClick}>
      { text }
    </button>
  );
};

export default ButtonComponent;
