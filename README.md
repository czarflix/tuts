# Job Application Automation System

Automate your job application process with AI! Upload a job posting screenshot, and the system will:

1. 📸 Extract job details using Vision LLM (Gemini)
2. 🔍 Enhance job description via web search
3. 📊 Auto-populate Excel with all details
4. 📝 Generate tailored resume using your transform-resume endpoint
5. 🔗 Embed downloadable resume link in Excel

## Features

- **Screenshot Parsing**: Uses Gemini Vision to extract job title, company, description, compensation, role type, and application details
- **Smart Enhancement**: Searches the web to find complete job descriptions if the screenshot has abbreviated info
- **Excel Integration**: Automatically maintains a beautiful Excel sheet with all job applications
- **Resume Transformation**: Calls your local `/transform-resume/` endpoint to generate tailored resumes
- **Remote Access**: Use ngrok tunneling to share with others (like your girlfriend!)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional (for web search enhancement)
GOOGLE_SEARCH_API_KEY=your_google_search_api_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id

# Transform Resume Endpoint (default: http://127.0.0.1:8000/transform-resume/)
TRANSFORM_RESUME_URL=http://127.0.0.1:8000/transform-resume/

# Optional (for ngrok tunneling)
NGROK_AUTH_TOKEN=your_ngrok_token
```

### 3. Prepare Your Base Resume

Place your base resume as `resumes/base_resume.pdf`, or upload it via the web interface.

### 4. Start Your Transform-Resume Server

Make sure your transform-resume endpoint is running:

```bash
# In your transform-resume project directory
python your_server.py  # or however you start it
```

It should be accessible at `http://127.0.0.1:8000/transform-resume/`

## Usage

### Option 1: Local Use Only

```bash
python main.py
```

Visit: `http://localhost:8001`

### Option 2: Remote Access (Share with Others)

```bash
python start_with_tunnel.py
```

This will:
- Start the app on port 8001
- Create an ngrok tunnel
- Display a public URL you can share

Example output:
```
🚀 Job Application Automation System Started!
📍 Local URL: http://localhost:8001
🌐 Public URL: https://abc123.ngrok.io
```

Share the public URL with your girlfriend, and she can use the system remotely!

### Option 3: Manual Start

```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

## How to Use the Web Interface

1. **Upload Base Resume** (Optional)
   - Upload your default resume PDF
   - This will be used for all job applications unless you specify otherwise

2. **Process Job Posting**
   - Upload a screenshot of the job posting
   - Check "Automatically transform resume" if you want a tailored resume
   - Optionally upload a custom resume for this specific job
   - Click "Process Job Posting"

3. **Download Excel**
   - Click "Download Excel Sheet" to get the Excel file with all your applications

## Excel Sheet Structure

The generated Excel file contains:

| Date Added | Company | Job Title | Role Type | Compensation | Job Description | Application Link | Application Method | Email Subject | Resume Link | Status |
|------------|---------|-----------|-----------|--------------|-----------------|------------------|-------------------|---------------|-------------|--------|
| 2025-11-08 | Google  | SWE Intern | Intern   | $50/hr       | Full description... | https://... | Website URL | - | [Download](#) | Resume Generated |

## API Endpoints

### `POST /process-job-posting/`

Process a job posting screenshot.

**Parameters:**
- `screenshot` (file): Job posting screenshot (required)
- `auto_transform_resume` (bool): Whether to transform resume (default: true)
- `base_resume` (file): Custom resume for this job (optional)

**Response:**
```json
{
  "success": true,
  "message": "Job posting processed successfully!",
  "job_data": {
    "company": "Google",
    "job_title": "Software Engineering Intern",
    "job_description": "...",
    "compensation": "$50/hour",
    "role_type": "Intern",
    "application_link": "https://...",
    "application_method": "Website URL",
    "email_subject": ""
  },
  "excel_row": 2,
  "resume_info": {
    "download_link": "http://...",
    "file_path": "..."
  }
}
```

### `POST /upload-base-resume/`

Upload a base resume.

**Parameters:**
- `resume` (file): PDF resume

### `GET /download-excel/`

Download the Excel file.

## Project Structure

```
tuts/
├── main.py                 # FastAPI application
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── start_with_tunnel.py   # Start with ngrok
├── .env                   # Environment variables
├── .env.example          # Example env file
├── README.md             # This file
├── services/
│   ├── __init__.py
│   ├── vision_service.py    # Gemini Vision integration
│   ├── search_service.py    # Web search for job descriptions
│   ├── excel_service.py     # Excel automation
│   └── resume_service.py    # Transform-resume integration
├── frontend/
│   └── index.html          # Web interface
├── uploads/               # Job posting screenshots
├── resumes/              # Resume files
│   └── base_resume.pdf   # Your base resume
└── job_applications.xlsx # Generated Excel file
```

## How It Works

### 1. Screenshot Parsing (Vision LLM)

The system uses **Gemini 2.0 Flash** (vision model) to analyze job posting screenshots and extract:
- Job title
- Company name
- Job description
- Compensation
- Role type (Intern/Full-time/etc.)
- Application link or email
- Email subject (if applicable)

### 2. Job Description Enhancement

If the job description appears incomplete (< 200 chars or marked as incomplete), the system:

**With Google Search API:**
- Searches for the complete job posting online
- Scrapes the full description from career pages
- Uses LLM to extract and format the description

**Without Google Search API (fallback):**
- Uses LLM to generate a comprehensive description
- Based on typical responsibilities for that role at that company
- Heavily customized and realistic

### 3. Excel Population

Creates/updates an Excel sheet with:
- Formatted headers
- Clickable links
- Wrapped text for descriptions
- Status tracking
- Professional styling

### 4. Resume Transformation

Calls your local `/transform-resume/` endpoint with:
- The job description
- Target job title
- Your base resume
- AI multiplier and other parameters

The transformed resume link is embedded in the Excel sheet.

## Remote Access Explained

Your transform-resume endpoint runs on `127.0.0.1:8000` (localhost). When you use ngrok:

1. **Your Machine**: `127.0.0.1:8001` → This app
2. **Ngrok Tunnel**: `https://abc123.ngrok.io` → `127.0.0.1:8001`
3. **Your Girlfriend**: Accesses `https://abc123.ngrok.io`
4. **Transform Resume**: This app calls `127.0.0.1:8000` from YOUR machine

So even though she's remote, the resume transformation happens on YOUR local machine!

## Troubleshooting

### "Base resume not found"
Upload your base resume via the web interface or place it at `resumes/base_resume.pdf`.

### "Error calling transform-resume endpoint"
Make sure your transform-resume server is running on `http://127.0.0.1:8000`.

### "Invalid API key"
Check your `.env` file and ensure `GEMINI_API_KEY` is set correctly.

### Ngrok tunnel disconnects
Free ngrok tunnels expire after 2 hours. Restart the app to get a new URL, or upgrade to ngrok paid plan.

## API Keys

### Gemini API Key (Required)
Get it from: https://makersuite.google.com/app/apikey

### Google Search API (Optional)
1. Go to: https://console.cloud.google.com/
2. Enable "Custom Search API"
3. Create credentials (API key)
4. Create a custom search engine: https://cse.google.com/cse/all

### Ngrok Auth Token (Optional, for remote access)
Get it from: https://dashboard.ngrok.com/get-started/your-authtoken

## License

MIT

## Author

Built with ❤️ for automating job applications!
