# code de la section 3.3
import typer
# code de la section 4.1 et 4.3
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
# imports des modules locaux
from .models import Task, Priority, Status
from .storage import load_tasks, save_tasks
from .display import display_tasks

app = typer.Typer()
console = Console()
# code de la section 4.2
err_console = Console(stderr=True)

# callback pour afficher le Panel de bienvenue à chaque commande
@app.callback()
def welcome():
    # code de la section 4.1
    console.print('[bold blue]taskr[/bold blue] task manager')
    console.print(Panel('Welcome to taskr', title='CLI Task Manager', border_style='blue'))

# code de la section 4.2
def get_task_by_id(tasks, task_id: str):
    matches = [t for t in tasks if t.id == task_id]
    if not matches:
        err_console.print(f'[red]x[/red] Error: No task found with ID [cyan]{task_id}[/cyan]')
        err_console.print('Run [bold]taskr list[/bold] to see available task IDs.')
        raise typer.Exit(code=1)
    return matches[0]

@app.command()
def add(
    title: str = typer.Argument(..., help='Task title'),
    priority: Priority = typer.Option(Priority.medium, help='Task priority'),
    due: str = typer.Option(None, help='Due date YYYY-MM-DD'),
    tag: str = typer.Option(None, help='Task tag')
):
    '''Add a new task.'''
    tasks = load_tasks()
    from datetime import date
    # code de la section 4.2
    try:
        due_date = date.fromisoformat(due) if due else None
    except ValueError:
        err_console.print(f'[red]x[/red] Error: Invalid date format: [cyan]{due}[/cyan]')
        err_console.print('Use format: [bold]YYYY-MM-DD[/bold]')
        raise typer.Exit(code=1)
        
    new_task = Task(title=title, priority=priority, due_date=due_date, tags=[tag] if tag else [])
    tasks.append(new_task)
    save_tasks(tasks)
    # fusion du message de la section 3.3 et du style 4.1 pour permettre au test de la section 5.3 de passer
    console.print(f'[green]✓[/green] Added: {title} [{priority.value}]')

# code pour la section 5.5 (Required Features)
@app.command()
def list(
    filter_status: Status = typer.Option(None, "--status", help="Filter by status"),
    filter_priority: Priority = typer.Option(None, "--priority", help="Filter by priority"),
    sort_by_due: bool = typer.Option(False, "--sort-due", help="Sort tasks by due date"),
    sort_by_priority: bool = typer.Option(False, "--sort-priority", help="Sort tasks by priority")
):
    '''List all tasks with optional filters.'''
    tasks = load_tasks()
    
    # Logique de filtrage (Section 5.5 requirements)
    if filter_status:
        tasks = [t for t in tasks if t.status == filter_status]
    if filter_priority:
        tasks = [t for t in tasks if t.priority == filter_priority]
        
    # Logique de tri (Section 5.5 requirements)
    if sort_by_due:
        tasks.sort(key=lambda x: (x.due_date is None, x.due_date))
    if sort_by_priority:
        priority_order = {"high": 0, "medium": 1, "low": 2}
        tasks.sort(key=lambda x: priority_order.get(x.priority.value, 3))
        
    display_tasks(tasks)

@app.command()
def done(task_id: str):
    '''Mark a task as complete.'''
    # utilisation du helper get_task_by_id
    tasks = load_tasks()
    task = get_task_by_id(tasks, task_id)
    task.status = Status.done
    save_tasks(tasks)
    console.print('[green]✓[/green] Task marked as done!')

# code pour la section 5.5 (pour askr stats et askr edit (Required Features))
@app.command()
def stats():
    '''Show task statistics.'''
    tasks = load_tasks()
    total = len(tasks)
    done_count = len([t for t in tasks if t.status == Status.done])
    overdue_count = len([t for t in tasks if t.is_overdue()])
    rate = (done_count / total * 100) if total > 0 else 0
    
    console.print(f"Total tasks: {total}")
    console.print(f"Completed: [green]{done_count}[/green]")
    console.print(f"Overdue: [red]{overdue_count}[/red]")
    console.print(f"Completion rate: [blue]{rate:.1f}%[/blue]")
    
    for p in Priority:
        count = len([t for t in tasks if t.priority == p])
        console.print(f"Priority {p.value}: {count}")

@app.command()
def edit(
    task_id: str = typer.Argument(..., help="ID of the task to edit"),
    title: str = typer.Option(None, "--title", help="New title"),
    priority: Priority = typer.Option(None, "--priority", help="New priority"),
    due: str = typer.Option(None, "--due", help="New due date YYYY-MM-DD")
):
    '''Edit task fields.'''
    tasks = load_tasks()
    task = get_task_by_id(tasks, task_id)
    
    if title: 
        task.title = title
    if priority: 
        task.priority = priority
    if due:
        from datetime import date
        try:
            task.due_date = date.fromisoformat(due)
        except ValueError:
            err_console.print(f'[red]x[/red] Error: Invalid date format: [cyan]{due}[/cyan]')
            raise typer.Exit(code=1)
            
    save_tasks(tasks)
    console.print(f'[green]✓[/green] Task [cyan]{task_id}[/cyan] updated!')


@app.command()
def delete(task_id: str):
    '''Delete a task by ID.'''
    # code de la section 4.3
    tasks = load_tasks()
    task = get_task_by_id(tasks, task_id)
    confirmed = Confirm.ask(f'Delete task [cyan]{task.title}[/cyan]?', default=False)
    if not confirmed:
        console.print('[yellow]Cancelled.[/yellow]')
        raise typer.Exit()
    tasks.remove(task)
    save_tasks(tasks)
    console.print(f'[green]Deleted:[/green] {task.title}')

if __name__ == "__main__":
    app()