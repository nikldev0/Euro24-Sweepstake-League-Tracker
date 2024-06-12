import pandas as pd

def process_api_data(data):
    df = pd.DataFrame(data['results'])  
    return df
