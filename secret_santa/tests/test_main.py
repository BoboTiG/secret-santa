from pathlib import Path
from unittest.mock import patch

from secret_santa.__main__ import main, usage
from secret_santa.utils import result_file


def test_no_data_file(capsys):
    assert main(Path("inexistent.black_hole")) == 2
    out, _ = capsys.readouterr()
    assert "introuvable" in out


def test_main(data, capsys):
    def send_emails(*_):
        pass

    with patch("secret_santa.emails.send_emails", send_emails):
        # First run
        assert main(data) == 0
        assert result_file(data).is_file()
        out, _ = capsys.readouterr()
        assert "Les résultats sont déjà connus" not in out

        # Second run
        assert main(data) == 1
        out, _ = capsys.readouterr()
        assert "Les résultats sont déjà connus" in out


def test_usage(capsys):
    usage()
    out, _ = capsys.readouterr()
    assert "python -m secret_santa FILE.yml" in out
