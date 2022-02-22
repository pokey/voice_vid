from typer.testing import CliRunner
from tests.data import get_data_path

from voice_vid.main import app

runner = CliRunner()


def test_app(snapshot):
    index_path = get_data_path("simple") / "index.toml"

    result = runner.invoke(app, [str(index_path)])

    assert result.exit_code == 0
    assert result.stdout == snapshot
