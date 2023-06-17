// pages/api/completions.ts
import { NextResponse } from 'next/server';
import api_url from '@/components/shared/api';

export async function POST(request: Request) {
  const requestHeaders: HeadersInit = new Headers();
  requestHeaders.set('Content-Type', 'application/json');
  if (!process.env.DATA_API_KEY) { 
    return NextResponse.json({"error": "Invalid API Key"});
  }
  requestHeaders.set('API-Key', process.env.DATA_API_KEY);  

  const requestBody = await request.json();
  const res = await fetch(`${api_url}/v1/completions`, {
    method: 'POST',
    headers: requestHeaders,
    body: JSON.stringify(requestBody),
  });
  return res;
}