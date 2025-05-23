from typing import List
import httpx
import os
from fastapi import HTTPException

from app.domain.model.n8n_schema import WorkflowCreate, WorkflowResponse, WorkflowExecute
from app.domain.service.n8n_factory import N8nFactory
from app.domain.repository.n8n_repository import N8nRepository

class N8nService:
    def __init__(self):
        self.n8n_url = os.getenv("N8N_URL", "http://n8n:5678")
        self.n8n_api_key = os.getenv("N8N_API_KEY")
        self.repository = N8nRepository()
        self.factory = N8nFactory()

    async def create_workflow(self, workflow: WorkflowCreate) -> WorkflowResponse:
        """새로운 워크플로우를 생성합니다."""
        async with httpx.AsyncClient() as client:
            headers = self._get_headers()
            n8n_workflow = self.factory.create_n8n_workflow(workflow)
            
            response = await client.post(
                f"{self.n8n_url}/api/v1/workflows",
                headers=headers,
                json=n8n_workflow
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            
            return self.factory.create_workflow_response(response.json())

    async def get_workflows(self) -> List[WorkflowResponse]:
        """모든 워크플로우 목록을 조회합니다."""
        async with httpx.AsyncClient() as client:
            headers = self._get_headers()
            response = await client.get(
                f"{self.n8n_url}/api/v1/workflows",
                headers=headers
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            
            return [self.factory.create_workflow_response(w) for w in response.json()]

    async def get_workflow(self, workflow_id: str) -> WorkflowResponse:
        """특정 워크플로우의 상세 정보를 조회합니다."""
        async with httpx.AsyncClient() as client:
            headers = self._get_headers()
            response = await client.get(
                f"{self.n8n_url}/api/v1/workflows/{workflow_id}",
                headers=headers
            )
            
            if response.status_code == 404:
                return None
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            
            return self.factory.create_workflow_response(response.json())

    async def execute_workflow(self, workflow_id: str, execution: WorkflowExecute):
        """워크플로우를 실행합니다."""
        async with httpx.AsyncClient() as client:
            headers = self._get_headers()
            response = await client.post(
                f"{self.n8n_url}/api/v1/workflows/{workflow_id}/execute",
                headers=headers,
                json=execution.dict()
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            
            return response.json()

    async def delete_workflow(self, workflow_id: str):
        """워크플로우를 삭제합니다."""
        async with httpx.AsyncClient() as client:
            headers = self._get_headers()
            response = await client.delete(
                f"{self.n8n_url}/api/v1/workflows/{workflow_id}",
                headers=headers
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)
            
            return {"message": "Workflow deleted successfully"}

    def _get_headers(self):
        """API 요청에 필요한 헤더를 생성합니다."""
        headers = {
            "Content-Type": "application/json"
        }
        if self.n8n_api_key:
            headers["X-N8N-API-KEY"] = self.n8n_api_key
        return headers 