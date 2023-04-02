import React, { useState, useEffect, useRef } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRocket } from '@fortawesome/free-solid-svg-icons';
import { Button } from 'react-bootstrap';


const Agent: React.FC = () => {

  // Return component JSX with ref attributes
  return (
    <>
      <div className="col-8 interaction">
        <div style={{ marginTop: '32px', width: '100%', height: '100%' }}>
          <div style={{ paddingLeft: '18%', paddingRight: '18%' }}>
            <div className="chat-widget">
              <ul
                className="no-bullets chat-history"
                style={{ maxHeight: '500px', overflow: 'scroll' }}
              ></ul>
              <div id="chat-input" className="row">
                <div className="col-9">
                  <textarea
                    id="user-input"
                    className="form-control"
                    rows={4}
                    style={{ width: '100%' }}
                  ></textarea>
                </div>
                <div className="col-3">
                  <Button id="send-message" className="btn btn-main">
                    <FontAwesomeIcon icon={faRocket} />
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Agent;
