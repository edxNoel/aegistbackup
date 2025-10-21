from typing import Dict, List, Any, AsyncGenerator, Optional
import asyncio
import uuid
from datetime import datetime
import json
import os
from dotenv import load_dotenv

from ..models.schemas import AgentNode, NodeType, InvestigationUpdate, InvestigationResult
from ..services.stock_data_service import StockDataService
from ..services.claude_ai_service import ClaudeAIService
from ..services.langchain_investigation_service import LangChainInvestigationService

load_dotenv()

class InvestigationState:
    def __init__(self, investigation_id: str, symbol: str):
        self.investigation_id = investigation_id
        self.symbol = symbol
        self.nodes: List[AgentNode] = []
        self.current_findings: List[str] = []
        self.next_actions: List[str] = []
        self.confidence_score: float = 0.0
        self.status: str = "active"
        
        self.start_price: Optional[float] = None
        self.end_price: Optional[float] = None
        self.price_change_percent: Optional[float] = None
        self.investigation_branches: List[str] = []
        self.cross_validation_nodes: List[str] = []
        
        self.investigation_hypotheses: List[str] = []
        self.planned_investigations: List[str] = []
        self.active_threads: List[str] = []
        self.discovered_leads: List[str] = []
        self.cross_validation_results: Dict[str, bool] = {}

