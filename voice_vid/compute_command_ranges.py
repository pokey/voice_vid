from dataclasses import dataclass
from itertools import pairwise

import opentimelineio as otio
import typer

from voice_vid.io.parse_transcript import Transcript, TranscriptItem
from voice_vid.reconcile_commands import ReconciledCommand

# How long to extend the phrase before and after to make things less abrupt in
# certain situations
GRACE_PERIOD_SECONDS = 1.02465608102


@dataclass
class CommandTiming:
    shift_seconds: float
    transcript_item: TranscriptItem
    target_grace_start_seconds: float
    target_start_seconds: float
    target_end_seconds: float
    target_grace_end_seconds: float


def compute_command_ranges(
    timeline: otio.schema.Timeline, reconciled_commands: list[ReconciledCommand]
):
    commands = sorted(
        (
            get_proposed_command_timing(
                timeline.duration().to_seconds(),
                reconciled_command.shift_seconds,
                reconciled_command.transcript_item,
            )
            for reconciled_command in reconciled_commands
        ),
        key=lambda command: command.target_start_seconds,
    )

    for command_1, command_2 in pairwise(commands):
        # Don't let grace period of a command extend backwards into the previous
        # command phrase. Note that we do allow it to extend into the end grace
        # period of the previous phrase if they overlap.  We give the start
        # grace period a bit of priority because it's more important for understanding
        # the command
        command_2.target_grace_start_seconds = max(
            command_2.target_grace_start_seconds, command_1.target_end_seconds
        )

        # As mentioned above, we cut the end grace period of a command short if
        # it extends into the start grace period of the next command.
        command_1.target_grace_end_seconds = min(
            command_1.target_grace_end_seconds, command_2.target_grace_start_seconds
        )

        # If the actual command phrases of two commands overlap, we give
        # priority to the start of the next command
        command_1.target_end_seconds = min(
            command_1.target_end_seconds, command_2.target_start_seconds
        )

    return commands


def get_proposed_command_timing(
    timeline_duration: float,
    shift_seconds: float,
    transcript_item: TranscriptItem,
):
    def shift_and_clamp(raw_seconds: float):
        return max(min(raw_seconds + shift_seconds, timeline_duration), 0)

    return CommandTiming(
        target_grace_start_seconds=shift_and_clamp(
            (transcript_item.phrase_start - GRACE_PERIOD_SECONDS)
        ),
        target_start_seconds=shift_and_clamp(transcript_item.phrase_start),
        target_end_seconds=shift_and_clamp(transcript_item.command_start),
        target_grace_end_seconds=shift_and_clamp(
            (transcript_item.command_start + GRACE_PERIOD_SECONDS)
        ),
        shift_seconds=shift_seconds,
        transcript_item=transcript_item,
    )
