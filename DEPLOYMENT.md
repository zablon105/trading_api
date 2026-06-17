# Deployment Guide: Render + Supabase

This guide walks you through deploying your trading-api application to **Render** using **Supabase** as your database.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Step 1: Prepare Supabase](#step-1-prepare-supabase)
3. [Step 2: Prepare your code](#step-2-prepare-your-code)
4. [Step 3: Connect to Render](#step-3-connect-to-render)
5. [Step 4: Configure Environment Variables](#step-4-configure-environment-variables)
6. [Step 5: Deploy](#step-5-deploy)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- GitHub account with your repository
- Supabase account (free tier available at https://supabase.com)
- Render account (free tier available at https://render.com)

---

## Step 1: Prepare Supabase

### 1.1 Create a Supabase Project
1. Go to https://app.supabase.com
2. Click "New Project"
3. Fill in project details (name, password, region)
4. Wait for project to be created (2-3 minutes)

### 1.2 Get Your Database Connection String
1. In Supabase dashboard, go to **Project Settings** (gear icon)
2. Go to **Database** section
3. Find **Connection string** section
4. Select **URI** tab
5. Copy the connection string (it looks like: `postgresql://postgres:PASSWORD@HOST:5432/postgres`)
6. **Replace `[YOUR-PASSWORD]` in the URL with the actual password you set**

> **IMPORTANT:** This URL is your `DATABASE_URL` - you'll paste it into Render next

---

## Step 2: Prepare Your Code

### 2.1 Verify Settings Configuration
Your `core/settings.py` already supports:
- **Production**: Uses `DATABASE_URL` environment variable (Supabase)
- **Development**: Uses individual `DB_*` variables (local PostgreSQL)

### 2.2 Commit Your Code to Git
```bash
git add .
git commit -m "Add Supabase and Render deployment configuration"
git push origin main
```

---

## Step 3: Connect to Render

### 3.1 Create a Render Web Service
1. Go to https://dashboard.render.com
2. Click **New +** button
3. Select **Web Service**
4. Choose **Connect a repository**
5. Select your GitHub repository (trading-api)
6. Click **Deploy**

### 3.2 Initial Configuration
Render will detect your `render.yaml` file automatically. You should see:
- **Name**: trading-api
- **Environment**: Python
- **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- **Start Command**: `gunicorn core.wsgi:application`

Keep these as-is.

---

## Step 4: Configure Environment Variables

### 4.1 Add DATABASE_URL
1. In your Render service page, go to **Environment** section
2. Click **Add Environment Variable**
3. Key: `DATABASE_URL`
4. Value: Paste your Supabase connection string (from Step 1.2)
5. Click **Save**

### 4.2 Add SECRET_KEY
1. Click **Add Environment Variable** again
2. Key: `SECRET_KEY`
3. Value: Render should have already generated one, but you can create a secure key:
   - Option A: Use Render's generated value
   - Option B: Generate one yourself: Use any online tool or Python: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
4. Click **Save**

### 4.3 Add DEBUG Setting
1. Click **Add Environment Variable**
2. Key: `DEBUG`
3. Value: `False`
4. Click **Save**

### 4.4 (Optional) Add ALLOWED_HOSTS
1. Click **Add Environment Variable**
2. Key: `ALLOWED_HOSTS`
3. Value: Your Render service URL (e.g., `trading-api.onrender.com`)
4. Click **Save**

---

## Step 5: Deploy

### 5.1 Trigger Initial Deployment
Once all environment variables are set:
1. Go to your Render service page
2. Click the **Manual Deploy** button (or just wait - it auto-deploys after config)
3. Watch the deployment logs in real-time

### 5.2 Monitor Logs
1. Go to **Logs** tab to see build and runtime logs
2. Look for:
   - ✅ `pip install -r requirements.txt` - Dependencies installed
   - ✅ `collectstatic` - Static files collected
   - ✅ `migrate` - Database migrations applied
   - ✅ `Listening on port 10000` - App is running

---

## Troubleshooting

### Database Connection Error
**Error**: `OperationalError: could not connect to server`

**Solution**:
1. Verify `DATABASE_URL` is correctly set in Render
2. Check Supabase connection string is not expired
3. Verify Supabase firewall allows Render IPs (usually automatic)
4. Test locally: `python manage.py shell` and run migrations

### Migration Errors
**Error**: `django.db.utils.ProgrammingError` during migrate

**Solution**:
1. Run migrations locally first to verify they work
2. Check Supabase has the `public` schema
3. Verify database user has CREATE TABLE permissions

### Static Files Not Loading
**Error**: CSS/images not showing, 404 errors

**Solution**:
1. WhiteNoise should handle this automatically
2. Verify `STATICFILES_STORAGE` in settings.py
3. Check Render logs for `collectstatic` errors

### Application Won't Start
**Error**: `Failed to start service` or keeps restarting

**Solution**:
1. Check Render logs for specific errors
2. Verify all environment variables are set
3. Test locally: `python manage.py runserver`
4. Check Python version compatibility

---

## Local Development Setup

To test locally before deploying:

```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create local .env file (already exists)
# Update DB_* variables if using local PostgreSQL

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

---

## Environment Variables Reference

| Variable | Example | Purpose |
|----------|---------|---------|
| `DATABASE_URL` | `postgresql://user:pass@host:5432/db` | Supabase connection string |
| `SECRET_KEY` | `abc123...` | Django session encryption key |
| `DEBUG` | `False` | Disable debug mode in production |
| `ALLOWED_HOSTS` | `trading-api.onrender.com` | Allowed domain names |
| `CSRF_TRUSTED_ORIGINS` | `https://trading-api.onrender.com` | Trusted origins for CSRF |

---

## Next Steps

1. ✅ Database is running on Supabase
2. ✅ App is deployed on Render
3. Test your API: `https://your-app.onrender.com/api/trades/`
4. Set up a custom domain (optional)
5. Configure monitoring and logging

---

## Support

- Render docs: https://render.com/docs
- Supabase docs: https://supabase.com/docs
- Django docs: https://docs.djangoproject.com
