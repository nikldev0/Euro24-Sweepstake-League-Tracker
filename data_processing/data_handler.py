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
        
        
def get_fixture_events(api_client, fixture_id):
    response = api_client.get(f"fixtures/events?fixture={fixture_id}")
    return response.get('response', [])
        

def process_card_events(events, home_team_id, away_team_id):
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



def process_hat_trick_events(events, home_team_id, away_team_id):
    home_goals = {}
    away_goals = {}
    home_hat_tricks = 0
    away_hat_tricks = 0
    
    for event in events:
        if event['type'] == 'Goal' and event['detail'] in ['Normal Goal', 'Penalty']:
            player_id = event['player']['id']
            if event['team']['id'] == home_team_id:
                if player_id in home_goals:
                    home_goals[player_id] += 1
                else:
                    home_goals[player_id] = 1
            elif event['team']['id'] == away_team_id:
                if player_id in away_goals:
                    away_goals[player_id] += 1
                else:
                    away_goals[player_id] = 1
    
    for goals in home_goals.values():
        if goals >= 3:
            home_hat_tricks += 1
    
    for goals in away_goals.values():
        if goals >= 3:
            away_hat_tricks += 1

    return home_hat_tricks, away_hat_tricks

        
def process_own_goal_events(events, home_team_id, away_team_id):
    home_own_goals = 0
    away_own_goals = 0
    
    for event in events:
        if event['type'] == 'Goal' and event['detail'] == 'Own Goal':
            if event['team']['id'] == home_team_id:
                away_own_goals += 1
            elif event['team']['id'] == away_team_id:
                home_own_goals += 1

    return home_own_goals, away_own_goals


def process_group_fixtures(api_client, fixtures, group_name):
    fixtures_data = []
    
    for fixture in fixtures:
        if group_name in fixture['league']['round']:
            fixture_id = fixture['fixture']['id']
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            home_team_id = fixture['teams']['home']['id']
            away_team_id = fixture['teams']['away']['id']
            
            events = get_fixture_events(api_client, fixture_id)
            
            if fixture['fixture']['status']['long'] == "Not Started":
                # If the match has not started, only add the fixture ID, home, and away team names
                fixtures_data.append([
                    fixture_id,
                    home_team,
                    away_team,
                    "", "", "", "", "", "", "", "", "", "", "", "", ""
                ])
            else:
                home_goals = fixture['goals']['home'] if fixture['goals']['home'] is not None else 0
                away_goals = fixture['goals']['away'] if fixture['goals']['away'] is not None else 0
                
                if fixture['teams']['home']['winner'] is None and fixture['teams']['away']['winner'] is None:
                    result = "Draw"
                elif fixture['teams']['home']['winner']:
                    result = f"{home_team} Victory"
                else:
                    result = f"{away_team} Victory"
                
                # Fetch the fixture events for cards
                home_yellow_cards, home_red_cards, away_yellow_cards, away_red_cards = process_card_events(events, home_team_id, away_team_id)
                
                # Fetch the hat trick events
                home_hat_tricks, away_hat_tricks = process_hat_trick_events(events, home_team_id, away_team_id)
                
                # Fetch the own goal events
                home_own_goals, away_own_goals = process_own_goal_events(events, home_team_id, away_team_id)
                
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
                    away_red_cards,
                    home_hat_tricks,
                    away_hat_tricks,
                    home_own_goals,
                    away_own_goals
                ])
    
    columns = ["Fixture ID", "Home", "Away", "Result", "Home Goals Scored", "Home Goals Conceded", "Away Goals Scored", "Away Goals Conceded", "Home Yellow Cards", "Home Red Cards", "Away Yellow Cards", "Away Red Cards", "Home Hat Tricks", "Away Hat Tricks", "Home Own Goals", "Away Own Goals"]
    
    df = pd.DataFrame(fixtures_data, columns=columns)
    
    # Replace NaN values with 0
    df = df.fillna(0)
    
    if not df.empty:
        return df
    else:
        print(f"No fixtures found for {group_name}")
        return pd.DataFrame(columns=columns)
    