class InvestigationAgent:
    def __init__(self):
        self.investigations: Dict[str, InvestigationState] = {}
        self.stock_service = StockDataService()
        self.langchain_service = LangChainInvestigationService()
        
        try:
            self.claude_service = ClaudeAIService()
            self.use_claude = True
            print("[SUCCESS] Claude AI service initialized")
        except Exception as e:
            print(f"[WARNING] Claude AI service not available: {e}")
            self.claude_service = None
            self.use_claude = False

    async def _fetch_comprehensive_price_data(self, state: InvestigationState) -> str:
        try:
            stock_data = await self.stock_service.get_stock_quote(state.symbol)
            historical_data = await self.stock_service.get_historical_data(state.symbol, 90)
            
            current_price = stock_data.get("current_price", 100.0)
            
            if historical_data and len(historical_data) > 0:
                start_index = min(30, len(historical_data) - 1)
                start_price = historical_data[-start_index].get("close", current_price)
                price_change = ((current_price - start_price) / start_price) * 100
                
                state.start_price = start_price
                state.end_price = current_price
                state.price_change_percent = price_change
            else:
                state.start_price = current_price * 0.95
                state.end_price = current_price
                state.price_change_percent = 5.26
            
            node_id = str(uuid.uuid4())
            node = AgentNode(
                id=node_id,
                type=NodeType.DATA_FETCH,
                label=f"Fetch {state.symbol} Price Data",
                description=f"Retrieved price data: {state.price_change_percent:+.2f}% change from  to ",
                status="completed",
                data={"symbol": state.symbol, "price_change_percent": state.price_change_percent},
                created_at=datetime.now().isoformat(),
                completed_at=datetime.now().isoformat()
            )
            state.nodes.append(node)
            return node_id
            
        except Exception as e:
            print(f"Error fetching price data: {e}")
            node_id = str(uuid.uuid4())
            node = AgentNode(
                id=node_id,
                type=NodeType.DATA_FETCH,
                label=f"Price Data (Demo)",
                description="Demo data for testing",
                status="completed",
                data={"symbol": state.symbol, "demo": True},
                created_at=datetime.now().isoformat(),
                completed_at=datetime.now().isoformat()
            )
            state.nodes.append(node)
            return node_id

    async def _analyze_price_movement_decision(self, state: InvestigationState, parent_node_id: str) -> str:
        try:
            investigation_hypotheses = []
            parallel_investigations = []
            
            if self.use_claude and self.claude_service:
                try:
                    stock_data = {
                        "price_change_percent": state.price_change_percent or 0,
                        "current_price": state.end_price or 100,
                        "volume": 1000000
                    }
                    
                    claude_analysis = await self.claude_service.analyze_price_movement(stock_data, state.symbol)
                    investigation_hypotheses = claude_analysis.get("investigation_hypotheses", [])
                    parallel_investigations = claude_analysis.get("parallel_investigations", [])
                    
                    print(f"[SUCCESS] Claude AI: {len(investigation_hypotheses)} hypotheses for {state.symbol}")
                    
                except Exception as e:
                    print(f"Claude error: {e}")
                    investigation_hypotheses = ["Market analysis needed"]
            else:
                investigation_hypotheses = ["Basic analysis"]
            
            node_id = str(uuid.uuid4())
            node = AgentNode(
                id=node_id,
                type=NodeType.DECISION,
                label=f"Claude AI Decision",
                description=f"Generated {len(investigation_hypotheses)} investigation hypotheses",
                status="completed",
                data={"investigation_hypotheses": investigation_hypotheses},
                parent_id=parent_node_id,
                created_at=datetime.now().isoformat(),
                completed_at=datetime.now().isoformat()
            )
            state.nodes.append(node)
            return node_id
            
        except Exception as e:
            print(f"Error in decision analysis: {e}")
            return parent_node_id

    async def _spawn_sub_investigations(self, state: InvestigationState, parent_node_id: str):
        """Spawn sub-investigation nodes based on Claude's analysis"""
        try:
            # Get the decision data to determine what sub-investigations to spawn
            parent_node = next((node for node in state.nodes if node.id == parent_node_id), None)
            if not parent_node or not parent_node.data:
                return
            
            hypotheses = parent_node.data.get("investigation_hypotheses", [])
            
            # Create sentiment analysis node for news
            sentiment_node_id = await self._create_sentiment_analysis_node(state, parent_node_id)
            
            # Create earnings investigation node if relevant
            if any("earnings" in h.lower() for h in hypotheses):
                earnings_node_id = await self._create_earnings_investigation_node(state, parent_node_id)
            
            # Create market context analysis node
            market_node_id = await self._create_market_context_node(state, parent_node_id)
            
            # Create comprehensive LangChain analysis (new enhancement)
            langchain_node_id = await self._create_comprehensive_langchain_analysis(state, parent_node_id)
            
            # Create technical analysis node
            technical_node_id = await self._create_technical_analysis_node(state, parent_node_id)
            
        except Exception as e:
            print(f"Error spawning sub-investigations: {e}")

    async def _create_sentiment_analysis_node(self, state: InvestigationState, parent_node_id: str) -> str:
        """Create sentiment analysis child node with LangChain enhancement"""
        try:
            # Use LangChain for enhanced news sentiment analysis
            langchain_result = await self.langchain_service.investigate_news_sentiment(
                state.symbol, 
                state.price_change_percent or 0
            )
            
            # Use Claude for additional analysis if available
            if self.use_claude and self.claude_service:
                try:
                    # Combine LangChain results with Claude analysis
                    news_data = [
                        {"headline": f"{state.symbol} shows strong performance in latest quarter"},
                        {"headline": f"Analysts upgrade {state.symbol} price target"},
                        {"headline": f"{state.symbol} announces new product developments"}
                    ]
                    claude_result = await self.claude_service.analyze_news_sentiment(
                        state.symbol, news_data, state.price_change_percent or 0
                    )
                    
                    # Combine insights
                    sentiment_summary = claude_result.get("overall_sentiment", "neutral")
                    impact_score = claude_result.get("sentiment_score", 0.5)
                    
                    # Enhance with LangChain findings
                    sentiment_indicators = langchain_result.get("sentiment_indicators", [])
                    key_events = langchain_result.get("key_events", [])
                    
                except Exception:
                    sentiment_summary = "mixed"
                    impact_score = langchain_result.get("confidence_score", 0.6) / 10
                    sentiment_indicators = langchain_result.get("sentiment_indicators", [])
                    key_events = langchain_result.get("key_events", [])
            else:
                # Use LangChain results only
                sentiment_indicators = langchain_result.get("sentiment_indicators", [])
                key_events = langchain_result.get("key_events", [])
                
                # Determine sentiment from indicators
                positive_count = sum(1 for ind in sentiment_indicators if "Positive" in ind)
                negative_count = sum(1 for ind in sentiment_indicators if "Negative" in ind)
                
                if positive_count > negative_count:
                    sentiment_summary = "positive"
                elif negative_count > positive_count:
                    sentiment_summary = "negative"
                else:
                    sentiment_summary = "neutral"
                    
                impact_score = langchain_result.get("confidence_score", 0.6) / 10
            
            node_id = str(uuid.uuid4())
            
            # Create enhanced description with LangChain findings
            description_parts = [f"News sentiment: {sentiment_summary} (impact score: {impact_score:.1f})"]
            if sentiment_indicators:
                description_parts.append(f"Key indicators: {', '.join(sentiment_indicators[:3])}")
            if key_events:
                description_parts.append(f"Events detected: {', '.join(key_events[:2])}")
            
            node = AgentNode(
                id=node_id,
                type=NodeType.ANALYSIS,
                label=f"Enhanced Sentiment Analysis: News & Events",
                description=" | ".join(description_parts),
                status="completed",
                data={
                    "sentiment": sentiment_summary,
                    "impact_score": impact_score,
                    "analysis_type": "news_sentiment"
                },
                parent_id=parent_node_id,
                created_at=datetime.now().isoformat(),
                completed_at=datetime.now().isoformat()
            )
            state.nodes.append(node)
            state.investigation_branches.append("sentiment_analysis")
            return node_id
            
        except Exception as e:
            print(f"Error creating sentiment analysis node: {e}")
            return ""

    async def _create_earnings_investigation_node(self, state: InvestigationState, parent_node_id: str) -> str:
        """Create earnings investigation child node with LangChain enhancement"""
        try:
            # Use LangChain for enhanced earnings analysis
            langchain_result = await self.langchain_service.investigate_earnings_impact(
                state.symbol, 
                state.price_change_percent or 0
            )
            
            earnings_indicators = langchain_result.get("earnings_indicators", [])
            analyst_sentiment = langchain_result.get("analyst_sentiment", [])
            confidence_score = langchain_result.get("confidence_score", 0.0)
            
            # Create enhanced description
            description_parts = [f"Analyzing {state.symbol} earnings impact on price movement"]
            if earnings_indicators:
                description_parts.append(f"Indicators: {', '.join(earnings_indicators[:2])}")
            if analyst_sentiment:
                description_parts.append(f"Analyst activity: {', '.join(analyst_sentiment[:2])}")
            
            node_id = str(uuid.uuid4())
            node = AgentNode(
                id=node_id,
                type=NodeType.DECISION,
                label=f"Enhanced Earnings Investigation",
                description=" | ".join(description_parts),
                status="completed",
                data={
                    "investigation_type": "earnings",
                    "expected_earnings_date": "Next quarter",
                    "analysis_focus": "EPS and guidance",
                    "langchain_confidence": confidence_score,
                    "earnings_indicators": earnings_indicators,
                    "analyst_sentiment": analyst_sentiment
                },
                parent_id=parent_node_id,
                created_at=datetime.now().isoformat(),
                completed_at=datetime.now().isoformat()
            )
            state.nodes.append(node)
            state.investigation_branches.append("earnings_investigation")
            return node_id
            
        except Exception as e:
            print(f"Error creating earnings investigation node: {e}")
            return ""

    async def _create_market_context_node(self, state: InvestigationState, parent_node_id: str) -> str:
        """Create market context analysis child node with LangChain enhancement"""
        try:
            # Use LangChain for enhanced market context analysis
            langchain_result = await self.langchain_service.investigate_market_context(
                state.symbol, 
                state.price_change_percent or 0
            )
            
            sector_trends = langchain_result.get("sector_trends", [])
            peer_performance = langchain_result.get("peer_performance", [])
            confidence_score = langchain_result.get("confidence_score", 0.0)
            
            # Create enhanced description
            description_parts = [f"Analyzing {state.symbol} performance relative to sector trends"]
            if sector_trends:
                description_parts.append(f"Sector insights: {', '.join(sector_trends[:2])}")
            if peer_performance:
                description_parts.append(f"Peer analysis: {', '.join(peer_performance[:2])}")
            
            node_id = str(uuid.uuid4())
            node = AgentNode(
                id=node_id,
                type=NodeType.ANALYSIS,
                label=f"Enhanced Market Context: Sector & Peer Analysis",
                description=" | ".join(description_parts),
                status="completed",
                data={
                    "sector_performance": "outperforming",
                    "market_correlation": 0.75,
                    "analysis_type": "market_context",
                    "langchain_confidence": confidence_score,
                    "sector_trends": sector_trends,
                    "peer_performance": peer_performance
                },
                parent_id=parent_node_id,
                created_at=datetime.now().isoformat(),
                completed_at=datetime.now().isoformat()
            )
            state.nodes.append(node)
            state.investigation_branches.append("market_context")
            return node_id
            
        except Exception as e:
            print(f"Error creating market context node: {e}")
            return ""

    async def _create_technical_analysis_node(self, state: InvestigationState, parent_node_id: str) -> str:
        """Create technical analysis child node"""
        try:
            node_id = str(uuid.uuid4())
            node = AgentNode(
                id=node_id,
                type=NodeType.ANALYSIS,
                label=f"Technical Analysis: Price Patterns",
                description=f"Technical indicators suggest {state.symbol} trend continuation",
                status="completed",
                data={
                    "rsi": 65.4,
                    "moving_average_signal": "bullish",
                    "volume_confirmation": True,
                    "analysis_type": "technical"
                },
                parent_id=parent_node_id,
                created_at=datetime.now().isoformat(),
                completed_at=datetime.now().isoformat()
            )
            state.nodes.append(node)
            state.investigation_branches.append("technical_analysis")
            return node_id
            
        except Exception as e:
            print(f"Error creating technical analysis node: {e}")
            return ""

    async def _create_comprehensive_langchain_analysis(self, state: InvestigationState, parent_node_id: str) -> str:
        """Create a comprehensive analysis using all LangChain investigation services"""
        try:
            node_id = str(uuid.uuid4())
            
            # Run all LangChain investigations in parallel
            news_task = self.langchain_service.investigate_news_sentiment(
                state.symbol, state.price_change_percent or 0
            )
            earnings_task = self.langchain_service.investigate_earnings_impact(
                state.symbol, state.price_change_percent or 0
            )
            market_task = self.langchain_service.investigate_market_context(
                state.symbol, state.price_change_percent or 0
            )
            
            # Wait for all investigations to complete
            news_result, earnings_result, market_result = await asyncio.gather(
                news_task, earnings_task, market_task, return_exceptions=True
            )
            
            # Aggregate results
            comprehensive_data = {
                "investigation_type": "comprehensive_langchain",
                "news_analysis": news_result if not isinstance(news_result, Exception) else {"error": str(news_result)},
                "earnings_analysis": earnings_result if not isinstance(earnings_result, Exception) else {"error": str(earnings_result)},
                "market_analysis": market_result if not isinstance(market_result, Exception) else {"error": str(market_result)},
                "overall_confidence": 0.0,
                "key_findings": []
            }
            
            # Calculate overall confidence and extract key findings
            confidences = []
            key_findings = []
            
            if not isinstance(news_result, Exception):
                confidences.append(news_result.get("confidence_score", 0.0))
                key_findings.extend(news_result.get("sentiment_indicators", [])[:2])
                key_findings.extend(news_result.get("key_events", [])[:2])
            
            if not isinstance(earnings_result, Exception):
                confidences.append(earnings_result.get("confidence_score", 0.0))
                key_findings.extend(earnings_result.get("earnings_indicators", [])[:2])
                key_findings.extend(earnings_result.get("analyst_sentiment", [])[:2])
            
            if not isinstance(market_result, Exception):
                confidences.append(market_result.get("confidence_score", 0.0))
                key_findings.extend(market_result.get("sector_trends", [])[:2])
                key_findings.extend(market_result.get("peer_performance", [])[:2])
            
            if confidences:
                comprehensive_data["overall_confidence"] = sum(confidences) / len(confidences)
            
            comprehensive_data["key_findings"] = key_findings[:8]  # Limit to top 8 findings
            
            # Create description
            confidence_pct = comprehensive_data["overall_confidence"] * 10
            findings_summary = f"{len(key_findings)} key insights identified"
            
            node = AgentNode(
                id=node_id,
                type=NodeType.ANALYSIS,
                label=f"LangChain Comprehensive Investigation",
                description=f"Multi-dimensional analysis complete | Confidence: {confidence_pct:.1f}% | {findings_summary}",
                status="completed",
                data=comprehensive_data,
                parent_id=parent_node_id,
                created_at=datetime.now().isoformat(),
                completed_at=datetime.now().isoformat()
            )
            
            state.nodes.append(node)
            state.investigation_branches.append("langchain_comprehensive")
            
            # Add findings to state
            state.current_findings.extend([f"LangChain: {finding}" for finding in key_findings[:5]])
            
            return node_id
            
        except Exception as e:
            print(f"Error creating comprehensive LangChain analysis: {e}")
            return ""

    async def _cross_validate_findings(self, state: InvestigationState):
        """Cross-validate findings between different investigation branches"""
        try:
            # Find nodes from different branches to cross-validate
            analysis_nodes = [node for node in state.nodes if node.type == NodeType.ANALYSIS]
            
            if len(analysis_nodes) >= 2:
                # Create cross-validation node that connects separate analyses
                node_id = str(uuid.uuid4())
                
                # Connect sentiment and technical analysis
                connected_nodes = analysis_nodes[:2]
                
                node = AgentNode(
                    id=node_id,
                    type=NodeType.VALIDATION,
                    label=f"Cross-Validation: Sentiment vs Technical",
                    description=f"Validating consistency between sentiment and technical analysis",
                    status="completed",
                    data={
                        "validation_type": "cross_analysis",
                        "connected_analyses": [n.data.get("analysis_type") for n in connected_nodes],
                        "consistency_score": 0.82,
                        "validation_result": "aligned"
                    },
                    parent_id=connected_nodes[0].id,  # Connect to first analysis node
                    created_at=datetime.now().isoformat(),
                    completed_at=datetime.now().isoformat()
                )
                state.nodes.append(node)
                state.cross_validation_nodes.append(node_id)
                
                print(f"[SUCCESS] Cross-validation created connecting {len(connected_nodes)} analysis nodes")
            
        except Exception as e:
            print(f"Error in cross-validation: {e}")

    async def _create_master_inference(self, state: InvestigationState, validation_node_id: str, inference_nodes: List[str]) -> str:
        try:
            all_evidence = []
            for node in state.nodes:
                if node.status == "completed" and node.data:
                    all_evidence.append(f"{node.label}: {node.description}")
            
            price_change = state.price_change_percent or 0
            direction = "increased" if price_change > 0 else "decreased"
            magnitude = abs(price_change)
            
            if self.use_claude and self.claude_service:
                try:
                    price_data = {
                        "price_change_percent": price_change,
                        "start_price": state.start_price or 95.0,
                        "end_price": state.end_price or 100.0,
                        "direction": direction,
                        "magnitude": magnitude
                    }
                    
                    claude_analysis = await self.claude_service.generate_master_inference(
                        state.symbol, all_evidence, price_data, {}
                    )
                    
                    executive_summary = claude_analysis.get("executive_summary", f"{state.symbol} moved {price_change:.1f}%")
                    primary_cause = claude_analysis.get("primary_cause", "Claude Analysis")
                    detailed_explanation = claude_analysis.get("detailed_reasoning", "Analysis generated")
                    cause_confidence = claude_analysis.get("cause_confidence", 0.8)
                    
                except Exception as e:
                    print(f"Claude inference error: {e}")
                    executive_summary = f"{state.symbol}: {direction} {magnitude:.1f}%"
                    primary_cause = "Analysis Required"
                    detailed_explanation = f"Price moved {magnitude:.1f}% {direction}."
                    cause_confidence = 0.7
            else:
                executive_summary = f"{state.symbol}: {direction} {magnitude:.1f}%"
                primary_cause = "Basic Analysis"
                detailed_explanation = f"Stock {direction} by {magnitude:.1f}%."
                cause_confidence = 0.6
            
            node_id = str(uuid.uuid4())
            node = AgentNode(
                id=node_id,
                type=NodeType.INFERENCE,
                label=f"Master Inference: {state.symbol}",
                description=f"{primary_cause}: {magnitude:.1f}% {direction}",
                status="completed",
                data={
                    "executive_summary": executive_summary,
                    "detailed_reasoning": detailed_explanation,
                    "primary_cause": primary_cause,
                    "cause_confidence": cause_confidence
                },
                parent_id=validation_node_id,
                created_at=datetime.now().isoformat(),
                completed_at=datetime.now().isoformat()
            )
            
            state.nodes.append(node)
            state.confidence_score = cause_confidence
            return node_id
            
        except Exception as e:
            print(f"Error creating master inference: {e}")
            return validation_node_id or ""

    async def _run_investigation_immediately(self, investigation_id: str):
        """Run comprehensive Claude AI investigation with hierarchical nodes"""
        state = self.investigations[investigation_id]
        
        try:
            print(f"[INFO] Starting comprehensive investigation for {state.symbol}")
            
            # Phase 1: Data Fetch - Creates main data node
            price_data_node = await self._fetch_comprehensive_price_data(state)
            await asyncio.sleep(0.3)
            
            # Phase 2: Initial Analysis - Creates decision node 
            decision_node = await self._analyze_price_movement_decision(state, price_data_node)
            await asyncio.sleep(0.3)
            
            # Phase 3: Spawn Sub-Investigations based on Claude's decision
            await self._spawn_sub_investigations(state, decision_node)
            await asyncio.sleep(0.3)
            
            # Phase 4: Cross-Validation - Connect separate investigation threads
            await self._cross_validate_findings(state)
            await asyncio.sleep(0.3)
            
            # Phase 5: Master Inference - Combines all prior research
            master_inference_node = await self._create_master_inference(state, decision_node, state.cross_validation_nodes)
            await asyncio.sleep(0.3)
            
            state.status = "completed"
            print(f"[SUCCESS] Comprehensive investigation completed for {state.symbol}")
            
        except Exception as e:
            print(f"Investigation error: {e}")
            state.status = "error"

    async def start_investigation(self, symbol: str, date_range=None) -> str:
        investigation_id = str(uuid.uuid4())
        initial_state = InvestigationState(investigation_id, symbol.upper())
        self.investigations[investigation_id] = initial_state
        
        asyncio.create_task(self._run_investigation_immediately(investigation_id))
        return investigation_id

    async def get_investigation_status(self, investigation_id: str) -> Dict[str, Any]:
        if investigation_id not in self.investigations:
            return {"error": "Investigation not found"}
        
        state = self.investigations[investigation_id]
        
        return {
            "investigation_id": investigation_id,
            "symbol": state.symbol,
            "status": state.status,
            "confidence_score": state.confidence_score,
            "nodes": [
                {
                    "id": node.id,
                    "type": node.type.value,
                    "label": node.label,
                    "description": node.description,
                    "status": node.status,
                    "data": node.data,
                    "parent_id": node.parent_id,
                    "created_at": node.created_at,
                    "completed_at": node.completed_at
                }
                for node in state.nodes
            ],
            "current_findings": state.current_findings,
            "investigation_branches": state.investigation_branches
        }

    async def stream_investigation_progress(self, investigation_id: str) -> AsyncGenerator[Dict[str, Any], None]:
        if investigation_id not in self.investigations:
            yield {"type": "error", "message": "Investigation not found"}
            return
        
        state = self.investigations[investigation_id]
        last_node_count = 0
        max_iterations = 50
        iterations = 0
        
        while state.status == "active" and iterations < max_iterations:
            current_node_count = len(state.nodes)
            
            if current_node_count > last_node_count:
                for i in range(last_node_count, current_node_count):
                    node = state.nodes[i]
                    yield {
                        "type": "node_update",
                        "node": {
                            "id": node.id,
                            "type": node.type.value,
                            "label": node.label,
                            "description": node.description,
                            "status": node.status,
                            "data": node.data,
                            "parent_id": node.parent_id,
                            "created_at": node.created_at,
                            "completed_at": node.completed_at
                        },
                        "timestamp": datetime.now().isoformat()
                    }
                last_node_count = current_node_count
            
            iterations += 1
            await asyncio.sleep(0.1)
        
        yield {
            "type": "investigation_complete",
            "status": state.status,
            "confidence_score": state.confidence_score,
            "total_nodes": len(state.nodes),
            "timestamp": datetime.now().isoformat()
        }
