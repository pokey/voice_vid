"""Console script for voice_vid."""
# Note: generate initial raw transcript using eg
#
# cat 'path/2022-02-17T14-52-51/talon-log.jsonl' \
#   | jq -c 'select(.type == talonCommandPhrase) | {phrase, phraseStart: .timeOffsets.speechStart, phraseEnd: .timeOffsets.prePhraseCallbackStart}' \
#   > 'path/raw-transcript.jsonl'
#
# And then remove anything you don't want
from pathlib import Path
import sys

import opentimelineio as otio
import typer
from voice_vid.generate_subtitles import generate_subtitles
from voice_vid.generate_transcript import generate_transcript

from voice_vid.io.parse_config import parse_config
from voice_vid.io.parse_transcript import parse_talon_transcript
from voice_vid.io.sbt import format_transcript
from voice_vid.io import reconciled_commands
from voice_vid.io import output_transcript
from voice_vid.reconcile_commands import reconcile_commands

app = typer.Typer()


@app.command()
def reconcile(
    index_path: Path, out: typer.FileTextWrite = typer.Argument("-", allow_dash=True)
):
    """Reconciles commands from talon transcript against clips in a video"""
    out_resolved = sys.stdout if out == "-" else out

    config = parse_config(index_path)

    talon_transcript = parse_talon_transcript(
        config.talon_log_dir_path / "talon-log.jsonl"
    )
    timeline = otio.adapters.read_from_file(config.timeline_path)

    reconciled = reconcile_commands(
        talon_transcript=talon_transcript,
        offset_str=config.talon_offset,
        timeline=timeline,
        recording_path=config.screen_recording_path,
    )

    reconciled_commands.write(out_resolved, reconciled)


@app.command()
def subtitles(
    index_path: Path,
    reconciled: typer.FileText = typer.Option(...),
    use_command_end: bool = False,
    end_offset: float = 0.0,
):
    """Generate subtitles for a video"""
    config = parse_config(index_path)

    talon_transcript = parse_talon_transcript(
        config.talon_log_dir_path / "talon-log.jsonl"
    )
    reconciled_command_list = reconciled_commands.read(reconciled)

    subtitles = generate_subtitles(
        talon_transcript, reconciled_command_list, use_command_end, end_offset
    )

    typer.echo(format_transcript(subtitles))


@app.command()
def transcript(
    index_path: Path,
    reconciled: typer.FileText = typer.Option(...),
    out: typer.FileTextWrite = typer.Argument("-", allow_dash=True),
):
    """Generate subtitles for a video"""
    config = parse_config(index_path)

    out_resolved = sys.stdout if out == "-" else out

    talon_transcript = parse_talon_transcript(
        config.talon_log_dir_path / "talon-log.jsonl"
    )
    reconciled_command_list = reconciled_commands.read(reconciled)

    transcript = generate_transcript(config, talon_transcript, reconciled_command_list)

    output_transcript.write(out_resolved, transcript)


if __name__ == "__main__":
    app()
