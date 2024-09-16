import gspread
from google.oauth2.service_account import Credentials
from supabase import create_client, Client

# Function to insert data from Google Sheets to Supabase
def insert_data_from_sheet_to_db(sheet_name, row_number, supabase_url, supabase_key, table_name):
    # Google Sheets credentials
    SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    CREDS = Credentials.from_service_account_file("sheet-syncer-de76056deee3.json", scopes=SCOPE)
    gc = gspread.authorize(CREDS)

    # Access the Google Sheet and get the data from the specified row
    spreadsheet = gc.open(sheet_name)
    worksheet = spreadsheet.sheet1
    row_data = worksheet.row_values(row_number)

    # Convert the row data into a dictionary
    data_dict = {"id": int(row_data[0]), "text": row_data[1]}
    print(f"Inserting data: {data_dict}")

    # Supabase credentials
    supabase: Client = create_client(supabase_url, supabase_key)

    # Insert the data into the specified Supabase table
    response = (
        supabase.table(table_name)
        .insert(data_dict)
        .execute()
    )

    # Print the response from the database
    print(response)
    return response

# Example usage
sheet_name = "demo1"
row_number = 4
supabase_url = "https://wqyqzaojukrlhfkvuops.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndxeXF6YW9qdWtybGhma3Z1b3BzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY0MjIxMjMsImV4cCI6MjA0MTk5ODEyM30.9NswMRI2YM1rgyD4skpYMRaBVdXxSPjTV8dWaFzqtG8"
table_name = "demo1"

# Call the function
insert_data_from_sheet_to_db(sheet_name, row_number, supabase_url, supabase_key, table_name)
