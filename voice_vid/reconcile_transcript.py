from dataclasses import dataclass
from pathlib import Path
import opentimelineio as otio

from voice_vid.parse_transcript import TranscriptItem


@dataclass
class SubtitleRange:
    range: otio.opentime.TimeRange
    text: str


def reconcile_transcript(
    talon_transcript: list[TranscriptItem],
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

    subtitle_source_ranges = [
        SubtitleRange(
            range=otio.opentime.TimeRange(
                start_time=(
                    talon_log_start
                    + otio.opentime.RationalTime.from_seconds(
                        transcript_item.phrase_start, framerate
                    )
                ),
                duration=otio.opentime.RationalTime.from_seconds(
                    transcript_item.phrase_end - transcript_item.phrase_start, framerate
                ),
            ),
            text=transcript_item.phrase,
        )
        for transcript_item in talon_transcript
    ]

    return sorted(
        {
            subtitle
            for clip in clips
            for subtitle in find_subtitles_in_clip(subtitle_source_ranges, clip)
        },
        key=lambda subtitle: subtitle.phrase_start,
    )


def find_subtitles_in_clip(
    subtitle_source_ranges: list[SubtitleRange],
    clip: otio.schema.Clip,
):
    source_range = clip.trimmed_range()
    target_range = clip.trimmed_range_in_parent()

    return [
        get_transcript_item(subtitle, source_range, target_range)
        for subtitle in subtitle_source_ranges
        if source_range.intersects(subtitle.range)
    ]


def get_transcript_item(
    subtitle: SubtitleRange,
    source_range: otio.opentime.TimeRange,
    target_range: otio.opentime.TimeRange,
):
    subtitle_target_range = otio.opentime.TimeRange(
        start_time=(
            target_range.start_time
            + (subtitle.range.start_time - source_range.start_time)
        ),
        duration=subtitle.range.duration,
    ).clamped(target_range)

    return TranscriptItem(
        phrase_start=subtitle_target_range.start_time.to_seconds(),
        phrase_end=subtitle_target_range.end_time_exclusive().to_seconds(),
        phrase=subtitle.text,
    )
