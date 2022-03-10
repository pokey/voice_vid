import json
from typing import TextIO

from voice_vid.compute_command_ranges import CommandTiming
from voice_vid.io.parse_transcript import Transcript


def read(file: TextIO, transcript: Transcript):
    raw_items = [json.loads(line.strip()) for line in file.readlines()]

    return [
        CommandTiming(
            shift_seconds=raw_item["shiftSeconds"],
            transcript_item=transcript.item_map[raw_item["transcriptItem"]],
            target_grace_start_seconds=raw_item["targetGraceStartSeconds"],
            target_start_seconds=raw_item["targetStartSeconds"],
            target_end_seconds=raw_item["targetEndSeconds"],
            target_grace_end_seconds=raw_item["targetGraceEndSeconds"],
        )
        for raw_item in raw_items
    ]


def write(file: TextIO, reconciled_commands: list[CommandTiming]):
    file.write(
        "\n".join(
            json.dumps(
                {
                    "shiftSeconds": reconciled_command.shift_seconds,
                    "transcriptItem": reconciled_command.transcript_item.id,
                    "targetGraceStartSeconds": reconciled_command.target_grace_start_seconds,
                    "targetStartSeconds": reconciled_command.target_start_seconds,
                    "targetEndSeconds": reconciled_command.target_end_seconds,
                    "targetGraceEndSeconds": reconciled_command.target_grace_end_seconds,
                }
            )
            for reconciled_command in reconciled_commands
        )
    )
