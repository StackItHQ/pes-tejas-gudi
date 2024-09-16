import gspread
import os
import json
from google.oauth2.service_account import Credentials
from supabase import create_client, Client

# gsheet creds
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS = Credentials.from_service_account_file("sheet-syncer-de76056deee3.json", scopes=SCOPE)
gc = gspread.authorize(CREDS)
spreadsheet = gc.open("demo1")
worksheet = spreadsheet.sheet1
row_data = worksheet.row_values(2)
data_dict = {"id": int(row_data[0]), "text": row_data[1]}
print(row_data)

# supabase creds
url: str = "https://wqyqzaojukrlhfkvuops.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndxeXF6YW9qdWtybGhma3Z1b3BzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY0MjIxMjMsImV4cCI6MjA0MTk5ODEyM30.9NswMRI2YM1rgyD4skpYMRaBVdXxSPjTV8dWaFzqtG8"
supabase: Client = create_client(url, key)
# response = supabase.table("demo1").select("*").execute()
response = (
    supabase.table("demo1")
    .insert(data_dict)
    .execute()
)
print(response)
