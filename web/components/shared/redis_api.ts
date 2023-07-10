const config = {
  // host: `${host}`,
  // host: '68.0.117.107',
  // host: 'agent',
  host: process.env.REDIS_HOST || '192.168.1.140',
  port: process.env.REDIS_PORT || 6379,
};

var redis_url = ''

if (config.port != undefined) {
  redis_url = `http://${config.host}:${config.port}`;
} else { 
  redis_url = `http://${config.host}`;
}

export default redis_url;
