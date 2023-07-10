import { NextApiRequest, NextApiResponse } from "next";
import Redis, { RedisOptions } from 'ioredis';
// import redis_url from '@/components/shared/redis_api';

const config = {
  // host: `${host}`,
  // host: '68.0.117.107',
  // host: 'agent',
  host: process.env.REDIS_HOST || '192.168.1.140',
  port: process.env.REDIS_PORT || '6379',
  password: undefined,
};

const options: RedisOptions = {
  host: config.host,
  lazyConnect: true,
  showFriendlyErrorStack: true,
  enableAutoPipelining: true,
  maxRetriesPerRequest: 0,
  retryStrategy: (times: number) => {
    if (times > 3) {
      throw new Error(`[Redis] Could not connect after ${times} attempts`);
    }

    return Math.min(times * 200, 1000);
  },
};

if (config.port) {
  options.port = parseInt(config.port);
}

if (config.password) {
  options.password = config.password;
}

const redis = new Redis(options);
const clients = new Map();

redis.subscribe('channel', (err, count) => {
  if (err) {
    console.error('Failed to subscribe', err);
    return;
  }
});

redis.on('message', (channel, message) => {
  for (const [_, writer] of Array.from(clients.entries())) {
    writer.write(new TextEncoder().encode("data: " + JSON.stringify({ channel, message }) + "\n\n"));
  }
});

redis.on('error', (err) => {
  console.error(err);
});


export async function GET(req: NextApiRequest, res: NextApiResponse) {
  let responseStream = new TransformStream();
  const writer = responseStream.writable.getWriter();
  let closed = false;

  clients.set(req, writer);

  // Periodically send a "heartbeat" message to detect if the client has disconnected
  const interval = setInterval(async () => {
    try {
      await writer.write(new TextEncoder().encode("\n"));
    } catch (err) {
      // If the write fails, the client has disconnected
      if (!closed) {
        writer.close();
        clients.delete(req);
        closed = true;
      }
      clearInterval(interval);
    }
  }, 1000);

  return new Response(responseStream.readable, {
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Content-Type": "text/event-stream; charset=utf-8",
      Connection: "keep-alive",
      "Cache-Control": "no-cache, no-transform",
      "X-Accel-Buffering": "no",
      "Content-Encoding": "none",
    },
  });
}


// export const config = {
//   runtime: "edge",
// };