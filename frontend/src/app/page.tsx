'use client';

import { useState, useEffect, useRef } from 'react';
import { InvestigationData, AgentNode } from '@/types';

// Simplified inline components to avoid import issues
const InvestigationForm = ({ onInvestigationStart, onReset, isLoading }: any) => {
  const [symbol, setSymbol] = useState('AAPL');
  const [startDate, setStartDate] = useState('2024-01-01');
  const [endDate, setEndDate] = useState('2024-12-31');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onInvestigationStart(symbol, { start_date: startDate, end_date: endDate });
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h2 className="text-white text-xl font-semibold mb-4">Stock Investigation</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-gray-300 text-sm font-medium mb-2">
            Stock Symbol
          </label>
          <input
            type="text"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white"
            placeholder="Enter stock symbol (e.g., AAPL)"
            required
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-gray-300 text-sm font-medium mb-2">
              Start Date
            </label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white"
            />
          </div>
          <div>
            <label className="block text-gray-300 text-sm font-medium mb-2">
              End Date
            </label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded text-white"
            />
          </div>
        </div>
        <div className="flex space-x-3">
          <button
            type="submit"
            disabled={isLoading}
            className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white py-2 px-4 rounded transition-colors"
          >
            {isLoading ? 'Investigating...' : 'Start Investigation'}
          </button>
          <button
            type="button"
            onClick={onReset}
            className="bg-gray-600 hover:bg-gray-700 text-white py-2 px-4 rounded transition-colors"
          >
            Reset
          </button>
        </div>
      </form>
    </div>
  );
};

