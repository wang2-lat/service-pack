import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime
import json
from pathlib import Path

app = typer.Typer(help="Standardize freelance services and generate quotes instantly")
console = Console()

DATA_DIR = Path.home() / ".service-pack"
DATA_DIR.mkdir(exist_ok=True)

SERVICES_FILE = DATA_DIR / "services.json"
QUOTES_FILE = DATA_DIR / "quotes.json"
PROJECTS_FILE = DATA_DIR / "projects.json"

def load_json(file_path):
    if file_path.exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

service_app = typer.Typer(help="Manage service packages")
quote_app = typer.Typer(help="Generate and manage quotes")
project_app = typer.Typer(help="Track projects and revenue")

app.add_typer(service_app, name="service")
app.add_typer(quote_app, name="quote")
app.add_typer(project_app, name="project")

@service_app.command("create")
def create_service(
    name: str = typer.Option(..., prompt=True),
    price: float = typer.Option(..., prompt=True),
    hours: int = typer.Option(..., prompt=True),
    deliverables: str = typer.Option(..., prompt=True, help="Comma-separated list")
):
    """Create a new service package"""
    services = load_json(SERVICES_FILE)
    service = {
        "id": len(services) + 1,
        "name": name,
        "price": price,
        "hours": hours,
        "deliverables": [d.strip() for d in deliverables.split(",")],
        "created_at": datetime.now().isoformat()
    }
    services.append(service)
    save_json(SERVICES_FILE, services)
    console.print(f"[green]Service package '{name}' created successfully![/green]")

@service_app.command("list")
def list_services():
    """List all service packages"""
    services = load_json(SERVICES_FILE)
    if not services:
        console.print("[yellow]No service packages found. Create one first![/yellow]")
        return
    
    table = Table(title="Service Packages")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Price", style="yellow")
    table.add_column("Hours", style="magenta")
    table.add_column("Deliverables")
    
    for s in services:
        table.add_row(
            str(s["id"]),
            s["name"],
            f"${s['price']:.2f}",
            str(s["hours"]),
            ", ".join(s["deliverables"])
        )
    console.print(table)

@service_app.command("delete")
def delete_service(service_id: int):
    """Delete a service package"""
    services = load_json(SERVICES_FILE)
    services = [s for s in services if s["id"] != service_id]
    save_json(SERVICES_FILE, services)
    console.print(f"[green]Service package {service_id} deleted![/green]")

@quote_app.command("generate")
def generate_quote(
    service_id: int = typer.Option(..., prompt=True),
    client_name: str = typer.Option(..., prompt=True),
    client_email: str = typer.Option(..., prompt=True)
):
    """Generate a quote for a client"""
    services = load_json(SERVICES_FILE)
    service = next((s for s in services if s["id"] == service_id), None)
    
    if not service:
        console.print(f"[red]Service package {service_id} not found![/red]")
        return
    
    quotes = load_json(QUOTES_FILE)
    quote = {
        "id": len(quotes) + 1,
        "service_id": service_id,
        "service_name": service["name"],
        "client_name": client_name,
        "client_email": client_email,
        "price": service["price"],
        "hours": service["hours"],
        "deliverables": service["deliverables"],
        "created_at": datetime.now().isoformat()
    }
    quotes.append(quote)
    save_json(QUOTES_FILE, quotes)
    
    panel_content = f"""
[bold]Quote #{quote['id']}[/bold]
Client: {client_name} ({client_email})
Service: {service['name']}
Price: ${service['price']:.2f}
Estimated Hours: {service['hours']}
Deliverables:
{chr(10).join(f"  • {d}" for d in service['deliverables'])}
    """
    console.print(Panel(panel_content, title="Quote Generated", border_style="green"))

@quote_app.command("list")
def list_quotes():
    """List all generated quotes"""
    quotes = load_json(QUOTES_FILE)
    if not quotes:
        console.print("[yellow]No quotes found. Generate one first![/yellow]")
        return
    
    table = Table(title="Generated Quotes")
    table.add_column("ID", style="cyan")
    table.add_column("Client", style="green")
    table.add_column("Service", style="yellow")
    table.add_column("Price", style="magenta")
    table.add_column("Date")
    
    for q in quotes:
        table.add_row(
            str(q["id"]),
            q["client_name"],
            q["service_name"],
            f"${q['price']:.2f}",
            q["created_at"][:10]
        )
    console.print(table)

@project_app.command("add")
def add_project(
    quote_id: int = typer.Option(..., prompt=True),
    status: str = typer.Option("in_progress", prompt=True, help="in_progress, completed, cancelled")
):
    """Add a project from a quote"""
    quotes = load_json(QUOTES_FILE)
    quote = next((q for q in quotes if q["id"] == quote_id), None)
    
    if not quote:
        console.print(f"[red]Quote {quote_id} not found![/red]")
        return
    
    projects = load_json(PROJECTS_FILE)
    project = {
        "id": len(projects) + 1,
        "quote_id": quote_id,
        "client_name": quote["client_name"],
        "service_name": quote["service_name"],
        "price": quote["price"],
        "hours": quote["hours"],
        "status": status,
        "created_at": datetime.now().isoformat()
    }
    projects.append(project)
    save_json(PROJECTS_FILE, projects)
    console.print(f"[green]Project added successfully![/green]")

@project_app.command("list")
def list_projects():
    """List all projects"""
    projects = load_json(PROJECTS_FILE)
    if not projects:
        console.print("[yellow]No projects found. Add one first![/yellow]")
        return
    
    table = Table(title="Projects")
    table.add_column("ID", style="cyan")
    table.add_column("Client", style="green")
    table.add_column("Service", style="yellow")
    table.add_column("Price", style="magenta")
    table.add_column("Status")
    
    for p in projects:
        table.add_row(
            str(p["id"]),
            p["client_name"],
            p["service_name"],
            f"${p['price']:.2f}",
            p["status"]
        )
    console.print(table)

@project_app.command("update")
def update_project(
    project_id: int = typer.Option(..., prompt=True),
    status: str = typer.Option(..., prompt=True, help="in_progress, completed, cancelled")
):
    """Update project status"""
    projects = load_json(PROJECTS_FILE)
    for p in projects:
        if p["id"] == project_id:
            p["status"] = status
            save_json(PROJECTS_FILE, projects)
            console.print(f"[green]Project {project_id} updated to {status}![/green]")
            return
    console.print(f"[red]Project {project_id} not found![/red]")

@project_app.command("stats")
def project_stats():
    """Show revenue and time statistics"""
    projects = load_json(PROJECTS_FILE)
    if not projects:
        console.print("[yellow]No projects found![/yellow]")
        return
    
    total_revenue = sum(p["price"] for p in projects if p["status"] == "completed")
    total_hours = sum(p["hours"] for p in projects if p["status"] == "completed")
    in_progress = len([p for p in projects if p["status"] == "in_progress"])
    completed = len([p for p in projects if p["status"] == "completed"])
    
    stats_content = f"""
[bold]Project Statistics[/bold]

Total Revenue (Completed): ${total_revenue:.2f}
Total Hours (Completed): {total_hours}
Projects In Progress: {in_progress}
Projects Completed: {completed}
Average Hourly Rate: ${total_revenue/total_hours:.2f} (if hours > 0)
    """
    console.print(Panel(stats_content, title="Statistics", border_style="blue"))

if __name__ == "__main__":
    app()
