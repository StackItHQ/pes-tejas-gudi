from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

# Set up credentials
SERVICE_ACCOUNT_FILE = 'sheet-syncer-de76056deee3.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/cloud-platform']

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)

# Set the spreadsheet ID and range to watch
spreadsheet_id = '11aQ83lWys2kk4SeAxKNWYz1u3HhPtLFZEjH8UT2-yRY'

# Set up the Pub/Sub topic for notifications
pubsub_topic = "projects/your-project-id/topics/google-sheets-updates"

# Create the watch request
watch_request_body = {
    "type": "web_hook",
    "address": pubsub_topic,  # This will send events to your Pub/Sub topic
}

# Send the watch request to Google Sheets
response = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

print(f"Subscribed to changes for sheet: {spreadsheet_id}")
