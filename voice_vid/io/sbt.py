from math import floor

from voice_vid.generate_subtitles import Subtitle


def format_time_stamp(total_seconds: float):
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = floor((seconds * 1000) % 1000)
    return f"{int(hours):02}:{int(minutes):02}:{floor(seconds):02},{milliseconds:03}"


def format_transcript(transcript: list[Subtitle]):
    transcript_items = [
        format_transcript_item(index, item) for index, item in enumerate(transcript)
    ]

    return "\n\n".join(transcript_items)


def format_transcript_item(index: int, item: Subtitle):
    return f"""
{index + 1}
{format_time_stamp(item.start_seconds)} --> {format_time_stamp(item.end_seconds)}
{item.text}
        """.strip()
