import pandas as pd
from random import sample

data = pd.read_csv('./data/March_Madness_2024_Silver_Bulletin_03_18_2024.csv').drop(['Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17', 'Unnamed: 18'], axis='columns')

def simulate_game(team1:pd.Series, team2:pd.Series, rd:int, precision:int=10000):
    team1_win_pct = team1[f'rd{rd+1}_win'] / (team1[f'rd{rd+1}_win'] + team2[f'rd{rd+1}_win'])
    return team1 if sample(range(precision), 1)[0] < team1_win_pct * precision else team2

# def simulate_round(data:list, rd:int):
#     if rd == 0:
#         data.loc[]

print([simulate_game(data.loc[2], data.loc[3], 1).team_name for i in range(100)])