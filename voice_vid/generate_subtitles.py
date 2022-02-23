from dataclasses import dataclass
from itertools import pairwise
from voice_vid.io.parse_transcript import Transcript, TranscriptItem
from voice_vid.reconcile_commands import ReconciledCommand


@dataclass(unsafe_hash=True)
class Subtitle:
    start_seconds: float
    end_seconds: float
    text: str


def generate_subtitles(
    talon_transcript: Transcript,
    reconciled_commands: list[ReconciledCommand],
    use_command_end: bool,
    end_offset: float,
):
    subtitles = sorted(
        {
            get_output_transcript_item(
                use_command_end,
                reconciled_command.shift_seconds,
                talon_transcript[reconciled_command.id],
            )
            for reconciled_command in reconciled_commands
        },
        key=lambda subtitle: subtitle.start_seconds,
    )

    for subtitle, next_subtitle in pairwise(subtitles):
        end_seconds = subtitle.end_seconds + end_offset

        if end_seconds > next_subtitle.start_seconds:
            end_seconds = next_subtitle.start_seconds

        subtitle.end_seconds = end_seconds

    return subtitles


def get_output_transcript_item(
    use_command_end: bool,
    shift_seconds: float,
    transcript_item: TranscriptItem,
):
    end = transcript_item.command_end if use_command_end else transcript_item.phrase_end

    return Subtitle(
        start_seconds=max(transcript_item.phrase_start + shift_seconds, 0),
        end_seconds=end + shift_seconds,
        text=transcript_item.phrase,
    )
