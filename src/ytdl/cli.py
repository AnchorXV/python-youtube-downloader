import typer
from rich import print as rprint

app = typer.Typer(help="YouTube Downloader")


@app.command()
def hello(name: str = "world"):
    """Say hello to user."""
    rprint(f"[bold green]Halo, {name}![/bold green] 🎉")


@app.command()
def version():
    """App version."""
    rprint("[cyan]ytdl v0.1.0[/cyan]")


if __name__ == "__main__":
    app()