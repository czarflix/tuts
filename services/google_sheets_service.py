import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from typing import Dict, Optional
import os
from config import config

class GoogleSheetsService:
    def __init__(self):
        self.enabled = config.GOOGLE_SHEETS_ENABLED
        self.credentials_file = config.GOOGLE_SHEETS_CREDENTIALS_FILE
        self.sheet_name = config.GOOGLE_SHEET_NAME
        self.client = None
        self.sheet = None

        if self.enabled:
            self._initialize_client()

    def _initialize_client(self):
        """Initialize Google Sheets client"""
        try:
            if not os.path.exists(self.credentials_file):
                print(f"⚠️  Google Sheets credentials file not found: {self.credentials_file}")
                print("Google Sheets integration will be disabled.")
                self.enabled = False
                return

            # Define the scope
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]

            # Authenticate
            creds = Credentials.from_service_account_file(self.credentials_file, scopes=scope)
            self.client = gspread.authorize(creds)

            # Try to open existing sheet or create new one
            try:
                self.sheet = self.client.open(self.sheet_name).sheet1
                print(f"✅ Connected to existing Google Sheet: {self.sheet_name}")
            except gspread.SpreadsheetNotFound:
                # Create new spreadsheet
                spreadsheet = self.client.create(self.sheet_name)
                self.sheet = spreadsheet.sheet1

                # Share with your email (so you can access it)
                # You'll need to manually share or add this in credentials setup
                print(f"✅ Created new Google Sheet: {self.sheet_name}")

                # Set up headers
                self._setup_headers()

        except Exception as e:
            print(f"❌ Error initializing Google Sheets: {str(e)}")
            print("Falling back to Excel-only mode.")
            self.enabled = False

    def _setup_headers(self):
        """Set up column headers in the Google Sheet"""
        if not self.sheet:
            return

        headers = [
            "Date Added",
            "Company",
            "Job Title",
            "Role Type",
            "Compensation",
            "Job Description",
            "Application Link",
            "Application Method",
            "Email Subject",
            "Resume Link",
            "Status",
            "Notes"
        ]

        # Write headers
        self.sheet.update('A1:L1', [headers])

        # Format headers (bold)
        self.sheet.format('A1:L1', {
            "textFormat": {"bold": True, "fontSize": 11},
            "backgroundColor": {"red": 0.27, "green": 0.45, "blue": 0.77}
        })

        # Set column widths
        requests = [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": self.sheet.id,
                        "dimension": "COLUMNS",
                        "startIndex": i,
                        "endIndex": i + 1
                    },
                    "properties": {"pixelSize": width},
                    "fields": "pixelSize"
                }
            }
            for i, width in enumerate([100, 150, 200, 100, 120, 400, 300, 120, 200, 300, 100, 200])
        ]

        self.sheet.spreadsheet.batch_update({"requests": requests})

    def add_job_application(self, job_data: Dict, resume_link: str = "") -> Optional[int]:
        """
        Add a new job application to Google Sheets
        Returns the row number where data was added
        """
        if not self.enabled or not self.sheet:
            return None

        try:
            # Prepare data
            row_data = [
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                job_data.get("company", ""),
                job_data.get("job_title", ""),
                job_data.get("role_type", ""),
                job_data.get("compensation", ""),
                job_data.get("job_description", ""),
                job_data.get("application_link", ""),
                job_data.get("application_method", ""),
                job_data.get("email_subject", ""),
                resume_link,
                "New",
                ""  # Notes column
            ]

            # Append row
            self.sheet.append_row(row_data)

            # Get the row number that was just added
            row_number = len(self.sheet.get_all_values())

            # Format the application link as hyperlink if it's a URL
            if job_data.get("application_link", "").startswith("http"):
                cell = f"G{row_number}"
                self.sheet.format(cell, {
                    "textFormat": {"link": {"uri": job_data.get("application_link")}}
                })

            # Format resume link as hyperlink if present
            if resume_link:
                cell = f"J{row_number}"
                self.sheet.format(cell, {
                    "textFormat": {"link": {"uri": resume_link}}
                })

            print(f"✅ Added to Google Sheets row: {row_number}")
            return row_number

        except Exception as e:
            print(f"❌ Error adding to Google Sheets: {str(e)}")
            return None

    def update_resume_link(self, row_number: int, resume_link: str):
        """Update the resume link for a specific row"""
        if not self.enabled or not self.sheet:
            return

        try:
            # Update resume link (column J)
            self.sheet.update(f'J{row_number}', resume_link)

            # Format as hyperlink
            self.sheet.format(f'J{row_number}', {
                "textFormat": {"link": {"uri": resume_link}}
            })

            # Update status (column K)
            self.sheet.update(f'K{row_number}', "Resume Generated")

            print(f"✅ Updated Google Sheets row {row_number} with resume link")

        except Exception as e:
            print(f"❌ Error updating Google Sheets: {str(e)}")

    def get_sheet_url(self) -> Optional[str]:
        """Get the URL to the Google Sheet"""
        if not self.enabled or not self.sheet:
            return None

        return f"https://docs.google.com/spreadsheets/d/{self.sheet.spreadsheet.id}"

    def is_enabled(self) -> bool:
        """Check if Google Sheets integration is enabled and working"""
        return self.enabled and self.sheet is not None
