import pandas as pd
from random import sample
from bracket import Bracket, Tournament

class Simulator:
    def __init__(self, data):
        self.data = data
        self.last_sim = 0

    def simulate_game(self, team1:pd.Series, team2:pd.Series, rd:int, precision:int=10000):
        team1_win_pct = team1[f'rd{rd+1}_win'] / (team1[f'rd{rd+1}_win'] + team2[f'rd{rd+1}_win'])
        return {'W':team1, 'L':team2} if sample(range(precision), 1)[0] < team1_win_pct * precision else {'W':team2, 'L':team1}

    def simulate_round(self, round_data, rd:int):
        ret_data = round_data.copy()
        games = round_data.copy()
        if rd == 0:
            games = games.loc[games.playin_flag==1]

        for i in range(0, games.shape[0], 2):
            loser = self.simulate_game(games.iloc[i], games.iloc[i+1], rd)['L']
            ret_data = ret_data[~(ret_data.team_id == loser.team_id)]
        return ret_data

    def make_data_dict(self):
        rd_64 = self.simulate_round(self.data, 0)
        rd_32 = self.simulate_round(rd_64, 1)
        rd_16 = self.simulate_round(rd_32, 2)
        rd_8 = self.simulate_round(rd_16, 3)
        rd_4 = self.simulate_round(rd_8, 4)
        rd_2 = self.simulate_round(rd_4, 5)
        champion = self.simulate_round(rd_2, 6)

        return {
            64: rd_64,
            32: rd_32,
            16: rd_16,
            8: rd_8,
            4: rd_4,
            2: rd_2,
            1: champion
        }

    def simulate_tournament(self):
        self.last_sim = Tournament(self.make_data_dict())

        return self.last_sim

class BracketSimulator(Simulator):
    def __init__(self, data):
        super().__init__(data)

    def simulate_game(self, team1:pd.Series, team2:pd.Series, rd:int, precision:int=10000):
        team1_pick_pct = team1[f'rd{rd+1}_pick'] / (team1[f'rd{rd+1}_pick'] + team2[f'rd{rd+1}_pick'])
        return {'W':team1, 'L':team2} if sample(range(precision), 1)[0] < team1_pick_pct * precision else {'W':team2, 'L':team1}
    
    def simulate_tournament(self):
        self.last_sim = Bracket(self.make_data_dict())

        return self.last_sim
