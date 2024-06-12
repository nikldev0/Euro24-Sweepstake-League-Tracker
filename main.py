# main.py

from api.api_client import ApiClient
from data_processing.data_handler import process_api_data
from google_sheets.google_sheets_client import initialize_google_sheets, update_google_sheet


def main():
    api_client = ApiClient()
    try:
        response = api_client.get("teams", params={"league": 4, "season" : 2024})
        
       # Extract the team names from the response
        team_names = [team_info['team']['name'] for team_info in response['response']]
        
        # Print the team names
        print("Team Names:")
        for name in team_names:
            print(name)
            
        df = process_api_data(response)

        sheet = initialize_google_sheets("Euro 24 Sweepstake Tracker")
        update_google_sheet(sheet, df)


    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
