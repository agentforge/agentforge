// Error.tsx
import React from 'react';

interface ErrorMessageProps {
  errorState: boolean;
  errorValue: string;
  closeError: () => void;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ errorState, errorValue, closeError }) => {
  return (
    <>
      <div className={`error-modal ${errorState ? '' : 'hidden'}`} id="errorModal">
        <div className="error-modal-content">
          <p className="modal-text">{errorValue}</p>
          <button onClick={closeError}>Close</button>
        </div>
      </div>
    </>
  );
};

export default ErrorMessage;
