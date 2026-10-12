import pytest

from unittest.mock import patch, MagicMock
from src.tools import search_jobs


@pytest.mark.parametrize("visa,expected_flag", [
    (True, True),
    (False, False),
])
def test_search_jobs_visa_flag(visa, expected_flag):
    with patch("src.tools.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="some job results")
        result = search_jobs(
            query="senior c# developer",
            country="GB",
            seniority="senior",
            skills="csharp,dotnet,aws",
            visa=visa,
            limit=10
        )
        called_cmd = mock_run.call_args[0][0]
        assert result == "some job results"
        if expected_flag:
            assert "--visa" in called_cmd
        else:
            assert "--visa" not in called_cmd
