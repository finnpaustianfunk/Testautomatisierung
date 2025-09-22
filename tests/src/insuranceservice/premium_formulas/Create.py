import requests

url = "https://apiv2.emil.de/insuranceservice/v1/premium-formulas"

exhibition_payload = {
    "type": "time",
    "unit": "oneTimePayment",
    "productVersionId": 6741,
    "group": "Ausstellungs-Versicherung",
    "name": "Ausstellungsvers.",
    "expression": "exhibition.add > 0 ? exhibition.add * 1.19 : 0",
    "itemType": "other",
    "order": 1
}

# Haftpflicht-Versicherung (Basis)
liability_payload = {
        "type": "time",
        "unit": "oneTimePayment",
        "productVersionId": 6741,
        "group": "Haftpflicht-Versicherung",
        "name": "Haftpflichtvers.",
        "expression": "liability.add > 0 ? liability.add * 1.19 : 0",
        "itemType": "other",
        "order": 2
}

# Unfall-Versicherung (Basis)
accident_payload = {
    "type": "time",
    "unit": "oneTimePayment",
    "productVersionId": 6741,
    "group": "Unfall-Versicherung",
    "name": "Unfallvers.",
    "expression": "accident.add > 0 ? accident.add * 1.19 : 0",
    "itemType": "other",
    "order": 3
}

# Ausstellung Kommission
exhibition_commission_payload = {
    "type": "time",
    "unit": "oneTimePayment",
    "productVersionId": 6741,
    "group": "Ausstellungs-Versicherung",
    "name": "Ausstellungsvers. Kommission",
    "expression": "exhibition.add > 0 ? exhibition.add * exhibition.commission : 0",
    "itemType": "other",
    "order": 4
}

# Haftpflicht Kommission – wie von dir vorgegeben mit exhibition.commission
liability_commission_payload = {
    "type": "time",
    "unit": "oneTimePayment",
    "productVersionId": 6741,
    "group": "Haftpflicht-Versicherung",
    "name": "Haftpflichtvers. Kommission",
    "expression": "liability.add > 0 ? liability.add * exhibition.commission : 0",
    "itemType": "other",
    "order": 5
}

# Unfall Kommission – analog, mit exhibition.commission
accident_commission_payload = {
    "type": "time",
    "unit": "oneTimePayment",
    "productVersionId": 6741,
    "group": "Unfall-Versicherung",
    "name": "Unfallvers. Kommission",
    "expression": "accident.add > 0 ? accident.add * exhibition.commission : 0",
    "itemType": "other",
    "order": 6
}


headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer eyJraWQiOiJTWG9PU3RWOEEzNlVKR2o3bGRsXC9ocGU2QUV6T2E1Nzc3YmM3dTVKeXEyMD0iLCJhbGciOiJSUzI1NiJ9.eyJjdXN0b206dGVuYW50X3NsdWciOiJmdW5rLXNhbmRib3gtcHJvZCIsInN1YiI6IjdkOWE0ZTBhLWNkNTgtNDEwYS05MDU2LTZiOTUyNzkyNDM4MSIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5ldS1jZW50cmFsLTEuYW1hem9uYXdzLmNvbVwvZXUtY2VudHJhbC0xXzJ4ZWtITzhTOSIsImNvZ25pdG86dXNlcm5hbWUiOiJjaHJpcytmdW5rYWRtaW4xQGVtaWwuZGUiLCJjdXN0b206dGVuYW50X2lkIjoiNDAiLCJnaXZlbl9uYW1lIjoiRnVuayIsImN1c3RvbTpjb2RlIjoidXNyX3VGMnZvQlJWR2wwUFMwUjFzYlp2SCIsIm9yaWdpbl9qdGkiOiJkNTAyMzlhYS1kYjQxLTQ5ZmItOWJhMi1mNGRkOTEzZTg5YmQiLCJhdWQiOiI2cmNvN2Y5dGtldXRxaDZvNjQ4cmZkdDVkbyIsImV2ZW50X2lkIjoiZTc3NGZmYzgtNTIxNS00ODhjLTlkMjQtN2JjNWE0NDM3YWNmIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NTgyNzE2NjIsImV4cCI6MTc1ODI3NTI2MiwiY3VzdG9tOnJvbGUiOiJ1c2VyIiwiaWF0IjoxNzU4MjcxNjYyLCJmYW1pbHlfbmFtZSI6IkFkbWluIiwiY3VzdG9tOnRlbmFudF9oaWVyYXJjaHkiOiJmdW5rLXNhbmRib3gtcHJvZCIsImp0aSI6IjIwZTgzOTcwLWVlZmEtNDlmNC1iNDczLTZjNDA5MjA3MGUzMiIsImVtYWlsIjoiY2hyaXMrZnVua2FkbWluMUBlbWlsLmRlIn0.XTC7-Pag5oWbJMR1jQlv1V243qkgKH9w6vg18kqmxQCtsAzlvLgYuJWEhKeMjGZY8gRm94DThA3niE-7cTd5o7Jjihq885ypSnW6ENnTkAJgSdsFpSjahewgvTU-cJwJt5zniSDGb4Dt16X0I35RCnhoRdow9mvGLrMPnv0xPDnaS0Iz_OThWfuHtQaf6trzkrDlIOOBp7FstB1_BnZQHMiR85lIRbY5SrMEUE1__9bpyCm5Ben2QpcugucXWlOoZ4uUncbJZHGPhTjmXnqUposj0Pg3AN5-Jv3b5Yjx0UPiq3_ejUro4acZhmuyf9ZHjgstgGOC3OTBe96TPSBSqw",
}

responses = []
for payload in (exhibition_payload, liability_payload, accident_payload, exhibition_commission_payload, liability_commission_payload, accident_commission_payload):
    response = requests.post(url, json=payload, headers=headers, verify=False)
    responses.append(response.text)


for r in responses:
    #print(responses)
    print(r)