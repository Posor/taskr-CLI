# code de la section 4.1
from rich.table import Table
from rich.console import Console
# import de Status pour la logique des icônes de statut
from .models import Status 

console = Console()

def display_tasks(tasks):
    table = Table(title='Your Tasks', border_style='blue')
    table.add_column('ID', style='cyan', no_wrap=True, width=8)
    table.add_column('Title', style='white', min_width=20)
    table.add_column('Priority', justify='center', width=12)
    table.add_column('Due', justify='center', width=12)
    table.add_column('Status', justify='center', width=10)

    for task in tasks:
        priority_color = {'high': 'red', 'medium': 'yellow', 'low': 'green'}[task.priority.value]
        due_str = task.due_date.strftime('%Y-%m-%d') if task.due_date else '-'
        
        status_icon = '✓' if task.status.value == 'done' else 'o'
        
        if task.is_overdue():
            due_str = f'[red]{due_str}[/red]'
            
        table.add_row(
            task.id,
            f'[dim]{task.title}[/dim]' if task.status.value == 'done' else task.title,
            f'[{priority_color}]{task.priority.value}[/{priority_color}]',
            due_str,
            f'[green]{status_icon}[/green]' if task.status.value == 'done' else status_icon,
        )
    console.print(table)