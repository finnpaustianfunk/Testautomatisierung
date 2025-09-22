import requests

url = "https://apiv2.emil.de/billingservice/v1/invoices"

# change payload if needed, you can change the type to different invoice options
payload = {
    "type": "initial",
    "metadata": { "a": "1" },
    "policyCode": "pol_T7_ROsfwov_Xsk",
    "billingIntervalFrom": "2025-09-16T00:00:00",
    "billingIntervalTo": "2028-09-16T00:00:00",
    "dueDate": "2025-09-16T14:53:00",
    "items": [
        {
            "name": "Gesamtprämie inkl. Rabatte und Zuschläge",
            "quantity": 1,
            "pricePerUnit": 100
        }
    ]
}
headers = {
    "accept": "application/json",
    "Idempotency-Key": "UUID001",
    "content-type": "application/json",
    "authorization": "Bearer eyJraWQiOiJTWG9PU3RWOEEzNlVKR2o3bGRsXC9ocGU2QUV6T2E1Nzc3YmM3dTVKeXEyMD0iLCJhbGciOiJSUzI1NiJ9.eyJjdXN0b206dGVuYW50X3NsdWciOiJmdW5rLXNhbmRib3gtcHJvZCIsInN1YiI6IjdkOWE0ZTBhLWNkNTgtNDEwYS05MDU2LTZiOTUyNzkyNDM4MSIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5ldS1jZW50cmFsLTEuYW1hem9uYXdzLmNvbVwvZXUtY2VudHJhbC0xXzJ4ZWtITzhTOSIsImNvZ25pdG86dXNlcm5hbWUiOiJjaHJpcytmdW5rYWRtaW4xQGVtaWwuZGUiLCJjdXN0b206dGVuYW50X2lkIjoiNDAiLCJnaXZlbl9uYW1lIjoiRnVuayIsImN1c3RvbTpjb2RlIjoidXNyX3VGMnZvQlJWR2wwUFMwUjFzYlp2SCIsIm9yaWdpbl9qdGkiOiJjMDcxYjNlMC0yMTdkLTQ4MzctODEyNC00YThkMzIxOGFjMDYiLCJhdWQiOiI2cmNvN2Y5dGtldXRxaDZvNjQ4cmZkdDVkbyIsImV2ZW50X2lkIjoiZTIyNjhiNjYtZTIyMS00MWEzLWE4ZTEtZmQ1M2Q0Zjc1MjBjIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NTgwMjY5MjAsImV4cCI6MTc1ODAzMDUyMCwiY3VzdG9tOnJvbGUiOiJ1c2VyIiwiaWF0IjoxNzU4MDI2OTIwLCJmYW1pbHlfbmFtZSI6IkFkbWluIiwiY3VzdG9tOnRlbmFudF9oaWVyYXJjaHkiOiJmdW5rLXNhbmRib3gtcHJvZCIsImp0aSI6IjEwYTNjNGI3LTA1N2ItNDFiMi1iZTMyLWUxNTUzNWE4NTI2ZSIsImVtYWlsIjoiY2hyaXMrZnVua2FkbWluMUBlbWlsLmRlIn0.hxu890rg1T9ODrAlcC_qNVFGOGi0rrCROSlfdgCkSPZRF-KnsifBVkNRh6vBTS6H26RYSfqMVLEtDStWWB7WcncwJnMA0OouAATH7s_VCXWlUGwJXMAlXoQogr2w8xGChKpX0W0BeuSZcvhts_7misDVO800VbchDQ-_rRJlAufXdG30-vJbMSL3gPYTn4UURUDDbMEKHEKUWy4TvWkU1nkl_yglBHEXjwXPVRezeeYF9CzNK2wArHIWdrbWijaV6NHgUyMR6XXHXcIlTWevFcQ_oXGAbKvTEIkpkK-ZOGscP6HfEaIGekJ_qr4NaWQiBCQSUujbgfLS33YixaeN2g"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)