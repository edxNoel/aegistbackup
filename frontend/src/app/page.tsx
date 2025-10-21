export default function Home() {
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
          <div className="mt-6 bg-gray-800 rounded-lg p-6">
            <h3 className="text-white font-semibold mb-3">🔧 System Status</h3>
            <div className="space-y-2 text-sm">
              <p className="text-green-400">✅ Next.js Frontend: Active</p>
              <p className="text-green-400">✅ LangChain Integration: Ready</p>
              <p className="text-green-400">✅ Deployment: Successful</p>
              <p className="text-blue-400">🔗 Version: 1.0.0 with LangChain</p>
            </div>
            <div className="mt-4">
              <a 
                href="/api/health" 
                className="inline-block bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition-colors"
              >
                Test API Health
              </a>
            </div>
          </div>
        </header>
      </div>
    </main>
  );
}
