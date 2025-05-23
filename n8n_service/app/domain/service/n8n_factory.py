from app.domain.model.n8n_schema import WorkflowCreate, WorkflowResponse

class N8nFactory:
    def create_n8n_workflow(self, workflow: WorkflowCreate) -> dict:
        """WorkflowCreate 모델을 n8n API 형식으로 변환합니다."""
        return {
            "name": workflow.name,
            "nodes": workflow.nodes,
            "connections": workflow.connections,
            "settings": workflow.settings,
            "tags": workflow.tags
        }

    def create_workflow_response(self, n8n_workflow: dict) -> WorkflowResponse:
        """n8n API 응답을 WorkflowResponse 모델로 변환합니다."""
        return WorkflowResponse(
            id=n8n_workflow.get("id"),
            name=n8n_workflow.get("name"),
            active=n8n_workflow.get("active", False),
            nodes=n8n_workflow.get("nodes", []),
            connections=n8n_workflow.get("connections", {}),
            settings=n8n_workflow.get("settings", {}),
            tags=n8n_workflow.get("tags", []),
            created_at=n8n_workflow.get("createdAt"),
            updated_at=n8n_workflow.get("updatedAt")
        ) 