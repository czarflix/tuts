# 🚀 Quick Start Guide

## ✅ Setup Complete!

Your Job Application Automation System is ready to use!

## 📋 Before You Start

### 1. Prepare Your Base Resume

Place your resume PDF at: `resumes/base_resume.pdf`

Or upload it via the web interface later.

### 2. Start Your Transform-Resume Server

Make sure your existing transform-resume endpoint is running:

```bash
# In your transform-resume project directory
# Make sure it's running on: http://127.0.0.1:8000/transform-resume/
```

## 🎯 Start the System

### Option 1: Local Use Only

```bash
cd /home/user/tuts
python simple_start.py
```

Then open: **http://localhost:8001**

### Option 2: With Remote Access (for your girlfriend)

```bash
cd /home/user/tuts
python start_with_tunnel.py
```

This will:
- Start the server
- Create an ngrok tunnel
- Display a public URL like: `https://abc123.ngrok.io`
- Share that URL with your girlfriend!

**Note:** For ngrok, you may need to sign up for a free account at https://ngrok.com and add your auth token to `.env`:

```env
NGROK_AUTH_TOKEN=your_token_here
```

## 🎨 How to Use the Web Interface

1. **Open the web interface** at http://localhost:8001

2. **Upload Your Base Resume** (one-time setup)
   - Click "Choose Base Resume (PDF)"
   - Select your resume PDF
   - Click "Save Base Resume"

3. **Process a Job Posting**
   - Take a screenshot of a job posting
   - Click "Choose Job Posting Screenshot"
   - Select your screenshot
   - Make sure "Automatically transform resume" is checked
   - Click "Process Job Posting"

4. **Wait for Magic** ✨
   - System parses the screenshot
   - Enhances job description
   - Adds to Excel
   - Transforms your resume
   - All done in ~30-60 seconds!

5. **Download Excel**
   - Click "Download Excel Sheet"
   - Open the file to see all your applications
   - Resume links are clickable!

## 📸 What to Screenshot

Screenshot the entire job posting including:
- Company name
- Job title
- Job description
- Salary/compensation (if visible)
- "Apply" button/link or email

**Examples of good sources:**
- LinkedIn job postings
- Company career pages
- Indeed listings
- Greenhouse job boards
- Any job posting with clear details

## 📊 Excel Output

Your `job_applications.xlsx` will contain:

| Column | Description |
|--------|-------------|
| Date Added | When you processed this job |
| Company | Company name |
| Job Title | Position title |
| Role Type | Intern/Full-time/Part-time/Contract |
| Compensation | Salary or stipend |
| Job Description | Full, enhanced description |
| Application Link | Where to apply (clickable) |
| Application Method | Website/Email |
| Email Subject | Subject line if applying via email |
| Resume Link | Download your tailored resume (clickable) |
| Status | New/Resume Generated |

## 🔧 Troubleshooting

### "Base resume not found"
→ Upload your resume via the web interface or place it at `resumes/base_resume.pdf`

### "Error calling transform-resume endpoint"
→ Make sure your transform-resume server is running on port 8000
→ Test it: `curl http://127.0.0.1:8000/transform-resume/`

### "Invalid API key"
→ Check your `.env` file - make sure `GEMINI_API_KEY` is set correctly

### Can't access remotely
→ Install ngrok: `pip install pyngrok --break-system-packages`
→ Get auth token from https://dashboard.ngrok.com
→ Add to `.env`: `NGROK_AUTH_TOKEN=your_token`

## 🌟 Pro Tips

1. **Batch Processing**: Process multiple jobs one after another - Excel updates automatically

2. **Custom Resumes**: For special applications, upload a custom resume instead of using the base resume

3. **Description Enhancement**: If Google Search API is configured, the system will search online for complete job descriptions. Otherwise, it uses LLM to create comprehensive descriptions.

4. **Remote Collaboration**: Use ngrok to let your girlfriend process jobs too - all data saves to YOUR Excel file on YOUR machine

## 📱 Remote Access for Girlfriend

When you run `python start_with_tunnel.py`:

```
🌐 Public URL: https://abc123.ngrok.io
```

She can:
1. Open that URL from anywhere
2. Upload job screenshots
3. Get tailored resumes
4. All processing happens on YOUR machine
5. Transform-resume uses YOUR local endpoint

Perfect for long-distance collaboration!

## 🎯 Example Workflow

1. **Morning**: Start the server with `python simple_start.py`

2. **Find Jobs**: Browse LinkedIn, Indeed, company sites

3. **Screenshot**: Take screenshots of interesting postings

4. **Upload**: Batch upload all screenshots via web interface

5. **Review Excel**: Download Excel to see all opportunities

6. **Apply**: Use the tailored resumes and application links in Excel

7. **Track**: Update status in Excel as you apply

## 📧 Need Help?

Check the full README.md for:
- Complete API documentation
- Architecture details
- Advanced configuration
- API key setup guides

---

**You're all set! 🚀**

Start with: `python simple_start.py`