const NodeVisualization = ({ nodes, isLoading }: any) => {
  const getNodeColor = (type: string, status: string) => {
    if (status === 'error') return 'bg-red-600 border-red-400';
    if (status === 'in_progress') return 'bg-yellow-600 border-yellow-400 animate-pulse';
    
    switch (type) {
      case 'data_fetch': return 'bg-blue-600 border-blue-400';
      case 'analysis': return 'bg-green-600 border-green-400';
      case 'decision': return 'bg-purple-600 border-purple-400';
      case 'inference': return 'bg-orange-600 border-orange-400';
      case 'validation': return 'bg-teal-600 border-teal-400';
      case 'spawn': return 'bg-indigo-600 border-indigo-400';
      default: return 'bg-gray-600 border-gray-400';
    }
  };

  const getNodeIcon = (type: string) => {
    switch (type) {
      case 'data_fetch': return 'DATA';
      case 'analysis': return 'ANALYZE';
      case 'decision': return 'DECIDE';
      case 'inference': return 'INFER';
      case 'validation': return 'VALIDATE';
      case 'spawn': return 'SPAWN';
      default: return 'PROCESS';
    }
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h2 className="text-white text-xl font-semibold mb-4">AI Investigation Progress</h2>
      
      {isLoading && (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-blue-400">AI agents are investigating...</p>
        </div>
      )}

      <div className="h-96 overflow-auto">
        {nodes.length === 0 && !isLoading ? (
          <div className="text-gray-400 text-center py-12">
            No investigation data yet. Start an investigation to see AI agents in action!
          </div>
        ) : (
          <div className="relative min-h-full">
            {/* Horizontal node flow */}
            <div className="flex items-start space-x-6 overflow-x-auto pb-4 min-w-max">
              {nodes.map((node: AgentNode, index: number) => (
                <div key={node.id || index} className="flex items-center">
                  {/* Node */}
                  <div className={`
                    ${getNodeColor(node.type, node.status)} 
                    rounded-lg p-4 min-w-64 max-w-80 text-white shadow-lg border-2
                    transition-all duration-300 hover:scale-105
                  `}>
                    {/* Node Header */}
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-2">
                        <div className="bg-black bg-opacity-30 px-2 py-1 rounded text-xs font-bold">
                          {getNodeIcon(node.type)}
                        </div>
                        <span className="text-xs font-semibold uppercase tracking-wide opacity-80">
                          {node.type.replace('_', ' ')}
                        </span>
                      </div>
                      
                      <div className={`
                        px-2 py-1 rounded-full text-xs font-semibold
                        ${node.status === 'completed' ? 'bg-green-500' : 
                          node.status === 'error' ? 'bg-red-500' : 
                          node.status === 'in_progress' ? 'bg-yellow-500' : 'bg-gray-500'}
                      `}>
                        {node.status.toUpperCase()}
                      </div>
                    </div>
                    
                    {/* Node Content */}
                    <h4 className="font-semibold text-sm mb-2 leading-tight">
                      {node.label}
                    </h4>
                    
                    <p className="text-xs opacity-90 leading-relaxed mb-3">
                      {node.description}
                    </p>
                    
                    {/* Node Footer */}
                    <div className="flex justify-between items-center text-xs opacity-75">
                      <span>
                        {new Date(node.created_at).toLocaleTimeString()}
                      </span>
                      {node.completed_at && (
                        <span>
                          Duration: {Math.round((new Date(node.completed_at).getTime() - new Date(node.created_at).getTime()) / 1000)}s
                        </span>
                      )}
                    </div>
                    
                    {/* Data Preview */}
                    {node.data && Object.keys(node.data).length > 0 && (
                      <details className="mt-3">
                        <summary className="cursor-pointer text-xs opacity-75 hover:opacity-100">
                          View Data
                        </summary>
                        <div className="mt-2 bg-black bg-opacity-30 rounded p-2 text-xs font-mono max-h-32 overflow-auto">
                          <pre className="whitespace-pre-wrap">
                            {JSON.stringify(node.data, null, 2).substring(0, 300)}
                            {JSON.stringify(node.data, null, 2).length > 300 ? '...' : ''}
                          </pre>
                        </div>
                      </details>
                    )}
                  </div>
                  
                  {/* Arrow connector */}
                  {index < nodes.length - 1 && (
                    <div className="flex items-center mx-3">
                      <div className="w-12 h-0.5 bg-gray-500"></div>
                      <div className="w-0 h-0 border-l-6 border-l-gray-500 border-y-4 border-y-transparent"></div>
                    </div>
                  )}
                </div>
              ))}
            </div>
            
            {/* Progress Summary */}
            {nodes.length > 0 && (
              <div className="mt-6 bg-gray-700 rounded-lg p-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-white font-semibold">Investigation Progress</span>
                  <span className="text-gray-300 text-sm">
                    {nodes.filter(n => n.status === 'completed').length} / {nodes.length} completed
                  </span>
                </div>
                
                <div className="bg-gray-600 rounded-full h-3">
                  <div 
                    className="bg-gradient-to-r from-blue-500 to-green-500 h-3 rounded-full transition-all duration-500"
                    style={{ 
                      width: `${nodes.length > 0 ? (nodes.filter(n => n.status === 'completed').length / nodes.length) * 100 : 0}%` 
                    }}
                  ></div>
                </div>
                
                {/* Node Type Summary */}
                <div className="flex flex-wrap gap-2 mt-3">
                  {Array.from(new Set(nodes.map(n => n.type))).map(type => {
                    const typeNodes = nodes.filter(n => n.type === type);
                    const completed = typeNodes.filter(n => n.status === 'completed').length;
                    return (
                      <div key={type} className="bg-gray-600 rounded px-2 py-1 text-xs">
                        <span className="font-semibold">{type.replace('_', ' ').toUpperCase()}: </span>
                        <span>{completed}/{typeNodes.length}</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default function Home() {
  const [investigationData, setInvestigationData] = useState<InvestigationData | null>(null);
  const [nodes, setNodes] = useState<AgentNode[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentWebSocket, setCurrentWebSocket] = useState<WebSocket | null>(null);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);

  // API endpoints - using relative URLs since we're on the same domain
  const API_ENDPOINTS = {
    validateStock: '/api/validate-stock',
    investigate: '/api/investigate', 
    websocket: (id: string) => `/ws/investigation/${id}`,
    health: '/api/health',
    langchainDemo: (symbol: string) => `/api/langchain-demo/${symbol}`,
    langchainTest: '/api/langchain-test'
  };

  // Cleanup on component unmount
  useEffect(() => {
    return () => {
      if (currentWebSocket) {
        currentWebSocket.close();
      }
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [currentWebSocket]);

  const handleInvestigationStart = async (symbol: string, dateRange: { start_date: string; end_date: string }) => {
    setIsLoading(true);
    setNodes([]);
    
    try {
      // Step 1: Validate stock first
      const validateResponse = await fetch(API_ENDPOINTS.validateStock, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol }),
      });

      if (!validateResponse.ok) {
        throw new Error(`Stock validation failed`);
      }

      const validationData = await validateResponse.json();
      console.log('Stock validated:', validationData);

      // Add validation node
      const validationNode: AgentNode = {
        id: 'validation',
        label: 'Stock Validation Complete',
        description: `${symbol} validated - Current Price: $${validationData.current_price?.toFixed(2)}, Change: ${validationData.change_percent}`,
        status: 'completed',
        type: 'validation',
        data: validationData,
        children_ids: [],
        created_at: new Date().toISOString(),
        completed_at: new Date().toISOString()
      };
      setNodes([validationNode]);

      // Step 2: Start main investigation
      const response = await fetch(API_ENDPOINTS.investigate, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          symbol,
          date_range: dateRange
        }),
      });

      if (!response.ok) {
        throw new Error(`Investigation failed: ${response.statusText}`);
      }

      const data = await response.json();
      setInvestigationData(data);

      // Add investigation start node
      const startNode: AgentNode = {
        id: 'investigation-start',
        label: 'Agent Decision: Begin Comprehensive Analysis',
        description: `AI agents initiated multi-dimensional investigation of ${symbol} across news sentiment, earnings data, and market context`,
        status: 'completed',
        type: 'spawn',
        data: data,
        children_ids: [],
        created_at: new Date().toISOString(),
        completed_at: new Date().toISOString()
      };
      setNodes(prev => [...prev, startNode]);

      // Step 3: Run LangChain analysis automatically
      setTimeout(async () => {
        try {
          console.log('Starting LangChain analysis for:', symbol);
          const langchainUrl = API_ENDPOINTS.langchainTest;
          console.log('LangChain URL:', langchainUrl);
          
          const langchainResponse = await fetch(langchainUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ symbol }),
          });
          
          console.log('LangChain response status:', langchainResponse.status);
          
          if (langchainResponse.ok) {
            const langchainData = await langchainResponse.json();
            console.log('LangChain analysis complete:', langchainData);
            
            // Add individual analysis nodes
            const analysisTypes = ['news_sentiment', 'earnings_impact', 'market_context'];
            
            for (let i = 0; i < analysisTypes.length; i++) {
              const analysisType = analysisTypes[i];
              const analysisData = langchainData.langchain_analysis[analysisType];
              
              setTimeout(() => {
                const analysisNode: AgentNode = {
                  id: `langchain-${analysisType}`,
                  label: `Fetch ${analysisType.replace('_', ' ').toUpperCase()} Data`,
                  description: `Analyzing ${symbol} through ${analysisData?.sentiment_indicators?.length || analysisData?.earnings_indicators?.length || analysisData?.sector_trends?.length || 0} data sources - Confidence Score: ${analysisData?.confidence_score}/10`,
                  status: 'completed',
                  type: 'analysis',
                  data: analysisData,
                  children_ids: [],
                  created_at: new Date().toISOString(),
                  completed_at: new Date().toISOString()
                };
                
                setNodes(prev => [...prev, analysisNode]);
              }, i * 2000); // Stagger the results by 2 seconds each
            }
            
            // Add final summary node
            setTimeout(() => {
              const summaryNode: AgentNode = {
                id: 'investigation-complete',
                label: 'Inference Node: Cross-Reference Analysis Complete',
                description: `AI agent synthesized ${Object.keys(langchainData.langchain_analysis).length} investigation streams into comprehensive market intelligence for ${symbol}`,
                status: 'completed',
                type: 'inference',
                data: {
                  total_analyses: Object.keys(langchainData.langchain_analysis).length,
                  langchain_enabled: true,
                  features: langchainData.demo_info?.features || [],
                  timestamp: new Date().toISOString()
                },
                children_ids: [],
                created_at: new Date().toISOString(),
                completed_at: new Date().toISOString()
              };
              
              setNodes(prev => [...prev, summaryNode]);
              setIsLoading(false);
            }, analysisTypes.length * 2000 + 1000);
            
          } else {
            const errorText = await langchainResponse.text();
            console.error('LangChain response error:', errorText);
            throw new Error(`LangChain analysis failed: ${langchainResponse.status} - ${errorText}`);
          }
        } catch (langchainError) {
          console.error('LangChain analysis error:', langchainError);
          
          // Add error node but continue
          const errorNode: AgentNode = {
            id: 'langchain-error',
            label: 'Agent Decision: LangChain Analysis Failed',
            description: `LangChain analysis encountered an issue: ${langchainError}`,
            status: 'error',
            type: 'analysis',
            data: { error: String(langchainError) },
            children_ids: [],
            created_at: new Date().toISOString()
          };
          
          setNodes(prev => [...prev, errorNode]);
          setIsLoading(false);
        }
      }, 1000); // Start LangChain analysis after 1 second

      // Set timeout to stop loading after 30 seconds max
      timeoutRef.current = setTimeout(() => {
        setIsLoading(false);
      }, 30000);

    } catch (error) {
      console.error('Investigation failed:', error);
      setIsLoading(false);
      
      // Show error node
      const errorNode: AgentNode = {
        id: 'error',
        label: 'Investigation Error: Process Failed',
        description: `Failed to investigate ${symbol}: ${error}`,
        status: 'error',
        type: 'analysis',
        data: { error: String(error) },
        children_ids: [],
        created_at: new Date().toISOString()
      };
      
      setNodes([errorNode]);
    }
  };

  const handleReset = () => {
    if (currentWebSocket) {
      currentWebSocket.close();
      setCurrentWebSocket(null);
    }
    
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
    
    setInvestigationData(null);
    setNodes([]);
    setIsLoading(false);
  };

  const testLangChain = async () => {
    try {
      const response = await fetch(API_ENDPOINTS.langchainTest, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ symbol: 'AAPL' }),
      });
      const data = await response.json();
      console.log('LangChain test:', data);
      alert('LangChain test successful! Check console for details.');
    } catch (error) {
      console.error('LangChain test failed:', error);
      alert('LangChain test failed. Check console for details.');
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 p-8">
      <div className="max-w-7xl mx-auto">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">
            AEGIS Stock Investigation System
          </h1>
          <p className="text-blue-200 text-lg">
            Advanced AI-powered real-time stock analysis with node-based investigation tracking
          </p>
          <div className="mt-4 flex justify-center space-x-4">
            <a 
              href="/api/health" 
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded transition-colors"
            >
              API Health
            </a>
            <button 
              onClick={testLangChain}
              className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded transition-colors"
            >
              Test LangChain
            </button>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Investigation Form */}
          <div className="lg:col-span-1">
            <InvestigationForm 
              onInvestigationStart={handleInvestigationStart}
              onReset={handleReset}
              isLoading={isLoading}
            />
            
            {investigationData && (
              <div className="mt-6 bg-gray-800 rounded-lg p-6">
                <h3 className="text-white font-semibold mb-3">Investigation Status</h3>
                <div className="space-y-2 text-sm">
                  <p className="text-gray-300">ID: {investigationData.investigation_id}</p>
                  <p className="text-gray-300">Status: <span className="text-green-400">{investigationData.status}</span></p>
                  <p className="text-gray-300">Investigation Nodes: <span className="text-blue-400">{nodes.length}</span></p>
                </div>
              </div>
            )}
          </div>

          {/* Node Visualization */}
          <div className="lg:col-span-2">
            <NodeVisualization nodes={nodes} isLoading={isLoading} />
          </div>
        </div>
      </div>
    </main>
  );
}
