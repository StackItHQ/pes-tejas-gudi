import gspread
from google.oauth2.service_account import Credentials

# Load credentials from the JSON key file
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS = Credentials.from_service_account_file("sheet-syncer-de76056deee3.json", scopes=SCOPE)

# Authenticate and connect to Google Sheets
gc = gspread.authorize(CREDS)

# Open the Google Sheet by name or URL
spreadsheet = gc.open("demo1")

# Select the first worksheet
worksheet = spreadsheet.sheet1

# Example: Read data from the first row
row_data = worksheet.row_values(1)
print("Row 1 Data:", row_data)
print(type(row_data))
# Example: Write data to the Google Sheet
# worksheet.update("A2", "Hello, Google Sheets!")
# worksheet.update([[1, 2], [3, 4]], 'A1')
# # Example: Insert a new row of data at the top
# new_row = ["Data 1", "Data 2", "Data 3"]
# worksheet.insert_row(new_row, 3)

print("Data updated successfully!")
