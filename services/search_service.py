import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict
from config import config
import google.generativeai as genai

genai.configure(api_key=config.GEMINI_API_KEY)

class SearchService:
    def __init__(self):
        self.search_api_key = config.GOOGLE_SEARCH_API_KEY
        self.search_engine_id = config.GOOGLE_SEARCH_ENGINE_ID
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    async def find_complete_job_description(self, company: str, job_title: str, partial_description: str) -> str:
        """
        Search the web to find the complete job posting and extract full description.
        """
        try:
            # Construct search query
            search_query = f"{company} {job_title} job posting site:linkedin.com OR site:greenhouse.io OR site:{company.lower()}.com/careers"

            # If Google Search API is configured, use it
            if self.search_api_key and self.search_engine_id:
                results = self._google_custom_search(search_query)
            else:
                # Fallback: Use LLM to enhance description based on company and role
                return await self._llm_enhance_description(company, job_title, partial_description)

            # Extract job descriptions from search results
            full_description = await self._extract_from_search_results(results, company, job_title)

            if full_description and len(full_description) > len(partial_description):
                return full_description
            else:
                # Fallback to LLM enhancement
                return await self._llm_enhance_description(company, job_title, partial_description)

        except Exception as e:
            print(f"Search error: {str(e)}")
            # Fallback to LLM enhancement
            return await self._llm_enhance_description(company, job_title, partial_description)

    def _google_custom_search(self, query: str) -> list:
        """Use Google Custom Search API"""
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.search_api_key,
            "cx": self.search_engine_id,
            "q": query,
            "num": 5
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        return data.get("items", [])

    async def _extract_from_search_results(self, results: list, company: str, job_title: str) -> Optional[str]:
        """Extract job description from search results"""
        for result in results:
            try:
                url = result.get("link")
                if not url:
                    continue

                # Fetch the page
                page_response = requests.get(url, timeout=10)
                soup = BeautifulSoup(page_response.content, 'html.parser')

                # Get page text
                page_text = soup.get_text(separator="\n", strip=True)

                # Use LLM to extract job description from page
                description = await self._extract_description_with_llm(page_text, company, job_title)

                if description:
                    return description

            except Exception as e:
                print(f"Error fetching {result.get('link')}: {str(e)}")
                continue

        return None

    async def _extract_description_with_llm(self, page_text: str, company: str, job_title: str) -> Optional[str]:
        """Use LLM to extract job description from scraped page"""
        try:
            # Truncate page text to avoid token limits (keep first 4000 chars)
            truncated_text = page_text[:4000]

            prompt = f"""
            From the following webpage text, extract the complete job description for the {job_title} position at {company}.

            Include:
            - Job responsibilities
            - Requirements and qualifications
            - Preferred qualifications
            - Any other relevant details

            Webpage text:
            {truncated_text}

            Return ONLY the job description, nothing else. If you cannot find a job description, return "NOT_FOUND".
            """

            response = self.model.generate_content(prompt)
            result = response.text.strip()

            if result != "NOT_FOUND" and len(result) > 100:
                return result
            else:
                return None

        except Exception as e:
            print(f"LLM extraction error: {str(e)}")
            return None

    async def _llm_enhance_description(self, company: str, job_title: str, partial_description: str) -> str:
        """
        Use LLM to create a comprehensive job description based on:
        - The partial description
        - Knowledge about similar roles at the company
        - Industry standards for this role
        """
        try:
            prompt = f"""
            You are a job description expert. Create a comprehensive, detailed job description for:

            Company: {company}
            Job Title: {job_title}
            Partial Description: {partial_description}

            Based on the partial description and your knowledge of similar roles at {company}, create a detailed job description that includes:

            1. **Role Overview**: What the position entails
            2. **Key Responsibilities**: 5-8 main responsibilities
            3. **Required Qualifications**: Education, experience, technical skills
            4. **Preferred Qualifications**: Nice-to-have skills
            5. **Technologies/Tools**: Specific technologies likely used in this role
            6. **Company Context**: Brief context about the company and team

            Make it professional, realistic, and heavily customized to this specific company and role.
            The description should be comprehensive (at least 300 words).

            Return ONLY the job description text, no JSON or extra formatting.
            """

            response = self.model.generate_content(prompt)
            enhanced = response.text.strip()

            # If enhancement is substantially longer, use it; otherwise keep original
            if len(enhanced) > len(partial_description) * 1.5:
                return enhanced
            else:
                return partial_description

        except Exception as e:
            print(f"LLM enhancement error: {str(e)}")
            return partial_description
