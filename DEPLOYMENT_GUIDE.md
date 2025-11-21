# 🚀 Deployment Guide

This guide covers deploying the Pluggable Rule Engine to various hosting platforms.

## Table of Contents
1. [Render Deployment](#render-deployment)
2. [Railway Deployment](#railway-deployment)
3. [Heroku Deployment](#heroku-deployment)
4. [DigitalOcean App Platform](#digitalocean-app-platform)
5. [Environment Variables](#environment-variables)
6. [Post-Deployment](#post-deployment)

---

## Render Deployment

### One-Click Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Manual Deployment

1. **Create a Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository: `pluggable-rule-engine`

3. **Configure Service**
   ```
   Name: pluggable-rule-engine
   Environment: Python
   Branch: main
   Build Command: sh build.sh
   Start Command: gunicorn config.wsgi:application
   ```

4. **Add Environment Variables**
   ```
   SECRET_KEY=<generate-a-secure-key>
   DEBUG=False
   ALLOWED_HOSTS=<your-app-url>.onrender.com
   PYTHON_VERSION=3.11.0
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (~3-5 minutes)
   - Access your app at `https://<your-app>.onrender.com`

### Generate SECRET_KEY

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Railway Deployment

### One-Click Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

### Manual Deployment

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `pluggable-rule-engine`

3. **Configure Environment Variables**
   ```
   SECRET_KEY=<secure-key>
   DEBUG=False
   ALLOWED_HOSTS=*
   ```

4. **Railway will automatically**:
   - Detect Python environment
   - Run migrations
   - Start the server

5. **Generate Domain**
   - Go to Settings → Domains
   - Click "Generate Domain"
   - Your app: `https://<your-app>.railway.app`

---

## Heroku Deployment

### Prerequisites
```bash
# Install Heroku CLI
# Windows: https://devcenter.heroku.com/articles/heroku-cli
# Mac: brew tap heroku/brew && brew install heroku
# Linux: curl https://cli-assets.heroku.com/install.sh | sh
```

### Deployment Steps

1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create Heroku App**
   ```bash
   cd pluggable-rule-engine
   heroku create your-app-name
   ```

3. **Add Buildpack**
   ```bash
   heroku buildpacks:set heroku/python
   ```

4. **Configure Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=.herokuapp.com
   ```

5. **Create Procfile**
   ```bash
   echo "web: gunicorn config.wsgi:application --log-file -" > Procfile
   ```

6. **Deploy**
   ```bash
   git add Procfile
   git commit -m "Add Procfile for Heroku"
   git push heroku main
   ```

7. **Run Migrations**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py seed_orders
   ```

8. **Open App**
   ```bash
   heroku open
   ```

---

## DigitalOcean App Platform

### Deployment Steps

1. **Create DigitalOcean Account**
   - Go to [digitalocean.com](https://www.digitalocean.com)
   - Create account

2. **Create New App**
   - Go to Apps
   - Click "Create App"
   - Choose GitHub
   - Select repository

3. **Configure Build**
   ```
   Build Command: pip install -r requirements.txt && python manage.py collectstatic --noinput
   Run Command: gunicorn --worker-tmp-dir /dev/shm config.wsgi
   ```

4. **Add Environment Variables**
   ```
   SECRET_KEY=<secure-key>
   DEBUG=False
   ALLOWED_HOSTS=<your-app>.ondigitalocean.app
   ```

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DEBUG` | Debug mode (always False in production) | `False` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `example.com,*.example.com` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | SQLite |
| `DJANGO_LOG_LEVEL` | Logging level | `INFO` |

### PostgreSQL Setup (Optional)

For production with PostgreSQL:

1. **Add to requirements.txt**
   ```
   psycopg2-binary==2.9.9
   ```

2. **Set DATABASE_URL**
   ```
   postgresql://user:password@host:5432/dbname
   ```

---

## Post-Deployment

### 1. Verify Deployment

```bash
# Check API is running
curl https://your-app.onrender.com/rules/

# Test rule check
curl -X POST https://your-app.onrender.com/rules/check/ \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1, "rules": ["min_total_100"]}'
```

### 2. Access Admin Panel

1. Create superuser (if platform allows shell):
   ```bash
   python manage.py createsuperuser
   ```

2. Access admin:
   ```
   https://your-app.onrender.com/admin/
   ```

### 3. Monitor Logs

**Render:**
```bash
# View logs in dashboard or
render logs -f
```

**Railway:**
```bash
# View in dashboard
```

**Heroku:**
```bash
heroku logs --tail
```

### 4. Check Health

Navigate to:
- Swagger UI: `https://your-app/`
- ReDoc: `https://your-app/redoc/`
- Rules List: `https://your-app/rules/`

### 5. Seed Database (if needed)

If your build script didn't run seeding:

**Render:**
```bash
# Use Render Shell
python manage.py seed_orders
```

**Heroku:**
```bash
heroku run python manage.py seed_orders
```

**Railway:**
```bash
# Use Railway CLI or dashboard shell
python manage.py seed_orders
```

---

## Troubleshooting

### Issue: Static Files Not Loading

**Solution:**
```bash
python manage.py collectstatic --noinput
```

Ensure `STATIC_ROOT` is set in settings.py

### Issue: Database Not Migrated

**Solution:**
```bash
python manage.py migrate
```

### Issue: SECRET_KEY Error

**Solution:**
Generate new key and set environment variable:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Issue: ALLOWED_HOSTS Error

**Solution:**
Add your domain to ALLOWED_HOSTS:
```bash
# For Render
ALLOWED_HOSTS=your-app.onrender.com

# For Railway
ALLOWED_HOSTS=your-app.railway.app

# For multiple domains
ALLOWED_HOSTS=domain1.com,domain2.com,*.example.com
```

---

## Custom Domain

### Render

1. Go to Settings → Custom Domains
2. Add your domain
3. Update DNS:
   ```
   CNAME: your-domain.com → your-app.onrender.com
   ```

### Railway

1. Go to Settings → Domains
2. Add custom domain
3. Update DNS as instructed

### Heroku

1. Add domain:
   ```bash
   heroku domains:add www.example.com
   ```
2. Configure DNS as instructed

---

## SSL/HTTPS

All platforms provide free SSL certificates:
- **Render**: Automatic
- **Railway**: Automatic
- **Heroku**: Automatic
- **DigitalOcean**: Automatic with Let's Encrypt

---

## Scaling

### Vertical Scaling (Upgrade Plan)

**Render:**
- Starter: $7/month
- Standard: $25/month

**Railway:**
- Pay per usage
- ~$5-20/month typical

**Heroku:**
- Hobby: $7/month
- Standard: $25-50/month

### Horizontal Scaling

All platforms support multiple dynos/instances:

```bash
# Heroku
heroku ps:scale web=2

# Render/Railway: Use dashboard
```

---

## Monitoring

### Built-in Monitoring

- **Render**: Dashboard metrics
- **Railway**: Resource usage
- **Heroku**: Metrics add-on

### External Monitoring

Consider adding:
- **Sentry** for error tracking
- **LogDNA** for log management
- **New Relic** for APM

---

## Backup

### Database Backup

**Heroku:**
```bash
heroku pg:backups:capture
heroku pg:backups:download
```

**Render/Railway:**
- Use platform backup features
- Or manually dump database

---

## Cost Estimation

### Free Tier (Limited)

- **Render**: Free tier available (sleeps after inactivity)
- **Railway**: $5 free credit/month
- **Heroku**: No longer offers free tier

### Production (Recommended)

- **Render Starter**: $7/month
- **Railway**: ~$5-10/month (usage-based)
- **DigitalOcean**: $5/month (basic droplet)

---

## Next Steps

1. ✅ Deploy to platform
2. ✅ Configure custom domain
3. ✅ Set up monitoring
4. ✅ Configure backups
5. ✅ Add authentication (if needed)
6. ✅ Scale as needed

---

**Need Help?**
- Check platform documentation
- Review logs for errors
- Open an issue on GitHub
- Contact support

**Happy Deploying! 🚀**
