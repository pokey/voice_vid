from typer.testing import CliRunner
from tests.data import get_data_file

from voice_vid.main import app

runner = CliRunner()


def test_app():
    raw_transcript = str(get_data_file("raw-transcript.jsonl"))
    expected_output = get_data_file("expected-output.srt").read_text()
    result = runner.invoke(app, [raw_transcript])
    assert result.exit_code == 0
    assert result.stdout == expected_output
