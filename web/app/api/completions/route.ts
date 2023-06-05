// pages/api/completions.ts
import { NextResponse } from 'next/server';
import api_url from '@/components/shared/api';

export async function POST(request: Request) {
  console.log(request);
  const requestBody = await request.json();
  const res = await fetch(`${api_url}/v1/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // 'API-Key': process.env.DATA_API_KEY,
    },
    body: JSON.stringify(requestBody),
  });
  console.log(res);
  // const data = await res.json();
 
  return res;
}