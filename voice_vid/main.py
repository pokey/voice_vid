"""Console script for voice_vid."""
# Note: generate initial raw transcript using eg
#
# cat 'path/2022-02-17T14-52-51/talon-log.jsonl' \
#   | jq -c 'select(.type == talonCommandPhrase) | {phrase, phraseStart: .timeOffsets.speechStart, phraseEnd: .timeOffsets.prePhraseCallbackStart}' \
#   > 'path/raw-transcript.jsonl'
#
# And then remove anything you don't want
from pathlib import Path

from voice_vid.parse_config import parse_config
from voice_vid.parse_transcript import parse_talon_transcript

from voice_vid.reconcile_transcript import reconcile_transcript
from voice_vid.sbt import format_transcript
import typer
import opentimelineio as otio

app = typer.Typer()


@app.command()
def main(index_path: Path):
    """Console script for voice_vid."""
    config = parse_config(index_path)

    talon_transcript = parse_talon_transcript(
        config.talon_log_dir_path / "talon-log.jsonl"
    )
    timeline = otio.adapters.read_from_file(config.timeline_path)

    transcript = reconcile_transcript(
        talon_transcript=talon_transcript,
        offset_str=config.talon_offset,
        timeline=timeline,
        recording_path=config.screen_recording_path,
    )

    typer.echo(format_transcript(transcript))

    return 0


if __name__ == "__main__":
    app()
