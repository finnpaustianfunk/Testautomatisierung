import requests

url = "https://apiv2.emil.de/insuranceservice/v1/leads/lea_2nrCPzWsWvA_9Ls1rHOcL"

headers = {
    "accept": "application/json",
    "authorization": "Bearer eyJraWQiOiJTWG9PU3RWOEEzNlVKR2o3bGRsXC9ocGU2QUV6T2E1Nzc3YmM3dTVKeXEyMD0iLCJhbGciOiJSUzI1NiJ9.eyJjdXN0b206dGVuYW50X3NsdWciOiJmdW5rLXNhbmRib3gtcHJvZCIsInN1YiI6IjdkOWE0ZTBhLWNkNTgtNDEwYS05MDU2LTZiOTUyNzkyNDM4MSIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5ldS1jZW50cmFsLTEuYW1hem9uYXdzLmNvbVwvZXUtY2VudHJhbC0xXzJ4ZWtITzhTOSIsImNvZ25pdG86dXNlcm5hbWUiOiJjaHJpcytmdW5rYWRtaW4xQGVtaWwuZGUiLCJjdXN0b206dGVuYW50X2lkIjoiNDAiLCJnaXZlbl9uYW1lIjoiRnVuayIsImN1c3RvbTpjb2RlIjoidXNyX3VGMnZvQlJWR2wwUFMwUjFzYlp2SCIsIm9yaWdpbl9qdGkiOiI0N2I5NDllMi1mZmRhLTQzYTEtOGY2MS0wMTU3ODU2MzRmMjYiLCJhdWQiOiI2cmNvN2Y5dGtldXRxaDZvNjQ4cmZkdDVkbyIsImV2ZW50X2lkIjoiYWEyNjc2NjQtMmJmNC00MjA4LTlmN2UtZTE0OTM3ODViMjc2IiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NTgyODY3NTYsImV4cCI6MTc1ODI5MDM1NiwiY3VzdG9tOnJvbGUiOiJ1c2VyIiwiaWF0IjoxNzU4Mjg2NzU2LCJmYW1pbHlfbmFtZSI6IkFkbWluIiwiY3VzdG9tOnRlbmFudF9oaWVyYXJjaHkiOiJmdW5rLXNhbmRib3gtcHJvZCIsImp0aSI6IjU4YmY3YWE0LThhYWMtNDNmMi1iMWRjLWQ0ZWQ5OGU0NTFhYSIsImVtYWlsIjoiY2hyaXMrZnVua2FkbWluMUBlbWlsLmRlIn0.XNG41T78xmlGUfkKkHEkvuB5QHqNWZ08mWbXC_h1ARLHv1upwxgrlTiiuD0LRdwUraRb5NNqHVlz9QSdfkQCZaucD50x5ZeWszLUFvgoORgNUJ_PUnn4XKZiemlEZWJBrIbmQiBqMQPZKWv1NnhBvrohWeHbMenh5oUwrzxRh9dzDRJCPljNpFc2yJT5RtPf-y1ZITA8G23yonxKgoZjGWsfAEi8WQBWGL-80ZlU75MzjNWHarqwMy2ePO2jH6_43OGqPgsDfcv_NMuCU0tIsGfBbMhkRjRs8wA7zz12DHMJbXMi12a2BN1VDxRPbIko-2Sb1oXVkU5J00PlveK1_g",
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
        # Lead-Objekt ggf. aus Wrapper extrahieren
        lead = data if isinstance(data, dict) else None
        if isinstance(data, dict) and not any(k in data for k in ("id", "code", "name")):
            lead = data.get("lead") or data.get("data") or data.get("item")

        if not isinstance(lead, dict):
            print("Kein Lead-Objekt gefunden")
        else:
            print("Lead:")
            print(f"ID:     {lead.get('id', '-')}")
            print(f"Name:   {lead.get('name', '-')}")
            print(f"Code:   {lead.get('code', '-')}")
            print(f"CreatedAt: {lead.get('createdAt', '-')}")
            details = lead.get("details") or lead.get("metadata")
            if isinstance(details, dict):
                print("Details:")
                for k, v in details.items():
                    print(f"  {k}: {v}")