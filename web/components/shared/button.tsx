import React from 'react';

interface ButtonComponentProps {
  text: string;
  onClick: () => void;
  type: 'button' | 'submit' | 'reset' | undefined;
  extraClasses?: string;
}

const ButtonComponent: React.FC<ButtonComponentProps> = ({ text, onClick, type, extraClasses }) => {
  var classesVal = "bg-transparent hover:bg-slate-500 text-slate-100 font-semibold hover:text-white py-2 px-4 border border-slate-100 hover:border-transparent rounded";
  if (extraClasses !== undefined) {
    classesVal += " " + extraClasses;
  }
  return (
    <button type={type} className={ classesVal } onClick={onClick}>
      { text }
    </button>
  );
};

export default ButtonComponent;
