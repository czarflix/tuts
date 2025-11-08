"""
Start the application with ngrok tunnel for remote access
This allows your girlfriend to access the app even though transform-resume is running locally
"""
import uvicorn
import os
from pyngrok import ngrok, conf
from config import config

def start_with_tunnel():
    """Start the FastAPI app with ngrok tunnel"""

    # Set ngrok auth token if provided
    if config.NGROK_AUTH_TOKEN:
        conf.get_default().auth_token = config.NGROK_AUTH_TOKEN

    # Start ngrok tunnel
    port = 8001
    public_url = ngrok.connect(port, bind_tls=True)

    print("\n" + "="*60)
    print("🚀 Job Application Automation System Started!")
    print("="*60)
    print(f"\n📍 Local URL: http://localhost:{port}")
    print(f"🌐 Public URL (share this): {public_url}")
    print("\nYou can share the public URL with your girlfriend!")
    print("The app will automatically use your local transform-resume endpoint.")
    print("\n" + "="*60 + "\n")

    # Start the FastAPI app
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

if __name__ == "__main__":
    start_with_tunnel()
