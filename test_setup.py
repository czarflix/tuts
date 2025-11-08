"""
Quick test to verify setup
"""
import google.generativeai as genai
from config import config

def test_gemini_api():
    """Test if Gemini API key is valid"""
    try:
        genai.configure(api_key=config.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')

        response = model.generate_content("Say 'API key is working!' if you can read this.")

        print("✅ Gemini API Key: WORKING")
        print(f"Response: {response.text}")
        return True

    except Exception as e:
        print(f"❌ Gemini API Error: {str(e)}")
        return False

def test_directories():
    """Check if all directories exist"""
    import os

    dirs = ['uploads', 'resumes', 'frontend']
    all_exist = True

    for d in dirs:
        if os.path.exists(d):
            print(f"✅ Directory '{d}': EXISTS")
        else:
            print(f"❌ Directory '{d}': MISSING")
            all_exist = False

    return all_exist

def test_env():
    """Check if environment variables are set"""
    print("\n🔍 Environment Check:")
    print(f"  GEMINI_API_KEY: {'✅ Set' if config.GEMINI_API_KEY else '❌ Missing'}")
    print(f"  TRANSFORM_RESUME_URL: {config.TRANSFORM_RESUME_URL}")
    print(f"  EXCEL_FILE_PATH: {config.EXCEL_FILE_PATH}")

if __name__ == "__main__":
    print("🧪 Testing Job Application Automation Setup\n")
    print("="*50)

    test_env()
    print("\n" + "="*50)

    print("\n📁 Directory Check:")
    test_directories()

    print("\n" + "="*50)
    print("\n🤖 Gemini API Check:")
    test_gemini_api()

    print("\n" + "="*50)
    print("\n✨ Setup test complete!")
    print("\nNext steps:")
    print("1. Make sure your transform-resume server is running on port 8000")
    print("2. Run: python main.py")
    print("3. Visit: http://localhost:8001")
    print("\nOr for remote access:")
    print("   python start_with_tunnel.py")
