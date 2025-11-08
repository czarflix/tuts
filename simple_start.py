"""
Simple starter - just runs the FastAPI app
"""
import uvicorn

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 Starting Job Application Automation System")
    print("="*60)
    print("\n📍 Local URL: http://localhost:8001")
    print("\n💡 Tips:")
    print("  1. Make sure your transform-resume server is running on port 8000")
    print("  2. Upload a job posting screenshot via the web interface")
    print("  3. System will auto-populate Excel and transform your resume")
    print("\n" + "="*60 + "\n")

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=False)
