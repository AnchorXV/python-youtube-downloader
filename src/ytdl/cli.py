"""CLI for ytdl."""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ytdl.core import Extractor, ExtractorError

app = typer.Typer(
    help="YouTube Downloader",
    no_args_is_help=True,
)
console = Console()


@app.command()
def info(
    url: str = typer.Argument(..., help="Youtube video URL"),
    show_formats: bool = typer.Option(
        False, "--formats", "-f",
        help="Show all available video formats",
    ),
):
    """Show video metadata from URL."""
    extractor = Extractor()
    
    with console.status("[cyan]Fetching video info..."):
        try:
            video = extractor.get_info(url)
        except ExtractorError as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            raise typer.Exit(code=1)
    
    # Main info panel
    console.print()
    console.print(Panel.fit(
        f"[bold cyan]{video.title}[/bold cyan]\n\n"
        f"[dim]Uploader:[/dim] {video.uploader}\n"
        f"[dim]Duration  :[/dim] {video.duration_str}\n"
        f"[dim]URL     :[/dim] {video.webpage_url}",
        title="[bold]Video Info[/bold]",
        border_style="cyan",
    ))
    
    # Format summary
    console.print(
        f"\n[dim]Total format:[/dim] {len(video.formats)} "
        f"([green]{len(video.video_formats)} video[/green], "
        f"[yellow]{len(video.audio_formats)} audio[/yellow])"
    )
    
    # Format table
    if show_formats:
        table = Table(title="\nFormat Video", show_lines=False)
        table.add_column("ID", style="cyan", justify="right")
        table.add_column("Ext", style="magenta")
        table.add_column("Resolution", style="green")
        table.add_column("VCodec", style="dim")
        
        for f in video.video_formats:
            table.add_row(
                str(f.get("format_id", "?")),
                f.get("ext", "?"),
                f.get("resolution", "N/A"),
                (f.get("vcodec") or "N/A")[:20],
            )
        
        console.print(table)


@app.command()
def version():
    """Show application version."""
    console.print("[cyan]ytdl v0.1.0[/cyan]")


if __name__ == "__main__":
    app()