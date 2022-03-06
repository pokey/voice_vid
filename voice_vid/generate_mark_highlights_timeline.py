from dataclasses import dataclass
from datetime import timedelta
from typing import Optional
from voice_vid.io.parse_config import Config
from voice_vid.io.parse_transcript import Command, Transcript, TranscriptItem
from voice_vid.reconcile_commands import ReconciledCommand
import opentimelineio as otio


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
    talon_transcript: Transcript,
    reconciled_commands: list[ReconciledCommand],
):
    timeline = otio.schema.Timeline(
        name="Timeline 1 (Resolve)",
        tracks=otio.schema.Stack(
            name="Timeline 1 (Resolve)",
            children=[
                otio.schema.Track(
                    name="",
                    children=[
                        otio.schema.Gap(
                            name="",
                            source_range=otio.opentime.TimeRange(
                                start_time=otio.opentime.RationalTime(value=0, rate=60),
                                duration=otio.opentime.RationalTime(
                                    value=2243, rate=60
                                ),
                            ),
                        ),
                        otio.schema.Clip(
                            name="Screen Recording 2022-03-01 at 17.34.23.mov",
                            media_reference=otio.schema.ExternalReference(
                                target_url="file:///Users/pokey/Movies/Cursorless/Completed/React%20component%20and%20fava%20beans/Screen%20Recording%202022-03-01%20at%2017.34.23.mov"
                            ),
                            source_range=otio.opentime.TimeRange(
                                start_time=otio.opentime.RationalTime(
                                    value=7359, rate=60
                                ),
                                duration=otio.opentime.RationalTime(value=10, rate=60),
                            ),
                            metadata={
                                "fcp_xml": {
                                    "@id": "Screen Recording 2022-03-01 at 17.34.23.mov 65",
                                    "comments": None,
                                    "compositemode": "normal",
                                    "enabled": "TRUE",
                                    "filter": [
                                        {
                                            "effect": {
                                                "effectcategory": "motion",
                                                "effectid": "basic",
                                                "effecttype": "motion",
                                                "mediatype": "video",
                                                "name": "Basic Motion",
                                                "parameter": [
                                                    {
                                                        "name": "Scale",
                                                        "parameterid": "scale",
                                                        "value": "100",
                                                        "valuemax": "10000",
                                                        "valuemin": "0",
                                                    },
                                                    {
                                                        "name": "Center",
                                                        "parameterid": "center",
                                                        "value": {
                                                            "horiz": "0",
                                                            "vert": "0",
                                                        },
                                                    },
                                                    {
                                                        "name": "Rotation",
                                                        "parameterid": "rotation",
                                                        "value": "0",
                                                        "valuemax": "100000",
                                                        "valuemin": "-100000",
                                                    },
                                                    {
                                                        "name": "Anchor Point",
                                                        "parameterid": "centerOffset",
                                                        "value": {
                                                            "horiz": "0",
                                                            "vert": "0",
                                                        },
                                                    },
                                                ],
                                            },
                                            "enabled": "TRUE",
                                            "end": "124718",
                                            "start": "0",
                                        },
                                        {
                                            "effect": {
                                                "effectcategory": "motion",
                                                "effectid": "crop",
                                                "effecttype": "motion",
                                                "mediatype": "video",
                                                "name": "Crop",
                                                "parameter": [
                                                    {
                                                        "name": "left",
                                                        "parameterid": "left",
                                                        "value": "0",
                                                        "valuemax": "100",
                                                        "valuemin": "0",
                                                    },
                                                    {
                                                        "name": "right",
                                                        "parameterid": "right",
                                                        "value": "0",
                                                        "valuemax": "100",
                                                        "valuemin": "0",
                                                    },
                                                    {
                                                        "name": "top",
                                                        "parameterid": "top",
                                                        "value": "0",
                                                        "valuemax": "100",
                                                        "valuemin": "0",
                                                    },
                                                    {
                                                        "name": "bottom",
                                                        "parameterid": "bottom",
                                                        "value": "0",
                                                        "valuemax": "100",
                                                        "valuemin": "0",
                                                    },
                                                ],
                                            },
                                            "enabled": "TRUE",
                                            "end": "124718",
                                            "start": "0",
                                        },
                                        {
                                            "effect": {
                                                "effectcategory": "motion",
                                                "effectid": "opacity",
                                                "effecttype": "motion",
                                                "mediatype": "video",
                                                "name": "Opacity",
                                                "parameter": {
                                                    "name": "opacity",
                                                    "parameterid": "opacity",
                                                    "value": "100",
                                                    "valuemax": "100",
                                                    "valuemin": "0",
                                                },
                                            },
                                            "enabled": "TRUE",
                                            "end": "124718",
                                            "start": "0",
                                        },
                                    ],
                                }
                            },
                        ),
                        otio.schema.Transition(
                            name="Cross Dissolve",
                            transition_type="SMPTE_Dissolve",
                            in_offset=otio.opentime.RationalTime(value=10, rate=60),
                            out_offset=otio.opentime.RationalTime(value=10, rate=60),
                            metadata={"fcp_xml": {"alignment": "center"}},
                        ),
                        otio.schema.Clip(
                            name="Screen Recording 2022-03-01 at 17.34.23.mov",
                            media_reference=otio.schema.ExternalReference(
                                target_url="file:///Users/pokey/Movies/Cursorless/Completed/React%20component%20and%20fava%20beans/Screen%20Recording%202022-03-01%20at%2017.34.23.mov"
                            ),
                            source_range=otio.opentime.TimeRange(
                                start_time=otio.opentime.RationalTime(
                                    value=755411, rate=60
                                ),
                                duration=otio.opentime.RationalTime(value=220, rate=60),
                            ),
                            metadata={
                                "fcp_xml": {
                                    "@id": "Screen Recording 2022-03-01 at 17.34.23.mov 67",
                                    "comments": None,
                                    "compositemode": "normal",
                                    "enabled": "TRUE",
                                    "filter": [
                                        {
                                            "effect": {
                                                "effectcategory": "motion",
                                                "effectid": "basic",
                                                "effecttype": "motion",
                                                "mediatype": "video",
                                                "name": "Basic Motion",
                                                "parameter": [
                                                    {
                                                        "name": "Scale",
                                                        "parameterid": "scale",
                                                        "value": "100",
                                                        "valuemax": "10000",
                                                        "valuemin": "0",
                                                    },
                                                    {
                                                        "name": "Center",
                                                        "parameterid": "center",
                                                        "value": {
                                                            "horiz": "0",
                                                            "vert": "0",
                                                        },
                                                    },
                                                    {
                                                        "name": "Rotation",
                                                        "parameterid": "rotation",
                                                        "value": "0",
                                                        "valuemax": "100000",
                                                        "valuemin": "-100000",
                                                    },
                                                    {
                                                        "name": "Anchor Point",
                                                        "parameterid": "centerOffset",
                                                        "value": {
                                                            "horiz": "0",
                                                            "vert": "0",
                                                        },
                                                    },
                                                ],
                                            },
                                            "enabled": "TRUE",
                                            "end": "12507799",
                                            "start": "0",
                                        },
                                        {
                                            "effect": {
                                                "effectcategory": "motion",
                                                "effectid": "crop",
                                                "effecttype": "motion",
                                                "mediatype": "video",
                                                "name": "Crop",
                                                "parameter": [
                                                    {
                                                        "name": "left",
                                                        "parameterid": "left",
                                                        "value": "0",
                                                        "valuemax": "100",
                                                        "valuemin": "0",
                                                    },
                                                    {
                                                        "name": "right",
                                                        "parameterid": "right",
                                                        "value": "0",
                                                        "valuemax": "100",
                                                        "valuemin": "0",
                                                    },
                                                    {
                                                        "name": "top",
                                                        "parameterid": "top",
                                                        "value": "0",
                                                        "valuemax": "100",
                                                        "valuemin": "0",
                                                    },
                                                    {
                                                        "name": "bottom",
                                                        "parameterid": "bottom",
                                                        "value": "0",
                                                        "valuemax": "100",
                                                        "valuemin": "0",
                                                    },
                                                ],
                                            },
                                            "enabled": "TRUE",
                                            "end": "12507799",
                                            "start": "0",
                                        },
                                        {
                                            "effect": {
                                                "effectcategory": "motion",
                                                "effectid": "opacity",
                                                "effecttype": "motion",
                                                "mediatype": "video",
                                                "name": "Opacity",
                                                "parameter": {
                                                    "name": "opacity",
                                                    "parameterid": "opacity",
                                                    "value": "100",
                                                    "valuemax": "100",
                                                    "valuemin": "0",
                                                },
                                            },
                                            "enabled": "TRUE",
                                            "end": "12507799",
                                            "start": "0",
                                        },
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
                                                        "value": "0.997122",
                                                        "valuemax": "10000",
                                                        "valuemin": "-10000",
                                                    },
                                                    {
                                                        "name": "reverse",
                                                        "parameterid": "reverse",
                                                        "value": "FALSE",
                                                    },
                                                    {
                                                        "name": "frameblending",
                                                        "parameterid": "frameblending",
                                                        "value": "FALSE",
                                                    },
                                                    {
                                                        "name": "variablespeed",
                                                        "parameterid": "variablespeed",
                                                        "value": "0",
                                                        "valuemax": "1",
                                                        "valuemin": "0",
                                                    },
                                                    {
                                                        "interpolation": {
                                                            "name": "FCPCurve"
                                                        },
                                                        "keyframe": [
                                                            {
                                                                "speedkfstart": "TRUE",
                                                                "speedvirtualkf": "TRUE",
                                                                "value": "0",
                                                                "when": "0",
                                                            },
                                                            {
                                                                "speedkfin": "TRUE",
                                                                "speedvirtualkf": "TRUE",
                                                                "value": "7532.37",
                                                                "when": "755411",
                                                            },
                                                            {
                                                                "speedkfout": "TRUE",
                                                                "speedvirtualkf": "TRUE",
                                                                "value": "7534.56",
                                                                "when": "755631",
                                                            },
                                                            {
                                                                "speedkfend": "TRUE",
                                                                "speedvirtualkf": "TRUE",
                                                                "value": "124719",
                                                                "when": "12507799",
                                                            },
                                                        ],
                                                        "name": "graphdict",
                                                        "parameterid": "graphdict",
                                                        "valuemax": "124717",
                                                        "valuemin": "0",
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
                        ),
                        otio.schema.Transition(
                            name="Cross Dissolve",
                            transition_type="SMPTE_Dissolve",
                            in_offset=otio.opentime.RationalTime(value=10, rate=60),
                            out_offset=otio.opentime.RationalTime(value=10, rate=60),
                            metadata={"fcp_xml": {"alignment": "center"}},
                        ),
                        otio.schema.Clip(
                            name="Screen Recording 2022-03-01 at 17.34.23.mov",
                            media_reference=otio.schema.ExternalReference(
                                target_url="file:///Users/pokey/Movies/Cursorless/Completed/React%20component%20and%20fava%20beans/Screen%20Recording%202022-03-01%20at%2017.34.23.mov"
                            ),
                            source_range=otio.opentime.TimeRange(
                                start_time=otio.opentime.RationalTime(
                                    value=753003, rate=60
                                ),
                                duration=otio.opentime.RationalTime(value=10, rate=60),
                            ),
                            metadata={
                                "fcp_xml": {
                                    "@id": "Screen Recording 2022-03-01 at 17.34.23.mov 69",
                                    "comments": None,
                                    "compositemode": "normal",
                                    "enabled": "TRUE",
                                    "filter": [
                                        {
                                            "effect": {
                                                "effectcategory": "motion",
                                                "effectid": "basic",
                                                "effecttype": "motion",
                                                "mediatype": "video",
                                                "name": "Basic Motion",
                                                "parameter": [
                                                    {
                                                        "name": "Scale",
                                                        "parameterid": "scale",
                                                        "value": "100",
                                                        "valuemax": "10000",
                                                        "valuemin": "0",
                                                    },
                                                    {
                                                        "name": "Center",
                                                        "parameterid": "center",
                                                        "value": {
                                                            "horiz": "0",
                                                            "vert": "0",
                                                        },
                                                    },
                                                    {
                                                        "name": "Rotation",
                                                        "parameterid": "rotation",
                                                        "value": "0",
                                                        "valuemax": "100000",
                                                        "valuemin": "-100000",
                                                    },
                                                    {
                                                        "name": "Anchor Point",
                                                        "parameterid": "centerOffset",
                                                        "value": {
                                                            "horiz": "0",
                                                            "vert": "0",
                                                        },
                                                    },
                                                ],
                                            },
                                            "enabled": "TRUE",
                                            "end": "12471800",
                                            "start": "0",
                                        },
                                        {
                                            "effect": {
                                                "effectcategory": "motion",
                                                "effectid": "crop",
                                                "effecttype": "motion",
                                                "mediatype": "video",
                                                "name": "Crop",
                                                "parameter": [
                                                    {
                                                        "name": "left",
                                                        "parameterid": "left",
                                                        "value": "0",
                                                        "valuemax": "100",
                                                        "valuemin": "0",
                                                    },
                                                    {
                                                        "name": "right",
                                                        "parameterid": "right",
                                                        "value": "0",
                                                        "valuemax": "100",
                                                        "valuemin": "0",
                                                    },
                                                    {
                                                        "name": "top",
                                                        "parameterid": "top",
                                                        "value": "0",
                                                        "valuemax": "100",
                                                        "valuemin": "0",
                                                    },
                                                    {
                                                        "name": "bottom",
                                                        "parameterid": "bottom",
                                                        "value": "0",
                                                        "valuemax": "100",
                                                        "valuemin": "0",
                                                    },
                                                ],
                                            },
                                            "enabled": "TRUE",
                                            "end": "12471800",
                                            "start": "0",
                                        },
                                        {
                                            "effect": {
                                                "effectcategory": "motion",
                                                "effectid": "opacity",
                                                "effecttype": "motion",
                                                "mediatype": "video",
                                                "name": "Opacity",
                                                "parameter": {
                                                    "name": "opacity",
                                                    "parameterid": "opacity",
                                                    "value": "100",
                                                    "valuemax": "100",
                                                    "valuemin": "0",
                                                },
                                            },
                                            "enabled": "TRUE",
                                            "end": "12471800",
                                            "start": "0",
                                        },
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
                                                        "value": "1",
                                                        "valuemax": "10000",
                                                        "valuemin": "-10000",
                                                    },
                                                    {
                                                        "name": "reverse",
                                                        "parameterid": "reverse",
                                                        "value": "FALSE",
                                                    },
                                                    {
                                                        "name": "frameblending",
                                                        "parameterid": "frameblending",
                                                        "value": "FALSE",
                                                    },
                                                    {
                                                        "name": "variablespeed",
                                                        "parameterid": "variablespeed",
                                                        "value": "0",
                                                        "valuemax": "1",
                                                        "valuemin": "0",
                                                    },
                                                    {
                                                        "interpolation": {
                                                            "name": "FCPCurve"
                                                        },
                                                        "keyframe": [
                                                            {
                                                                "speedkfstart": "TRUE",
                                                                "speedvirtualkf": "TRUE",
                                                                "value": "0",
                                                                "when": "0",
                                                            },
                                                            {
                                                                "speedkfin": "TRUE",
                                                                "speedvirtualkf": "TRUE",
                                                                "value": "7530.03",
                                                                "when": "753003",
                                                            },
                                                            {
                                                                "speedkfout": "TRUE",
                                                                "speedvirtualkf": "TRUE",
                                                                "value": "7530.13",
                                                                "when": "753013",
                                                            },
                                                            {
                                                                "speedkfend": "TRUE",
                                                                "speedvirtualkf": "TRUE",
                                                                "value": "124719",
                                                                "when": "12471800",
                                                            },
                                                        ],
                                                        "name": "graphdict",
                                                        "parameterid": "graphdict",
                                                        "valuemax": "124717",
                                                        "valuemin": "0",
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
                        ),
                    ],
                    source_range=None,
                    metadata={"fcp_xml": {"enabled": "TRUE", "locked": "FALSE"}},
                ),
            ],
            source_range=None,
            metadata={},
        ),
    )
    return timeline


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
