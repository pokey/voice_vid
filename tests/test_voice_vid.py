from typer.testing import CliRunner
from tests.data import get_data_path

from voice_vid.main import app

runner = CliRunner()


def test_app():
    data_dir = get_data_path("simple")
    index_path = data_dir / "index.toml"
    expected_output = (data_dir / "expected-output.srt").read_text()

    result = runner.invoke(app, [str(index_path)])

    assert result.exit_code == 0
    assert result.stdout == expected_output
