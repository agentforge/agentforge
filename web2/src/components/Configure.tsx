import React, { useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Row, Col, Form, Button } from 'react-bootstrap';
import axios from 'axios';
import config from '../config/config';

interface ConfigureProps {}

export interface Configuration {
  email: string;
  username: string;
}

// Grabs the configuration JSON for the User from the DB backend
export const getConfiguration = async (): Promise<Configuration> => {
  const defaultConfig: Configuration = {
    email: 'user@email.com',
    username: 'username',
  };
  try {
    const response = await axios.get(`${config.host}:${config.port}/v1/configure`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    });
    const retConfig: Configuration = {
      email: response.data.email,
      username: response.data.username,
    };
    return retConfig;
  } catch (error) {
    console.error(error);
    return defaultConfig;
  }
};

const Configure: React.FC<ConfigureProps> = () => {
  const emailRef = useRef<HTMLInputElement>(null);
  const usernameRef = useRef<HTMLInputElement>(null);

  //Grabs local configuration data
  const getLocalConfiguration = (): Configuration => {
    const email = emailRef.current?.value || '';
    const username = usernameRef.current?.value || '';
    return { email, username };
  };

  const setLocalConfiguration = (config: Configuration) => {
    if (emailRef.current) emailRef.current.value = config.email;
    if (usernameRef.current) usernameRef.current.value = config.username;
  };

  const setConfiguration = async (userConfig: Configuration) => {
    try {
      const response = await axios.post(`${config.host}:${config.port}/v1/configure`, {
        token: localStorage.getItem('token'),
        config: getLocalConfiguration(),
      });
      return { err: false };
    } catch (error) {
      console.error(error);
      return { err: true };
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const config = getLocalConfiguration();
    const res = setConfiguration(config);
    res.then((data) => {
      if (data.err) {
        //report error to Notification
      } else {
        // report success to Notification
      }
    });
  };

  useEffect(() => {
    const fetchAndSetConfiguration = async () => {
      const config = await getConfiguration();
      setLocalConfiguration(config);
    };
    fetchAndSetConfiguration();
  }, []);

  return (
    <div className="row form-interactor">
      <div className="col interaction main-control">
        <Container>
          <h2>Configuration For the Agent Playground</h2>
          <Form onSubmit={handleSubmit}>
            <Row>
              <Col md={4}>
                <Form.Group controlId="userEmail">
                  <Form.Label>User Email</Form.Label>
                  <Form.Control type="email" ref={emailRef} />
                </Form.Group>
              </Col>
            </Row>
            <Row>
              <Col md={4}>
                <Form.Group controlId="username">
                  <Form.Label>Username</Form.Label>
                  <Form.Control type="text" ref={usernameRef} />
                </Form.Group>
              </Col>
            </Row>
            <Button type="submit">Save</Button>
          </Form>
        </Container>
      </div>
    </div>
  );
};

export default Configure;
