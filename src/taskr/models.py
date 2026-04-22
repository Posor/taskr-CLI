# code de la section 3.4
from dataclasses import dataclass, field
from datetime import date
from typing import Optional
from enum import Enum
import uuid

class Priority(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'

class Status(str, Enum):
    todo = 'todo'
    done = 'done'

@dataclass
class Task:
    title: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    priority: Priority = Priority.medium
    status: Status = Status.todo
    due_date: Optional[date] = None
    tags: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: date.today().isoformat())

    def is_overdue(self) -> bool:
        if self.due_date and self.status != Status.done:
            return date.today() > self.due_date
        return False

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'priority': self.priority.value,
            'status': self.status.value,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'tags': self.tags,
            'created_at': self.created_at,
        }