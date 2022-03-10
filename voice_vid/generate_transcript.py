from dataclasses import dataclass
from datetime import timedelta
from typing import Optional
from voice_vid.compute_command_ranges import CommandTiming
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
    reconciled_commands: list[CommandTiming],
):
    return OutputTranscript(
        title=config.title,
        youtube_slug=config.youtube_slug,
        transcript_items=[
            OutputTranscriptItem(
                id=reconciled_command.transcript_item.id,
                start_offset=reconciled_command.target_grace_start_seconds,
                end_offset=reconciled_command.target_grace_end_seconds,
                phrase=reconciled_command.transcript_item.phrase,
                commands=reconciled_command.transcript_item.commands,
            )
            for reconciled_command in reconciled_commands
        ],
    )
