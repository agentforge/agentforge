import React from 'react';

const Gutter: React.FC = () => {

  // Return component JSX with ref attributes
  return (
    <>
    <div className="col-2 secondary-control">
      <div className="container">
        <ul
          className="thought-history"
          style={{ maxHeight: '500px', overflow: 'scroll', fontSize: '10px' }}
        ></ul>
      </div>
    </div>  
    </>
  );
};

export default Gutter;