import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from typer.testing import CliRunner
from voice_vid.main import app

from tests.data import get_data_path

runner = CliRunner()

testdata = [("simple"), ("version_0")]


@pytest.mark.parametrize("data_dir", testdata)
def test_reconcile(snapshot, data_dir):
    index_path = get_data_path(data_dir) / "index.toml"

    result = runner.invoke(app, ["reconcile", str(index_path)])

    assert result.exit_code == 0
    assert result.stdout == snapshot


@pytest.mark.parametrize("data_dir", testdata)
def test_subtitles(snapshot, data_dir):
    data_dir = get_data_path(data_dir)
    index_path = data_dir / "index.toml"
    reconciled_path = data_dir / "reconciled.jsonl"

    result = runner.invoke(
        app, ["subtitles", "--reconciled", str(reconciled_path), str(index_path)]
    )

    assert result.exit_code == 0
    assert result.stdout == snapshot


@pytest.mark.parametrize("data_dir", testdata)
def test_transcript(snapshot, data_dir):
    data_dir = get_data_path(data_dir)
    index_path = data_dir / "index.toml"
    reconciled_path = data_dir / "reconciled.jsonl"

    result = runner.invoke(
        app, ["transcript", "--reconciled", str(reconciled_path), str(index_path)]
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout) == snapshot


@pytest.mark.parametrize("data_dir", testdata)
def test_mark_highlights(snapshot, data_dir):
    data_dir = get_data_path(data_dir)
    index_path = data_dir / "index.toml"
    reconciled_path = data_dir / "reconciled.jsonl"

    with TemporaryDirectory() as temp_dir:
        output_path = Path(temp_dir) / "output.xml"

        result = runner.invoke(
            app,
            [
                "mark-highlights",
                "--reconciled",
                str(reconciled_path),
                str(index_path),
                str(output_path),
            ],
        )

        assert result.exit_code == 0
        assert output_path.read_text() == snapshot
