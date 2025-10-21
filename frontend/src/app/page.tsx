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
      <h2 className="text-white text-xl font-semibold mb-4">🔍 Stock Investigation</h2>
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
            {isLoading ? '🔄 Investigating...' : '🚀 Start Investigation'}
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
  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h2 className="text-white text-xl font-semibold mb-4">🤖 AI Investigation Progress</h2>
      
      {isLoading && (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-blue-400">AI agents are investigating...</p>
        </div>
      )}

      <div className="space-y-3 max-h-96 overflow-y-auto">
        {nodes.map((node: AgentNode, index: number) => (
          <div key={node.id || index} className="bg-gray-700 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-white font-medium">{node.label}</h3>
              <span className={`px-2 py-1 rounded text-xs ${
                node.status === 'completed' ? 'bg-green-600 text-white' : 
                node.status === 'in_progress' ? 'bg-yellow-600 text-white' : 
                'bg-gray-600 text-white'
              }`}>
                {node.status}
              </span>
            </div>
            <p className="text-gray-300 text-sm">{node.description}</p>
            {node.data && (
              <div className="mt-2 text-xs text-gray-400">
                <pre className="whitespace-pre-wrap">
                  {JSON.stringify(node.data, null, 2).substring(0, 200)}...
                </pre>
              </div>
            )}
          </div>
        ))}
        
        {nodes.length === 0 && !isLoading && (
          <p className="text-gray-400 text-center py-8">
            No investigation data yet. Start an investigation to see AI agents in action!
          </p>
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
    langchainDemo: (symbol: string) => `/api/langchain-demo/${symbol}`
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
      // First, try the LangChain demo endpoint to test functionality
      try {
        const langchainResponse = await fetch(API_ENDPOINTS.langchainDemo(symbol), {
          method: 'POST',
        });
        
        if (langchainResponse.ok) {
          const langchainData = await langchainResponse.json();
          console.log('LangChain demo successful:', langchainData);
          
          // Add LangChain results as nodes
          const langchainNode: AgentNode = {
            id: 'langchain-demo',
            label: '🔗 LangChain Analysis Complete',
            description: `Analyzed ${symbol} with ${Object.keys(langchainData.langchain_analysis).length} investigation types`,
            status: 'completed',
            type: 'analysis',
            data: langchainData.langchain_analysis,
            created_at: new Date().toISOString(),
            completed_at: new Date().toISOString()
          };
          
          setNodes([langchainNode]);
        }
      } catch (error) {
        console.log('LangChain demo not available, trying main investigation');
      }

      // Validate stock first
      const validateResponse = await fetch(API_ENDPOINTS.validateStock, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol }),
      });

      if (!validateResponse.ok) {
        const errorData = await validateResponse.text();
        throw new Error(`Stock validation failed: ${errorData}`);
      }

      const validationData = await validateResponse.json();
      console.log('Stock validated:', validationData);

      // Start investigation with date range
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

      // Try WebSocket connection for real-time updates
      try {
        const wsUrl = `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}${API_ENDPOINTS.websocket(data.investigation_id)}`;
        const ws = new WebSocket(wsUrl);
        setCurrentWebSocket(ws);
        
        ws.onmessage = (event) => {
          const update = JSON.parse(event.data);
          console.log('Received update:', update);

          if (update.type === 'node_update' || update.type === 'node_completed') {
            setNodes(prev => [...prev, update.node]);
          } else if (update.type === 'investigation_complete') {
            console.log('Investigation completed');
            setIsLoading(false);
            ws.close();
          }
        };

        ws.onerror = (error) => {
          console.error('WebSocket error:', error);
        };

        ws.onclose = () => {
          console.log('WebSocket connection closed');
          setIsLoading(false);
          setCurrentWebSocket(null);
        };
      } catch (wsError) {
        console.log('WebSocket not available, investigation will run without real-time updates');
        setIsLoading(false);
      }

      // Set timeout to stop loading after 2 minutes
      timeoutRef.current = setTimeout(() => {
        setIsLoading(false);
        if (currentWebSocket) {
          currentWebSocket.close();
        }
      }, 120000);

    } catch (error) {
      console.error('Investigation failed:', error);
      setIsLoading(false);
      
      // Show error node
      const errorNode: AgentNode = {
        id: 'error',
        label: '❌ Investigation Error',
        description: `Failed to investigate ${symbol}: ${error}`,
        status: 'error',
        type: 'error',
        data: { error: String(error) },
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
      const response = await fetch(API_ENDPOINTS.langchainDemo('AAPL'), {
        method: 'POST',
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
            🚀 AEGIS Stock Investigation System
          </h1>
          <p className="text-blue-200 text-lg">
            LangChain-Enhanced AI Stock Investigation Platform
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
                <h3 className="text-white font-semibold mb-3">📊 Investigation Status</h3>
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
