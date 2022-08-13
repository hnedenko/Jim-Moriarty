import pyautogui
import time
import random
from datetime import datetime
import copy
from support import CARD_ENCODER as CE

"Preflop"
"Flop"
"Turn"
"River"


class Probabilist:

    def __init__(self):
        self.folder = 'c_probabilist'
        self.last_digital_cards = None
        self.probability = None
        self.final_probability = None

        self.card_suits = ["blue", "green", "grey", "red"]
        self.card_ns = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.CARD_DECK = list()
        for suit in self.card_suits:
            for n in self.card_ns:
                self.CARD_DECK.append([suit, n])

        self.prime_numbers_ns = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
        self.prime_numbers_suits = [43, 47, 53, 59]

    def get_win_probability(self, digital_cards):
        if digital_cards != self.last_digital_cards:

            game_state = copy.deepcopy(digital_cards)

            # encode game state
            for i in range(len(game_state["hand"])):
                game_state["hand"][i] = CE.encoder[game_state["hand"][i]]
            for i in range(len(game_state["board"])):
                game_state["board"][i] = CE.encoder[game_state["board"][i]]

            temp_list = list()
            for i in range(len(game_state["hand"])):
                if game_state["hand"][i] != '0.jpg' and\
                        game_state["hand"][i] is not None and\
                        game_state["hand"][i] != []:
                    temp_list.append(game_state["hand"][i])
            game_state["hand"] = temp_list

            temp_list = list()
            for i in range(len(game_state["board"])):
                if game_state["board"][i] != '0.jpg' and\
                        game_state["board"][i] is not None and\
                        game_state["board"][i] != []:
                    temp_list.append(game_state["board"][i])
            game_state["board"] = temp_list

            distribution = dict()
            distribution["player_hand"] = game_state["hand"]
            distribution["board"] = game_state["board"]
            distribution["enemy_hand"] = []

            all_games, winnes, loses = self.count_probability(distribution, 1)

            self.last_digital_cards = digital_cards

            probability = int(100*winnes/all_games)
            final_probability = (100*probability)/((100 - probability)*(game_state["members"] - 1) + probability)

            self.probability = probability
            self.final_probability = final_probability
        else:
            probability = self.probability
            final_probability = self.final_probability

        return probability, final_probability

    def _get_card_multiply(self, distribution):
        card_multiply = 1

        for card in distribution:
            for i in range(len(self.card_suits)):
                if card[0] == self.card_suits[i]:
                    card_multiply = card_multiply * self.prime_numbers_suits[i]

        for card in distribution:
            for i in range(len(self.card_ns)):
                if card[1] == self.card_ns[i]:
                    card_multiply = card_multiply * self.prime_numbers_ns[i]

        return card_multiply

    def _is_Royal_Flush(self, distribution):
        rezult = False

        # sort distribution
        intermediate = None
        for i in range(len(distribution)):
            for j in range(len(distribution) - 1):
                if self.card_ns.index(distribution[j][1]) > self.card_ns.index(distribution[j + 1][1]):
                    intermediate = distribution[j]
                    distribution[j] = distribution[j + 1]
                    distribution[j + 1] = intermediate

        # determinate royal flush
        for i in range(3):
            if distribution[i][0] == distribution[i + 1][0]:
                if distribution[i + 1][0] == distribution[i + 2][0]:
                    if distribution[i + 2][0] == distribution[i + 3][0]:
                        if distribution[i + 3][0] == distribution[i + 4][0]:
                            if self.card_ns.index(distribution[i][1]) + 1 == self.card_ns.index(distribution[i + 1][1]):
                                if self.card_ns.index(distribution[i + 1][1]) + 1 == self.card_ns.index(distribution[i + 2][1]):
                                    if self.card_ns.index(distribution[i + 2][1]) + 1 == self.card_ns.index(
                                            distribution[i + 3][1]):
                                        if self.card_ns.index(distribution[i + 3][1]) + 1 == self.card_ns.index(
                                                distribution[i + 4][1]):
                                            if distribution[i + 4][1] == 'A':
                                                rezult = True
        return rezult

    def _is_Straight_Flush(self, distribution):
        rezult = False

        # sort distribution
        intermediate = None
        for i in range(len(distribution)):
            for j in range(len(distribution) - 1):
                if self.card_ns.index(distribution[j][1]) > self.card_ns.index(distribution[j + 1][1]):
                    intermediate = distribution[j]
                    distribution[j] = distribution[j + 1]
                    distribution[j + 1] = intermediate

        # determinate straight flush
        for i in range(3):
            if distribution[i][0] == distribution[i + 1][0]:
                if distribution[i + 1][0] == distribution[i + 2][0]:
                    if distribution[i + 2][0] == distribution[i + 3][0]:
                        if distribution[i + 3][0] == distribution[i + 4][0]:
                            if self.card_ns.index(distribution[i][1]) + 1 == self.card_ns.index(distribution[i + 1][1]):
                                if self.card_ns.index(distribution[i + 1][1]) + 1 == self.card_ns.index(distribution[i + 2][1]):
                                    if self.card_ns.index(distribution[i + 2][1]) + 1 == self.card_ns.index(
                                            distribution[i + 3][1]):
                                        if self.card_ns.index(distribution[i + 3][1]) + 1 == self.card_ns.index(
                                                distribution[i + 4][1]):
                                            rezult = True
        return rezult

    def _is_Kare(self, distribution):
        rezult = False

        card_multiply = self._get_card_multiply(distribution)

        kares = list()

        fourth_degrees = list()
        for prime_numbers in self.prime_numbers_ns:
            fourth_degrees.append(prime_numbers ** 4)

        for fourth_degree in fourth_degrees:
            if card_multiply % fourth_degree == 0:
                kares.append(int(fourth_degree ** (1 / 4)))

        if len(kares) >= 1:
            rezult = kares

        return rezult

    def _is_Full_House(self, distribution):
        rezult = False

        card_multiply = self._get_card_multiply(distribution)

        full_houses = list()

        full_house_multiplys = list()
        for prime_number_01 in self.prime_numbers_ns:
            for prime_number_02 in self.prime_numbers_ns:
                if prime_number_01 != prime_number_02:
                    full_house_multiplys.append(prime_number_01 ** 3 * prime_number_02 ** 2)

        for full_house_multiply in full_house_multiplys:
            if card_multiply % full_house_multiply == 0:
                full_houses.append(full_house_multiply)

        if len(full_houses) >= 1:
            rezult = full_houses

        return rezult

    def _is_Flush(self, distribution):
        rezult = False

        card_multiply = self._get_card_multiply(distribution)

        flushes = list()

        fifth_degrees = list()
        for prime_numbers_suit in self.prime_numbers_suits:
            fifth_degrees.append(prime_numbers_suit ** 5)

        for fifth_degree in fifth_degrees:
            if card_multiply % fifth_degree == 0:
                flushes.append(int(fifth_degree ** (1 / 5)))

        if len(flushes) >= 1:
            rezult = flushes

        return rezult

    def _is_Straight(self, distribution):
        rezult = False

        card_multiply = self._get_card_multiply(distribution)

        straightes = list()

        straight_samples = list()
        for i in range(9):
            straight_samples.append(self.prime_numbers_ns[i] *
                                    self.prime_numbers_ns[i + 1] *
                                    self.prime_numbers_ns[i + 2] *
                                    self.prime_numbers_ns[i + 3] *
                                    self.prime_numbers_ns[i + 4])

        for straight_sample in straight_samples:
            if card_multiply % straight_sample == 0:
                straightes.append(straight_sample)

        if len(straightes) >= 1:
            rezult = straightes

        return rezult

    def _is_Set(self, distribution):
        rezult = False

        card_multiply = self._get_card_multiply(distribution)

        sets = list()

        cubes = list()

        for prime_number in self.prime_numbers_ns:
            cubes.append(prime_number ** 3)

        for cube in cubes:
            if card_multiply % cube == 0:
                card_multiply = card_multiply // cube
                sets.append(int(cube ** (1 / 3)))

        if len(sets) >= 1:
            rezult = sets

        return rezult

    def _is_Two_Pairs(self, distribution):
        rezult = False

        card_multiply = self._get_card_multiply(distribution)

        pairs = list()

        squares = list()

        for prime_number in self.prime_numbers_ns:
            squares.append(prime_number ** 2)

        for square in squares:
            if card_multiply % square == 0:
                card_multiply = card_multiply // square
                pairs.append(int(square ** 0.5))

        if len(pairs) >= 2:
            rezult = pairs

        return rezult

    def _is_Pair(self, distribution):
        rezult = False

        card_multiply = self._get_card_multiply(distribution)

        pairs = list()

        squares = list()

        for prime_number in self.prime_numbers_ns:
            squares.append(prime_number ** 2)

        for square in squares:
            if card_multiply % square == 0:
                card_multiply = card_multiply // square
                pairs.append(int(square ** 0.5))

        if len(pairs) >= 1:
            rezult = pairs

        return rezult

    def _determinate_winner(self, distribution):

        player_hand_with_board = distribution["player_hand"] + distribution["board"]
        enemy_hand_with_board = distribution["enemy_hand"] + distribution["board"]

        winner = ""

        # Royar Flush treatment
        if winner == "":
            player = self._is_Royal_Flush(player_hand_with_board)
            enemy = self._is_Royal_Flush(enemy_hand_with_board)
            if player == True and enemy == False:
                winner = "player"
            if player == False and enemy == True:
                winner = "enemy"

        # Straight Flush treatment
        if winner == "":
            player = self._is_Straight_Flush(player_hand_with_board)
            enemy = self._is_Straight_Flush(enemy_hand_with_board)
            if player == True and enemy == False:
                winner = "player"
            if player == False and enemy == True:
                winner = "enemy"

        # Kare treatment
        if winner == "":
            player = self._is_Kare(player_hand_with_board)
            enemy = self._is_Kare(enemy_hand_with_board)
            if player != False and enemy == False:
                winner = "player"
            if player == False and enemy != False:
                winner = "enemy"

        # Full House treatment
        if winner == "":
            player = self._is_Full_House(player_hand_with_board)
            enemy = self._is_Full_House(enemy_hand_with_board)
            if player != False:
                if enemy != False:
                    if max(player) > max(enemy):
                        winner = "player"
                    if max(player) < max(enemy):
                        winner = "enemy"
                else:
                    winner = "player"
            else:
                if enemy != False:
                    winner = "enemy"

        # Flush treatment
        if winner == "":
            player = self._is_Flush(player_hand_with_board)
            enemy = self._is_Flush(enemy_hand_with_board)
            if player != False and enemy == False:
                winner = "player"
            if player == False and enemy != False:
                winner = "enemy"

        # Straight treatment
        if winner == "":
            player = self._is_Straight(player_hand_with_board)
            enemy = self._is_Straight(enemy_hand_with_board)
            if player != False:
                if enemy != False:
                    if max(player) > max(enemy):
                        winner = "player"
                    if max(player) < max(enemy):
                        winner = "enemy"

                    player = list()
                    player.append(self.card_ns.index(distribution["player_hand"][0][1]))
                    player.append(self.card_ns.index(distribution["player_hand"][1][1]))

                    enemy = list()
                    enemy.append(self.card_ns.index(distribution["enemy_hand"][0][1]))
                    enemy.append(self.card_ns.index(distribution["enemy_hand"][1][1]))

                    if max(player) > max(enemy):
                        winner = "player"
                    if max(player) < max(enemy):
                        winner = "enemy"
                else:
                    winner = "player"
            else:
                if enemy != False:
                    winner = "enemy"

        # Set treatment
        if winner == "":
            player = self._is_Set(player_hand_with_board)
            enemy = self._is_Set(enemy_hand_with_board)
            if player != False:
                if enemy != False:
                    if max(player) > max(enemy):
                        winner = "player"
                    if max(player) < max(enemy):
                        winner = "enemy"
                else:
                    winner = "player"
            else:
                if enemy != False:
                    winner = "enemy"

        # Two Pairs treatment
        if winner == "":
            player = self._is_Two_Pairs(player_hand_with_board)
            enemy = self._is_Two_Pairs(enemy_hand_with_board)
            if player != False:
                if enemy != False:
                    if max(player) > max(enemy):
                        winner = "player"
                    if max(player) < max(enemy):
                        winner = "enemy"
                else:
                    winner = "player"
            else:
                if enemy != False:
                    winner = "enemy"

        # Pair treatment
        if winner == "":
            player = self._is_Pair(player_hand_with_board)
            enemy = self._is_Pair(enemy_hand_with_board)
            if player != False:
                if enemy != False:
                    if max(player) > max(enemy):
                        winner = "player"
                    if max(player) < max(enemy):
                        winner = "enemy"
                else:
                    winner = "player"
            else:
                if enemy != False:
                    winner = "enemy"

        # Major Card treatment
        if winner == "":
            player = list()
            player.append(self.card_ns.index(distribution["player_hand"][0][1]))
            player.append(self.card_ns.index(distribution["player_hand"][1][1]))

            enemy = list()
            enemy.append(self.card_ns.index(distribution["enemy_hand"][0][1]))
            enemy.append(self.card_ns.index(distribution["enemy_hand"][1][1]))

            if max(player) > max(enemy):
                winner = "player"
            if max(player) < max(enemy):
                winner = "enemy"

        return winner

    def count_probability(self, distribution, time):

        winnes = 0
        loses = 0
        all_games = 0

        start_time = datetime.now()
        end_time = datetime.now()
        delta = end_time - start_time

        while delta.seconds < time:
            local_deck_copy = copy.deepcopy(self.CARD_DECK)
            local_distribution_copy = copy.deepcopy(distribution)

            while len(local_distribution_copy["player_hand"]) < 2:
                adding_card = random.choice(local_deck_copy)
                local_distribution_copy["player_hand"].append(adding_card)
                local_deck_copy.remove(adding_card)

            while len(local_distribution_copy["enemy_hand"]) < 2:
                adding_card = random.choice(local_deck_copy)
                local_distribution_copy["enemy_hand"].append(adding_card)
                local_deck_copy.remove(adding_card)

            while len(local_distribution_copy["board"]) < 5:
                adding_card = random.choice(local_deck_copy)
                local_distribution_copy["board"].append(adding_card)
                local_deck_copy.remove(adding_card)

            winner = self._determinate_winner(local_distribution_copy)

            all_games += 1
            if winner == "player":
                winnes += 1
            elif winner == "enemy":
                loses += 1

            end_time = datetime.now()
            delta = end_time - start_time

        return all_games, winnes, loses
