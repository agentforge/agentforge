import React, { useState, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios';
import config from '../config/config';

interface LoginProps {
  setIsLoggedIn?: React.Dispatch<React.SetStateAction<boolean>>;
}

const Login: React.FC<LoginProps> = ({ setIsLoggedIn }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e: FormEvent) => {
    try {
      e.preventDefault();
      const response = await axios.post(`${config.host}:${config.port}/login`, {
        username,
        password,
      });
      localStorage.setItem('token', response.data.token);
      setIsLoggedIn && setIsLoggedIn(true); // Set isLoggedIn to true
      navigate('/');
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="login">
      <div className="form-container">
        <h1 className="text-center mb-4">Login</h1>
        <Form onSubmit={handleLogin}>
          <Form.Group controlId="username">
            <Form.Label>Username:</Form.Label>
            <Form.Control type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
          </Form.Group>
          <Form.Group controlId="password">
            <Form.Label>Password:</Form.Label>
            <Form.Control type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          </Form.Group>
          <Button variant="primary" type="submit" className="d-block w-100">
            Login
          </Button>
        </Form>
      </div>
    </div>
  );
};

export default Login;
