from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from datetime import datetime
from typing import Optional

from services.vision_service import VisionService
from services.search_service import SearchService
from services.excel_service import ExcelService
from services.resume_service import ResumeService
from config import config

# Create necessary directories
os.makedirs(config.UPLOAD_DIR, exist_ok=True)
os.makedirs(config.RESUME_DIR, exist_ok=True)

app = FastAPI(title="Job Application Automation System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
vision_service = VisionService()
search_service = SearchService()
excel_service = ExcelService()
resume_service = ResumeService()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the frontend HTML"""
    with open("frontend/index.html", "r") as f:
        return f.read()

@app.post("/process-job-posting/")
async def process_job_posting(
    screenshot: UploadFile = File(...),
    auto_transform_resume: bool = Form(True),
    base_resume: Optional[UploadFile] = File(None)
):
    """
    Main endpoint to process job posting screenshot

    Steps:
    1. Parse screenshot with Vision LLM
    2. Enhance job description with web search
    3. Add to Excel
    4. Optionally transform resume
    5. Update Excel with resume link
    """
    try:
        # Save screenshot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_filename = f"job_posting_{timestamp}.png"
        screenshot_path = os.path.join(config.UPLOAD_DIR, screenshot_filename)

        with open(screenshot_path, "wb") as buffer:
            shutil.copyfileobj(screenshot.file, buffer)

        # Step 1: Parse screenshot
        print("Parsing job posting screenshot...")
        job_data = await vision_service.parse_job_posting(screenshot_path)

        # Step 2: Enhance job description if needed
        print("Enhancing job description...")
        if job_data.get("description_incomplete", False) or len(job_data.get("job_description", "")) < 200:
            enhanced_description = await search_service.find_complete_job_description(
                company=job_data.get("company", ""),
                job_title=job_data.get("job_title", ""),
                partial_description=job_data.get("job_description", "")
            )
            job_data["job_description"] = enhanced_description

        # Step 3: Add to Excel (without resume link initially)
        print("Adding to Excel...")
        row_number = excel_service.add_job_application(job_data, resume_link="")

        resume_info = None

        # Step 4: Transform resume if requested
        if auto_transform_resume:
            try:
                # Determine which resume to use
                if base_resume:
                    # Save uploaded resume temporarily
                    resume_filename = f"temp_resume_{timestamp}.pdf"
                    resume_path = os.path.join(config.RESUME_DIR, resume_filename)
                    with open(resume_path, "wb") as buffer:
                        shutil.copyfileobj(base_resume.file, buffer)
                else:
                    # Use default base resume
                    resume_path = resume_service.get_base_resume_path()

                print("Transforming resume...")
                resume_result = await resume_service.transform_resume(
                    resume_file_path=resume_path,
                    job_description=job_data.get("job_description", ""),
                    target_job_title=job_data.get("job_title", ""),
                    time_in_weeks=1,
                    ai_multiplier=2,
                    model="gemini-2.5-pro"
                )

                resume_info = resume_result

                # Step 5: Update Excel with resume link
                excel_service.update_resume_link(row_number, resume_result.get("download_link", ""))

            except FileNotFoundError as e:
                resume_info = {"error": str(e)}
            except Exception as e:
                resume_info = {"error": f"Resume transformation failed: {str(e)}"}

        return JSONResponse(content={
            "success": True,
            "message": "Job posting processed successfully!",
            "job_data": job_data,
            "excel_row": row_number,
            "excel_path": excel_service.get_excel_path(),
            "resume_info": resume_info
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download-excel/")
async def download_excel():
    """Download the Excel file"""
    excel_path = excel_service.get_excel_path()
    return FileResponse(
        path=excel_path,
        filename="job_applications.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.post("/upload-base-resume/")
async def upload_base_resume(resume: UploadFile = File(...)):
    """Upload a base resume to be used for all job applications"""
    try:
        resume_path = os.path.join(config.RESUME_DIR, "base_resume.pdf")

        with open(resume_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)

        return JSONResponse(content={
            "success": True,
            "message": "Base resume uploaded successfully!",
            "path": resume_path
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Job Application Automation System is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
