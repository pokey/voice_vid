from dataclasses import dataclass
from datetime import timedelta
from voice_vid.io.parse_transcript import Command, Transcript, TranscriptItem
from voice_vid.reconcile_commands import ReconciledCommand


@dataclass
class OutputTranscriptItem:
    id: str
    offset: timedelta
    phrase: str
    commands: list[Command]


def generate_transcript(
    talon_transcript: Transcript, reconciled_commands: list[ReconciledCommand]
):
    return sorted(
        [
            get_output_transcript_item(
                reconciled_command.shift_seconds,
                talon_transcript[reconciled_command.id],
            )
            for reconciled_command in reconciled_commands
        ],
        key=lambda item: item.offset,
    )


def get_output_transcript_item(shift_seconds: float, transcript_item: TranscriptItem):
    seconds = round(max(transcript_item.phrase_start + shift_seconds, 0))

    return OutputTranscriptItem(
        id=transcript_item.id,
        offset=timedelta(seconds=seconds),
        phrase=transcript_item.phrase,
        commands=transcript_item.commands,
    )
