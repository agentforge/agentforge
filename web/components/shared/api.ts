const config = {
  // host: `${host}`,
  // host: '68.0.117.107',
  // host: 'agent',
  host: process.env.API_HOST || '192.168.1.140',
  port: process.env.API_PORT || undefined,
  redis_host: process.env.REDIS_HOST || 'localhost',
  redis_port: process.env.REDIS_PORT || 6379,

};

export var api_port = ''
export var redis_port = ''

if (config.port != undefined) {
  api_port = `:${config.port}`
} else { 
  api_port = ''
}

if (config.redis_port != undefined) {
  redis_port = `:${config.redis_port}`
} else { 
  redis_port = ''
}

export const redis_url = `${config.redis_host}${redis_port}`
export const api_url = `${config.host}${api_port}`