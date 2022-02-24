import json
from typing import TextIO

from voice_vid.generate_transcript import OutputTranscriptItem


def write(file: TextIO, transcript: list[OutputTranscriptItem]):
    json.dump(
        [
            {
                "id": transcript_item.id,
                "startTimecode": str(transcript_item.start_offset),
                "endTimecode": str(transcript_item.end_offset),
                "phrase": transcript_item.phrase,
                "commands": [
                    {
                        "phrase": command.phrase,
                        "grammar": command.grammar,
                        "rule": command.rule,
                        "ruleUri": command.rule_uri,
                        "isCursorlessCommand": command.is_cursorless_command,
                    }
                    for command in transcript_item.commands
                ],
            }
            for transcript_item in transcript
        ],
        file,
    )
