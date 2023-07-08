import { NextResponse } from 'next/server';
import { api_url } from '@/components/shared/api';

export async function GET(
  requestPromise: Request,
  {
    params,
  }: {
    params: { user_id: string };
  },
) {
  const user_id = params.user_id; // user_id
  const res = await fetch(`${api_url}/v1/user/${user_id}/model-profiles`, {
    headers: {
      'Content-Type': 'application/json',
      // 'API-Key': process.env.DATA_API_KEY,
    },
  });
  const data = await res.json();
  return NextResponse.json(data);
}
