# code de la section 3.5
import json
from pathlib import Path
from typing import List
# ajout nécessaire car date est utilisé dans load_tasks
from datetime import date
# ajout des imports du fichier models.py pour permettre la reconstruction des objets Task
from .models import Task, Priority, Status 

DATA_DIR = Path.home() / '.taskr'
DATA_FILE = DATA_DIR / 'tasks.json'

def ensure_data_dir():
    DATA_DIR.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text('[]')

def load_tasks() -> List[Task]:
    ensure_data_dir()
    data = json.loads(DATA_FILE.read_text())
    tasks = []
    for d in data:
        t = Task(title=d['title'], id=d['id'])
        t.priority = Priority(d['priority'])
        t.status = Status(d['status'])
        if d.get('due_date'):
            t.due_date = date.fromisoformat(d['due_date'])
        t.tags = d.get('tags', [])
        t.created_at = d.get('created_at', '')
        tasks.append(t)
    return tasks

def save_tasks(tasks: List[Task]):
    ensure_data_dir()
    DATA_FILE.write_text(json.dumps([t.to_dict() for t in tasks], indent=2))