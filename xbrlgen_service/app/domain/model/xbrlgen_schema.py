from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class XBRLGenRequest(BaseModel):
    company_id: int
    reporting_period: str
    template_type: str
    
class XBRLGenResponse(BaseModel):
    id: int
    company_id: int
    reporting_period: str
    template_type: str
    created_at: datetime
    status: str
    
class XBRLGenStatusResponse(BaseModel):
    status: str
    message: str 