from typer.testing import CliRunner
from tests.data import get_data_path

from voice_vid.main import app

runner = CliRunner()


def test_reconcile(snapshot):
    index_path = get_data_path("simple") / "index.toml"

    result = runner.invoke(app, ["reconcile", str(index_path)])

    assert result.exit_code == 0
    assert result.stdout == snapshot


def test_subtitles(snapshot):
    data_dir = get_data_path("simple")
    index_path = data_dir / "index.toml"
    reconciled_path = data_dir / "reconciled.jsonl"

    result = runner.invoke(
        app, ["subtitles", "--reconciled", str(reconciled_path), str(index_path)]
    )

    assert result.exit_code == 0
    assert result.stdout == snapshot
