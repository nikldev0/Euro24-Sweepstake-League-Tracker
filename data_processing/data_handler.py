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
        
        
def process_group_fixtures(fixtures, group_name):
    fixtures_data = []
    
    for fixture in fixtures:
        if group_name in fixture['league']['round']:
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            home_goals = fixture['goals']['home']
            away_goals = fixture['goals']['away']
            
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
                away_goals,
                home_goals
            ])
    
    columns = ["Home", "Away", "Result", "Home Goals Scored", "Home Goals Conceded", "Away Goals Scored", "Away Goals Conceded"]
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