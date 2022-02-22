import json
from typing import TextIO

from voice_vid.reconcile_commands import ReconciledCommand


def read(file: TextIO):
    raw_items = [json.loads(line.strip()) for line in file.readlines()]

    return [
        ReconciledCommand(
            shift_seconds=raw_item["shiftSeconds"],
            id=raw_item["id"],
        )
        for raw_item in raw_items
    ]


def write(file: TextIO, reconciled_commands: list[ReconciledCommand]):
    file.write(
        "\n".join(
            json.dumps(
                {
                    "shiftSeconds": reconciled_command.shift_seconds,
                    "id": reconciled_command.id,
                }
            )
            for reconciled_command in reconciled_commands
        )
    )
