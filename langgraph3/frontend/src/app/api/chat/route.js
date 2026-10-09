import { NextResponse } from 'next/server';

export async function POST(req) {
  try {
    const { messages } = await req.json();

    // Here you can add your chat logic
    // For now, we'll just echo back the last message
    const lastMessage = messages[messages.length - 1];
    
    return NextResponse.json({
      role: 'assistant',
      content: `I received your message: ${lastMessage.content}. How can I help you with the hiring process?`
    });
  } catch (error) {
    console.error('Chat API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
} 