# Deployment Guide

This guide will help you deploy the PDF Compressor application to GitHub and Vercel.

## Prerequisites

- Git installed on your system
- GitHub account
- Vercel account (free tier available at [vercel.com](https://vercel.com))
- GitHub CLI or Git configured with your credentials

## Step 1: Push to GitHub

The repository is ready to be pushed to: `https://github.com/draphael123/pdfcompress.git`

### Commands to Push

```bash
# Navigate to your project directory
cd "C:\Users\danie\Downloads\PDF Compression"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit the files
git commit -m "Initial commit: PDF Compressor application"

# Add the remote repository
git remote add origin https://github.com/draphael123/pdfcompress.git

# Push to GitHub
git branch -M main
git push -u origin main
```

If you encounter authentication issues, you may need to use a Personal Access Token (PAT) instead of your password.

## Step 2: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard (Recommended)

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "Add New Project"
3. Import your GitHub repository: `draphael123/pdfcompress`
4. Vercel will automatically detect the configuration from `vercel.json`
5. Click "Deploy"
6. Wait for the deployment to complete
7. Your app will be live at `https://your-project-name.vercel.app`

### Option B: Deploy via Vercel CLI

```bash
# Install Vercel CLI globally
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# For production deployment
vercel --prod
```

## Important Considerations for Vercel Deployment

### ⚠️ Limitations

Vercel has some limitations for serverless functions:

1. **Execution Time**: 
   - Hobby plan: 10 seconds max
   - Pro plan: 60 seconds max (configured in vercel.json)
   - Large PDF compression may exceed these limits

2. **Memory**: 
   - Default: 1024 MB
   - Configured: 3008 MB (requires Pro plan)

3. **Payload Size**: 
   - Request body limit: 4.5 MB (Hobby), 100 MB (Pro)
   - Large file uploads may fail on Hobby plan

4. **File System**: 
   - Only `/tmp` is writable
   - Files in `/tmp` are deleted after function execution

### 💡 Recommendations

**For Production Use:**

If you need to handle very large PDFs (>100MB), consider these alternatives:

1. **Railway** ([railway.app](https://railway.app))
   - Better for long-running processes
   - More memory available
   - Simpler Python deployment

2. **Render** ([render.com](https://render.com))
   - Free tier for web services
   - No execution time limits
   - Great for Flask apps

3. **DigitalOcean App Platform** ([digitalocean.com](https://www.digitalocean.com/products/app-platform))
   - More resources available
   - Better for file processing

4. **Heroku** ([heroku.com](https://heroku.com))
   - Classic PaaS platform
   - Good Flask support

**For Vercel (Best for smaller PDFs):**

- Upgrade to Pro plan for better limits
- Consider breaking large PDFs into chunks
- Add file size warnings in the UI

## Configuration Files Explained

### `vercel.json`
- Configures Python runtime
- Sets memory to 3008 MB (Pro plan)
- Sets max duration to 60 seconds (Pro plan)
- Routes all traffic to Flask app

### `runtime.txt`
- Specifies Python version (3.12.0)

### `.gitignore`
- Prevents temporary files and PDFs from being committed
- Excludes Python cache files

## Environment Variables

No environment variables are required for basic operation. The app automatically detects when running on Vercel via the `VERCEL` environment variable.

## Updating the Deployment

After making changes:

```bash
# Commit your changes
git add .
git commit -m "Your commit message"

# Push to GitHub
git push origin main
```

Vercel will automatically redeploy when you push to the main branch (if you enabled auto-deployment).

## Troubleshooting

### "Execution Timeout" Error
- Your PDF is too large or takes too long to compress
- Consider upgrading to Vercel Pro
- Or use an alternative platform like Railway or Render

### "Payload Too Large" Error
- File exceeds upload limit
- Requires Vercel Pro plan for 100MB limit
- Or use alternative platform

### "Out of Memory" Error
- PDF compression requires more memory
- Requires Vercel Pro plan for increased memory
- Or use alternative platform with more resources

### Deployment Fails
- Check that all dependencies are in `requirements.txt`
- Ensure Python version in `runtime.txt` is supported
- Check Vercel build logs for specific errors

## Testing Locally Before Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py

# Open browser to http://localhost:5000
```

## Post-Deployment

1. Test with a small PDF first (< 10 MB)
2. Monitor Vercel function logs for errors
3. Check execution time in Vercel dashboard
4. Consider adding file size limits in the UI

## Custom Domain (Optional)

1. Go to your Vercel project settings
2. Navigate to "Domains"
3. Add your custom domain
4. Follow Vercel's DNS configuration instructions

## Support

- Vercel Documentation: https://vercel.com/docs
- Flask Documentation: https://flask.palletsprojects.com/
- Issues: Open an issue on the GitHub repository

---

## Quick Deployment Checklist

- [ ] Push code to GitHub
- [ ] Create Vercel account
- [ ] Import GitHub repository in Vercel
- [ ] Deploy and test with small PDF
- [ ] Monitor performance
- [ ] Consider upgrading plan if needed
- [ ] (Optional) Add custom domain

Happy deploying! 🚀

