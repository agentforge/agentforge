import React from 'react';

interface ButtonComponentProps {
  onClick: () => void;
  type: 'button' | 'submit' | 'reset' | undefined;
  children: React.ReactNode;
  extraClasses?: string;
}

const Button: React.FC<ButtonComponentProps> = ({ onClick, type, children, extraClasses }) => {
  var classesVal = "bg-transparent hover:bg-slate-500 text-slate-100 font-semibold hover:text-white py-2 px-4 border border-slate-100 hover:border-transparent rounded";
  if (extraClasses !== undefined) {
    classesVal += " " + extraClasses;children
  }
  return (
    <button type={type} className={ classesVal } onClick={onClick}>
      {children}
    </button>
  );
};

export default Button;
