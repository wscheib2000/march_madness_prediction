import pandas as pd
from random import sample
from team import Team

data = pd.read_csv('./data/March_Madness_2024_Silver_Bulletin_03_18_2024.csv').drop(['Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17', 'Unnamed: 18'], axis='columns')
print(data.iloc[:, -10:])

def row_to_instance(row):
    win_probs = {
        0: row['rd1_win'],
        1: row['rd2_win'],
        2: row['rd3_win'],
        3: row['rd4_win'],
        4: row['rd5_win'],
        5: row['rd6_win'],
        6: row['rd7_win']
    }
    instance = Team(id=row['team_id'], name=row['team_name'], seed=row['team_seed'], win_probs=win_probs)
    return instance

data2 = data.apply(row_to_instance, axis=1)

def simulate_game(team1:Team, team2:Team, rd:int, precision:int=10000):
    team1_win_pct = team1.win_probs[rd] / (team1.win_probs[rd] + team2.win_probs[rd])
    print(sample(range(precision), 1)[0])
    return team1 if sample(range(precision), 1)[0] < team1_win_pct * precision else team2

print(data2[64].name)
print([simulate_game(data2[2], data2[3], 1).name for i in range(100)])