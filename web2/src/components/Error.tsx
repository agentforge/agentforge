// Error.tsx
import React from 'react';

interface ErrorMessageProps {
  message: string;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ message }) => {
  return (
    <>
      <ul>
        <li>
          <div className="error-modal" id="errorModal">
            <div className="modal-content">
              <p className="modal-text">{message}</p>
            </div>
          </div>
        </li>
      </ul>
    </>
  );
};

export default ErrorMessage;
