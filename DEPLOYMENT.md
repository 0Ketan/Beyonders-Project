# 🚀 Streamlit Cloud Deployment Guide

## Quick Deployment Steps

### 1. Prepare GitHub Repository

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Campus Assist - Streamlit web app with Google Sheets integration"

# Create main branch
git branch -M main

# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/YOUR_USERNAME/Beyonders-Project.git

# Push to GitHub
git push -u origin main
```

### 2. Deploy on Streamlit Community Cloud

1. **Visit**: [share.streamlit.io](https://share.streamlit.io)

2. **Sign in** with your GitHub account

3. **Click** "New app" button

4. **Fill in the deployment form**:
   - **Repository**: Select `YOUR_USERNAME/Beyonders-Project`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (optional): Choose a custom subdomain

5. **Click** "Deploy!"

6. **Wait** for deployment (usually 2-3 minutes)

7. **Get your live URL**: `https://your-app-name.streamlit.app`

### 3. Share Your App

Once deployed, you'll have a public URL that you can share for your hackathon demo!

---

## Troubleshooting

### Issue: App won't deploy

**Solution**: Check that:
- `requirements.txt` is in the root directory
- `app.py` is in the root directory
- All dependencies are listed in `requirements.txt`

### Issue: Data not loading

**Solution**: Verify that:
- Google Sheets are set to "Anyone with the link → Viewer"
- CSV export URLs are correct in `app.py`
- Internet connection is available

### Issue: App crashes on startup

**Solution**: Check Streamlit Cloud logs:
- Click on "Manage app" in Streamlit Cloud
- View logs for error messages
- Common issues: missing dependencies, incorrect file paths

---

## Updating Your Deployed App

After deployment, any changes you push to GitHub will automatically redeploy:

```bash
# Make your changes to app.py or other files

# Commit changes
git add .
git commit -m "Update: description of changes"

# Push to GitHub
git push

# Streamlit Cloud will automatically redeploy (takes 1-2 minutes)
```

---

## Environment Variables (Optional)

If you need to use secrets (API keys, etc.) in the future:

1. Go to your app in Streamlit Cloud
2. Click "Settings" → "Secrets"
3. Add secrets in TOML format:
   ```toml
   [google]
   api_key = "your-api-key-here"
   ```
4. Access in code:
   ```python
   import streamlit as st
   api_key = st.secrets["google"]["api_key"]
   ```

---

## Performance Tips

1. **Caching**: Already implemented with `@st.cache_data`
2. **Data refresh**: Currently set to 5 minutes (300 seconds)
3. **Optimize images**: Keep images small for faster loading
4. **Minimize dependencies**: Only include necessary packages in `requirements.txt`

---

## Custom Domain (Optional)

Streamlit Cloud provides a free subdomain, but you can also use a custom domain:

1. Purchase a domain (e.g., from Google Domains)
2. In Streamlit Cloud, go to app settings
3. Add your custom domain
4. Update DNS records as instructed

---

## Monitoring Your App

Streamlit Cloud provides:
- **Analytics**: View app usage and visitor stats
- **Logs**: Real-time application logs
- **Resource usage**: Monitor CPU and memory

Access these from the "Manage app" dashboard.

---

**Ready to deploy? Follow the steps above and your app will be live in minutes!**
