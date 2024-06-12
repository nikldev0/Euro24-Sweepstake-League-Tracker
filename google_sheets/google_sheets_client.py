import gspread
from oauth2client.service_account import ServiceAccountCredentials

def initialize_google_sheets(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("path_to_your_credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    return sheet

def update_google_sheet(sheet, df):
    sheet.update([df.columns.values.tolist()] + df.values.tolist())
