from dataclasses import dataclass
from datetime import timedelta
from typing import Optional
from voice_vid.io.parse_config import Config
from voice_vid.io.parse_transcript import Command, Transcript, TranscriptItem
from voice_vid.reconcile_commands import ReconciledCommand


@dataclass
class OutputTranscriptItem:
    id: str
    start_offset: float
    end_offset: float
    phrase: str
    commands: list[Command]


@dataclass
class OutputTranscript:
    youtube_slug: Optional[str]
    title: str
    transcript_items: list[OutputTranscriptItem]


def generate_transcript(
    config: Config,
    talon_transcript: Transcript,
    reconciled_commands: list[ReconciledCommand],
):
    return OutputTranscript(
        title=config.title,
        youtube_slug=config.youtube_slug,
        transcript_items=sorted(
            [
                get_output_transcript_item(
                    reconciled_command.shift_seconds,
                    talon_transcript[reconciled_command.id],
                )
                for reconciled_command in reconciled_commands
            ],
            key=lambda item: item.start_offset,
        ),
    )


def get_output_transcript_item(shift_seconds: float, transcript_item: TranscriptItem):
    start_seconds = max(transcript_item.phrase_start + shift_seconds, 0)
    end_seconds = max(transcript_item.phrase_end + shift_seconds, 0)

    return OutputTranscriptItem(
        id=transcript_item.id,
        start_offset=start_seconds,
        end_offset=end_seconds,
        phrase=transcript_item.phrase,
        commands=transcript_item.commands,
    )
