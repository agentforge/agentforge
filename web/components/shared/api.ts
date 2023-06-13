const config = {
  // host: `${host}`,
  // host: '68.0.117.107',
  // host: 'agent',
  host: process.env.API_HOST || '192.168.1.140',
  port: process.env.API_PORT || 3000,
};

export const api_url = `http://${config.host}:${config.port}`;

export default api_url;
