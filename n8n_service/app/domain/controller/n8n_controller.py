from typing import List
from fastapi import HTTPException

from app.domain.service.n8n_service import N8nService
from app.domain.model.n8n_schema import WorkflowCreate, WorkflowResponse, WorkflowExecute

class N8nController:
    def __init__(self):
        self.n8n_service = N8nService()

    async def create_workflow(self, workflow: WorkflowCreate) -> WorkflowResponse:
        try:
            return await self.n8n_service.create_workflow(workflow)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_workflows(self) -> List[WorkflowResponse]:
        try:
            return await self.n8n_service.get_workflows()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_workflow(self, workflow_id: str) -> WorkflowResponse:
        try:
            workflow = await self.n8n_service.get_workflow(workflow_id)
            if not workflow:
                raise HTTPException(status_code=404, detail="Workflow not found")
            return workflow
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def execute_workflow(self, workflow_id: str, execution: WorkflowExecute):
        try:
            return await self.n8n_service.execute_workflow(workflow_id, execution)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_workflow(self, workflow_id: str):
        try:
            return await self.n8n_service.delete_workflow(workflow_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) 