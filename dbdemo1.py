import os
from supabase import create_client, Client

url: str = "https://wqyqzaojukrlhfkvuops.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndxeXF6YW9qdWtybGhma3Z1b3BzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY0MjIxMjMsImV4cCI6MjA0MTk5ODEyM30.9NswMRI2YM1rgyD4skpYMRaBVdXxSPjTV8dWaFzqtG8"
supabase: Client = create_client(url, key)
response = supabase.table("demo1").select("*").execute()
response = (
    supabase.table("demo1")
    .insert({"id": 1, "text": "abc"})
    .execute()
)

print(response)