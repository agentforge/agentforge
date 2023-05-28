import React from 'react';

interface MainProps { }

const features = [
  {
    title: "AgentForge",
    description:
      "Click Test Agent to test an existing agent or Configure to create/modifiy an existing agent"
  }];

const Main: React.FC<MainProps> = () => {

  return (
    <div className="md:block w-full h-full md:w-8/12">

      <div className="center-items justify-center text-center">
          {features.map(({ title, description }) => (
            <div key={title} className='text-white'>
              <h3 className="text-2xl font-bold">{title}</h3>
              <p>{description}</p>
            </div>
          ))}
      </div>
    </div>
  );
};

export default Main;