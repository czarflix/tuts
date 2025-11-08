import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
    GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

    # Transform Resume Endpoint
    TRANSFORM_RESUME_URL = os.getenv("TRANSFORM_RESUME_URL", "http://127.0.0.1:8000/transform-resume/")

    # Excel Configuration
    EXCEL_FILE_PATH = os.getenv("EXCEL_FILE_PATH", "job_applications.xlsx")

    # Ngrok
    NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")

    # Upload settings
    UPLOAD_DIR = "uploads"
    RESUME_DIR = "resumes"

config = Config()
