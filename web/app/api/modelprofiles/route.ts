// pages/api/avatars.ts
import { NextResponse } from 'next/server';
import api_url from '@/components/shared/api';

export async function POST(
  requestPromise: Request,
  {}: {},
) {
  const requestHeaders: HeadersInit = new Headers();
  requestHeaders.set('Content-Type', 'application/json');
  if (!process.env.DATA_API_KEY) { 
    return NextResponse.json({"error": "Invalid API Key"});
  }
  requestHeaders.set('API-Key', process.env.DATA_API_KEY);  

  const request = await requestPromise.json();
  console.log(request);
    const res = await fetch(`${api_url}/v1/model-profiles`, {
      method: 'POST',
      headers: requestHeaders,
      body: JSON.stringify(request),
    });
  const data = await res.json();
  console.log(data)
  return NextResponse.json(data);
}
