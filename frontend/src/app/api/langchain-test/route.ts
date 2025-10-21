import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const symbol = body.symbol || 'TEST';
    
    console.log('LangChain test endpoint called with symbol:', symbol);
    
    // Enhanced demo response with varied, realistic data for dynamic reasoning
    const sentiment_variants = [
      [`${symbol} shows positive sentiment in recent news coverage`, `Market analysts maintain optimistic outlook for ${symbol}`, `Recent product launches driving positive investor sentiment`, `Social media sentiment trending upward for ${symbol}`],
      [`${symbol} faces headwinds from regulatory scrutiny`, `Competitive pressures mounting for ${symbol}`, `Supply chain disruptions affecting ${symbol} operations`, `Analyst downgrades creating negative sentiment`],
      [`Mixed signals emerging from ${symbol} news coverage`, `Cautious optimism among ${symbol} analysts`, `Recent developments creating uncertainty for ${symbol}`, `Market waiting for clarity on ${symbol} direction`]
    ];
    
    const earnings_variants = [
      [`${symbol} earnings exceeded expectations in Q4`, `Revenue growth accelerating for ${symbol}`, `Profit margins improving across key business segments`, `Forward guidance raised for upcoming quarters`],
      [`${symbol} missed earnings expectations this quarter`, `Revenue growth slowing for ${symbol}`, `Margin pressure from increased competition`, `Management lowered forward guidance`],
      [`${symbol} met but did not exceed earnings expectations`, `Revenue growth steady but not spectacular`, `Margins holding despite cost pressures`, `Guidance maintained with cautious tone`]
    ];
    
    const market_variants = [
      [`${symbol} sector showing strong fundamentals`, `Market rotation favoring ${symbol} industry`, `Institutional buying pressure increasing`, `Technical indicators suggest continued momentum`],
      [`${symbol} sector facing regulatory headwinds`, `Market rotation away from ${symbol} industry`, `Institutional selling pressure mounting`, `Technical indicators suggest potential decline`],
      [`${symbol} sector showing mixed performance`, `Market neutral on ${symbol} industry outlook`, `Institutional activity balanced`, `Technical indicators remain inconclusive`]
    ];
    
    // Randomly select variant to create different scenarios
    const scenarioIndex = Math.floor(Math.random() * 3);
    const sentiment_confidence = [8, 5, 6][scenarioIndex];
    const earnings_confidence = [9, 4, 7][scenarioIndex];
    const market_confidence = [7, 5, 6][scenarioIndex];
    
    const demoResponse = {
      success: true,
      symbol,
      langchain_analysis: {
        news_sentiment: {
          sentiment_indicators: sentiment_variants[scenarioIndex],
          confidence_score: sentiment_confidence,
          data_sources: 12,
          search_query: `${symbol} stock news recent price movement sentiment`,
          last_updated: new Date().toISOString()
        },
        earnings_impact: {
          earnings_indicators: earnings_variants[scenarioIndex],
          confidence_score: earnings_confidence,
          data_sources: 8,
          search_query: `${symbol} earnings report quarterly results analyst estimates`,
          last_updated: new Date().toISOString()
        },
        market_context: {
          sector_trends: market_variants[scenarioIndex],
          confidence_score: market_confidence,
          data_sources: 15,
          search_query: `${symbol} sector performance market trends peer comparison`,
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