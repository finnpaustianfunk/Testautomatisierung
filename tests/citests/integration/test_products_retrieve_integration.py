import os
import pytest
import requests


@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("EMIL_API_TOKEN"),
    reason="EMIL_API_TOKEN not set; skipping real API integration test",
)
def test_retrieve_product_real_api():
    token = os.getenv("EMIL_API_TOKEN")
    product_code = os.getenv("EMIL_PRODUCT_CODE", "4741")

    url = f"https://apiv2.emil.de/insuranceservice/v1/products/code/{product_code}"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {token}",
    }

    response = requests.get(url, headers=headers, timeout=30)
    assert response.status_code == 200, f"Unexpected status {response.status_code}: {response.text}"

    data = response.json()
    product = data if isinstance(data, dict) else None
    if isinstance(data, dict) and not any(k in data for k in ("id", "code", "name")):
        product = data.get("product") or data.get("data") or data.get("item")

    assert isinstance(product, dict), "No product object found in response"
    # Minimal field checks
    assert "code" in product, "Product has no 'code' field"
    assert product["code"], "Product code is empty"
