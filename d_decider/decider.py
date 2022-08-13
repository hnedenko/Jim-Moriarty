import random


class Decider:

    def __init__(self):
        self.folder = 'd_decider'

    def get_recommendations(self, probability):
        recommendation = random.choice(["ФОЛД", "500"])
        return recommendation
