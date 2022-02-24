from dataclasses import dataclass
from datetime import timedelta
from voice_vid.io.parse_transcript import Command, Transcript, TranscriptItem
from voice_vid.reconcile_commands import ReconciledCommand


@dataclass
class OutputTranscriptItem:
    id: str
    start_offset: timedelta
    end_offset: timedelta
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
        key=lambda item: item.start_offset,
    )


def get_output_transcript_item(shift_seconds: float, transcript_item: TranscriptItem):
    start_seconds = round(max(transcript_item.phrase_start + shift_seconds, 0))
    end_seconds = round(max(transcript_item.phrase_end + shift_seconds, 0))

    return OutputTranscriptItem(
        id=transcript_item.id,
        start_offset=timedelta(seconds=start_seconds),
        end_offset=timedelta(seconds=end_seconds),
        phrase=transcript_item.phrase,
        commands=transcript_item.commands,
    )
