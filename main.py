from simulator import Simulator, BracketSimulator
import pandas as pd
from collections import Counter

DATA_FILEPATH = 'data/March_Madness_2024_Silver_Bulletin_03_18_2024.csv'
PICK_DATA_FILEPATH = 'data/yahoo_pick_distributions.csv'

data = pd.read_csv(DATA_FILEPATH).drop(['Unnamed: 15', 'Unnamed: 16', 'Unnamed: 17', 'Unnamed: 18'], axis='columns')
data.team_seed = data.team_seed.str[0:2].astype(int)

tournament_sim = Simulator(data)

pick_data = pd.read_csv(PICK_DATA_FILEPATH)

bracket_sim = BracketSimulator(pick_data)

winning_champions = []
for i in range(0,10000):
    result_sim = tournament_sim.simulate_tournament()

    champions = []
    scores = []
    # for j in range(0,100):
    #     sim = bracket_sim.simulate_tournament()
    #     score = sim.score_bracket(result_sim)
    #     champions.append(sim.data[1].iloc[0]['team_name'])
    #     scores.append(score)

    # winning_champions.append(champions[scores.index(max(scores))])
    # print(f'Champion: {result_sim.data[1].iloc[0]['team_name']}')
    winning_champions.append(result_sim.data[1].iloc[0]['team_name'])
    if (i+1)%100 == 0:
        print(f'{(i+1)//100}% finished')
    # print(f'Winning score: {max(scores)}\nWinning bracket champion: {champions[scores.index(max(scores))]}\nActual champion: {result_sim.data[1].iloc[0]['team_name']}')

print(Counter(winning_champions))