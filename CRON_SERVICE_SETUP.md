# 🕐 External Cron Service Setup Guide

## Recommended: cron-job.org

### Step 1: Sign Up
1. Go to https://cron-job.org
2. Click "Register" (free account)
3. Verify your email address

### Step 2: Create Cron Job
1. Login to cron-job.org
2. Click "Create Cronjob"
3. Fill in the details:

**Basic Settings:**
- **Title**: Veelearn Keep-Alive
- **URL**: https://api.veelearn.org/api/health
- **Method**: GET
- **Timeout**: 30 seconds

**Schedule:**
- **Minutes**: */10 (every 10 minutes)
- **Hours**: *
- **Days**: *
- **Months**: *
- **Weekdays**: *

**Advanced:**
- **Timezone**: Your local timezone
- **Email notifications**: Enabled (get alerts on failures)
- **Retry on failure**: 2 times

### Step 3: Test and Save
1. Click "Test" to verify it works
2. Check response: Should show HTTP 200
3. Click "Create Cronjob"

### Step 4: Monitor
- Check "Cronjobs" tab for status
- Look for green checkmarks (successful)
- Red X means failed (check logs)

---

## Alternative: uptimerobot.com

### Setup Steps:
1. Sign up at https://uptimerobot.com
2. Click "Add New Monitor"
3. Select "HTTP(s)"
4. URL: https://api.veelearn.org/api/health
5. Monitor Interval: 5 minutes
6. Alert Contacts: Add your email
7. Click "Create Monitor"

---

## Alternative: cron-monitor.org

### Setup Steps:
1. Sign up at https://cron-monitor.org
2. Create new job
3. URL: https://api.veelearn.org/api/health
4. Schedule: */10 * * * *
5. Notifications: Email alerts
6. Save and test

---

## Testing Your Setup

### Manual Test:
```bash
curl -I https://api.veelearn.org/api/health
```
Should return: `HTTP/2 200`

### Browser Test:
Visit: https://api.veelearn.org/api/health
Should show JSON with status "ok"

---

## Troubleshooting

### If Cron Job Fails:
1. Check if server is running
2. Verify URL is correct
3. Check network connectivity
4. Look at error logs in cron service

### Common Issues:
- **404 Error**: Wrong URL or server down
- **Timeout**: Server starting up (normal during wake-up)
- **Connection Refused**: Server not running
- **SSL Error**: Certificate issues

---

## Recommended Configuration

**Primary**: cron-job.org (every 10 minutes)
**Backup**: uptimerobot.com (every 5 minutes)
**Local**: Python script on your Alienware

This 3-layer system ensures maximum reliability! 🚀
