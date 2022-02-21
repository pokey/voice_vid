from dataclasses import dataclass


@dataclass
class TranscriptItem:
    phrase_start: float
    phrase_end: float
    phrase: str


def reconcile_transcript(raw_transcript: list[dict], offset: float):
    return [
        TranscriptItem(
            phrase_start=raw_transcript_item["timeOffsets"]["speechStart"] + offset,
            phrase_end=raw_transcript_item["timeOffsets"]["prePhraseCallbackStart"]
            + offset,
            phrase=raw_transcript_item["phrase"],
        )
        for raw_transcript_item in raw_transcript
        if raw_transcript_item["type"] == "talonCommandPhrase"
    ]
