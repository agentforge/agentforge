// pages/api/completions.ts
import type { NextApiRequest, NextApiResponse } from 'next';

async function callCompletionsAPI(prompt: string, languageModelConfig: object) {
  const res = await fetch('https://your-completions-api-url', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // 'API-Key': process.env.DATA_API_KEY,// TODO: Add API key
    },
    body: JSON.stringify({ prompt, ...languageModelConfig }),
  });

  const data = await res.json();
  return data;
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    const { prompt, languageModelConfig } = req.body;
    try {
      const data = await callCompletionsAPI(prompt, languageModelConfig);
      res.status(200).json(data);
    } catch (error) {
      res.status(500).json({ error: 'Error calling completions API' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
