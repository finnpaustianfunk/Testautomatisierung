from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import tempfile
import os
from pathlib import Path
import shutil

import requests

# TODO: WORKFLOWS einbauen

CONTRACTS_ENDPOINT = "https://apiv2.emil.de/insuranceservice/v1/policies"
API_TOKEN = "eyJraWQiOiJTWG9PU3RWOEEzNlVKR2o3bGRsXC9ocGU2QUV6T2E1Nzc3YmM3dTVKeXEyMD0iLCJhbGciOiJSUzI1NiJ9.eyJjdXN0b206dGVuYW50X3NsdWciOiJmdW5rLXNhbmRib3gtcHJvZCIsInN1YiI6IjdkOWE0ZTBhLWNkNTgtNDEwYS05MDU2LTZiOTUyNzkyNDM4MSIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5ldS1jZW50cmFsLTEuYW1hem9uYXdzLmNvbVwvZXUtY2VudHJhbC0xXzJ4ZWtITzhTOSIsImNvZ25pdG86dXNlcm5hbWUiOiJjaHJpcytmdW5rYWRtaW4xQGVtaWwuZGUiLCJjdXN0b206dGVuYW50X2lkIjoiNDAiLCJnaXZlbl9uYW1lIjoiRnVuayIsImN1c3RvbTpjb2RlIjoidXNyX3VGMnZvQlJWR2wwUFMwUjFzYlp2SCIsIm9yaWdpbl9qdGkiOiIwZjc4NWJjNC00M2Q2LTRhY2MtOTZiMC0yMjA5N2E4NzIwNzYiLCJhdWQiOiI2cmNvN2Y5dGtldXRxaDZvNjQ4cmZkdDVkbyIsImV2ZW50X2lkIjoiYjY3MTE2ZWUtZjFhNS00YzgwLTk1NzYtNGYzZmMzOWM4MjhhIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE3NTg1NTAxNjMsImV4cCI6MTc1ODU1Mzc2MywiY3VzdG9tOnJvbGUiOiJ1c2VyIiwiaWF0IjoxNzU4NTUwMTYzLCJmYW1pbHlfbmFtZSI6IkFkbWluIiwiY3VzdG9tOnRlbmFudF9oaWVyYXJjaHkiOiJmdW5rLXNhbmRib3gtcHJvZCIsImp0aSI6ImJlOGY3NDgxLWExZWEtNDNmOC1hYzFkLTIyOTViMTdjMWIzMyIsImVtYWlsIjoiY2hyaXMrZnVua2FkbWluMUBlbWlsLmRlIn0.juC90J0LxPtQDgJj4bmB3QJC_bQlT1c66_DmpCo0veOk1mYzuvjIvNQ4PXfbNgH_-9mGXgAxW7gTK2gehthkWcAzPStGWacMxnUH0xYnKkb_vcmlaCpo4MvXgKBFFiYdy8o_6GZX8VZw3QsdrxQ11f1lAdUsaJ7_BpNpgvjk49S0lSoRwk038U3B-an_owwghcfpgTfIITxSqBBQGaot5kHPhUPlNzCMYl_xQj2Gfa61yHk_IbE8zu48nysyJ0NuVMwwqj1z-McYkqiQbGr3_MGdOw38gynEhEtBkUXiuJb_T26SwzS0qmrgSQtszI11wjzmCq9gEpNIY7ecj0-GHA"


VERIFY_SSL = False


def iso_utc(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def fetch_todays_contracts(
    base_endpoint: str,
    bearer_token: str,
    max_pages: int = 50,
) -> List[Dict[str, Any]]:
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {bearer_token}",
    }

    items: List[Dict[str, Any]] = []
    page_token: Optional[str] = None

    for _ in range(max_pages):
        # Nur sortieren; Datum filtern wir clientseitig robust auf "heute"
        params: Dict[str, Any] = {"order": "createdAt"}
        if page_token:
            params["pageToken"] = page_token

        resp = requests.get(
            base_endpoint,
            headers=headers,
            params=params,
            timeout=30,
            verify=VERIFY_SSL,
        )
        if not resp.ok:
            raise RuntimeError(f"Request failed: {resp.status_code} {resp.text}")

        try:
            data = resp.json()
        except Exception:
            data = []
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


def get_created_at(contract: Dict[str, Any]) -> str:
    return (
        contract.get("createdAt")
        or contract.get("created")
        or (contract.get("audit") or {}).get("createdAt")
        or ""
    )


def is_today_utc(iso_str: str) -> bool:
    try:
        if not iso_str:
            return False
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc).date() == datetime.now(timezone.utc).date()
    except Exception:
        return False


def format_date_only(value: Any) -> str:
    try:
        s = str(value)
        if not s or s == "-":
            return "-"
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y")
    except Exception:
        return str(value) if value else "-"


def build_pdf_dashboard(contracts: List[Dict[str, Any]], report_title: str) -> str:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    except Exception as e:
        raise e

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
        table_data: List[List[str]] = [["#", "ID", "policyNumber", "Produkt", "Status", "Abgeschlossen am", "Startdatum"]]

        for idx, c in enumerate(contracts, start=1):
            contract_id = str(c.get("id") or c.get("contractId") or "-")
            p_number = str(c.get("policyNumber") or c.get("policyNumber") or "-")
            product_code = str(c.get("productName") or (c.get("productName") or {}).get("code") or "-")
            status = str(c.get("status") or "-")
            created_at = format_date_only(c.get("createdAt") or c.get("created") or "-")
            start_date = format_date_only(c.get("policyStartDate") or "-")
            #customer_name = str((customer.get("name") if isinstance(customer, dict) else None) or "-")

            table_data.append([str(idx), contract_id, p_number, product_code, status, created_at, start_date])

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


if __name__ == "__main__":
    all_contracts = fetch_todays_contracts(CONTRACTS_ENDPOINT, API_TOKEN)
    contracts = [c for c in all_contracts if is_today_utc(get_created_at(c))]

    now = datetime.now(timezone.utc)
    title = f"Daily Contracts Report – {now.strftime('%Y-%m-%d')}"
    tmp_pdf_path = build_pdf_dashboard(contracts, title)

    # In tests/reports/dashboard.pdf speichern
    out_dir = Path("tests/reports")
    out_dir.mkdir(parents=True, exist_ok=True)
    dest_path = out_dir / "dashboard.pdf"
    shutil.copy(tmp_pdf_path, dest_path)
    print(f"PDF gespeichert: {dest_path}")