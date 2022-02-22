from math import floor

from voice_vid.io.parse_transcript import TranscriptItem


def format_time_stamp(total_seconds: float):
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = floor((seconds * 1000) % 1000)
    return f"{int(hours):02}:{int(minutes):02}:{floor(seconds):02},{milliseconds:03}"


def format_transcript(transcript: list[TranscriptItem]):
    transcript_items = [
        format_transcript_item(index, item) for index, item in enumerate(transcript)
    ]

    return "\n\n".join(transcript_items)


def format_transcript_item(index: int, item: TranscriptItem):
    return f"""
{index + 1}
{format_time_stamp(item.phrase_start)} --> {format_time_stamp(item.phrase_end)}
{item.phrase}
        """.strip()
