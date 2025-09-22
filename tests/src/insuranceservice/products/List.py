import requests

url = "https://apiv2.emil.de/insuranceservice/v1/products?pageToken=2&order=createdAt"

headers = {
    "accept": "application/json",
    "authorization": "Bearer eyJraWQiOiJTWG9PU3RWOEEzNlVKR2o3bGRsXC9ocGU2QUV6T2E1Nzc3YmM3dTVKeXEyMD0iLCJhbGciOiJSUzI1NiJ9.eyJjdXN0b206dGVuYW50X3NsdWciOiJmdW5rLXNhbmRib3gtcHJvZCIsInN1YiI6IjdkOWE0ZTBhLWNkNTgtNDEwYS05MDU2LTZiOTUyNzkyNDM4MSIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5ldS1jZW50cmFsLTEuYW1hem9uYXdzLmNvbVwvZXUtY2VudHJhbC0xXzJ4ZWtITzhTOSIsImNvZ25pdG86dXNlcm5hbWUiOiJjaHJpcytmdW5rYWRtaW4xQGVtaWwuZGUiLCJjdXN0b206dGVuYW50X2lkIjoiNDAiLCJnaXZlbl9uYW1lIjoiRnVuayIsImN1c3RvbTpjb2RlIjoidXNyX3VGMnZvQlJWR2wwUFMwUjFzYlp2SCIsIm9yaWdpbl9qdGkiOiI2NTU5ZmNmMC05NDJlLTRkNWQtODNjZC1mMjJkMGI3ZTA5MzIiLCJhdWQiOiI2cmNvN2Y5dGtldXRxaDZvNjQ4cmZkdDVkbyIsImV2ZW50X2lkIjoiYjM4MTIzZDYtODRjYi00ODcyLWIzODgtZWQ0ZDdmZWE4YzY5IiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NTgyNjY3MzcsImV4cCI6MTc1ODI3MDMzNiwiY3VzdG9tOnJvbGUiOiJ1c2VyIiwiaWF0IjoxNzU4MjY2NzM3LCJmYW1pbHlfbmFtZSI6IkFkbWluIiwiY3VzdG9tOnRlbmFudF9oaWVyYXJjaHkiOiJmdW5rLXNhbmRib3gtcHJvZCIsImp0aSI6ImU5YWUxNGZiLTM1MmMtNDcwYi1iZGIwLTM5Y2Q1YjcwZWM4OCIsImVtYWlsIjoiY2hyaXMrZnVua2FkbWluMUBlbWlsLmRlIn0.cqj6Lui1UTbRuX9ROlhnRyBrsWrEKKjVFVD849IwzrIKCxm2AM-_Zv3BZSHdrP9ZU2dyOOuHMf-jnpz3mAD7TX10r4lExVPdJzHbNXvWln3bP-v3LwTc0Ol58tzG4WTfpK3bg9muI8_jcePWhcgE2O19Aqz8u3OXKm2goisODDdie52EvA0vg-x-6Bk9OBTB-3ofwQqg-gdCqQg6K7nx7qdqGukN2-fMO01hRDFxNan143FcL_97Dxuf-uErv6_vw26btr3uRyOssGgUgRYG-FiPM2akc1UCM3TO_Rv86kZ-Rg4u-92_9RXu3tb3SVv5GTq6-2hw-dLDCLumaV__qg"
}

response = requests.get(url, headers=headers, verify=False)


if not response.ok:
    print("request fehlgeschlagen")
else:
    try:
        data = response.json()
    except ValueError:
        print("not json format")
    else:
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            items = data.get("items") or data.get("data") or []
        else:
            items = []
        if not items:
            print("Keine Produkte gefunden")
        else:
            print(f"Folgende Produkte haben wir: {len(items)}")
            for index, product in enumerate(items, start=1):
                if isinstance(product, dict):
                    product_id = product.get("id")
                    product_name = product.get("name") 
                    product_code = product.get("code")
                    product_created = product.get("createdAt")

                    print(f"\n[{index}]")
                    print(f"ID: {product_id}")
                    print(f"Name: {product_name}")
                    print(f"Code: {product_code}")
                    print(f"CreatedAt: {product_created}")
                else:
                    print(f"[{index}] {product}")