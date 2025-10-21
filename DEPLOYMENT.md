# Vercel Deployment Guide

## Prerequisites
1. **GitHub Repository**: Push your code to GitHub
2. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
3. **OpenAI API Key**: Get one from [OpenAI](https://platform.openai.com/api-keys)

## Step-by-Step Deployment

### 1. **Push to GitHub**
```bash
# Ensure all changes are committed and pushed
git add .
git commit -m "Ready for Vercel deployment"
git push origin main
```

### 2. **Deploy to Vercel**
1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will auto-detect it as a Next.js project
5. **Important**: Set these configurations:
   - **Framework Preset**: Next.js
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: `npm run vercel-build`
   - **Output Directory**: `frontend/.next`

### 3. **Environment Variables**
In your Vercel project dashboard:
1. Go to **Settings** → **Environment Variables**
2. Add these variables:
   ```
   OPENAI_API_KEY = your_actual_openai_api_key
   PYTHON_VERSION = 3.11
   ```

### 4. **Deploy**
1. Click **Deploy**
2. Wait for deployment to complete (~3-5 minutes)
3. Your app will be live at `https://your-project-name.vercel.app`

## Configuration Details

### **File Structure for Vercel**
```
├── vercel.json          # Deployment configuration
├── package.json         # Root build scripts
├── frontend/            # Next.js app
│   ├── package.json
│   └── next.config.ts   # Production optimizations
└── backend/             # FastAPI backend
    ├── main.py          # API routes
    └── requirements.txt
```

### **API Routing**
- Frontend: `https://your-app.vercel.app`
- Backend API: `https://your-app.vercel.app/api/*`
- WebSocket: `wss://your-app.vercel.app/ws/*`

## Important Notes

1. **Environment Variables**: Make sure to add your OpenAI API key in Vercel settings
2. **WebSocket Limitations**: Vercel has a 10-second timeout for WebSocket connections
3. **Cold Starts**: First request might be slower due to serverless cold starts
4. **Function Timeout**: Set to 30 seconds in vercel.json for AI processing

## Troubleshooting

### **Build Errors**
- Check that all dependencies are in `frontend/package.json`
- Ensure TypeScript errors are resolved
- Verify Tailwind CSS v3 is being used (not v4)

### **API Not Working**
- Verify environment variables are set correctly
- Check Vercel function logs in the dashboard

### **WebSocket Issues**
- WebSocket connections may timeout - consider polling as fallback
- Check browser console for connection errors

## Recent Fixes Applied

### **Build Configuration**
- ✅ Fixed Tailwind CSS v4 → v3 compatibility issues
- ✅ Removed `--turbopack` flag from build command
- ✅ Updated PostCSS configuration for stable deployment
- ✅ Added proper `outputFileTracingRoot` for monorepo

### **Dependencies**
- ✅ Stable Tailwind CSS v3.4 (no more lightningcss conflicts)
- ✅ Standard PostCSS and Autoprefixer setup
- ✅ Next.js 15.5.6 with proper configuration

## Success!
Your AI Stock Investigation System should now be live and accessible worldwide!

**Features Available:**
- Real-time AI agent investigation
- Interactive node visualization  
- Comprehensive stock analysis
- Professional investment reports
- Responsive design for all devices