import runpy
from pathlib import Path
from unittest.mock import Mock, patch


def test_retrieve_product_prints_expected_fields(capsys):
    script_path = Path(__file__).parents[2] / "src" / "insuranceservice" / "products" / "Retrieve.py"

    mock_response = Mock()
    mock_response.ok = True
    mock_response.json.return_value = {
        "id": "123",
        "name": "Test Product",
        "code": "4741",
        "createdAt": "2025-09-22T10:00:00Z",
        "details": {"k1": "v1"},
    }

    with patch("requests.get", return_value=mock_response):
        runpy.run_path(str(script_path), run_name="__main__")

    out = capsys.readouterr()
    assert "Produkt:" in out
    assert "ID:        123" in out
    assert "Name:      Test Product" in out
    assert "Code:      4741" in out
    print(out)