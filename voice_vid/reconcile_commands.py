from dataclasses import dataclass
from pathlib import Path

import opentimelineio as otio
import typer

from voice_vid.io.parse_transcript import Transcript, TranscriptItem
from voice_vid.itertools import unique


@dataclass
class SubtitleRange:
    phrase_source_range: otio.opentime.TimeRange
    raw_phrase_start_time: otio.opentime.RationalTime
    transcript_item: TranscriptItem


@dataclass
class ReconciledCommand:
    shift_seconds: float
    transcript_item: TranscriptItem


def reconcile_commands(
    talon_transcript: Transcript,
    offset_str: str,
    timeline: otio.schema.Timeline,
    recording_path: Path,
):
    recording_path_uri = recording_path.as_uri()

    clips = [
        clip
        for clip in timeline.each_clip()
        if clip.media_reference.target_url == recording_path_uri
    ]

    framerate = int(clips[0].media_reference.metadata["fcp_xml"]["rate"]["timebase"])
    talon_log_start = otio.opentime.RationalTime.from_timecode(offset_str, framerate)

    subtitle_source_ranges = list(
        filter(
            None,
            (
                get_subtitle_source_range(talon_log_start, framerate, transcript_item)
                for transcript_item in talon_transcript
            ),
        )
    )

    return list(
        unique(
            (
                subtitle
                for clip in clips
                for subtitle in find_subtitles_in_clip(subtitle_source_ranges, clip)
            ),
            key=lambda command: (command.shift_seconds, command.transcript_item.id),
        )
    )


def get_subtitle_source_range(
    talon_log_start: otio.opentime.RationalTime,
    framerate: int,
    transcript_item: TranscriptItem,
):
    if transcript_item.phrase_start < 0:
        # For some reason, occasionally a phrase will have a negative start time.
        # It's pretty rare so we just ignore it and warn
        typer.echo(
            f"WARNING: Invalid phrase start on command {transcript_item.id}", err=True
        )
        return None

    raw_phrase_start_time = otio.opentime.RationalTime.from_seconds(
        transcript_item.phrase_start, framerate
    )

    return SubtitleRange(
        phrase_source_range=otio.opentime.TimeRange(
            start_time=talon_log_start + raw_phrase_start_time,
            duration=otio.opentime.RationalTime.from_seconds(
                transcript_item.phrase_end - transcript_item.phrase_start, framerate
            ),
        ),
        raw_phrase_start_time=raw_phrase_start_time,
        transcript_item=transcript_item,
    )


def find_subtitles_in_clip(
    subtitle_source_ranges: list[SubtitleRange],
    clip: otio.schema.Clip,
):
    source_range = clip.trimmed_range()
    target_range = clip.trimmed_range_in_parent()

    return [
        get_reconciled_command(subtitle, source_range, target_range)
        for subtitle in subtitle_source_ranges
        if source_range.intersects(subtitle.phrase_source_range)
    ]


def get_reconciled_command(
    subtitle: SubtitleRange,
    source_range: otio.opentime.TimeRange,
    target_range: otio.opentime.TimeRange,
):
    subtitle_target_range = otio.opentime.TimeRange(
        start_time=(
            target_range.start_time
            + (subtitle.phrase_source_range.start_time - source_range.start_time)
        ),
        duration=subtitle.phrase_source_range.duration,
    )

    return ReconciledCommand(
        shift_seconds=(
            subtitle_target_range.start_time - subtitle.raw_phrase_start_time
        ).to_seconds(),
        transcript_item=subtitle.transcript_item,
    )
