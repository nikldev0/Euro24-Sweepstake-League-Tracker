# data_processing/data_handler.py

import pandas as pd

def extract_team_names(fixtures):

        # Extract team names and create a DataFrame
        # Initialize an empty set to store unique team names
        team_names = set()

        # Iterate over each fixture in the response
        for fixture in fixtures:
            # Skip fixtures from qualifying rounds
            if "Qualifying" in fixture['league']['round']:
                continue
            
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            
            # Add the team names to the set (sets automatically handle deduplication)
            team_names.add(home_team)
            team_names.add(away_team)

        # Convert the set to a list and sort it
        unique_team_names = sorted(list(team_names))


        if unique_team_names:
            return pd.DataFrame(unique_team_names, columns=['Team Names'])
        else:
            print("No team names found")
            return pd.DataFrame(columns=['Team Names'])
        

        
def process_fixture_events(api_client, fixture_id, home_team_id, away_team_id):

    response = api_client.get(f"fixtures/events?fixture={fixture_id}")
    events = response.get('response', [])
    
    home_yellow_cards = 0
    home_red_cards = 0
    away_yellow_cards = 0
    away_red_cards = 0
    
    for event in events:
        if event['type'] == 'Card':
            if event['detail'] == 'Yellow Card':
                if event['team']['id'] == home_team_id:
                    home_yellow_cards += 1
                elif event['team']['id'] == away_team_id:
                    away_yellow_cards += 1
            elif event['detail'] == 'Red Card':
                if event['team']['id'] == home_team_id:
                    home_red_cards += 1
                elif event['team']['id'] == away_team_id:
                    away_red_cards += 1

    return home_yellow_cards, home_red_cards, away_yellow_cards, away_red_cards

        
        
def process_group_fixtures(api_client, fixtures, group_name):
    fixtures_data = []
    
    for fixture in fixtures:
        if group_name in fixture['league']['round']:
            fixture_id = fixture['fixture']['id']
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            home_team_id = fixture['teams']['home']['id']
            away_team_id = fixture['teams']['away']['id']
            
            if fixture['fixture']['status']['long'] == "Not Started":
                # If the match has not started, only add the fixture ID, home, and away team names
                fixtures_data.append([
                    fixture_id,
                    home_team,
                    away_team,
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    ""
                ])
            else:
                home_goals = fixture['goals']['home']
                away_goals = fixture['goals']['away']
                
                if fixture['teams']['home']['winner'] is None and fixture['teams']['away']['winner'] is None:
                    result = "Draw"
                elif fixture['teams']['home']['winner']:
                    result = f"{home_team} Victory"
                else:
                    result = f"{away_team} Victory"
                
                # Fetch the fixture events for cards
                home_yellow_cards, home_red_cards, away_yellow_cards, away_red_cards = process_fixture_events(api_client, fixture_id, home_team_id, away_team_id)
                
                fixtures_data.append([
                    fixture_id,
                    home_team,
                    away_team,
                    result,
                    home_goals,
                    away_goals,
                    away_goals,
                    home_goals,
                    home_yellow_cards,
                    home_red_cards,
                    away_yellow_cards,
                    away_red_cards
                ])
    
    columns = ["Fixture ID", "Home", "Away", "Result", "Home Goals Scored", "Home Goals Conceded", "Away Goals Scored", "Away Goals Conceded", "Home Yellow Cards", "Home Red Cards", "Away Yellow Cards", "Away Red Cards"]
    if fixtures_data:
        return pd.DataFrame(fixtures_data, columns=columns)
    else:
        print(f"No fixtures found for {group_name}")
        return pd.DataFrame(columns=columns)
    



# def process_group_a_fixtures(fixtures):
#     fixtures_data = []
    
#     for fixture in fixtures:
#         # Check if the round contains "Group A"
#         if "Group A" in fixture['league']['round']:
#             home_team = fixture['teams']['home']['name']
#             away_team = fixture['teams']['away']['name']
#             home_goals = fixture['goals']['home']
#             away_goals = fixture['goals']['away']
            
#             # Determine the result
#             if fixture['teams']['home']['winner'] is None and fixture['teams']['away']['winner'] is None:
#                 result = "Draw"
#             elif fixture['teams']['home']['winner']:
#                 result = f"{home_team} Victory"
#             else:
#                 result = f"{away_team} Victory"
            
#             fixtures_data.append([
#                 home_team,
#                 away_team,
#                 result,
#                 home_goals,
#                 away_goals,
#                 away_goals,  # Away Goals Scored
#                 home_goals   # Home Goals Conceded
#             ])
    
#     if fixtures_data:
#         columns = ["Home", "Away", "Result", "Home Goals Scored", "Home Goals Conceded", "Away Goals Scored", "Away Goals Conceded"]
#         return pd.DataFrame(fixtures_data, columns=columns)
#     else:
#         print("No Group A fixtures found")
#         return pd.DataFrame(columns=["Home", "Away", "Result", "Home Goals Scored", "Home Goals Conceded", "Away Goals Scored", "Away Goals Conceded"])


# def process_group_b_fixtures(fixtures):
#     fixtures_data = []
    
#     for fixture in fixtures:
#         # Check if the round contains "Group B"
#         if "Group B" in fixture['league']['round']:
#             home_team = fixture['teams']['home']['name']
#             away_team = fixture['teams']['away']['name']
#             home_goals = fixture['goals']['home']
#             away_goals = fixture['goals']['away']
            
#             # Determine the result
#             if fixture['teams']['home']['winner'] is None and fixture['teams']['away']['winner'] is None:
#                 result = "Draw"
#             elif fixture['teams']['home']['winner']:
#                 result = f"{home_team} Victory"
#             else:
#                 result = f"{away_team} Victory"
            
#             fixtures_data.append([
#                 home_team,
#                 away_team,
#                 result,
#                 home_goals,
#                 away_goals,
#                 away_goals,  # Away Goals Scored
#                 home_goals   # Home Goals Conceded
#             ])
    
#     columns = ["Home", "Away", "Result", "Home Goals Scored", "Home Goals Conceded", "Away Goals Scored", "Away Goals Conceded"]
#     return pd.DataFrame(fixtures_data, columns=columns)


# def process_group_c_fixtures(fixtures):
    fixtures_data = []
    
    for fixture in fixtures:
        # Check if the round contains "Group C"
        if "Group C" in fixture['league']['round']:
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            home_goals = fixture['goals']['home']
            away_goals = fixture['goals']['away']
            
            # Determine the result
            if fixture['teams']['home']['winner'] is None and fixture['teams']['away']['winner'] is None:
                result = "Draw"
            elif fixture['teams']['home']['winner']:
                result = f"{home_team} Victory"
            else:
                result = f"{away_team} Victory"
            
            fixtures_data.append([
                home_team,
                away_team,
                result,
                home_goals,
                away_goals,
                away_goals,  # Away Goals Scored
                home_goals   # Home Goals Conceded
            ])
    
    columns = ["Home", "Away", "Result", "Home Goals Scored", "Home Goals Conceded", "Away Goals Scored", "Away Goals Conceded"]
    return pd.DataFrame(fixtures_data, columns=columns)