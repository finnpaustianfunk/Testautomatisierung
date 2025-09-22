from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import tempfile
import os
import base64
from pathlib import Path

import requests
from msal import ConfidentialClientApplication
from msgraph import GraphServiceClient
from msgraph.generated.models.message import Message
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.recipient import Recipient
from msgraph.generated.models.email_address import EmailAddress
from msgraph.generated.models.attachment_item import AttachmentItem
from msgraph.generated.models.file_attachment import FileAttachment

# =====================
# Konfiguration (ohne .env)
# =====================

# API
CONTRACTS_ENDPOINT = "https://app.emil.de/u/0/policies#policy-grid={%22query%22:%22%22,%22orderBy%22:{%22id%22:%22createdAt%22,%22desc%22:true}}"  # z. B. https://apiv2.emil.de/contractservice/v1/contracts
API_TOKEN = "eyJraWQiOiJTWG9PU3RWOEEzNlVKR2o3bGRsXC9ocGU2QUV6T2E1Nzc3YmM3dTVKeXEyMD0iLCJhbGciOiJSUzI1NiJ9.eyJjdXN0b206dGVuYW50X3NsdWciOiJmdW5rLXNhbmRib3gtcHJvZCIsInN1YiI6IjdkOWE0ZTBhLWNkNTgtNDEwYS05MDU2LTZiOTUyNzkyNDM4MSIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5ldS1jZW50cmFsLTEuYW1hem9uYXdzLmNvbVwvZXUtY2VudHJhbC0xXzJ4ZWtITzhTOSIsImNvZ25pdG86dXNlcm5hbWUiOiJjaHJpcytmdW5rYWRtaW4xQGVtaWwuZGUiLCJjdXN0b206dGVuYW50X2lkIjoiNDAiLCJnaXZlbl9uYW1lIjoiRnVuayIsImN1c3RvbTpjb2RlIjoidXNyX3VGMnZvQlJWR2wwUFMwUjFzYlp2SCIsIm9yaWdpbl9qdGkiOiI0N2I5NDllMi1mZmRhLTQzYTEtOGY2MS0wMTU3ODU2MzRmMjYiLCJhdWQiOiI2cmNvN2Y5dGtldXRxaDZvNjQ4cmZkdDVkbyIsImV2ZW50X2lkIjoiYWEyNjc2NjQtMmJmNC00MjA4LTlmN2UtZTE0OTM3ODViMjc2IiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NTgyODY3NTYsImV4cCI6MTc1ODI5MDM1NiwiY3VzdG9tOnJvbGUiOiJ1c2VyIiwiaWF0IjoxNzU4Mjg2NzU2LCJmYW1pbHlfbmFtZSI6IkFkbWluIiwiY3VzdG9tOnRlbmFudF9oaWVyYXJjaHkiOiJmdW5rLXNhbmRib3gtcHJvZCIsImp0aSI6IjU4YmY3YWE0LThhYWMtNDNmMi1iMWRjLWQ0ZWQ5OGU0NTFhYSIsImVtYWlsIjoiY2hyaXMrZnVua2FkbWluMUBlbWlsLmRlIn0.XNG41T78xmlGUfkKkHEkvuB5QHqNWZ08mWbXC_h1ARLHv1upwxgrlTiiuD0LRdwUraRb5NNqHVlz9QSdfkQCZaucD50x5ZeWszLUFvgoORgNUJ_PUnn4XKZiemlEZWJBrIbmQiBqMQPZKWv1NnhBvrohWeHbMenh5oUwrzxRh9dzDRJCPljNpFc2yJT5RtPf-y1ZITA8G23yonxKgoZjGWsfAEi8WQBWGL-80ZlU75MzjNWHarqwMy2ePO2jH6_43OGqPgsDfcv_NMuCU0tIsGfBbMhkRjRs8wA7zz12DHMJbXMi12a2BN1VDxRPbIko-2Sb1oXVkU5J00PlveK1_g"

# Microsoft Graph Konfiguration
TENANT_ID = "YOUR_TENANT_ID"  # Azure AD Tenant ID
CLIENT_ID = "YOUR_CLIENT_ID"  # Azure AD App Registration Client ID
CLIENT_SECRET = "YOUR_CLIENT_SECRET"  # Azure AD App Registration Client Secret
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

# E-Mail Konfiguration
EMAIL_FROM = "f.paustian@funk-gruppe.de"
EMAIL_TO = ["f.paustian@funk-gruppe.de"]  # Liste für mehrere Empfänger


def iso_utc(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def get_graph_client() -> GraphServiceClient:
    """
    Erstellt einen authentifizierten Microsoft Graph Client
    """
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY
    )
    
    # Token für Client Credentials Flow abrufen
    result = app.acquire_token_silent(SCOPES, account=None)
    if not result:
        result = app.acquire_token_for_client(scopes=SCOPES)
    
    if "access_token" in result:
        # GraphServiceClient mit dem Access Token erstellen
        from msgraph.generated.models.o_data_errors.o_data_error import ODataError
        from msgraph.core import GraphClientFactory
        
        def auth_provider(request):
            request.headers['Authorization'] = f'Bearer {result["access_token"]}'
            return request
        
        return GraphServiceClient(credentials=auth_provider)
    else:
        raise Exception(f"Fehler bei der Authentifizierung: {result.get('error_description', 'Unbekannter Fehler')}")


