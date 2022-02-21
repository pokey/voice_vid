from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class TranscriptItem:
    phrase_start: float
    phrase_end: float
    phrase: str


def parse_talon_transcript(path: Path):
    raw_transcript = [json.loads(line) for line in path.read_text().splitlines()]

    return [
        TranscriptItem(
            phrase_start=raw_transcript_item["timeOffsets"]["speechStart"],
            phrase_end=raw_transcript_item["timeOffsets"]["prePhraseCallbackStart"],
            phrase=raw_transcript_item["phrase"],
        )
        for raw_transcript_item in raw_transcript
        if raw_transcript_item["type"] == "talonCommandPhrase"
    ]
