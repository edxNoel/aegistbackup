import { NextRequest, NextResponse } from 'next/server';

export async function POST(
  request: NextRequest,
  { params }: { params: { symbol: string } }
) {
  try {
    const symbol = params.symbol.toUpperCase();
    
    // Simulate LangChain analysis with demo data
    const demoResponse = {
      symbol,
      langchain_analysis: {
        news_sentiment: {
          search_query: `${symbol} stock news recent price movement earnings`,
          sentiment_indicators: [
            "Positive: strong performance",
            "Positive: analyst upgrades", 
            "Neutral: market volatility"
          ],
          key_events: [
            "Event detected: earnings report",
            "Event detected: market trends"
          ],
          confidence_score: 7.5,
          investigation_type: "news_sentiment",
          timestamp: new Date().toISOString(),
          note: "Demo data - LangChain integration ready"
        },
        earnings_impact: {
          search_query: `${symbol} earnings report quarterly results analyst estimates guidance`,
          earnings_indicators: [
            "Earnings indicator: EPS beat",
            "Earnings indicator: revenue growth",
            "Earnings indicator: positive guidance"
          ],
          analyst_sentiment: [
            "Analyst activity: price target raised",
            "Analyst activity: rating upgrade",
            "Analyst activity: positive outlook"
          ],
          confidence_score: 8.0,
          investigation_type: "earnings_impact",
          timestamp: new Date().toISOString(),
          note: "Demo data - LangChain integration ready"
        },
        market_context: {
          search_query: `${symbol} sector performance market trends peer comparison industry analysis`,
          sector_trends: [
            "Sector trend: technology outperforming",
            "Sector trend: growth momentum",
            "Sector trend: market leadership"
          ],
          peer_performance: [
            "Peer comparison: outperforming competitors",
            "Peer comparison: market share gains",
            "Peer comparison: innovation advantage"
          ],
          confidence_score: 6.5,
          investigation_type: "market_context",
          timestamp: new Date().toISOString(),
          note: "Demo data - LangChain integration ready"
        }
      },
      demo_info: {
        description: "LangChain-powered investigation using DuckDuckGo search and AI analysis",
        features: [
          "Real-time web search for news and analysis",
          "Sentiment indicator extraction",
          "Earnings event detection", 
          "Sector trend analysis",
          "Peer comparison insights"
        ],
        confidence_scoring: "Each analysis includes confidence scores (0-10 scale)",
        search_integration: "Uses DuckDuckGo API for external data gathering",
        status: "Demo mode - full LangChain backend deployed and ready"
      },
      timestamp: new Date().toISOString()
    };

    return NextResponse.json(demoResponse);
    
  } catch (error) {
    console.error('LangChain demo error:', error);
    return NextResponse.json(
      { error: 'LangChain demo failed', details: String(error) },
      { status: 500 }
    );
  }
}