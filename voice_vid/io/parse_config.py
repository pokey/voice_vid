from dataclasses import dataclass
from pathlib import Path
import toml


@dataclass
class Config:
    timeline_path: Path
    talon_log_dir_path: Path
    screen_recording_path: Path
    talon_offset: str
    vscode_offset: str


def parse_config(path: Path):
    raw_config = toml.load(path)

    def resolve_path(raw_path_str: str):
        raw_path = Path(raw_path_str)

        if not raw_path.is_absolute():
            raw_path = path.parent / raw_path

        return raw_path.resolve(strict=True)

    return Config(
        timeline_path=resolve_path(raw_config["timeline_path"]),
        talon_log_dir_path=resolve_path(raw_config["talon_log_dir_path"]),
        screen_recording_path=resolve_path(raw_config["screen_recording_path"]),
        talon_offset=raw_config["talon_offset"],
        vscode_offset=raw_config["vscode_offset"],
    )
