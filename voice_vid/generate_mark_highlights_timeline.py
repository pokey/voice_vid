import copy
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import opentimelineio as otio

from voice_vid.calculate_mark_highlights_timing import calculate_mark_highlights_timing
from voice_vid.compute_command_ranges import CommandTiming
from voice_vid.io.parse_config import Config
from voice_vid.io.parse_transcript import Command


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


def generate_mark_highlights_timeline(
    config: Config,
    input_timeline: otio.schema.Timeline,
    reconciled_commands: list[CommandTiming],
):
    media_reference = extract_media_reference(
        config.screen_recording_path, input_timeline
    )

    source_framerate = int(media_reference.metadata["fcp_xml"]["rate"]["timebase"])
    timeline_framerate = int(
        input_timeline.metadata["fcp_xml"]["timecode"]["rate"]["timebase"]
    )

    highlight_timings = calculate_mark_highlights_timing(
        config,
        reconciled_commands,
        source_framerate,
        timeline_framerate,
        input_timeline.duration().to_seconds(),
    )

    transition_time = otio.opentime.RationalTime(value=10, rate=timeline_framerate)

    current_time = otio.opentime.RationalTime(value=0, rate=timeline_framerate)
    items = []
    for highlight_timing in highlight_timings:
        if highlight_timing.target_start_seconds > current_time:
            items.append(
                otio.schema.Gap(
                    name=f"{highlight_timing.transcript_item.id}.leading-gap",
                    source_range=otio.opentime.TimeRange.range_from_start_end_time(
                        current_time, highlight_timing.target_start_seconds
                    ),
                )
            )

        items += [
            otio.schema.Clip(
                name=f"{highlight_timing.transcript_item.id}.leading-clip",
                media_reference=media_reference,
                source_range=otio.opentime.TimeRange(
                    start_time=(
                        highlight_timing.target_start_seconds
                        + highlight_timing.target_to_source_shift
                    ),
                    duration=transition_time,
                ),
            ),
            create_transition(transition_time),
            create_freeze_frame(
                name=f"{highlight_timing.transcript_item.id}.highlights",
                media_reference=media_reference,
                source_time=highlight_timing.source_highlight_offset_seconds,
                duration=(
                    highlight_timing.target_end_seconds
                    - highlight_timing.target_start_seconds
                    - transition_time
                    - transition_time
                ),
            ),
            create_transition(transition_time),
            create_freeze_frame(
                name=f"{highlight_timing.transcript_item.id}.trailing-unhighlighted",
                media_reference=media_reference,
                source_time=highlight_timing.source_unhighlighted_offset_seconds,
                duration=transition_time,
            ),
        ]

        current_time = highlight_timing.target_end_seconds

    track = otio.schema.Track(
        name="Mark highlights",
        metadata={"fcp_xml": {"enabled": "TRUE", "locked": "FALSE"}},
        children=items,
    )

    timeline = copy.deepcopy(input_timeline)
    timeline.name = "Mark highlights timeline"
    timeline.tracks[:] = [track]

    return timeline


def extract_media_reference(
    screen_recording_path: Path, timeline: otio.schema.Timeline
):
    recording_path_uri = screen_recording_path.as_uri()

    clip = next(
        clip
        for clip in timeline.each_clip()
        if clip.media_reference.target_url == recording_path_uri
    )

    return clip.media_reference


# To do a freeze frame we actually just slow the source video down a bunch. The
# below speed is the speed which we use for freeze frame, where 1 is full speed.
# Note that we can't make this speed too slow, because the source timestamps get
# divided by this value, and if they're two large things get messed up
FREEZE_FRAME_SPEED = 0.997122 / 500

# Speed is expected to be a string where 100 represents full speed
FREEZE_FRAME_SPEED_STR = str(FREEZE_FRAME_SPEED * 100)


def create_freeze_frame(
    name: str,
    media_reference: otio.schema.ExternalReference,
    source_time: otio.opentime.RationalTime,
    duration: otio.opentime.RationalTime,
):
    start_time = (
        otio.opentime.RationalTime(
            source_time.value / FREEZE_FRAME_SPEED, source_time.rate
        )
        - duration
    )

    return otio.schema.Clip(
        name=name,
        media_reference=media_reference,
        source_range=otio.opentime.TimeRange(
            start_time=start_time,
            duration=duration,
        ),
        metadata={
            "fcp_xml": {
                "filter": [
                    {
                        "effect": {
                            "effectcategory": "motion",
                            "effectid": "timeremap",
                            "effecttype": "motion",
                            "mediatype": "video",
                            "name": "Time Remap",
                            "parameter": [
                                {
                                    "name": "speed",
                                    "parameterid": "speed",
                                    "value": FREEZE_FRAME_SPEED_STR,
                                    "valuemax": "10000",
                                    "valuemin": "-10000",
                                },
                            ],
                        },
                        "enabled": "TRUE",
                        "end": "-1",
                        "start": "-1",
                    },
                ],
            }
        },
    )


def create_transition(transition_time: otio.opentime.RationalTime):
    return otio.schema.Transition(
        name="Cross Dissolve",
        transition_type="SMPTE_Dissolve",
        in_offset=transition_time,
        out_offset=transition_time,
        metadata={
            "fcp_xml": {
                "alignment": "center",
                "effect": {
                    "name": "Cross Dissolve",
                    "effectid": "Cross Dissolve",
                    "effecttype": "transition",
                    "mediatype": "video",
                    "effectcategory": "Dissolve",
                    "startratio": 0,
                    "endratio": 1,
                    "reverse": False,
                },
            },
        },
    )
