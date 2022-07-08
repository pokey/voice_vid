from dataclasses import dataclass

import opentimelineio as otio

from voice_vid.compute_command_ranges import CommandTiming
from voice_vid.io.parse_config import Config
from voice_vid.io.parse_transcript import TranscriptItem


@dataclass
class Highlight:
    transcript_item: TranscriptItem
    target_to_source_shift: otio.opentime.RationalTime
    target_start_seconds: otio.opentime.RationalTime
    target_end_seconds: otio.opentime.RationalTime
    source_highlight_offset_seconds: otio.opentime.RationalTime
    source_unhighlighted_offset_seconds: otio.opentime.RationalTime


def calculate_mark_highlights_timing(
    config: Config,
    reconciled_commands: list[CommandTiming],
    source_framerate: int,
    timeline_framerate: int,
    timeline_duration: float,
):
    talon_log_start = otio.opentime.RationalTime.from_timecode(
        config.talon_offset, source_framerate
    ).rescaled_to(timeline_framerate)

    return list(
        filter(
            None,
            (
                get_highlight_timing(
                    talon_log_start,
                    timeline_framerate,
                    timeline_duration,
                    reconciled_command,
                )
                for reconciled_command in reconciled_commands
            ),
        )
    )


def get_highlight_timing(
    talon_log_start: otio.opentime.RationalTime,
    framerate: int,
    timeline_duration: float,
    reconciled_command: CommandTiming,
):
    transcript_item = reconciled_command.transcript_item
    shift_seconds = reconciled_command.shift_seconds

    source_highlight_offset_seconds = (
        transcript_item.mark_highlight_screenshot_offset_seconds
    )

    if source_highlight_offset_seconds is None:
        return None

    def target_shift_and_clamp(raw_seconds: float):
        return otio.opentime.RationalTime.from_seconds(
            max(min(raw_seconds + shift_seconds, timeline_duration), 0), framerate
        )

    def source_shift(raw_seconds: float):
        return talon_log_start + otio.opentime.RationalTime.from_seconds(
            raw_seconds, framerate
        )

    return Highlight(
        target_to_source_shift=(
            talon_log_start
            - otio.opentime.RationalTime.from_seconds(shift_seconds, framerate)
        ),
        transcript_item=reconciled_command.transcript_item,
        target_start_seconds=otio.opentime.RationalTime.from_seconds(
            reconciled_command.target_grace_start_seconds, framerate
        ),
        # NB: We need the target to end exactly at command start so that it
        # obscures the highlight flash but doesn't obscure command execution
        target_end_seconds=target_shift_and_clamp(transcript_item.command_start),
        source_highlight_offset_seconds=source_shift(source_highlight_offset_seconds),
        source_unhighlighted_offset_seconds=source_shift(
            transcript_item.pre_phrase_screenshot_offset_seconds
        ),
    )
