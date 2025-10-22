import os
import json
import re
from typing import Dict, List, Any, Optional
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class ClaudeAIService:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"  # Latest Claude model
    
    def _parse_claude_json(self, content: str) -> Dict[str, Any]:
        """Robust JSON parsing for Claude responses"""
        try:
            # First, try direct parsing
            return json.loads(content)
        except json.JSONDecodeError:
            pass
        
        try:
            # Clean control characters except newlines and tabs
            cleaned_content = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', content)
            
            # Try to extract JSON from markdown code blocks
            json_patterns = [
                r'```json\s*(\{.*?\})\s*```',
                r'```\s*(\{.*?\})\s*```',
                r'(\{[^{}]*\{[^{}]*\}[^{}]*\})',  # Nested JSON
                r'(\{[^{}]+\})'  # Simple JSON
            ]
            
            for pattern in json_patterns:
                matches = re.findall(pattern, cleaned_content, re.DOTALL)
                if matches:
                    json_str = matches[0].strip()
                    try:
                        return json.loads(json_str)
                    except json.JSONDecodeError:
                        continue
            
            # If all else fails, try to manually extract key-value pairs
            result = {}
            key_patterns = [
                r'"executive_summary":\s*"([^"]*)"',
                r'"primary_cause":\s*"([^"]*)"',
                r'"detailed_reasoning":\s*"([^"]*)"',
                r'"confidence_score":\s*([0-9.]+)',
                r'"cause_confidence":\s*([0-9.]+)'
            ]
            
            for i, pattern in enumerate(key_patterns):
                match = re.search(pattern, cleaned_content)
                if match:
                    key = ["executive_summary", "primary_cause", "detailed_reasoning", "confidence_score", "cause_confidence"][i]
                    value = match.group(1)
                    if key in ["confidence_score", "cause_confidence"]:
                        result[key] = float(value)
                    else:
                        result[key] = value
            
            if result:
                return result
            
            raise ValueError("Could not parse JSON from Claude response")
            
        except Exception as e:
            print(f"JSON parsing error: {e}")
            print(f"Content preview: {content[:200]}...")
            raise
    
    async def analyze_price_movement(self, stock_data: Dict[str, Any], symbol: str) -> Dict[str, Any]:
        """Use Claude to analyze price movement based purely on data - no preset categories"""
        
        price_change = stock_data.get("price_change_percent", 0)
        current_price = stock_data.get("current_price", 0)
        volume = stock_data.get("volume", 0)
        
        prompt = f"""You are analyzing {symbol} stock movement. Here's what happened:

PRICE MOVEMENT: {price_change:.2f}%
CURRENT PRICE: ${current_price:.2f}
VOLUME: {volume:,}

Based ONLY on this price and volume data, explain what you observe. Don't categorize or use preset frameworks. Just analyze what this specific movement and volume pattern tells you about what might have happened.

Respond with your raw analysis - no JSON format, no categories, just your reasoning about what this data suggests."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=800,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            return {"raw_analysis": content.strip()}
            
        except Exception as e:
            print(f"Error in Claude price movement analysis: {e}")
            return {"raw_analysis": f"Price moved {price_change:.2f}% with volume of {volume:,}. Analysis requires investigation of underlying factors."}
    
    async def analyze_news_sentiment(self, symbol: str, news_articles: List[Dict], price_change: float) -> Dict[str, Any]:
        """Free-form news analysis based purely on headlines and price movement"""
        
        headlines = [article.get("headline", "") for article in news_articles[:5]]
        
        prompt = f"""Look at these news headlines about {symbol} and the {price_change:.2f}% price movement:

HEADLINES:
{chr(10).join([f"- {headline}" for headline in headlines])}

PRICE MOVEMENT: {price_change:.2f}%

Just read these headlines and tell me what story they're telling. What themes do you see? How do they relate to the price movement? Don't score or categorize - just analyze what the news is actually saying and whether it connects to the price action."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=800,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            return {"news_analysis": content.strip()}
            
        except Exception as e:
            print(f"Error in Claude news analysis: {e}")
            return {"news_analysis": f"News analysis unavailable. {len(headlines)} headlines reviewed relating to {price_change:.2f}% movement."}
    
    async def analyze_earnings_impact(self, symbol: str, earnings_data: Dict[str, Any], price_change: float) -> Dict[str, Any]:
        """Free-form earnings analysis without preset categories"""
        
        prompt = f"""Look at {symbol}'s earnings data and the {price_change:.2f}% price movement:

EARNINGS DATA:
- EPS: ${earnings_data.get('last_quarter_eps', 0):.2f} vs Expected: ${earnings_data.get('expected_eps', 0):.2f}
- Revenue Growth: {earnings_data.get('revenue_growth', 0):.1f}%
- Beat Expectations: {earnings_data.get('beat_estimate', False)}
- Guidance Updated: {earnings_data.get('guidance_updated', False)}

PRICE MOVEMENT: {price_change:.2f}%

Just analyze what this earnings performance tells you. Did they beat, miss, or meet expectations? What does that mean for the business? How does the price reaction make sense given these numbers? Think through it step by step."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=800,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            return {"earnings_analysis": content.strip()}
            
        except Exception as e:
            print(f"Error in Claude earnings analysis: {e}")
            return {"earnings_analysis": f"Earnings analysis unavailable for {symbol} with {price_change:.2f}% movement."}
    
    async def generate_master_inference(self, symbol: str, all_findings: List[str], 
                                      price_data: Dict[str, Any], 
                                      investigation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Pure reasoning analysis - no preset formats or categories"""
        
        price_change = price_data.get("price_change_percent", 0)
        start_price = price_data.get("start_price", 0)
        end_price = price_data.get("end_price", 0)
        
        findings_text = "\n".join([f"- {finding}" for finding in all_findings])
        
        prompt = f"""You've investigated why {symbol} moved {price_change:.2f}% from ${start_price:.2f} to ${end_price:.2f}.

Here's what your investigation found:
{findings_text}

Additional data from investigation:
{json.dumps(investigation_data, indent=2) if investigation_data else "No additional structured data"}

Now think through this step by step:
1. What actually happened to cause this price movement?
2. What's the most logical explanation based on ALL the evidence?
3. Why did investors react this way?
4. What does this mean going forward?

Don't use any preset categories or frameworks. Just reason through the evidence and explain what really happened. Be specific about the cause and confident in your conclusion."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1200,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            return {"comprehensive_analysis": content.strip()}
            
        except Exception as e:
            print(f"Error in Claude master inference: {e}")
            return {"comprehensive_analysis": f"{symbol} moved {price_change:.2f}% from ${start_price:.2f} to ${end_price:.2f}. Comprehensive analysis requires review of investigation findings."}
    
    async def generate_investigation_decision(self, current_findings: List[str], symbol: str) -> Dict[str, Any]:
        """AI decides what to investigate next based on current findings"""
        
        findings_text = "\n".join([f"- {finding}" for finding in current_findings])
        
        prompt = f"""You're investigating {symbol}. Here's what you've found so far:

{findings_text}

Based on these findings, what should you investigate next to get to the bottom of what's driving the price movement? What specific questions do these findings raise? What gaps do you see that need to be filled?

Think like a detective - what leads should you follow up on?"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=600,
                temperature=0.2,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            return {"investigation_reasoning": content.strip()}
            
        except Exception as e:
            print(f"Error in Claude investigation decision: {e}")
            return {"investigation_reasoning": f"Continue investigating {symbol} based on current findings. Additional analysis needed."}