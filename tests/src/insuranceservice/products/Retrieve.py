import requests

url = "https://apiv2.emil.de/insuranceservice/v1/products/code/4741"

headers = {
    "accept": "application/json",
    "authorization": "Bearer eyJraWQiOiJTWG9PU3RWOEEzNlVKR2o3bGRsXC9ocGU2QUV6T2E1Nzc3YmM3dTVKeXEyMD0iLCJhbGciOiJSUzI1NiJ9.eyJjdXN0b206dGVuYW50X3NsdWciOiJmdW5rLXNhbmRib3gtcHJvZCIsInN1YiI6IjdkOWE0ZTBhLWNkNTgtNDEwYS05MDU2LTZiOTUyNzkyNDM4MSIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5ldS1jZW50cmFsLTEuYW1hem9uYXdzLmNvbVwvZXUtY2VudHJhbC0xXzJ4ZWtITzhTOSIsImNvZ25pdG86dXNlcm5hbWUiOiJjaHJpcytmdW5rYWRtaW4xQGVtaWwuZGUiLCJjdXN0b206dGVuYW50X2lkIjoiNDAiLCJnaXZlbl9uYW1lIjoiRnVuayIsImN1c3RvbTpjb2RlIjoidXNyX3VGMnZvQlJWR2wwUFMwUjFzYlp2SCIsIm9yaWdpbl9qdGkiOiI2NTU5ZmNmMC05NDJlLTRkNWQtODNjZC1mMjJkMGI3ZTA5MzIiLCJhdWQiOiI2cmNvN2Y5dGtldXRxaDZvNjQ4cmZkdDVkbyIsImV2ZW50X2lkIjoiYjM4MTIzZDYtODRjYi00ODcyLWIzODgtZWQ0ZDdmZWE4YzY5IiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NTgyNjY3MzcsImV4cCI6MTc1ODI3MDMzNiwiY3VzdG9tOnJvbGUiOiJ1c2VyIiwiaWF0IjoxNzU4MjY2NzM3LCJmYW1pbHlfbmFtZSI6IkFkbWluIiwiY3VzdG9tOnRlbmFudF9oaWVyYXJjaHkiOiJmdW5rLXNhbmRib3gtcHJvZCIsImp0aSI6ImU5YWUxNGZiLTM1MmMtNDcwYi1iZGIwLTM5Y2Q1YjcwZWM4OCIsImVtYWlsIjoiY2hyaXMrZnVua2FkbWluMUBlbWlsLmRlIn0.cqj6Lui1UTbRuX9ROlhnRyBrsWrEKKjVFVD849IwzrIKCxm2AM-_Zv3BZSHdrP9ZU2dyOOuHMf-jnpz3mAD7TX10r4lExVPdJzHbNXvWln3bP-v3LwTc0Ol58tzG4WTfpK3bg9muI8_jcePWhcgE2O19Aqz8u3OXKm2goisODDdie52EvA0vg-x-6Bk9OBTB-3ofwQqg-gdCqQg6K7nx7qdqGukN2-fMO01hRDFxNan143FcL_97Dxuf-uErv6_vw26btr3uRyOssGgUgRYG-FiPM2akc1UCM3TO_Rv86kZ-Rg4u-92_9RXu3tb3SVv5GTq6-2hw-dLDCLumaV__qg"
}

response = requests.get(url, headers=headers, verify=False)

if not response.ok:
    print(f"Request fehlgeschlagen: {response.status_code}")
    print(response.text)
else:
    try:
        data = response.json()
    except ValueError:
        print("Antwort ist kein gültiges JSON")
    else:
        # Einzelnes Produkt-Objekt; API kann es in einem Wrapper liefern, z. B. {"product": {...}}
        product = data if isinstance(data, dict) else None
        if isinstance(data, dict) and not any(k in data for k in ("id", "code", "name")):
            product = (
                data.get("product")
                or data.get("data")
                or data.get("item")
            )

        if not isinstance(product, dict):
            print("Kein Produktobjekt gefunden")
        else:
            print("Produkt:")
            print(f"ID:        {product.get('id', '-')}")
            print(f"Name:      {product.get('name', '-')}")
            print(f"Code:      {product.get('code', '-')}")
            print(f"CreatedAt: {product.get('createdAt', '-')}")
            # Optional: weitere Felder sauber anzeigen
            details = product.get("details") or product.get("metadata")
            if isinstance(details, dict):
                print("Details:")
                for k, v in details.items():
                    print(f"  {k}: {v}")