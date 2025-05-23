from fastapi import UploadFile
from ..service.report_service import ReportService
from typing import Optional

class ReportController:
    def __init__(self):
        self.service = ReportService()
    
    async def process_report(self, file: UploadFile, description: Optional[str] = None):
        """
        Process uploaded PDF report
        
        Args:
            file: Uploaded PDF file
            description: Optional description
            
        Returns:
            dict: Processing result
        """
        return await self.service.process_pdf(file, description) 