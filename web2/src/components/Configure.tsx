import React, { useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Row, Col, Form, Button } from 'react-bootstrap';
import axios from 'axios';
import config from '../config/config';

interface ConfigureProps {}

const Configure: React.FC<ConfigureProps> = () => {
  const navigate = useNavigate();
  const emailRef = useRef<HTMLInputElement>(null);
  const usernameRef = useRef<HTMLInputElement>(null);

  interface Configuration {
    email: string;
    username: string;
  }

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

  const getConfiguration = async (): Promise<Configuration> => {
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

  const setConfiguration = async (userConfig: Configuration) => {
    try {
      const response = await axios.post(`${config.host}:${config.port}/v1/configure`, {
        token: localStorage.getItem('token'),
        config: getLocalConfiguration(),
      });
      localStorage.setItem('token', response.data.token);
      navigate('/');
    } catch (error) {
      console.error(error);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const config = getLocalConfiguration();
    setConfiguration(config);
  };

  useEffect(() => {
    const fetchAndSetConfiguration = async () => {
      const config = await getConfiguration();
      setLocalConfiguration(config);
    };
    fetchAndSetConfiguration();
  }, []);

  return (
    <div className="row">
      <div className="col interaction main-control">
        <Container>
          <Form onSubmit={handleSubmit}>
            <Row>
              <Col md={6}>
                <Form.Group controlId="userEmail">
                  <Form.Label>User Email</Form.Label>
                  <Form.Control type="email" readOnly ref={emailRef} />
                </Form.Group>
              </Col>
              <Col md={6}>
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
