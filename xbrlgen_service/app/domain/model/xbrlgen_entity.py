from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class XBRLGenEntity(BaseModel):
    id: Optional[int] = None
    company_id: int
    reporting_period: str
    template_type: str
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None
    status: str = "pending"
    xbrl_content: Optional[str] = None 