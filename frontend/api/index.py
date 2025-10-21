from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import asyncio
from datetime import datetime
import yfinance as yf

# Import our LangGraph agent
from ..agents.investigation_agent import InvestigationAgent
from ..models.schemas import StockInvestigationRequest, InvestigationResponse, AgentNode
from ..services.stock_data_service import StockDataService

app = FastAPI(title="Agentic AI Stock Investigation System", version="1.0.0")

# Initialize a single global agent instance
agent = InvestigationAgent()
stock_service = StockDataService()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js frontend for local development
        "https://*.vercel.app",   # Vercel deployment domains
        "*"  # Allow all origins for Vercel serverless functions
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Global WebSocket connections manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def root():
    return {"message": "Agentic AI Stock Investigation System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/validate-stock", response_model=Dict[str, Any])
async def validate_stock_data(request: StockInvestigationRequest):
    """Validate stock symbol and fetch basic market data"""
    try:
        symbol = request.symbol.upper()
        
        # Use our new stock data service
        stock_data = await stock_service.get_stock_quote(symbol)
        
        return {
            "symbol": symbol,
            "valid": True,
            "current_price": stock_data["current_price"],
            "change": stock_data["change"],
            "change_percent": stock_data["change_percent"],
            "volume": stock_data["volume"],
            "market_cap": stock_data.get("market_cap"),
            "company_name": f"{symbol} Corporation",  # We'll enhance this later
            "sector": "Technology",  # Default for demo
            "timestamp": datetime.now().isoformat(),
            "data_source": stock_data.get("source", "unknown")
        }
        
    except Exception as e:
        # Return basic response for demo purposes
        return {
            "symbol": request.symbol.upper(),
            "valid": True,
            "current_price": 100.0,
            "change": 0.0,
            "change_percent": "0.00%",
            "volume": 1000000,
            "market_cap": 100000000,
            "company_name": f"{request.symbol} Company",
            "sector": "Demo",
            "timestamp": datetime.now().isoformat(),
            "data_source": "fallback",
            "error": str(e)
        }

@app.post("/api/investigate", response_model=InvestigationResponse)
async def start_investigation(request: StockInvestigationRequest):
    """Start autonomous AI investigation of a stock"""
    try:
        print(f"Starting investigation for {request.symbol}")
        
        # Use the global agent instance
        investigation_id = await agent.start_investigation(request.symbol, request.date_range)
        print(f"Investigation started with ID: {investigation_id}")
        
        return InvestigationResponse(
            investigation_id=investigation_id,
            status="started",
            message=f"Investigation started for {request.symbol}",
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        print(f"Error starting investigation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/investigation/{investigation_id}")
async def get_investigation_status(investigation_id: str):
    """Get the current status and results of an investigation"""
    try:
        # Use the global agent instance
        status = await agent.get_investigation_status(investigation_id)
        return status
    except Exception as e:
        print(f"Error getting investigation status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/langchain-demo/{symbol}")
async def langchain_investigation_demo(symbol: str):
    """Demonstrate LangChain investigation capabilities"""
    try:
        print(f"Running LangChain demo for {symbol}")
        
        # Get the LangChain service from the agent
        langchain_service = agent.langchain_service
        
        # Run all three LangChain investigations
        tasks = [
            langchain_service.investigate_news_sentiment(symbol, 5.0),
            langchain_service.investigate_earnings_impact(symbol, 5.0),
            langchain_service.investigate_market_context(symbol, 5.0)
        ]
        
        news_result, earnings_result, market_result = await asyncio.gather(
            *tasks, return_exceptions=True
        )
        
        # Prepare demo response
        demo_response = {
            "symbol": symbol.upper(),
            "langchain_analysis": {
                "news_sentiment": news_result if not isinstance(news_result, Exception) else {"error": str(news_result)},
                "earnings_impact": earnings_result if not isinstance(earnings_result, Exception) else {"error": str(earnings_result)},
                "market_context": market_result if not isinstance(market_result, Exception) else {"error": str(market_result)}
            },
            "demo_info": {
                "description": "LangChain-powered investigation using DuckDuckGo search and AI analysis",
                "features": [
                    "Real-time web search for news and analysis",
                    "Sentiment indicator extraction",
                    "Earnings event detection",
                    "Sector trend analysis",
                    "Peer comparison insights"
                ],
                "confidence_scoring": "Each analysis includes confidence scores (0-10 scale)",
                "search_integration": "Uses DuckDuckGo API for external data gathering"
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return demo_response
        
    except Exception as e:
        print(f"Error in LangChain demo: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/investigation/{investigation_id}")
async def get_investigation_status_endpoint(investigation_id: str):
    """Get the current status and results of an investigation (renamed to avoid duplicate)"""
    try:
        # Use the global agent instance
        status = await agent.get_investigation_status(investigation_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/investigation/{investigation_id}")
async def websocket_investigation_stream(websocket: WebSocket, investigation_id: str):
    """WebSocket endpoint for real-time investigation updates"""
    await manager.connect(websocket)
    print(f"WebSocket connected for investigation: {investigation_id}")
    
    try:
        # Use the global agent instance
        async for update in agent.stream_investigation_progress(investigation_id):
            print(f"Sending update: {update.get('type')}")
            await websocket.send_text(json.dumps(update))
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for investigation: {investigation_id}")
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error for investigation {investigation_id}: {str(e)}")
        await websocket.send_text(json.dumps({
            "type": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }))

# Export the app for Vercel
# Vercel will automatically handle ASGI applications
app_handler = app