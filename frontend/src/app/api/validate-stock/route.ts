import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { symbol } = body;
    
    if (!symbol) {
      return NextResponse.json(
        { error: 'Symbol is required' },
        { status: 400 }
      );
    }
    
    const symbolUpper = symbol.toUpperCase();
    
    // Demo stock validation response
    const validationData = {
      symbol: symbolUpper,
      valid: true,
      current_price: Math.random() * 200 + 50, // Random price between 50-250
      change: (Math.random() - 0.5) * 10, // Random change between -5 to +5
      change_percent: `${((Math.random() - 0.5) * 10).toFixed(2)}%`,
      volume: Math.floor(Math.random() * 10000000) + 1000000, // Random volume
      market_cap: Math.floor(Math.random() * 1000000000000) + 100000000000, // Random market cap
      company_name: `${symbolUpper} Corporation`,
      sector: "Technology", // Default for demo
      timestamp: new Date().toISOString(),
      data_source: "demo_api",
      note: "Demo data - stock validation successful"
    };
    
    return NextResponse.json(validationData);
    
  } catch (error) {
    console.error('Stock validation error:', error);
    return NextResponse.json(
      { error: 'Stock validation failed', details: String(error) },
      { status: 500 }
    );
  }
}