def fetch_todays_contracts(
    base_endpoint: str,
    bearer_token: str,
    max_pages: int = 50,
) -> List[Dict[str, Any]]:
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {bearer_token}",
    }

    now = datetime.now(timezone.utc)
    start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
    start_iso = iso_utc(start)
    end_iso = iso_utc(now)

    items: List[Dict[str, Any]] = []
    page_token: Optional[str] = None

    for _ in range(max_pages):
        params: Dict[str, Any] = {
            "order": "createdAt",
            "from": start_iso,
            "to": end_iso,
        }
        if page_token:
            params["pageToken"] = page_token

        resp = requests.get(base_endpoint, headers=headers, params=params, timeout=30)
        if not resp.ok:
            raise RuntimeError(f"Request failed: {resp.status_code} {resp.text}")

        data = resp.json()
        page_items: List[Dict[str, Any]] = []

        if isinstance(data, dict):
            page_items = (
                data.get("items")
                or data.get("data")
                or data.get("contracts")
                or []
            )
            page_token = data.get("nextPageToken") or data.get("next_token")
        elif isinstance(data, list):
            page_items = data
            page_token = None
        else:
            page_items = []
            page_token = None

        if not isinstance(page_items, list):
            page_items = []

        items.extend([i for i in page_items if isinstance(i, dict)])

        if not page_token:
            break

    return items


def build_pdf_dashboard(contracts: List[Dict[str, Any]], report_title: str) -> str:
    # Erfordert reportlab: pip install reportlab
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    except Exception as e:
        raise RuntimeError("reportlab ist erforderlich: pip install reportlab") from e

    tmp_pdf = tempfile.NamedTemporaryFile(prefix="contracts_report_", suffix=".pdf", delete=False)
    filename = tmp_pdf.name
    tmp_pdf.close()

    doc = SimpleDocTemplate(filename, pagesize=A4, title=report_title)
    styles = getSampleStyleSheet()
    story: List[Any] = []

    story.append(Paragraph(report_title, styles["Title"]))
    story.append(Spacer(1, 12))

    total = len(contracts)
    story.append(Paragraph(f"Anzahl neuer Verträge: <b>{total}</b>", styles["Normal"]))
    story.append(Spacer(1, 12))

    if contracts:
        table_data: List[List[str]] = [["#", "ID", "Number", "ProductCode", "Status", "CreatedAt", "Customer"]]

        for idx, c in enumerate(contracts, start=1):
            contract_id = str(c.get("id") or c.get("contractId") or "-")
            number = str(c.get("number") or c.get("contractNumber") or "-")
            product_code = str(c.get("productCode") or (c.get("product") or {}).get("code") or "-")
            status = str(c.get("status") or "-")
            created_at = str(c.get("createdAt") or c.get("created") or "-")
            customer = c.get("customer") or c.get("policyHolder") or {}
            customer_name = str((customer.get("name") if isinstance(customer, dict) else None) or "-")

            table_data.append([str(idx), contract_id, number, product_code, status, created_at, customer_name])

        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#ECF0F1")),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.gray),
        ]))

        story.append(table)

    doc.build(story)
    return filename


def send_email_with_attachment(subject: str, body: str, attachment_path: str) -> None:
    """
    Sendet eine E-Mail mit Anhang über Microsoft Graph
    """
    try:
        # Graph Client erstellen
        graph_client = get_graph_client()
        
        # Anhang vorbereiten
        attachment_name = Path(attachment_path).name
        with open(attachment_path, "rb") as f:
            attachment_content = base64.b64encode(f.read()).decode('utf-8')
        
        # File Attachment erstellen
        file_attachment = FileAttachment()
        file_attachment.name = attachment_name
        file_attachment.content_bytes = attachment_content
        file_attachment.content_type = "application/pdf"
        
        # Empfänger erstellen
        recipients = []
        for email in EMAIL_TO:
            recipient = Recipient()
            email_address = EmailAddress()
            email_address.address = email
            recipient.email_address = email_address
            recipients.append(recipient)
        
        # E-Mail Body erstellen
        email_body = ItemBody()
        email_body.content_type = BodyType.Text
        email_body.content = body
        
        # Message erstellen
        message = Message()
        message.subject = subject
        message.body = email_body
        message.to_recipients = recipients
        message.attachments = [file_attachment]
        
        # E-Mail senden
        graph_client.me.send_mail.post(body=message)
        print(f"E-Mail erfolgreich gesendet an: {', '.join(EMAIL_TO)}")
        
    except Exception as e:
        print(f"Fehler beim Senden der E-Mail: {str(e)}")
        raise


if __name__ == "__main__":
    contracts = fetch_todays_contracts(CONTRACTS_ENDPOINT, API_TOKEN)

    now = datetime.now(timezone.utc)
    title = f"Daily Contracts Report – {now.strftime('%Y-%m-%d')}"
    pdf_path = build_pdf_dashboard(contracts, title)

    email_body = (
        "Täglicher Vertrags-Report.\n"
        f"Anzahl neuer Verträge heute: {len(contracts)}\n"
        "Im Anhang findest du die Detailübersicht als PDF."
    )

    send_email_with_attachment(title, email_body, pdf_path)
    print(f"Report erstellt und versendet: {pdf_path}")



