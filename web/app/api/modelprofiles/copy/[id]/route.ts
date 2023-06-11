// pages/api/avatars.ts
import { NextResponse } from 'next/server';
import api_url from '@/components/shared/api';

export async function POST(
  requestPromise: Request,
  {
    params,
  }: {
    params: { id: string };
  },
) {
    const id = params.id; // user_id
    const res = await fetch(`${api_url}/v1/model-profiles/copy/${id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // 'API-Key': process.env.DATA_API_KEY,
      },
    });
    const data = await res.json();
    return NextResponse.json(data);
}