def process_round_of_16_fixtures(api_client, fixtures):
    
    fixtures_data = []
    
    for fixture in fixtures:
        if fixture['league']['round'] == "Round of 16":
            fixture_id = fixture['fixture']['id']
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            home_team_id = fixture['teams']['home']['id']
            away_team_id = fixture['teams']['away']['id']
            
            events = get_fixture_events(api_client, fixture_id)
            
            if fixture['fixture']['status']['long'] == "Not Started":
                # If the match has not started, only add the fixture ID, home, and away team names
                fixtures_data.append([
                    fixture_id,
                    home_team,
                    away_team,
                    "", "", "", "", "", "", "", "", "", "", "", "", "", ""
                ])
            else:
                home_goals = fixture['goals']['home'] if fixture['goals']['home'] is not None else 0
                away_goals = fixture['goals']['away'] if fixture['goals']['away'] is not None else 0
                
                if fixture['teams']['home']['winner'] is None and fixture['teams']['away']['winner'] is None:
                    result = "Draw"
                elif fixture['teams']['home']['winner']:
                    result = f"{home_team} Victory"
                else:
                    result = f"{away_team} Victory"
                
                # Check if the match was decided by penalties
                victory_on_penalties = "TRUE" if fixture['fixture']['status']['short'] == "PEN" else "FALSE"
                
                # Fetch the fixture events for cards
                home_yellow_cards, home_red_cards, away_yellow_cards, away_red_cards = process_card_events(events, home_team_id, away_team_id)
                
                # Fetch the hat trick events
                home_hat_tricks, away_hat_tricks = process_hat_trick_events(events, home_team_id, away_team_id)
                
                # Fetch the own goal events
                home_own_goals, away_own_goals = process_own_goal_events(events, home_team_id, away_team_id)
                
                fixtures_data.append([
                    fixture_id,
                    home_team,
                    away_team,
                    result,
                    victory_on_penalties,
                    home_goals,
                    away_goals,
                    away_goals,
                    home_goals,
                    home_yellow_cards,
                    home_red_cards,
                    away_yellow_cards,
                    away_red_cards,
                    home_hat_tricks,
                    away_hat_tricks,
                    home_own_goals,
                    away_own_goals
                ])
    
    columns = ["Fixture ID", "Home", "Away", "Result", "Victory on Penalties?", "Home Goals Scored", "Home Goals Conceded", "Away Goals Scored", "Away Goals Conceded", "Home Yellow Cards", "Home Red Cards", "Away Yellow Cards", "Away Red Cards", "Home Hat Tricks", "Away Hat Tricks", "Home Own Goals", "Away Own Goals"]
    
    df = pd.DataFrame(fixtures_data, columns=columns)
    
    # Replace NaN values with 0
    df = df.fillna(0)
    
    if not df.empty:
        return df
    else:
        print(f"No fixtures found for Round of 16")
        return pd.DataFrame(columns=columns)
    










