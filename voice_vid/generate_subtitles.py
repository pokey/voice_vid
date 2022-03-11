from dataclasses import dataclass
from itertools import pairwise
from voice_vid.compute_command_ranges import CommandTiming
from voice_vid.io.parse_transcript import Transcript, TranscriptItem
from voice_vid.reconcile_commands import ReconciledCommand


@dataclass
class Subtitle:
    start_seconds: float
    end_seconds: float
    text: str


def generate_subtitles(reconciled_commands: list[CommandTiming]):
    return [
        Subtitle(
            start_seconds=command.target_grace_start_seconds,
            end_seconds=command.target_grace_end_seconds,
            text=command.transcript_item.phrase,
        )
        for command in reconciled_commands
    ]
