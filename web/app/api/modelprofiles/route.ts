// pages/api/avatars.ts
import { NextResponse } from 'next/server';
import api_url from '@/components/shared/api';

export async function POST(
  requestPromise: Request,
  {}: {},
) {
  try {
    const request = await requestPromise.json();
    const res = await fetch(`${api_url}/v1/model-profiles/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // 'API-Key': process.env.DATA_API_KEY,
      },
      body: JSON.stringify(request.body),
    });
    const data = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ message: "Error creating model profiles.", status: 500 });
  }
}
