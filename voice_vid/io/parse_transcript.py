import json
from dataclasses import dataclass
from functools import reduce
from itertools import groupby
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4

import giturlparse

from voice_vid.deep_merge import deep_merge


@dataclass
class RepoInfo:
    type: str
    talon_path: Path
    repo_base_url: str
    is_cursorless: bool


@dataclass
class Command:
    phrase: str
    grammar: str
    rule: str
    rule_uri: str
    is_cursorless_command: bool


@dataclass(frozen=True)
class TranscriptItem:
    id: str
    is_error: bool
    phrase_start: float
    phrase_end: float
    command_start: float
    command_end: Optional[float]
    mark_highlight_screenshot_offset_seconds: Optional[float]
    pre_phrase_screenshot_offset_seconds: float
    phrase: str
    commands: list[Command]


class Transcript:
    def __init__(
        self, items: list[TranscriptItem], repo_infos: list[RepoInfo], talon_dir: Path
    ):
        self.items = items
        self.item_map = {item.id: item for item in self.items}
        self.talon_dir = talon_dir

    def __iter__(self):
        return iter(self.items)

    def __getitem__(self, key: str):
        return self.item_map[key]


def construct_command(
    talon_dir: Path,
    repo_infos: list[RepoInfo],
    raw_command: dict[str, Any],
):
    local_path = talon_dir / raw_command["file"]
    line_number = raw_command["user_rule"]["line"]

    repo_info = next(
        repo_info
        for repo_info in repo_infos
        if local_path.is_relative_to(repo_info.talon_path)
    )

    path = local_path.relative_to(repo_info.talon_path)

    rule_uri = f"{repo_info.repo_base_url}/{path}#L{line_number}"

    return Command(
        phrase=raw_command["phrase"],
        grammar=raw_command["grammar"],
        rule=raw_command["user_rule"]["rule"],
        rule_uri=rule_uri,
        is_cursorless_command=repo_info.is_cursorless,
    )


def construct_repo_info(raw_repo_info: dict[str, Any]):
    parsed: Any = giturlparse.parse(raw_repo_info["repoRemoteUrl"])
    commit_sha = raw_repo_info["commitSha"]
    repo_prefix = raw_repo_info["repoPrefix"]
    prefix = f"/{repo_prefix}" if repo_prefix else ""

    base_url = (
        f"https://github.com/{parsed.owner}/{parsed.repo}/blob/{commit_sha}{prefix}"
    )

    return RepoInfo(
        type=raw_repo_info["type"],
        talon_path=Path(raw_repo_info["localPath"]),
        repo_base_url=base_url,
        is_cursorless=(parsed.owner == "cursorless-dev"),
    )


def parse_talon_transcript(path: Path):
    fragmented_raw_transcript: list[dict[str, Any]] = [
        json.loads(line) for line in path.read_text().splitlines()
    ]

    # If two items appear with the same id we do a deep merge on everything in
    # that item
    unfiltered = [
        reduce(deep_merge, group)
        for _, group in groupby(
            fragmented_raw_transcript, lambda item: item.get("id", uuid4())
        )
    ]
    raw_transcript = list(
        filter(
            lambda x: "type" in x,
            unfiltered,
        )
    )
    initial_info = next(
        item for item in raw_transcript if item["type"] == "initialInfo"
    )
    initial_info["version"] = initial_info.get("version", 0)

    talon_dir = Path(initial_info["talonDir"])

    repo_infos = [
        construct_repo_info(raw_repo_info)
        for raw_repo_info in raw_transcript
        if raw_repo_info["type"] == "directoryInfo"
    ]

    return Transcript(
        items=list(
            filter(
                None,
                [
                    construct_transcript_item(
                        initial_info["version"],
                        talon_dir,
                        repo_infos,
                        raw_transcript_item,
                    )
                    for raw_transcript_item in raw_transcript
                    if raw_transcript_item["type"] == "talonCommandPhrase"
                ],
            )
        ),
        repo_infos=repo_infos,
        talon_dir=talon_dir,
    )


def construct_transcript_item(
    version: int, talon_dir: Path, repo_infos: list[RepoInfo], raw_transcript_item: dict
):
    raw_screenshots: dict = raw_transcript_item["screenshots"]

    if version >= 2:
        decorated_mark_screenshots = raw_screenshots.get("decoratedMarks.all")

        mark_highlight_screenshot_offset_seconds = (
            None
            if decorated_mark_screenshots is None
            else decorated_mark_screenshots["timeOffset"]
        )
    else:
        decorated_mark_screenshots = raw_screenshots["decoratedMarks"]

        mark_highlight_screenshot_offset_seconds = (
            None
            if decorated_mark_screenshots is None
            else decorated_mark_screenshots["all"]["timeOffset"]
        )

    try:
        return TranscriptItem(
            id=raw_transcript_item["id"],
            phrase_start=raw_transcript_item["timeOffsets"]["speechStart"],
            phrase_end=raw_transcript_item["timeOffsets"]["prePhraseCallbackStart"],
            command_start=raw_transcript_item["timeOffsets"]["prePhraseCallbackEnd"],
            mark_highlight_screenshot_offset_seconds=mark_highlight_screenshot_offset_seconds,
            pre_phrase_screenshot_offset_seconds=raw_screenshots["preCommand"][
                "timeOffset"
            ],
            command_end=raw_transcript_item["timeOffsets"].get(
                "postPhraseCallbackStart", None
            ),
            # In version 0, we only got commands that completed successfully. In
            # later versions, we also log commands that didn't complete
            # successfully. We know the command completed successfully if it has a
            # `commandCompleted` attribute set
            is_error=not raw_transcript_item.get("commandCompleted", version == 0),
            phrase=raw_transcript_item["phrase"],
            commands=[
                construct_command(talon_dir, repo_infos, raw_command)
                for raw_command in raw_transcript_item["commands"]
            ],
        )
    except:
        return None
