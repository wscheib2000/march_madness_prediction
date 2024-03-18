import pandas as pd
from random import sample
from collections import Counter

data = pd.read_csv('./data/March_Madness_2024_Silver_Bulletin_03_18_2024.csv').drop(['Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17', 'Unnamed: 18'], axis='columns')
data.team_seed = data.team_seed.str[0:2].astype(int)

def simulate_game(team1:pd.Series, team2:pd.Series, rd:int, precision:int=10000):
    team1_win_pct = team1[f'rd{rd+1}_win'] / (team1[f'rd{rd+1}_win'] + team2[f'rd{rd+1}_win'])
    return {'W':team1, 'L':team2} if sample(range(precision), 1)[0] < team1_win_pct * precision else {'W':team2, 'L':team1}

def simulate_round(data:pd.DataFrame, rd:int):
    ret_data = data.copy()
    if rd == 0:
        data = data.loc[data.playin_flag==1]

    for i in range(0, data.shape[0], 2):
        loser = simulate_game(data.iloc[i], data.iloc[i+1], rd)['L']
        ret_data = ret_data[~(ret_data.team_id == loser.team_id)]
    return ret_data

def simulate_tournament(data:pd.DataFrame):
    rd_64 = simulate_round(data, 0)
    rd_32 = simulate_round(rd_64, 1)
    rd_16 = simulate_round(rd_32, 2)
    rd_8 = simulate_round(rd_16, 3)
    rd_4 = simulate_round(rd_8, 4)
    rd_2 = simulate_round(rd_4, 5)
    champion = simulate_round(rd_2, 6)

    return {
        64: rd_64,
        32: rd_32,
        16: rd_16,
        8: rd_8,
        4: rd_4,
        2: rd_2,
        1: champion
    }
# print(Counter([simulate_game(data.loc[0], data.loc[1], 1)['W'].team_name for i in range(10000)]))
# print(rd_32)