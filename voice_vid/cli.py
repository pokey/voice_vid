"""Console script for voice_vid."""
# Note: generate initial raw transcript using eg
#
# cat 'path/2022-02-17T14-52-51/talon-log.jsonl' \
#   | jq -c 'select(.type == talonCommandPhrase) | {phrase, phraseStart: .timeOffsets.speechStart, phraseEnd: .timeOffsets.prePhraseCallbackStart}' \
#   > 'path/raw-transcript.jsonl'
#
# And then remove anything you don't want
import sys
import click

import json

from voice_vid.reconcile_transcript import reconcile_transcript
from voice_vid.sbt import format_transcript

offset = 78 - 80.06904987200323


@click.command()
def main(args=None):
    """Console script for voice_vid."""
    with open(
        "/Users/pokey/Movies/Cursorless/Completed/Two Sum/raw-transcript.jsonl"
    ) as f:
        raw_transcript = [json.loads(line) for line in f]

    transcript = reconcile_transcript(raw_transcript, offset)

    click.echo(format_transcript(transcript))

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
