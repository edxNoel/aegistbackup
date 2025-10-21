# Deploying AEGIS with LangChain to Vercel

## Quick Deployment Steps

### 1. Connect Repository to Vercel
- Go to [vercel.com/new](https://vercel.com/new)
- Import your GitHub repository: `edxNoel/aegistbackup`
- Select the repository and click "Import"

### 2. Configure Build Settings
- **Framework Preset**: Next.js
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

### 3. Environment Variables
Add these environment variables in Vercel dashboard:

```
ANTHROPIC_API_KEY=your_claude_api_key_here
NEXT_PUBLIC_API_URL=https://your-app.vercel.app
```

### 4. Deployment Configuration
The project includes:
- ✅ `vercel.json` - Routing configuration
- ✅ `package.json` with vercel-build script
- ✅ Python requirements for serverless functions
- ✅ LangChain dependencies included

### 5. Test the Deployment
After deployment, test these endpoints:
- `GET /` - Main application
- `GET /api/health` - Health check
- `POST /api/langchain-demo/AAPL` - LangChain demo
- `POST /api/investigate` - Full investigation

### 6. LangChain Features Available
- ✅ Real-time web search (DuckDuckGo)
- ✅ News sentiment analysis
- ✅ Earnings investigation
- ✅ Market context analysis
- ✅ Confidence scoring
- ✅ Intelligent fallbacks

## Troubleshooting

### If Build Fails:
1. Check the build logs in Vercel dashboard
2. Ensure all dependencies are in requirements.txt
3. Verify Python runtime compatibility

### If LangChain APIs Don't Work:
- DuckDuckGo search may be rate-limited (normal behavior)
- Fallback demo data will be returned automatically
- Check function logs for specific errors

### Common Issues:
- **Import errors**: Check relative import paths
- **Package conflicts**: Ensure compatible versions
- **Timeout issues**: LangChain searches may take 10-30 seconds

## Monitoring
- Check Vercel function logs for LangChain execution
- Monitor API response times
- Watch for rate limiting messages from DuckDuckGo