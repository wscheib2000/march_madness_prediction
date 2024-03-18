class Tournament:
    def __init__(self, data:dict):
        self.data = data

    def score_bracket(self, solution):
        raise TypeError("Cannot score a tournament results simulation.")

class Bracket(Tournament):
    def __init__(self, data: dict):
        super().__init__(data)

    def score_bracket(self, solution):
        score = 0
        for (round, teams) in self.data.items():
            if round == 64:
                continue
            for idx, row in teams.iterrows():
                play_in = False
                if row.team_id == 38 or row.team_id == 68:
                    play_in = 38 in solution.data[round].team_id.values or 68 in solution.data[round].team_id.values
                elif row.team_id == 258 or row.team_id == 36:
                    play_in = 258 in solution.data[round].team_id.values or 36 in solution.data[round].team_id.values
                elif row.team_id == 47 or row.team_id == 2681:
                    play_in = 47 in solution.data[round].team_id.values or 2681 in solution.data[round].team_id.values
                elif row.team_id == 147 or row.team_id == 2755:
                    play_in = 147 in solution.data[round].team_id.values or 2755 in solution.data[round].team_id.values

                if row.team_id in solution.data[round].team_id.values or play_in:
                    old_score = score
                    score += 32//round
        return score