import React from 'react';
import ChatWidget from '@/components/shared/chatwidget';
import ErrorMessage from '@/components/shared/error';
interface MainProps {}

const Main: React.FC<MainProps> = () => {

//TODO Fix error handling, use a react context provider
// err handling
// const [errorState, setErrorState] = useState(false);
// const [errorValue, setErrorValue] = useState('');
// const closeError = () => {
//   setErrorState(false);
//   setErrorValue('');
// };

// const openError = (error: any) => {
//   setErrorState(true);
//   setErrorValue(error);
// };

// const errMessage = async (error: string) => {
//   openError(`You have encountered a problem. Please contact support. Error message ${error}`);
// };

  return (
    <div className="px-18%">
      <ChatWidget />
      <div>
        {/* <ErrorMessage errorState={errorState} errorValue={errorValue} closeError={closeError} /> */}
      </div>
    </div>
  );
};

export default Main;