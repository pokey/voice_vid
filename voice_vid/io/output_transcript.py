import json
from typing import TextIO

from voice_vid.generate_transcript import OutputTranscript


def write(file: TextIO, transcript: OutputTranscript):
    json.dump(
        {
            "youtubeSlug": transcript.youtube_slug,
            "title": transcript.title,
            "transcript": [
                {
                    "id": transcript_item.id,
                    "startOffset": transcript_item.start_offset,
                    "endOffset": transcript_item.end_offset,
                    "phrase": transcript_item.phrase,
                    "isError": transcript_item.is_error,
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
                for transcript_item in transcript.transcript_items
            ],
        },
        file,
    )
