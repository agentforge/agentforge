const config = {
  // host: `${host}`,
  host: '192.168.1.140',
  // host: '68.0.117.107',
  // host: 'agent',
  port: 3000,
};

export const api_url = `http://${config.host}:${config.port}`;
console.log(api_url);

// const api = axios.create({
//   baseURL: api_url,
//   withCredentials: true, // Enable cross-site requests
//   headers: {
//     'Content-Type': 'application/json',
//   },
// });

export default api_url;
