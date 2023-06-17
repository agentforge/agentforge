// pages/api/completions.ts
import { NextResponse } from 'next/server';
import api_url from '@/components/shared/api';

export async function POST(request: Request) {
  const requestBody = await request.json();
  const res = await fetch(`${api_url}/v1/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-API-KEY': process.env.DATA_API_KEY,
    },
    body: JSON.stringify(requestBody),
  });
  return res;
}