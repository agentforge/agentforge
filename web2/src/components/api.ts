import axios from 'axios';
import config from '../config/config';

const api = axios.create({
  baseURL: `https://${config.host}:${config.port}/`,
});

export default api;
