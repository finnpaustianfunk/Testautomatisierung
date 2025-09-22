from pathlib import Path
import runpy
from unittest.mock import Mock, patch



def test_retrieve_lead_and_print_fields(capsys):
    script_path = Path(__file__).parents[2] / "src" / "insuranceservice" / "leads" / "Retrieve.py"

    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {
        "id": "1111",
        "name": "Test-Lead",
        "code": "2234",
        "createdAt": "2025-09-22T13:00:00Z",
        "details": {"k2", "v2"},
    }

    with patch("request.get", return_value=mock_response):
        runpy.run_path(str(script_path), run_name="__main__")

    out, err = capsys.readouterr()
    assert "Lead:" in out
    assert "ID:     1111" in out
    assert "Name:   Test-Lead",
    assert "Code:   2234" in out
    print(out)
