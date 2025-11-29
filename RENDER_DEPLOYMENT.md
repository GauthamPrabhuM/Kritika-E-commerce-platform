# Kritika E-commerce Platform — Deployment on Render.com

Deploy your Flask app to Render.com with free tier in **5 minutes**! 🚀

## Prerequisites

- GitHub account (already have one ✅)
- Render.com account (free)
- Your code pushed to GitHub (already done ✅)

## Step-by-Step Deployment

### Step 1: Create a Render Account

1. Go to **https://render.com** (make sure you're not logged in)
2. Click **"Sign Up"**
3. Sign up with your **GitHub account** (easiest option)
   - This will allow Render to access your repositories
4. Authorize Render to access your GitHub account

### Step 2: Connect Your Repository

1. After signing in, click **"New +"** button (top right)
2. Select **"Web Service"**
3. Under "Public repositories," find **Kritika-E-commerce-platform**
   - If you don't see it, click "Connect account" to link your GitHub
4. Select the repository and click **"Connect"**

### Step 3: Configure the Web Service

Fill in the form with these values:

| Field | Value |
|-------|-------|
| **Name** | `kritika-ecommerce` (or any name you prefer) |
| **Environment** | `Python 3` |
| **Region** | `Oregon` (or closest to you) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn -w 4 -b 0.0.0.0:8080 main:app` |
| **Plan** | `Free` |

### Step 4: Set Environment Variables (Optional but Recommended)

Click **"Advanced"** section and add:

```
FLASK_ENV=production
FLASK_DEBUG=0
```

### Step 5: Deploy!

1. Click **"Create Web Service"**
2. Render will automatically:
   - Pull your code from GitHub
   - Install dependencies from `requirements.txt`
   - Start your Flask app with gunicorn
   - Assign you a URL like: `https://kritika-ecommerce.onrender.com`

3. **Wait 2-3 minutes** for deployment to complete
   - You'll see a progress log in the dashboard
   - When it says "Build successful" and "Live", you're done! ✅

### Step 6: Access Your Live App

Your app is now live at: **`https://YOUR-APP-NAME.onrender.com`**

Visit it and test all features:
- ✅ Browse products
- ✅ Register/Login
- ✅ Add to cart
- ✅ Checkout
- ✅ Admin panel (with admin credentials)

## Important Notes

### Database
- Your SQLite database (`database.db`) will persist on Render's free tier
- Data is stored between restarts

### Cold Starts
- Free tier apps go to sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds (normal)
- After that, responses are instant

### Scaling
- When ready to upgrade:
  - Go to your service settings
  - Click "Change Plan"
  - Choose "Paid" tier for guaranteed uptime

## Troubleshooting

### "Build Failed" Error
Check the build logs:
1. Click your service name
2. Scroll to "Logs" tab
3. Look for error messages
4. Common fixes:
   - Ensure all dependencies are in `requirements.txt`
   - Check Python version compatibility

### "Application Error" After Deploy
1. Click "Logs" tab
2. Look for Python stack traces
3. Most common: missing imports or SQLite path issues

### Database Issues
If database.db is not found:
1. Render uses `/var/data/` for persistent storage
2. Our app uses relative path `./database.db` (works fine)
3. If needed, create database on first run

## Auto-Deployment

Every time you push to GitHub `main` branch:
1. Render automatically detects changes
2. Rebuilds and deploys automatically
3. No manual intervention needed!

## Custom Domain (Optional)

To add your own domain:
1. In Render dashboard, click your service
2. Go to "Settings" tab
3. Scroll to "Custom Domain"
4. Enter your domain and follow DNS instructions

## Next Steps

1. **[Deploy now](https://render.com)** 🚀
2. **Test your live app** with all features
3. **Share your URL** with others
4. **Make code changes** and push to GitHub for auto-deployment

## Need Help?

- Render docs: https://render.com/docs
- Flask docs: https://flask.palletsprojects.com
- Check your service logs for errors

---

**Your app will be live in ~5 minutes!** 🎉

Good luck! If you have issues, check the logs on Render dashboard.
