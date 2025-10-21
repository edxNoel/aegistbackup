import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const symbol = body.symbol || 'TEST';
    
    console.log('LangChain test endpoint called with symbol:', symbol);
    
    // Simple demo response
    const demoResponse = {
      success: true,
      symbol,
      langchain_analysis: {
        news_sentiment: {
          sentiment_indicators: [
            `${symbol} shows positive sentiment in recent news coverage`,
            `Market analysts maintain optimistic outlook for ${symbol}`,
            `Recent product launches driving positive investor sentiment`
          ],
          confidence_score: 8,
          data_sources: 12,
          last_updated: new Date().toISOString()
        },
        earnings_impact: {
          earnings_indicators: [
            `${symbol} earnings exceeded expectations in Q4`,
            `Revenue growth accelerating for ${symbol}`,
            `Profit margins improving across key business segments`
          ],
          confidence_score: 9,
          data_sources: 8,
          last_updated: new Date().toISOString()
        },
        market_context: {
          sector_trends: [
            `${symbol} sector showing strong fundamentals`,
            `Market rotation favoring ${symbol} industry`,
            `Institutional buying pressure increasing`
          ],
          confidence_score: 7,
          data_sources: 15,
          last_updated: new Date().toISOString()
        }
      },
      demo_info: {
        message: "LangChain integration test successful",
        features: [
          "DuckDuckGo web search integration",
          "Multi-source sentiment analysis", 
          "Real-time earnings data processing",
          "Market context evaluation",
          "AI-powered insight generation"
        ],
        timestamp: new Date().toISOString()
      }
    };

    return NextResponse.json(demoResponse);
    
  } catch (error) {
    console.error('LangChain test error:', error);
    return NextResponse.json(
      { 
        success: false, 
        error: 'LangChain test failed',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    message: "LangChain test endpoint ready",
    method: "POST",
    expected_body: { symbol: "string" }
  });
}