import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
from supabase import create_client, Client

# Google Sheets and Supabase credentials
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "sheet-syncer-de76056deee3.json"
LOG_SHEET_URL = "https://docs.google.com/spreadsheets/d/11aQ83lWys2kk4SeAxKNWYz1u3HhPtLFZEjH8UT2-yRY/edit?gid=444651832"
ACTUAL_SHEET_URL = "https://docs.google.com/spreadsheets/d/11aQ83lWys2kk4SeAxKNWYz1u3HhPtLFZEjH8UT2-yRY/edit?gid=1234567890"  # Update with the actual sheet URL
LAST_CHANGED_FILE = "last_changed_time.txt"

# Supabase credentials
supabase_url = "https://wqyqzaojukrlhfkvuops.supabase.co"
supabase_key = "your-supabase-key"  # Replace with your Supabase API key
table_name = "demo1"  # Example table name

def get_last_changed_time():
    """Get the last processed changed time from a file."""
    if os.path.exists(LAST_CHANGED_FILE):
        with open(LAST_CHANGED_FILE, "r") as file:
            return datetime.strptime(file.read().strip(), "%Y-%m-%d %H:%M:%S")
    return datetime.min

def store_last_changed_time(log_time):
    """Store the last processed changed time in a file."""
    with open(LAST_CHANGED_FILE, "w") as file:
        file.write(log_time.strftime("%Y-%m-%d %H:%M:%S"))

def insert_data_into_db(id, text):
    try:
        # Create Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)

        # Data to be inserted or updated
        data = {"id": id, "text": text}
        print(f"Inserting/Updating data: {data}")

        # Use upsert to insert or update the record
        response = supabase.table(table_name).upsert(data).execute()
        print("Insert/Update response:", response.data)

        if response.error:
            print(f"Error during insert/update: {response.error}")

        return response
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_data_from_db(id):
    try:
        # Create Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)

        # Delete data from Supabase table
        print(f"Deleting data with ID: {id}")
        response = supabase.table(table_name).delete().eq("id", id).execute()

        print("Delete response:", response.data)

        if response.error:
            print(f"Error during delete: {response.error}")

        return response
    except Exception as e:
        print(f"An error occurred: {e}")

def fetch_new_logs():
    # Google Sheets credentials
    CREDS = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPE)
    gc = gspread.authorize(CREDS)

    # Access the log sheet
    log_spreadsheet = gc.open_by_url(LOG_SHEET_URL)
    log_worksheet = log_spreadsheet.worksheet("ChangeLog")  # Assuming the log sheet name is "ChangeLog"

    # Access the actual data sheet
    actual_spreadsheet = gc.open_by_url(ACTUAL_SHEET_URL)
    actual_worksheet = actual_spreadsheet.get_worksheet(0)  # Assuming the actual data sheet is the first one

    # Get all data from the log sheet
    log_data = log_worksheet.get_all_values()
    print("Raw data from log sheet:", log_data)

    # Convert the data into a DataFrame
    if len(log_data) > 1:
        df_logs = pd.DataFrame(log_data[1:], columns=log_data[0])  # Skip header row
    else:
        print("No data found in the log sheet.")
        return

    # Print DataFrame for debugging
    print("DataFrame before processing logs:", df_logs)

    # Ensure that the DataFrame columns match the expected names
    expected_columns = ['Timestamp', 'Sheet', 'Cell', 'Old Value', 'New Value']
    if len(df_logs.columns) == len(expected_columns):
        df_logs.columns = expected_columns
    else:
        print(f"Unexpected number of columns: {len(df_logs.columns)}. Expected: {len(expected_columns)}")
        return

    # Print DataFrame after renaming columns
    print("DataFrame after renaming columns:", df_logs)

    # Convert 'Timestamp' column to datetime format
    df_logs['Timestamp'] = pd.to_datetime(df_logs['Timestamp'], errors='coerce')

    # Sort by Timestamp to process the latest changes
    df_logs = df_logs.sort_values(by='Timestamp', ascending=False)

    # Get the latest log timestamp from the local log file
    last_timestamp = get_last_changed_time()

    # Filter logs to include only those newer than the last processed timestamp
    new_logs = df_logs[df_logs['Timestamp'] > last_timestamp]

    # Process the new logs
    for _, row in new_logs.iterrows():
        print(f"Processing log: Timestamp: {row['Timestamp']}, Sheet: {row['Sheet']}, Cell: {row['Cell']}, Old Value: {row['Old Value']}, New Value: {row['New Value']}")
        process_log(row)

    # Update the last log timestamp
    if not new_logs.empty:
        latest_timestamp = new_logs['Timestamp'].max()
        store_last_changed_time(latest_timestamp)

def process_log(row):
    log_time_str = row['Timestamp']
    sheet_name = row['Sheet']
    cell = row['Cell']
    old_value = row['Old Value']
    new_value = row['New Value']

    # Assuming the ID is derived from cell address or another logic
    id = cell.split(":")[0]  # Adjust as needed
    text = new_value if new_value not in ["Cleared", "Deleted"] else None

    # Handle deletion or clear
    if new_value == "Cleared":
        delete_data_from_db(id)
    elif new_value == "Deleted":
        delete_data_from_db(id)
    elif text is not None:
        insert_data_into_db(id, text)

# Call the function
fetch_new_logs()
