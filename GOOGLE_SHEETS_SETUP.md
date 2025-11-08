# 📊 Google Sheets Setup Guide

This guide will help you set up Google Sheets integration so you and your girlfriend can access the job applications tracker from anywhere!

## Why Google Sheets?

- ✅ **Real-time collaboration** - Both of you see updates instantly
- ✅ **Access anywhere** - No need to download Excel files
- ✅ **Always in sync** - Automatic updates when you process jobs
- ✅ **Cloud-based** - Never lose your data
- ✅ **Shareable** - Easy to share with anyone

## 🚀 Quick Setup (5 minutes)

### Step 1: Create a Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Click "**Select a project**" → "**New Project**"
3. Name it: `Job Application Automation`
4. Click "**Create**"

### Step 2: Enable Google Sheets API

1. In the project dashboard, click "**Enable APIs and Services**"
2. Search for "**Google Sheets API**"
3. Click on it, then click "**Enable**"
4. Also enable "**Google Drive API**" (search and enable it too)

### Step 3: Create Service Account Credentials

1. Go to "**APIs & Services**" → "**Credentials**"
2. Click "**Create Credentials**" → "**Service Account**"
3. Fill in:
   - **Service account name**: `job-app-automation`
   - **Service account ID**: (auto-filled)
   - Click "**Create and Continue**"
4. **Grant access** (optional): Skip this, click "**Continue**"
5. Click "**Done**"

### Step 4: Create and Download Key

1. Click on the service account you just created
2. Go to "**Keys**" tab
3. Click "**Add Key**" → "**Create new key**"
4. Choose "**JSON**"
5. Click "**Create**"
6. A JSON file will download - **this is your credentials file!**

### Step 5: Setup Credentials in Your Project

1. **Rename** the downloaded file to `credentials.json`
2. **Move** it to your project folder:
   ```bash
   mv ~/Downloads/job-app-automation-*.json /home/user/tuts/credentials.json
   ```
3. **Never share this file** - it's like a password!

### Step 6: Get the Service Account Email

1. Open `credentials.json` in a text editor
2. Find the line with `"client_email"`
3. Copy that email address (looks like: `job-app-automation@xxx.iam.gserviceaccount.com`)
4. **Keep this email** - you'll need it in Step 7!

### Step 7: Share Google Sheet with Service Account

**Option A: Let the system create the sheet (easiest)**

1. Just run the application:
   ```bash
   python simple_start.py
   ```
2. It will create a sheet called "**Job Applications Tracker**"
3. Go to your Google Drive: https://drive.google.com
4. Find the sheet named "**Job Applications Tracker**"
5. Right-click → "**Share**"
6. Paste the service account email from Step 6
7. Give it "**Editor**" access
8. Uncheck "**Notify people**"
9. Click "**Share**"

**Option B: Use existing Google Sheet**

1. Open your existing Google Sheet
2. Click "**Share**" (top right)
3. Paste the service account email from Step 6
4. Give it "**Editor**" access
5. Uncheck "**Notify people**"
6. Click "**Share**"
7. Update `.env` file with your sheet name:
   ```env
   GOOGLE_SHEET_NAME=Your Sheet Name
   ```

### Step 8: Enable in Environment

Your `.env` file should already have:
```env
GOOGLE_SHEETS_ENABLED=true
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_NAME=Job Applications Tracker
```

### Step 9: Test It!

```bash
python simple_start.py
```

Look for this message:
```
📊 Storage Services Status:
  Excel: ✅ Always enabled (local backup)
  Google Sheets: ✅ Enabled
  Sheet URL: https://docs.google.com/spreadsheets/d/...
```

If you see "✅ Enabled", you're good to go!

## 🎯 How It Works

When you process a job posting:

1. **System saves to both**:
   - Local Excel file (backup)
   - Google Sheets (cloud)

2. **You and your girlfriend can**:
   - View the Google Sheet anytime
   - See real-time updates
   - Add notes/comments
   - Track application status

3. **Resume links are clickable** in Google Sheets!

## 📱 Sharing with Your Girlfriend

After setup, share the Google Sheet:

1. Go to https://drive.google.com
2. Find "**Job Applications Tracker**"
3. Click "**Share**"
4. Add her email address
5. Give her "**Editor**" access
6. Click "**Send**"

Now she can:
- View all job applications
- Click resume download links
- Add notes/comments
- Track application status
- See updates in real-time!

## 🔒 Security Notes

### ⚠️ NEVER share these files:
- `credentials.json` - Contains authentication
- `.env` - Contains API keys

### ✅ Safe to share:
- The Google Sheet URL
- Invite people to the sheet via Google's sharing

## 🐛 Troubleshooting

### "Google Sheets: ⚠️ Disabled"

**Cause**: Credentials file not found

**Fix**:
1. Make sure `credentials.json` is in `/home/user/tuts/`
2. Check `.env` has: `GOOGLE_SHEETS_ENABLED=true`
3. Restart the server

### "Permission Denied" when writing to sheet

**Cause**: Service account doesn't have access

**Fix**:
1. Open the Google Sheet
2. Click "Share"
3. Add the service account email (from `credentials.json`)
4. Give "Editor" access
5. Try again

### "Sheet not found"

**Cause**: Sheet name doesn't match

**Fix**:
1. Check the exact name of your Google Sheet
2. Update `.env`:
   ```env
   GOOGLE_SHEET_NAME=Exact Sheet Name Here
   ```
3. Restart server

### Want to disable Google Sheets?

Set in `.env`:
```env
GOOGLE_SHEETS_ENABLED=false
```

The system will only use Excel (local backup).

## 📊 Sheet Structure

The Google Sheet has these columns:

| Column | Description |
|--------|-------------|
| Date Added | When job was processed |
| Company | Company name |
| Job Title | Position title |
| Role Type | Intern/Full-time/etc. |
| Compensation | Salary/stipend |
| Job Description | Full description |
| Application Link | Clickable apply link |
| Application Method | Website/Email |
| Email Subject | Subject if email apply |
| Resume Link | Clickable download link |
| Status | New/Applied/Interview/etc. |
| Notes | Your custom notes |

## 🎨 Customization

### Change Sheet Name

In `.env`:
```env
GOOGLE_SHEET_NAME=My Custom Job Tracker
```

### Use Different Credentials

In `.env`:
```env
GOOGLE_SHEETS_CREDENTIALS_FILE=my-credentials.json
```

### Multiple Sheets

To track jobs in different sheets:
1. Create multiple `.env` files
2. Or manually change `GOOGLE_SHEET_NAME` in `.env`
3. Restart server

## ✨ Benefits

**For You:**
- Process jobs via screenshots
- Auto-populate Google Sheets
- Download tailored resumes
- Track everything in one place

**For Your Girlfriend:**
- View all your applications
- Access from anywhere
- No software needed
- Real-time updates

**Together:**
- Collaborate on job search
- Share notes and feedback
- Track application progress
- Stay organized!

---

**Ready?** Follow the steps above and you'll have Google Sheets working in 5 minutes! 🚀

**Need help?** Check the troubleshooting section or feel free to ask!
