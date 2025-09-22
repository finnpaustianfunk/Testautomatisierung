from ast import main
import time
import requests

def create_lead():

    url = "https://apiv2.emil.de/insuranceservice/v1/leads"

    payload = {
        "account": {
            #"customFields": { "newKey": "New Value" },
            "title": "",
            "firstName": "test",
            "lastName": "api",
            "email": "amil",
            "gender": "male",
            "street": "valentinskamp 18",
            "zipCode": "32656",
            "city": "Hamburg",
            "houseNumber": "13",
            "birthDate": "1999-01-01T00:00:00",
            "phone": "+4912345148458",
            "type": "person",
            "companyName": "moin",
            "accountNumber": "acc_bzljqrigFVoAT893qU0QO"
        },
        "policy": {
            "productVersionId": 1,
            "accountCode": "acc_bzljqrigFVoAT893qU0QO",
            #"holder": "holder",
            #"leadCode": "leadcode"
        },
        "code": "lea_0hdbUrAmCiMWp4IN1pr16",
        "productVersionId": 1,
        "accountCode": "acc_bzljqrigFVoAT893qU0QO",
        "bankAccount": {
            "accountCode": "acc_bzljqrigFVoAT893qU0QO",
            "iban": "DE02120300000000202051"
        },
        "status": "accept",
        "paymentMethod": { "type": "sepa" }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer eyJraWQiOiJTWG9PU3RWOEEzNlVKR2o3bGRsXC9ocGU2QUV6T2E1Nzc3YmM3dTVKeXEyMD0iLCJhbGciOiJSUzI1NiJ9.eyJjdXN0b206dGVuYW50X3NsdWciOiJmdW5rLXNhbmRib3gtcHJvZCIsInN1YiI6IjdkOWE0ZTBhLWNkNTgtNDEwYS05MDU2LTZiOTUyNzkyNDM4MSIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5ldS1jZW50cmFsLTEuYW1hem9uYXdzLmNvbVwvZXUtY2VudHJhbC0xXzJ4ZWtITzhTOSIsImNvZ25pdG86dXNlcm5hbWUiOiJjaHJpcytmdW5rYWRtaW4xQGVtaWwuZGUiLCJjdXN0b206dGVuYW50X2lkIjoiNDAiLCJnaXZlbl9uYW1lIjoiRnVuayIsImN1c3RvbTpjb2RlIjoidXNyX3VGMnZvQlJWR2wwUFMwUjFzYlp2SCIsIm9yaWdpbl9qdGkiOiI4ZGJhMDY5MC02ZmQ0LTQ1NmItYjZjMC02YTA3NmU4NDUwYmYiLCJhdWQiOiI2cmNvN2Y5dGtldXRxaDZvNjQ4cmZkdDVkbyIsImV2ZW50X2lkIjoiMDJkZTQ1OTYtOGViNC00NDViLWE4NDQtNmIxYjAyNTAxZmNiIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NTgxMDgzNjIsImV4cCI6MTc1ODExMTk2MiwiY3VzdG9tOnJvbGUiOiJ1c2VyIiwiaWF0IjoxNzU4MTA4MzYyLCJmYW1pbHlfbmFtZSI6IkFkbWluIiwiY3VzdG9tOnRlbmFudF9oaWVyYXJjaHkiOiJmdW5rLXNhbmRib3gtcHJvZCIsImp0aSI6IjIxMDQ1MWI0LWJlMzUtNDIyMS1hYzNjLWY5ZmI0NDU5ZjA3YSIsImVtYWlsIjoiY2hyaXMrZnVua2FkbWluMUBlbWlsLmRlIn0.d86kaaW0eGqb2B9Jhdvz2toNGbNW3nL3QY-E5x_x--s3fQAGpZQxjJZVS3rPcUTrqrB8AC83uiNNnOk59s5r89q5X7AOyB4rkepx1AYRreHkHZ7A1X2s8MYnVKuXs62xVTa6UIRL-7r3qkekENB6lgldbL77rs3eBSroXFKYvpJ07rdGwfxPtnhPyewMgvSCw6BOoqBrlr64we2yvznh18fEZK-YzRBhDi7cUoAgbtsCZPyiTOMvH3IPveb7m5HzJ-n8E9tBhX4a0U_GxYXRZxU16GusHquzkDm8RkhxGCJYbQfqoM0hBfVnqhUSvk6X6APj8HnHDQuCJU12Mlb-IA"
    }

    response = requests.post(url, json=payload, headers=headers, verify=False)
    print(response.text)


if __name__ == "__main__":
    while True:
        create_lead()
        time.sleep(3600)