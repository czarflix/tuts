import httpx
import os
from config import config
from typing import Dict

class ResumeService:
    def __init__(self):
        self.transform_url = config.TRANSFORM_RESUME_URL
        self.resume_dir = config.RESUME_DIR
        os.makedirs(self.resume_dir, exist_ok=True)

    async def transform_resume(
        self,
        resume_file_path: str,
        job_description: str,
        target_job_title: str,
        time_in_weeks: int = 1,
        ai_multiplier: int = 2,
        model: str = "gemini-2.5-pro"
    ) -> Dict:
        """
        Call the transform-resume endpoint to generate a tailored resume

        Returns:
        {
            "download_link": "URL to download the resume",
            "file_path": "Local path to the resume"
        }
        """
        try:
            async with httpx.AsyncClient(timeout=300.0) as client:
                # Prepare the multipart form data
                with open(resume_file_path, 'rb') as resume_file:
                    files = {
                        'resume_file': (os.path.basename(resume_file_path), resume_file, 'application/pdf')
                    }

                    data = {
                        'job_description': job_description,
                        'target_job_title': target_job_title,
                        'time_in_weeks': time_in_weeks,
                        'ai_multiplier': ai_multiplier,
                        'model': model
                    }

                    # Call the endpoint
                    response = await client.post(
                        self.transform_url,
                        files=files,
                        data=data
                    )

                    response.raise_for_status()

                    # Parse response
                    result = response.json()

                    return {
                        "download_link": result.get("download_link", ""),
                        "file_path": result.get("file_path", ""),
                        "message": result.get("message", "Resume transformed successfully")
                    }

        except httpx.HTTPError as e:
            raise Exception(f"Error calling transform-resume endpoint: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error transforming resume: {str(e)}")

    def get_base_resume_path(self) -> str:
        """
        Get the path to the user's base resume
        This should be configured or uploaded by the user
        """
        # For now, assume there's a file called "base_resume.pdf" in the resume directory
        base_resume = os.path.join(self.resume_dir, "base_resume.pdf")

        if not os.path.exists(base_resume):
            raise FileNotFoundError(
                f"Base resume not found at {base_resume}. "
                "Please upload your base resume as 'base_resume.pdf' in the resumes directory."
            )

        return base_resume
