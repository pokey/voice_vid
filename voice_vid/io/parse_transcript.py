import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TranscriptItem:
    id: str
    phrase_start: float
    phrase_end: float
    phrase: str


class Transcript:
    def __init__(self, items: list[TranscriptItem]):
        self.items = items
        self.item_map = {item.id: item for item in self.items}

    def __iter__(self):
        return iter(self.items)

    def __getitem__(self, key: str):
        return self.item_map[key]


def parse_talon_transcript(path: Path):
    raw_transcript = [json.loads(line) for line in path.read_text().splitlines()]

    return Transcript(
        [
            TranscriptItem(
                id=raw_transcript_item["id"],
                phrase_start=raw_transcript_item["timeOffsets"]["speechStart"],
                phrase_end=raw_transcript_item["timeOffsets"]["prePhraseCallbackStart"],
                phrase=raw_transcript_item["phrase"],
            )
            for raw_transcript_item in raw_transcript
            if raw_transcript_item["type"] == "talonCommandPhrase"
        ]
    )
