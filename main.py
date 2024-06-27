# main.py

from api.api_client import ApiClient
from data_processing.data_handler import extract_team_names, process_group_fixtures
from google_sheets.google_sheets_client import initialize_google_sheets, update_google_sheet
import pandas as pd


def update_sheet_with_group_data(api_client, response, group_name, sheet_name):
    group_df = process_group_fixtures(api_client, response['response'], group_name)
    
    print(f"{sheet_name} Fixtures DataFrame:")
    print(group_df)
    
    if not group_df.empty:
        sheet = initialize_google_sheets("Euro 24 Sweepstake League Tracker", sheet_name)
        update_google_sheet(sheet, group_df)



def main():
    api_client = ApiClient()
    try:
        response = api_client.get("fixtures", params={"league": 4, "season": 2024})

        # Extract team names and create a DataFrame
        team_names_df = extract_team_names(response['response'])

        # Print the Team Names DataFrame for debugging
        print("Team Names DataFrame:")
        print(team_names_df)
        
        # Initialize Google Sheet
        sheet = initialize_google_sheets("Euro 24 Sweepstake League Tracker", "Team Names")
        
        # Update Google Sheet with DataFrame
        # update_google_sheet(sheet, team_names_df)

        # update_sheet_with_group_data(api_client, response, "Group A", "Group A")
        # update_sheet_with_group_data(api_client, response, "Group B", "Group B")
        # update_sheet_with_group_data(api_client, response, "Group C", "Group C")
        # update_sheet_with_group_data(api_client, response, "Group D", "Group D")
        update_sheet_with_group_data(api_client, response, "Group E", "Group E")
        update_sheet_with_group_data(api_client, response, "Group F", "Group F")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()