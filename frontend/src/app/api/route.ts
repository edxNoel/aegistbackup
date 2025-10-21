import { NextRequest, NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({ 
    message: "AEGIS Stock Investigation API", 
    status: "healthy",
    timestamp: new Date().toISOString(),
    langchain_enabled: true 
  });
}

export async function POST() {
  return NextResponse.json({ 
    message: "AEGIS API is running", 
    methods: ["GET", "POST"],
    endpoints: [
      "/api/health",
      "/api/validate-stock", 
      "/api/investigate",
      "/api/langchain-demo"
    ]
  });
}