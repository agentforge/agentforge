// pages/api/avatars.ts
import { NextResponse } from 'next/server';
import api_url from '@/components/shared/api';

export async function GET(
  {
    params,
  }: {
    params: { user_id: string };
  },
) {
  const user_id = params.user_id; // user_id
  const res = await fetch(`${api_url}/v1/model-profiles/${user_id}`, {
    headers: {
      'Content-Type': 'application/json',
      // 'API-Key': process.env.DATA_API_KEY,
    },
  });
  const data = await res.json();
  return NextResponse.json(data);
}

export async function POST(
  requestPromise: Request,
  {
    params,
  }: {
    params: { user_id: string };
  },
) {
  const user_id = params.user_id; // user_id
  const request = await requestPromise.json();
  const res = await fetch(`${api_url}/v1/model-profiles/${user_id}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // 'API-Key': process.env.DATA_API_KEY,
    },
    body: JSON.stringify(request),
  });
  const data = await res.json();
  return NextResponse.json(data);
}