import google.generativeai as genai
from PIL import Image
from config import config
import json
from typing import Dict, Optional

genai.configure(api_key=config.GEMINI_API_KEY)

class VisionService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    async def parse_job_posting(self, image_path: str) -> Dict:
        """
        Parse job posting screenshot using Gemini Vision.
        Extract: job title, company, job description, compensation, role type, application link/email
        """
        try:
            image = Image.open(image_path)

            prompt = """
            Analyze this job posting screenshot and extract the following information in JSON format:

            {
                "job_title": "The job title/position",
                "company": "Company name",
                "job_description": "Complete job description (as detailed as possible)",
                "compensation": "Salary/compensation mentioned (or 'Not mentioned')",
                "role_type": "Type of role: 'Intern', 'Full-time', 'Part-time', 'Contract', etc.",
                "application_link": "URL to apply (or email address if application is via email)",
                "application_method": "Website URL' or 'Email' or 'Other'",
                "email_subject": "If application is via email, what should be the subject line? Extract from screenshot or suggest based on job title"
            }

            IMPORTANT:
            - For job_description: Extract ALL details visible in the screenshot. Be comprehensive.
            - If the job description seems abbreviated or incomplete, note that in a field called "description_incomplete": true/false
            - For compensation: Look for salary, hourly rate, stipend, or any monetary information
            - For application_link: Look for "Apply Now", "Apply Here", email addresses, or URLs
            - For email_subject: If applying via email, extract or infer the subject line format

            Return ONLY valid JSON, no markdown formatting.
            """

            response = self.model.generate_content([prompt, image])

            # Clean response
            response_text = response.text.strip()

            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            response_text = response_text.strip()

            # Parse JSON
            job_data = json.loads(response_text)

            return job_data

        except Exception as e:
            raise Exception(f"Error parsing job posting: {str(e)}")

    async def enhance_job_description(self, company: str, job_title: str, current_description: str) -> str:
        """
        If the job description seems incomplete, use LLM to suggest enhancements
        based on similar roles at the company.
        """
        try:
            prompt = f"""
            Given this job posting information:
            Company: {company}
            Job Title: {job_title}
            Current Description: {current_description}

            This description might be incomplete. Based on typical responsibilities for this role at this company,
            provide a more detailed and comprehensive job description. Include:
            - Key responsibilities
            - Required qualifications
            - Preferred qualifications
            - Technologies/tools likely used

            Make it professional and realistic. Return ONLY the enhanced description, no JSON.
            """

            response = self.model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            return current_description  # Return original if enhancement fails
