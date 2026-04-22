# code de la section 5.3
import pytest
from typer.testing import CliRunner
from taskr.main import app 

runner = CliRunner()

def test_add_task():
    result = runner.invoke(app, ['add', 'Buy groceries'])
    assert result.exit_code == 0
    assert 'Buy groceries' in result.output

def test_add_task_with_priority():
    result = runner.invoke(app, ['add', 'Urgent task', '--priority', 'high'])
    assert result.exit_code == 0

# ajout du test pour atteindre les 5 tests requis
def test_list_tasks():
    result = runner.invoke(app, ['list'])
    assert result.exit_code == 0

def test_invalid_date():
    result = runner.invoke(app, ['add', 'Task', '--due', 'not-a-date'])
    assert result.exit_code == 1
    assert 'Invalid date' in result.output

def test_done_invalid_id():
    result = runner.invoke(app, ['done', 'nonexistent'])
    assert result.exit_code == 1