// pages/api/avatars.ts
import { NextResponse } from 'next/server';
import api_url from '@/components/shared/api';

export async function PUT(
  requestPromise: Request,
  {
    params,
  }: {
    params: { id: string };
  },
) {
    const id = params.id; // user_id
    const request = await requestPromise.json();
    console.log(request);
    const res = await fetch(`${api_url}/v1/model-profiles/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        // 'API-Key': process.env.DATA_API_KEY,
      },
      body: JSON.stringify(request),
    });
    const data = await res.json();
    return NextResponse.json(data);
}

export async function GET(
  requestPromise: Request,
  {
    params,
  }: {
    params: { id: string };
  },
) {
    const id = params.id; // user_id
    const res = await fetch(`${api_url}/v1/model-profiles/${id}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        // 'API-Key': process.env.DATA_API_KEY,
      }
    });
    const data = await res.json();
    return NextResponse.json(data);
}

export async function DELETE(
  requestPromise: Request,
  {
    params,
  }: {
    params: { id: string };
  },
) {
    const id = params.id; // user_id
    const res = await fetch(`${api_url}/v1/model-profiles/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        // 'API-Key': process.env.DATA_API_KEY,
      }
    });
    const data = await res.json();
    return NextResponse.json(data);
}