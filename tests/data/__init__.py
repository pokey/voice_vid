import os
from pathlib import Path


def get_data_file(name: str):
    return Path(os.path.dirname(__file__)) / name
