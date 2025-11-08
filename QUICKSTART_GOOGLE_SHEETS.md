# 🚀 Quick Start: Google Sheets Integration

**Want both you AND your girlfriend to see job applications in real-time?**

This 5-minute setup connects your job automation system to Google Sheets!

## 📊 What You Get

✅ **Real-time updates** - Both see changes instantly
✅ **Cloud access** - View from anywhere
✅ **Automatic sync** - No manual uploads
✅ **Clickable links** - Resumes and applications
✅ **Local backup** - Excel file still created

## ⚡ Quick Setup (5 minutes)

### Step 1: Enable Google Sheets API

1. Go to: https://console.cloud.google.com/
2. Create new project: "Job App Automation"
3. Enable these APIs:
   - **Google Sheets API**
   - **Google Drive API**

### Step 2: Create Service Account

1. Go to: **APIs & Services** → **Credentials**
2. Click: **Create Credentials** → **Service Account**
3. Name: `job-app-automation`
4. Click: **Create** and then **Done**

### Step 3: Download Credentials

1. Click on your service account
2. Go to **Keys** tab
3. Click: **Add Key** → **Create new key** → **JSON**
4. File downloads automatically!

### Step 4: Install Credentials

```bash
# Rename and move the downloaded file
mv ~/Downloads/job-app-*.json /home/user/tuts/credentials.json
```

### Step 5: Get Service Account Email

```bash
# View the credentials file
cat /home/user/tuts/credentials.json | grep client_email
```

Copy that email (looks like: `job-app-automation@xxx.iam.gserviceaccount.com`)

### Step 6: Start the App

```bash
cd /home/user/tuts
python simple_start.py
```

You'll see:
```
📊 Storage Services Status:
  Excel: ✅ Always enabled (local backup)
  Google Sheets: ✅ Enabled
  Sheet URL: https://docs.google.com/spreadsheets/d/...
```

### Step 7: Share the Sheet

1. **Copy the Sheet URL** from the startup message
2. **Open it** in your browser
3. Click **Share**
4. **Paste the service account email** from Step 5
5. Give it **Editor** access
6. Uncheck "Notify people"
7. Click **Share**

### Step 8: Share with Your Girlfriend

1. Click **Share** again (in the Google Sheet)
2. Add **her email address**
3. Give her **Editor** access
4. Click **Send**

**Done!** 🎉

## 🎯 How to Use

Just use the system normally:

1. Upload job screenshot
2. System automatically:
   - ✅ Saves to **Excel** (local backup)
   - ✅ Saves to **Google Sheets** (cloud)
3. Both you and your girlfriend see it!

## 📱 Access Google Sheets

**From the web interface:**
- After processing a job, click "📊 Open Google Sheets"

**Direct link:**
- Use the URL from startup message
- Or find it in Google Drive

## 🔧 Troubleshooting

### "Google Sheets: ⚠️ Disabled"

Make sure `credentials.json` exists:
```bash
ls /home/user/tuts/credentials.json
```

If not, go back to Step 3-4.

### "Permission Denied"

You forgot to share the sheet! Go back to Step 7.

### Want to disable Google Sheets?

In `.env`:
```env
GOOGLE_SHEETS_ENABLED=false
```

## 💡 Pro Tips

1. **Bookmark the sheet** - Quick access for both of you

2. **Add custom columns** - Status, notes, interview dates

3. **Use filters** - Sort by company, role type, etc.

4. **Mobile access** - Open in Google Sheets app

5. **Offline mode** - Download Excel for offline work

## 🌟 Benefits

**For You:**
- Process jobs via screenshots
- Everything saves automatically
- Local Excel backup

**For Your Girlfriend:**
- See all applications in real-time
- Click resume links to download
- Add notes and feedback
- No software needed!

**Together:**
- Collaborate on job search
- Track application progress
- Stay organized!

---

**Full detailed guide:** See `GOOGLE_SHEETS_SETUP.md`

**Just want it to work?** Follow the 8 steps above - 5 minutes total! 🚀
