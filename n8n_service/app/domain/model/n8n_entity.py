from datetime import datetime
from typing import List, Dict, Any, Optional

class Workflow:
    def __init__(
        self,
        id: str,
        name: str,
        active: bool = False,
        nodes: List[Dict[str, Any]] = None,
        connections: Dict[str, Any] = None,
        settings: Dict[str, Any] = None,
        tags: List[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.active = active
        self.nodes = nodes or []
        self.connections = connections or {}
        self.settings = settings or {}
        self.tags = tags or []
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Workflow":
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            active=data.get("active", False),
            nodes=data.get("nodes", []),
            connections=data.get("connections", {}),
            settings=data.get("settings", {}),
            tags=data.get("tags", []),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt")
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "active": self.active,
            "nodes": self.nodes,
            "connections": self.connections,
            "settings": self.settings,
            "tags": self.tags,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        } 