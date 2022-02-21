"""Console script for voice_vid."""
# Note: generate initial raw transcript using eg
#
# cat 'path/2022-02-17T14-52-51/talon-log.jsonl' \
#   | jq -c 'select(.type == talonCommandPhrase) | {phrase, phraseStart: .timeOffsets.speechStart, phraseEnd: .timeOffsets.prePhraseCallbackStart}' \
#   > 'path/raw-transcript.jsonl'
#
# And then remove anything you don't want
from pathlib import Path

import json
from voice_vid.parse_config import parse_config

from voice_vid.reconcile_transcript import reconcile_transcript
from voice_vid.sbt import format_transcript
import typer

offset = 78 - 80.06904987200323


app = typer.Typer()


@app.command()
def main(
    index_path: Path,
):
    """Console script for voice_vid."""
    config = parse_config(index_path)

    recording_log = config.talon_log_dir_path / "talon-log.jsonl"

    raw_transcript = [
        json.loads(line) for line in recording_log.read_text().splitlines()
    ]

    transcript = reconcile_transcript(raw_transcript, offset)

    typer.echo(format_transcript(transcript))

    return 0


if __name__ == "__main__":
    app()