def process_quarter_final_fixtures(api_client, fixtures):
    
    fixtures_data = []
    
    for fixture in fixtures:
        if fixture['league']['round'] == "Quarter-finals":
            fixture_id = fixture['fixture']['id']
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            home_team_id = fixture['teams']['home']['id']
            away_team_id = fixture['teams']['away']['id']
            
            events = get_fixture_events(api_client, fixture_id)
            
            if fixture['fixture']['status']['long'] == "Not Started":
                # If the match has not started, only add the fixture ID, home, and away team names
                fixtures_data.append([
                    fixture_id,
                    home_team,
                    away_team,
                    "", "", "", "", "", "", "", "", "", "", "", "", "", ""
                ])
            else:
                home_goals = fixture['goals']['home'] if fixture['goals']['home'] is not None else 0
                away_goals = fixture['goals']['away'] if fixture['goals']['away'] is not None else 0
                
                if fixture['teams']['home']['winner'] is None and fixture['teams']['away']['winner'] is None:
                    result = "Draw"
                elif fixture['teams']['home']['winner']:
                    result = f"{home_team} Victory"
                else:
                    result = f"{away_team} Victory"
                
                # Check if the match was decided by penalties
                victory_on_penalties = "TRUE" if fixture['fixture']['status']['short'] == "PEN" else "FALSE"
                
                # Fetch the fixture events for cards
                home_yellow_cards, home_red_cards, away_yellow_cards, away_red_cards = process_card_events(events, home_team_id, away_team_id)
                
                # Fetch the hat trick events
                home_hat_tricks, away_hat_tricks = process_hat_trick_events(events, home_team_id, away_team_id)
                
                # Fetch the own goal events
                home_own_goals, away_own_goals = process_own_goal_events(events, home_team_id, away_team_id)
                
                fixtures_data.append([
                    fixture_id,
                    home_team,
                    away_team,
                    result,
                    victory_on_penalties,
                    home_goals,
                    away_goals,
                    away_goals,
                    home_goals,
                    home_yellow_cards,
                    home_red_cards,
                    away_yellow_cards,
                    away_red_cards,
                    home_hat_tricks,
                    away_hat_tricks,
                    home_own_goals,
                    away_own_goals
                ])
    
    columns = ["Fixture ID", "Home", "Away", "Result", "Victory on Penalties?", "Home Goals Scored", "Home Goals Conceded", "Away Goals Scored", "Away Goals Conceded", "Home Yellow Cards", "Home Red Cards", "Away Yellow Cards", "Away Red Cards", "Home Hat Tricks", "Away Hat Tricks", "Home Own Goals", "Away Own Goals"]
    
    df = pd.DataFrame(fixtures_data, columns=columns)
    
    # Replace NaN values with 0
    df = df.fillna(0)
    
    if not df.empty:
        return df
    else:
        print(f"No fixtures found for Quarter-finals")
        return pd.DataFrame(columns=columns)
    



def process_semi_final_fixtures(api_client, fixtures):

    fixtures_data = []
    
    for fixture in fixtures:
        if fixture['league']['round'] == "Semi-finals":
            fixture_id = fixture['fixture']['id']
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            home_team_id = fixture['teams']['home']['id']
            away_team_id = fixture['teams']['away']['id']
            
            events = get_fixture_events(api_client, fixture_id)
            
            if fixture['fixture']['status']['long'] == "Not Started":
                # If the match has not started, only add the fixture ID, home, and away team names
                fixtures_data.append([
                    fixture_id,
                    home_team,
                    away_team,
                    "", "", "", "", "", "", "", "", "", "", "", "", "", ""
                ])
            else:
                home_goals = fixture['goals']['home'] if fixture['goals']['home'] is not None else 0
                away_goals = fixture['goals']['away'] if fixture['goals']['away'] is not None else 0
                
                if fixture['teams']['home']['winner'] is None and fixture['teams']['away']['winner'] is None:
                    result = "Draw"
                elif fixture['teams']['home']['winner']:
                    result = f"{home_team} Victory"
                else:
                    result = f"{away_team} Victory"
                
                # Check if the match was decided by penalties
                victory_on_penalties = "TRUE" if fixture['fixture']['status']['short'] == "PEN" else "FALSE"
                
                # Fetch the fixture events for cards
                home_yellow_cards, home_red_cards, away_yellow_cards, away_red_cards = process_card_events(events, home_team_id, away_team_id)
                
                # Fetch the hat trick events
                home_hat_tricks, away_hat_tricks = process_hat_trick_events(events, home_team_id, away_team_id)
                
                # Fetch the own goal events
                home_own_goals, away_own_goals = process_own_goal_events(events, home_team_id, away_team_id)
                
                fixtures_data.append([
                    fixture_id,
                    home_team,
                    away_team,
                    result,
                    victory_on_penalties,
                    home_goals,
                    away_goals,
                    away_goals,
                    home_goals,
                    home_yellow_cards,
                    home_red_cards,
                    away_yellow_cards,
                    away_red_cards,
                    home_hat_tricks,
                    away_hat_tricks,
                    home_own_goals,
                    away_own_goals
                ])
    
    columns = ["Fixture ID", "Home", "Away", "Result", "Victory on Penalties?", "Home Goals Scored", "Home Goals Conceded", "Away Goals Scored", "Away Goals Conceded", "Home Yellow Cards", "Home Red Cards", "Away Yellow Cards", "Away Red Cards", "Home Hat Tricks", "Away Hat Tricks", "Home Own Goals", "Away Own Goals"]
    
    df = pd.DataFrame(fixtures_data, columns=columns)
    
    # Replace NaN values with 0
    df = df.fillna(0)
    
    if not df.empty:
        return df
    else:
        print(f"No fixtures found for Semi-finals")
        return pd.DataFrame(columns=columns)
    

