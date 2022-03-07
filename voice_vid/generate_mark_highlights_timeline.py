import copy
from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

import opentimelineio as otio

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


def generate_mark_highlights_timeline(
    config: Config,
    input_timeline: otio.schema.Timeline,
    talon_transcript: Transcript,
    reconciled_commands: list[ReconciledCommand],
):
    recording_path_uri = config.screen_recording_path.as_uri()
    clip = next(
        clip
        for clip in input_timeline.each_clip()
        if clip.media_reference.target_url == recording_path_uri
    )

    media_reference = clip.media_reference
    framerate = int(media_reference.metadata["fcp_xml"]["rate"]["timebase"])

    items = [
        otio.schema.Gap(
            name="",
            source_range=otio.opentime.TimeRange(
                start_time=otio.opentime.RationalTime(value=0, rate=60),
                duration=otio.opentime.RationalTime(value=2243, rate=60),
            ),
        ),
        otio.schema.Clip(
            name="Screen Recording 2022-03-01 at 17.34.23.mov",
            media_reference=media_reference,
            source_range=otio.opentime.TimeRange(
                start_time=otio.opentime.RationalTime(value=7359, rate=60),
                duration=otio.opentime.RationalTime(value=10, rate=60),
            ),
        ),
        create_transition(),
        create_freeze_frame(
            media_reference,
            time=otio.opentime.RationalTime(value=7532.36927142, rate=60),
            duration=otio.opentime.RationalTime(value=220, rate=60),
        ),
        create_transition(),
        create_freeze_frame(
            media_reference,
            time=otio.opentime.RationalTime(value=7508.35857366, rate=60),
            duration=otio.opentime.RationalTime(value=10, rate=60),
        ),
    ]

    track = otio.schema.Track(
        name="",
        metadata={"fcp_xml": {"enabled": "TRUE", "locked": "FALSE"}},
        children=items,
    )

    timeline = copy.deepcopy(input_timeline)
    timeline.tracks[:] = [track]

    return timeline


FREEZE_FRAME_SPEED = 0.997122 / 100
FREEZE_FRAME_SPEED_STR = str(FREEZE_FRAME_SPEED * 100)


def create_freeze_frame(
    media_reference: otio.schema.ExternalReference,
    time: otio.opentime.RationalTime,
    duration: otio.opentime.RationalTime,
):
    start_time = otio.opentime.RationalTime(time.value / FREEZE_FRAME_SPEED, time.rate)

    return otio.schema.Clip(
        name="Screen Recording 2022-03-01 at 17.34.23.mov",
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


def create_transition():
    return otio.schema.Transition(
        name="Cross Dissolve",
        transition_type="SMPTE_Dissolve",
        in_offset=otio.opentime.RationalTime(value=10, rate=60),
        out_offset=otio.opentime.RationalTime(value=10, rate=60),
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


def get_output_transcript_item(shift_seconds: float, transcript_item: TranscriptItem):
    start_seconds = max(transcript_item.phrase_start + shift_seconds, 0)
    end_seconds = max(transcript_item.phrase_end + shift_seconds, 0)

    return OutputTranscriptItem(
        id=transcript_item.id,
        start_offset=start_seconds,
        end_offset=end_seconds,
        phrase=transcript_item.phrase,
        commands=transcript_item.commands,
    )
