"""CLI for ytdl."""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from pathlib import Path

from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

from ytdl.core import Downloader, DownloaderError, Extractor, ExtractorError

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
def download(
    url: str = typer.Argument(..., help="YouTube video URL"),
    quality: str = typer.Option(
        "best", "--quality", "-q",
        help="Video quality: best, 1080p, 720p, 480p, 360p",
    ),
    audio_only: bool = typer.Option(
        False, "--audio", "-a",
        help="Download audio only (mp3)",
    ),
    output_dir: Path = typer.Option(
        Path("downloads"), "--output", "-o",
        help="Output directory",
    ),
):
    """Download a video from URL."""
    # Progress bar
    progress = Progress(
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
    )
    
    with progress:
        task_id = progress.add_task("Preparing...", total=None)
        
        def hook(d):
            if d["status"] == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate")
                downloaded = d.get("downloaded_bytes", 0)
                progress.update(
                    task_id,
                    total=total,
                    completed=downloaded,
                    description="Downloading",
                )
            elif d["status"] == "finished":
                progress.update(task_id, description="Processing...")
        
        downloader = Downloader(output_dir=output_dir)
        
        try:
            path = downloader.download(
                url,
                quality=quality,
                audio_only=audio_only,
                progress_hook=hook,
            )
        except DownloaderError as e:
            progress.stop()
            console.print(f"[bold red]Error:[/bold red] {e}")
            raise typer.Exit(code=1)
    
    console.print(f"\n[bold green]✓[/bold green] Saved to: [cyan]{path}[/cyan]")


@app.command()
def version():
    """Show application version."""
    console.print("[cyan]ytdl v0.1.0[/cyan]")


if __name__ == "__main__":
    app()