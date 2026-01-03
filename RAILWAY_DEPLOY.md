# 🚂 Railway Deployment Guide

Railway is MUCH better for PDF compression than Vercel! Here's why:

✅ **No serverless limitations**  
✅ **Handles large files** (up to 200 MB)  
✅ **Longer execution times** (no 10 second timeout)  
✅ **More memory available**  
✅ **FREE tier with $5 monthly credit**  
✅ **All libraries work properly** (pikepdf included)

---

## 🚀 Deploy to Railway (5 Minutes)

### Step 1: Go to Railway

**Visit**: https://railway.app

Click **"Start a New Project"**

### Step 2: Sign In

- Click **"Login with GitHub"**
- Authorize Railway to access your GitHub account

### Step 3: Create New Project

1. Click **"Deploy from GitHub repo"**
2. If this is your first time:
   - Click **"Configure GitHub App"**
   - Select **"draphael123/pdfcompress"** repository
   - Click **"Install & Authorize"**
3. Select **"draphael123/pdfcompress"** from the list

### Step 4: Deploy

1. Railway will automatically:
   - ✅ Detect it's a Python project
   - ✅ Read the configuration files
   - ✅ Install dependencies
   - ✅ Start the app with gunicorn

2. **Wait 2-3 minutes** for the build to complete

3. You'll see: **"Building"** → **"Deploying"** → **"Active"**

### Step 5: Get Your URL

1. Once deployed, click on your service
2. Go to **"Settings"** tab
3. Scroll to **"Networking"**
4. Click **"Generate Domain"**
5. Your app will be live at: `https://your-app.up.railway.app`

---

## 🎉 That's It!

Your PDF compressor is now live on Railway!

### What You Can Do Now:

✅ **Upload PDFs up to 200 MB**  
✅ **Compress to 199 MB without quality loss**  
✅ **No timeout errors**  
✅ **Full pikepdf support for better compression**  
✅ **Share the URL with anyone**

---

## 📊 Railway Free Tier

Railway gives you **$5 of free usage per month**, which includes:

- ~500 hours of runtime (more than enough for personal use)
- Unlimited deployments
- Custom domains
- Environment variables
- Logs and metrics

**Cost after free tier**: Only ~$0.000463 per minute when app is running

---

## 🔧 Configuration Files (Already Set Up)

Your repository now includes:

- ✅ `railway.json` - Railway configuration
- ✅ `Procfile` - Start command for Railway
- ✅ `nixpacks.toml` - Build configuration
- ✅ `requirements.txt` - Includes gunicorn for production
- ✅ `app.py` - Updated with Railway environment detection

---

## 💡 Railway vs Vercel

| Feature | Railway | Vercel Free |
|---------|---------|-------------|
| **File Upload Size** | 200 MB | 4.5 MB |
| **Execution Time** | ~10 minutes | 10 seconds |
| **Memory** | 8 GB | 1 GB |
| **pikepdf Support** | ✅ Yes | ❌ Usually fails |
| **Best For** | File processing | Static sites/APIs |
| **Free Tier** | $5/month credit | Limited |

**Winner for PDF compression**: 🚂 **Railway**

---

## 🧪 Testing Your Railway App

Once deployed:

1. Open your Railway URL: `https://your-app.up.railway.app`
2. Upload a PDF (can be up to 200 MB!)
3. Set target size (default: 199 MB)
4. Click "Compress PDF"
5. Download your compressed file

### Test Files:

- ✅ Small PDFs (< 10 MB) - Works perfectly
- ✅ Medium PDFs (10-50 MB) - Works great
- ✅ Large PDFs (50-200 MB) - Still works!
- ✅ Very large PDFs (> 200 MB) - May need chunking

---

## 📈 Monitoring Your App

### View Logs:

1. Go to your Railway dashboard
2. Click on your service
3. Go to **"Deployments"** tab
4. Click **"View Logs"**

### Check Usage:

1. Click on your project
2. Go to **"Usage"** tab
3. See your monthly credit usage

---

## 🎨 Custom Domain (Optional)

1. In Railway, go to **"Settings"**
2. Scroll to **"Networking"**
3. Click **"Custom Domain"**
4. Enter your domain (e.g., `pdfcompress.yourdomain.com`)
5. Add the CNAME record to your DNS provider
6. Done!

---

## 🔄 Updating Your App

Railway automatically redeploys when you push to GitHub:

```bash
# Make your changes
git add .
git commit -m "Your changes"
git push origin main
```

Railway will detect the push and redeploy automatically!

---

## 🆘 Troubleshooting

### App won't start?

1. Check the build logs in Railway
2. Make sure all files are committed to GitHub
3. Try redeploying manually in Railway dashboard

### Out of free credits?

Railway will pause your app. Options:
- Wait until next month (credits reset)
- Add a payment method (only pay for what you use)
- Estimated cost: ~$1-3/month for light use

### Upload fails?

- Check Railway logs for errors
- Make sure file is under 200 MB
- Try a smaller file first

---

## 🌟 Railway Features

### Environment Variables (if needed):

1. Go to **"Variables"** tab
2. Add any environment variables
3. Deploy will restart automatically

### Metrics:

- CPU usage
- Memory usage
- Network traffic
- All visible in Railway dashboard

### Logs:

- Real-time logs
- Search and filter
- Download log history

---

## 📦 What's Included

Your Railway deployment includes:

- ✅ **Flask** - Web framework
- ✅ **gunicorn** - Production WSGI server
- ✅ **PyPDF2** - PDF manipulation
- ✅ **pikepdf** - Advanced PDF compression
- ✅ **Beautiful UI** - Modern, responsive design
- ✅ **Auto-cleanup** - Files deleted after download

---

## 🔐 Security

Railway provides:

- ✅ HTTPS by default
- ✅ Automatic SSL certificates
- ✅ DDoS protection
- ✅ Private networking
- ✅ Environment variable encryption

---

## 💰 Pricing After Free Tier

Railway charges only for resources used:

- **Execution**: $0.000463 per minute
- **Memory**: Included in execution
- **Bandwidth**: First 100 GB free

**Example costs**:
- 100 compressions/month: ~$0.50
- 500 compressions/month: ~$2.50
- 1000 compressions/month: ~$5.00

Much more affordable than Vercel Pro ($20/month)!

---

## 🎯 Quick Links

- **Railway Dashboard**: https://railway.app/dashboard
- **Your GitHub Repo**: https://github.com/draphael123/pdfcompress
- **Railway Docs**: https://docs.railway.app
- **Support**: https://help.railway.app

---

## ✅ Deployment Checklist

- [x] Railway account created
- [x] GitHub connected to Railway
- [x] Repository imported
- [x] App deployed
- [x] Domain generated
- [ ] Test with a PDF
- [ ] Share your URL!

---

## 🎊 Success!

Your PDF compressor is now running on Railway with:

- **No serverless limitations**
- **200 MB file support**
- **Fast compression with pikepdf**
- **Beautiful, modern interface**
- **Free hosting (with $5 monthly credit)**

**Enjoy your PDF compressor!** 🚀📄

---

## Next Steps

1. Test your app thoroughly
2. Share the URL with friends
3. Monitor your usage in Railway
4. (Optional) Add a custom domain
5. (Optional) Add more features!

Need help? Check the Railway docs or open an issue on GitHub!


