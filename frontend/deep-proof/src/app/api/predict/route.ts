import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const videoFile = formData.get('video') as Blob;

    if (!(videoFile instanceof Blob)) {
      console.error("No video file provided or not of type Blob");
      return NextResponse.json({ error: 'No video file provided' }, { status: 400 });
    }

    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Flask response error:", errorText);
      return NextResponse.json({ error: errorText }, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error("Error forwarding request:", error);
    return NextResponse.json({ error: 'An error occurred' }, { status: 500 });
  }
}
