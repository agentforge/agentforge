import axios from 'axios';
import config from '../config/config';

export const api_url = `http://${config.host}:${config.port}`;
console.log(api_url);

const api = axios.create({
  baseURL: api_url,
  withCredentials: true, // Enable cross-site requests
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
