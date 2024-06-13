import gspread
from oauth2client.service_account import ServiceAccountCredentials

def initialize_google_sheets(sheet_name, worksheet_name):
    # Define the scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # Path to the credentials file
    creds = ServiceAccountCredentials.from_json_keyfile_name("./config/credentials.json", scope)
    
    # Authorize the client
    client = gspread.authorize(creds)
    
    # Open the Google Sheet
    sheet = client.open(sheet_name).worksheet(worksheet_name)
    return sheet

def update_google_sheet(sheet, df):
    # Update the Google Sheet with DataFrame content
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