def process_final_fixture(api_client, fixtures):

    fixtures_data = []
    
    for fixture in fixtures:
        if fixture['league']['round'] == "Final":
            fixture_id = fixture['fixture']['id']
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            home_team_id = fixture['teams']['home']['id']
            away_team_id = fixture['teams']['away']['id']
            
            events = get_fixture_events(api_client, fixture_id)
            
            if fixture['fixture']['status']['long'] == "Not Started":
                # If the match has not started, only add the fixture ID, home, and away team names
                fixtures_data.append([
                    fixture_id,
                    home_team,
                    away_team,
                    "", "", "", "", "", "", "", "", "", "", "", "", "", ""
                ])
            else:
                home_goals = fixture['goals']['home'] if fixture['goals']['home'] is not None else 0
                away_goals = fixture['goals']['away'] if fixture['goals']['away'] is not None else 0
                
                if fixture['teams']['home']['winner'] is None and fixture['teams']['away']['winner'] is None:
                    result = "Draw"
                elif fixture['teams']['home']['winner']:
                    result = f"{home_team} Victory"
                else:
                    result = f"{away_team} Victory"
                
                # Check if the match was decided by penalties
                victory_on_penalties = "TRUE" if fixture['fixture']['status']['short'] == "PEN" else "FALSE"
                
                # Fetch the fixture events for cards
                home_yellow_cards, home_red_cards, away_yellow_cards, away_red_cards = process_card_events(events, home_team_id, away_team_id)
                
                # Fetch the hat trick events
                home_hat_tricks, away_hat_tricks = process_hat_trick_events(events, home_team_id, away_team_id)
                
                # Fetch the own goal events
                home_own_goals, away_own_goals = process_own_goal_events(events, home_team_id, away_team_id)
                
                fixtures_data.append([
                    fixture_id,
                    home_team,
                    away_team,
                    result,
                    victory_on_penalties,
                    home_goals,
                    away_goals,
                    away_goals,
                    home_goals,
                    home_yellow_cards,
                    home_red_cards,
                    away_yellow_cards,
                    away_red_cards,
                    home_hat_tricks,
                    away_hat_tricks,
                    home_own_goals,
                    away_own_goals
                ])
    
    columns = ["Fixture ID", "Home", "Away", "Result", "Victory on Penalties?", "Home Goals Scored", "Home Goals Conceded", "Away Goals Scored", "Away Goals Conceded", "Home Yellow Cards", "Home Red Cards", "Away Yellow Cards", "Away Red Cards", "Home Hat Tricks", "Away Hat Tricks", "Home Own Goals", "Away Own Goals"]
    
    df = pd.DataFrame(fixtures_data, columns=columns)
    
    # Replace NaN values with 0
    df = df.fillna(0)
    
    if not df.empty:
        return df
    else:
        print(f"No fixtures found for Final")
        return pd.DataFrame(columns=columns)
    