from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class WorkflowBase(BaseModel):
    name: str
    nodes: List[Dict[str, Any]] = []
    connections: Dict[str, Any] = {}
    settings: Dict[str, Any] = {}
    tags: List[str] = []

class WorkflowCreate(WorkflowBase):
    pass

class WorkflowResponse(WorkflowBase):
    id: str
    active: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class WorkflowExecute(BaseModel):
    workflow_data: Optional[Dict[str, Any]] = None
    run_data: Optional[Dict[str, Any]] = None 