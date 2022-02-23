import giturlparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class RepoInfo:
    type: str
    talon_path: Path
    repo_base_url: str


@dataclass
class Command:
    phrase: str
    grammar: str
    rule_uri: str


@dataclass(frozen=True)
class TranscriptItem:
    id: str
    phrase_start: float
    phrase_end: float
    command_end: float
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


def construct_rule_uri(
    repo_infos: list[RepoInfo],
    local_path: Path,
    line_number: int,
):
    repo_info = next(
        repo_info
        for repo_info in repo_infos
        if local_path.is_relative_to(repo_info.talon_path)
    )

    path = local_path.relative_to(repo_info.talon_path)

    return f"{repo_info.repo_base_url}/{path}#L{line_number}"


{
    "type": "directoryInfo",
    "localPath": "/Users/pokey/.talon/user/cursorless-talon",
    "localRealPath": "/Users/pokey/src/cursorless-talon",
    "repoRemoteUrl": "git@github.com:cursorless-dev/cursorless-talon.git",
    "repoPrefix": "",
    "commitSha": "eb5e57c49b8f854f13ca1671b67d80a91c832c2f",
}


def construct_repo_base_url(raw_repo_info: dict[str, Any]):
    parsed: Any = giturlparse.parse(raw_repo_info["repoRemoteUrl"])
    commit_sha = raw_repo_info["commitSha"]
    repo_prefix = raw_repo_info["repoPrefix"]
    prefix = f"/{repo_prefix}" if repo_prefix else ""

    return f"https://github.com/{parsed.owner}/{parsed.repo}/blob/{commit_sha}{prefix}"


def parse_talon_transcript(path: Path):
    raw_transcript: list[dict[str, Any]] = [
        json.loads(line) for line in path.read_text().splitlines()
    ]
    initial_info = next(
        item for item in raw_transcript if item["type"] == "initialInfo"
    )
    talon_dir = Path(initial_info["talonDir"])

    repo_infos = [
        RepoInfo(
            type=raw_repo_info["type"],
            talon_path=Path(raw_repo_info["localPath"]),
            repo_base_url=construct_repo_base_url(raw_repo_info),
        )
        for raw_repo_info in raw_transcript
        if raw_repo_info["type"] == "directoryInfo"
    ]

    return Transcript(
        items=[
            TranscriptItem(
                id=raw_transcript_item["id"],
                phrase_start=raw_transcript_item["timeOffsets"]["speechStart"],
                phrase_end=raw_transcript_item["timeOffsets"]["prePhraseCallbackStart"],
                command_end=raw_transcript_item["timeOffsets"][
                    "postPhraseCallbackStart"
                ],
                phrase=raw_transcript_item["phrase"],
                commands=[
                    Command(
                        phrase=raw_command["phrase"],
                        grammar=raw_command["grammar"],
                        rule_uri=construct_rule_uri(
                            repo_infos,
                            talon_dir / raw_command["file"],
                            raw_command["user_rule"]["line"],
                        ),
                    )
                    for raw_command in raw_transcript_item["commands"]
                ],
            )
            for raw_transcript_item in raw_transcript
            if raw_transcript_item["type"] == "talonCommandPhrase"
        ],
        repo_infos=repo_infos,
        talon_dir=talon_dir,
    )
