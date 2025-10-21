from typing import Dict, List, Any, Optional
import os
from langchain.agents import Tool
from langchain.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
import json
from datetime import datetime


class LangChainInvestigationService:
    """Enhanced investigation service using LangChain agents and tools"""
    
    def __init__(self):
        self.search_tool = self._create_search_tool()
        self.investigation_prompt = self._create_investigation_prompt()
        
    def _create_search_tool(self) -> Tool:
        """Create a search tool for gathering external information"""
        search = DuckDuckGoSearchRun(api_wrapper=DuckDuckGoSearchAPIWrapper())
        
        return Tool(
            name="search",
            description="Search for recent news, analysis, and information about stocks, companies, and market events. Use this to find relevant information about stock price movements, earnings, news, and market sentiment.",
            func=search.run
        )
    
    def _create_investigation_prompt(self) -> PromptTemplate:
        """Create a specialized prompt for stock investigation"""
        template = """
You are an expert financial analyst conducting a comprehensive investigation into stock price movements.

CONTEXT:
- Stock Symbol: {symbol}
- Price Change: {price_change}%
- Investigation Focus: {focus_area}
- Current Findings: {current_findings}

AVAILABLE TOOLS:
{tools}

INVESTIGATION METHODOLOGY:
1. Research recent news and events related to the company
2. Analyze market sentiment and analyst opinions
3. Investigate sector trends and peer comparisons
4. Examine earnings reports and financial metrics
5. Consider macroeconomic factors

INSTRUCTIONS:
- Use the search tool to gather relevant information
- Focus on the specific investigation area: {focus_area}
- Provide evidence-based insights
- Suggest follow-up investigation areas
- Rate confidence level (1-10) for each finding

Previous actions: {agent_scratchpad}

Question: {input}
"""
        return PromptTemplate(
            input_variables=["symbol", "price_change", "focus_area", "current_findings", "tools", "agent_scratchpad", "input"],
            template=template
        )
    
    async def investigate_news_sentiment(self, symbol: str, price_change: float) -> Dict[str, Any]:
        """Use LangChain to investigate news sentiment and its impact"""
        try:
            search_query = f"{symbol} stock news recent price movement earnings"
            search_results = self.search_tool.func(search_query)
            
            # Parse and analyze search results
            analysis = {
                "search_query": search_query,
                "raw_results": search_results[:500],  # Limit for API constraints
                "sentiment_indicators": self._extract_sentiment_indicators(search_results),
                "key_events": self._extract_key_events(search_results, symbol),
                "confidence_score": 7.5,  # Base confidence, can be enhanced
                "investigation_type": "news_sentiment",
                "timestamp": datetime.now().isoformat()
            }
            
            return analysis
            
        except Exception as e:
            print(f"Error in LangChain news sentiment investigation: {e}")
            # Return fallback demo data when search is rate-limited
            return {
                "search_query": f"{symbol} stock news recent price movement earnings",
                "raw_results": f"Demo results for {symbol} - LangChain would search for recent news, analyst reports, and market sentiment",
                "sentiment_indicators": [
                    "Positive: strong" if price_change > 0 else "Negative: decline",
                    "Positive: growth" if price_change > 2 else "Neutral: stable",
                    "Positive: outperform" if price_change > 5 else "Negative: underperform"
                ],
                "key_events": [
                    "Event detected: earnings",
                    "Event detected: analyst upgrade" if price_change > 0 else "Event detected: market volatility"
                ],
                "confidence_score": 7.5,
                "investigation_type": "news_sentiment",
                "timestamp": datetime.now().isoformat(),
                "note": "Demo data - Live search may be rate-limited",
                "error": str(e)
            }
    
    async def investigate_earnings_impact(self, symbol: str, price_change: float) -> Dict[str, Any]:
        """Use LangChain to investigate earnings-related price movements"""
        try:
            search_query = f"{symbol} earnings report quarterly results analyst estimates guidance"
            search_results = self.search_tool.func(search_query)
            
            analysis = {
                "search_query": search_query,
                "raw_results": search_results[:500],
                "earnings_indicators": self._extract_earnings_indicators(search_results),
                "analyst_sentiment": self._extract_analyst_sentiment(search_results),
                "confidence_score": 8.0,
                "investigation_type": "earnings_impact",
                "timestamp": datetime.now().isoformat()
            }
            
            return analysis
            
        except Exception as e:
            print(f"Error in LangChain earnings investigation: {e}")
            # Return fallback demo data
            return {
                "search_query": f"{symbol} earnings report quarterly results analyst estimates guidance",
                "raw_results": f"Demo results for {symbol} - LangChain would analyze earnings reports, analyst estimates, and guidance",
                "earnings_indicators": [
                    "Earnings indicator: EPS",
                    "Earnings indicator: revenue",
                    "Earnings indicator: beat" if price_change > 0 else "Earnings indicator: miss",
                    "Earnings indicator: guidance"
                ],
                "analyst_sentiment": [
                    "Analyst activity: rating",
                    "Analyst activity: upgrade" if price_change > 0 else "Analyst activity: downgrade",
                    "Analyst activity: price target"
                ],
                "confidence_score": 8.0,
                "investigation_type": "earnings_impact",
                "timestamp": datetime.now().isoformat(),
                "note": "Demo data - Live search may be rate-limited",
                "error": str(e)
            }
    
    async def investigate_market_context(self, symbol: str, price_change: float) -> Dict[str, Any]:
        """Use LangChain to investigate broader market context"""
        try:
            search_query = f"{symbol} sector performance market trends peer comparison industry analysis"
            search_results = self.search_tool.func(search_query)
            
            analysis = {
                "search_query": search_query,
                "raw_results": search_results[:500],
                "sector_trends": self._extract_sector_trends(search_results),
                "peer_performance": self._extract_peer_performance(search_results),
                "confidence_score": 6.5,
                "investigation_type": "market_context",
                "timestamp": datetime.now().isoformat()
            }
            
            return analysis
            
        except Exception as e:
            print(f"Error in LangChain market context investigation: {e}")
            # Return fallback demo data
            return {
                "search_query": f"{symbol} sector performance market trends peer comparison industry analysis",
                "raw_results": f"Demo results for {symbol} - LangChain would analyze sector trends, peer performance, and industry context",
                "sector_trends": [
                    "Sector trend: technology",
                    "Sector trend: growth" if price_change > 0 else "Sector trend: volatility",
                    "Sector trend: market share"
                ],
                "peer_performance": [
                    "Peer comparison: competitor",
                    "Peer comparison: outperform" if price_change > 0 else "Peer comparison: underperform",
                    "Peer comparison: market position"
                ],
                "confidence_score": 6.5,
                "investigation_type": "market_context",
                "timestamp": datetime.now().isoformat(),
                "note": "Demo data - Live search may be rate-limited",
                "error": str(e)
            }
    
    def _extract_sentiment_indicators(self, search_results: str) -> List[str]:
        """Extract sentiment indicators from search results"""
        positive_indicators = ["positive", "bullish", "upgrade", "beat", "strong", "growth", "outperform"]
        negative_indicators = ["negative", "bearish", "downgrade", "miss", "weak", "decline", "underperform"]
        
        found_indicators = []
        lower_results = search_results.lower()
        
        for indicator in positive_indicators:
            if indicator in lower_results:
                found_indicators.append(f"Positive: {indicator}")
        
        for indicator in negative_indicators:
            if indicator in lower_results:
                found_indicators.append(f"Negative: {indicator}")
        
        return found_indicators[:5]  # Limit to top 5
    
    def _extract_key_events(self, search_results: str, symbol: str) -> List[str]:
        """Extract key events from search results"""
        event_keywords = ["earnings", "acquisition", "merger", "partnership", "lawsuit", "FDA", "approval", "recall"]
        found_events = []
        
        lower_results = search_results.lower()
        for keyword in event_keywords:
            if keyword in lower_results:
                found_events.append(f"Event detected: {keyword}")
        
        return found_events[:3]  # Limit to top 3
    
    def _extract_earnings_indicators(self, search_results: str) -> List[str]:
        """Extract earnings-related indicators"""
        earnings_keywords = ["EPS", "revenue", "guidance", "forecast", "estimate", "beat", "miss", "inline"]
        found_indicators = []
        
        lower_results = search_results.lower()
        for keyword in earnings_keywords:
            if keyword in lower_results:
                found_indicators.append(f"Earnings indicator: {keyword}")
        
        return found_indicators[:4]
    
    def _extract_analyst_sentiment(self, search_results: str) -> List[str]:
        """Extract analyst sentiment indicators"""
        analyst_keywords = ["analyst", "rating", "price target", "recommendation", "upgrade", "downgrade"]
        found_sentiment = []
        
        lower_results = search_results.lower()
        for keyword in analyst_keywords:
            if keyword in lower_results:
                found_sentiment.append(f"Analyst activity: {keyword}")
        
        return found_sentiment[:3]
    
    def _extract_sector_trends(self, search_results: str) -> List[str]:
        """Extract sector trend indicators"""
        sector_keywords = ["sector", "industry", "peers", "competitors", "market share", "trend"]
        found_trends = []
        
        lower_results = search_results.lower()
        for keyword in sector_keywords:
            if keyword in lower_results:
                found_trends.append(f"Sector trend: {keyword}")
        
        return found_trends[:3]
    
    def _extract_peer_performance(self, search_results: str) -> List[str]:
        """Extract peer performance indicators"""
        peer_keywords = ["competitor", "peer", "versus", "compared to", "outperform", "underperform"]
        found_performance = []
        
        lower_results = search_results.lower()
        for keyword in peer_keywords:
            if keyword in lower_results:
                found_performance.append(f"Peer comparison: {keyword}")
        
        return found_performance[:3]