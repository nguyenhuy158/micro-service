from datetime import datetime, timezone
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class DomainEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    event_type: str
    payload: Any
    correlation_id: Optional[UUID] = None  # To track the saga
