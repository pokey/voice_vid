from voice_vid.io.parse_transcript import Transcript, TranscriptItem
from voice_vid.reconcile_commands import ReconciledCommand


def generate_subtitles(
    talon_transcript: Transcript, reconciled_commands: list[ReconciledCommand]
):
    return sorted(
        {
            get_output_transcript_item(
                reconciled_command.shift_seconds,
                talon_transcript[reconciled_command.id],
            )
            for reconciled_command in reconciled_commands
        },
        key=lambda subtitle: subtitle.phrase_start,
    )


def get_output_transcript_item(shift_seconds: float, transcript_item: TranscriptItem):
    return TranscriptItem(
        phrase_start=max(transcript_item.phrase_start + shift_seconds, 0),
        phrase_end=transcript_item.phrase_end + shift_seconds,
        phrase=transcript_item.phrase,
        id=transcript_item.id,
    )
