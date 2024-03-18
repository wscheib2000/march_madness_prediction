class Team:
    def __init__(self, id, name, seed, win_probs:dict) -> None:
        self.id = id
        self.name = name
        self.seed = seed
        self.win_probs = win_probs