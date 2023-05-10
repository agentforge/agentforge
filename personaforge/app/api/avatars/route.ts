// pages/api/avatars.ts
import { NextResponse } from 'next/server';
import api_url from '@/components/shared/api';

export async function GET() {
  const res = await fetch(`${api_url}/v1/avatars`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      // 'API-Key': process.env.DATA_API_KEY,
    }
  });
  console.log(res);
  const data = await res.json();
 
  return NextResponse.json(data);
}