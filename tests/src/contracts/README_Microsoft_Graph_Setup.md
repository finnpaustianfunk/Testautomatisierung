# Microsoft Graph Integration für Newcontracts.py

## Übersicht
Die `Newcontracts.py` wurde erfolgreich von SMTP auf Microsoft Graph umgestellt. Diese Anleitung erklärt, wie Sie die Microsoft Graph Integration einrichten.

## Voraussetzungen

### 1. Azure AD App Registration erstellen

1. Gehen Sie zum [Azure Portal](https://portal.azure.com)
2. Navigieren Sie zu "Azure Active Directory" > "App registrations"
3. Klicken Sie auf "New registration"
4. Geben Sie einen Namen ein (z.B. "Contract Report Service")
5. Wählen Sie "Accounts in this organizational directory only"
6. Klicken Sie auf "Register"

### 2. Client Secret erstellen

1. In Ihrer App Registration, gehen Sie zu "Certificates & secrets"
2. Klicken Sie auf "New client secret"
3. Geben Sie eine Beschreibung ein und wählen Sie ein Ablaufdatum
4. Klicken Sie auf "Add"
5. **WICHTIG**: Kopieren Sie den Secret Value sofort - er wird nur einmal angezeigt!

### 3. API Permissions konfigurieren

1. In Ihrer App Registration, gehen Sie zu "API permissions"
2. Klicken Sie auf "Add a permission"
3. Wählen Sie "Microsoft Graph"
4. Wählen Sie "Application permissions"
5. Fügen Sie folgende Permissions hinzu:
   - `Mail.Send` - E-Mails senden
   - `User.Read.All` - Benutzerinformationen lesen (optional)
6. Klicken Sie auf "Grant admin consent"

## Konfiguration

### 1. Konfigurationswerte aktualisieren

Öffnen Sie `Newcontracts.py` und aktualisieren Sie folgende Werte:

```python
# Microsoft Graph Konfiguration
TENANT_ID = "Ihre-Tenant-ID"  # Azure AD Tenant ID
CLIENT_ID = "Ihre-Client-ID"  # Azure AD App Registration Client ID
CLIENT_SECRET = "Ihr-Client-Secret"  # Azure AD App Registration Client Secret
```

### 2. Tenant ID finden

1. Im Azure Portal, gehen Sie zu "Azure Active Directory" > "Overview"
2. Kopieren Sie die "Tenant ID"

### 3. Client ID finden

1. In Ihrer App Registration, gehen Sie zu "Overview"
2. Kopieren Sie die "Application (client) ID"

## Installation der Abhängigkeiten

```bash
pip install -r requirements.txt
```

Die folgenden neuen Pakete wurden hinzugefügt:
- `msal==1.25.0` - Microsoft Authentication Library
- `msgraph-core==0.2.2` - Microsoft Graph Core
- `msgraph-sdk==1.0.0` - Microsoft Graph SDK
- `reportlab==4.0.7` - PDF Generation

## Verwendung

Die Verwendung bleibt gleich wie vorher:

```python
python Newcontracts.py
```

Das Skript wird:
1. Heutige Verträge von der API abrufen
2. Ein PDF-Report erstellen
3. Den Report per E-Mail über Microsoft Graph versenden

## Vorteile der Microsoft Graph Integration

1. **Sicherheit**: Keine SMTP-Passwörter im Code
2. **Zuverlässigkeit**: Microsoft Graph ist hochverfügbar
3. **Features**: Zugriff auf erweiterte E-Mail-Features
4. **Skalierbarkeit**: Bessere Performance bei vielen E-Mails
5. **Audit**: Vollständige Nachverfolgung in Azure AD

## Fehlerbehebung

### Häufige Probleme

1. **Authentifizierungsfehler**: Überprüfen Sie Tenant ID, Client ID und Client Secret
2. **Permission-Fehler**: Stellen Sie sicher, dass die API Permissions korrekt konfiguriert sind
3. **E-Mail-Fehler**: Überprüfen Sie, ob die E-Mail-Adresse in Azure AD existiert

### Debug-Modus

Für detaillierte Fehlermeldungen können Sie die Logging-Level erhöhen:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Sicherheitshinweise

1. **Niemals** Client Secrets in Version Control committen
2. Verwenden Sie Umgebungsvariablen für sensible Daten
3. Regelmäßig Client Secrets erneuern
4. Minimale Permissions verwenden (Principle of Least Privilege)

## Beispiel für Umgebungsvariablen

Erstellen Sie eine `.env` Datei:

```env
TENANT_ID=your-tenant-id
CLIENT_ID=your-client-id
CLIENT_SECRET=your-client-secret
EMAIL_FROM=your-email@domain.com
EMAIL_TO=recipient1@domain.com,recipient2@domain.com
```

Und aktualisieren Sie den Code entsprechend:

```python
import os
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO").split(",")
```
