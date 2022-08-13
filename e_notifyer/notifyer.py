import pygame
from support import RGB


class Notifyer:

    def __init__(self):
        self.folder = 'e_notifyer'
        self.card_size = (43, 47)

    def show_final_probability(self, screen, final_probability):
        # tuning text
        font = pygame.font.Font(self.folder + "/arkhip.ttf", 75)
        font.set_bold(True)
        text = font.render(str(int(final_probability)) + "%",
                           True,
                           RGB.DARC_BROWN)
        text_width = text.get_rect()[2]
        text_height = text.get_rect()[3]

        # show parchment
        image = pygame.image.load(self.folder + '/parchment.png').convert_alpha()
        scaled_image = pygame.transform.scale(image, (text_width + 60, 125))
        screen.blit(scaled_image, (360 - (text_width + 60)/2, 20))

        # show text
        screen.blit(text, (360 - text_width/2, 85 - text_height/2))

    def show_cards(self, screen, game_state):
        # show parchment to hand
        image = pygame.image.load(self.folder + '/parchment.png').convert_alpha()
        hand_parchment_width = 30 + 2 * self.card_size[0] + 20 + 30
        hand_scaled_image = pygame.transform.scale(image, (hand_parchment_width, 80))
        screen.blit(hand_scaled_image, (10, 160))

        # show hand cards
        image_hand_1 = pygame.image.load(self.folder + '/cards/' + str(game_state["hand"][0])).convert_alpha()
        image_hand_2 = pygame.image.load(self.folder + '/cards/' + str(game_state["hand"][1])).convert_alpha()
        screen.blit(image_hand_1, (20 + self.card_size[0]/2, 225 - self.card_size[1]))
        screen.blit(image_hand_2, (20 + self.card_size[0] + 40, 225 - self.card_size[1]))

        # show parchment to board
        n_board_cards = 5
        for card in game_state["board"]:
            if card == "0.jpg":
                n_board_cards -= 1
        board_parchment_width = 40 + n_board_cards * self.card_size[0] + (n_board_cards - 1) * 20 + 30
        board_scaled_image = pygame.transform.scale(image, (board_parchment_width, 80))
        screen.blit(board_scaled_image, (720 - (10 + board_parchment_width + 10), 160))

        # show board card
        left_card_frame = 720 - board_parchment_width + 10
        for i in range(n_board_cards):
            card_image = pygame.image.load(self.folder + '/cards/' + str(game_state["board"][i])).convert_alpha()
            screen.blit(card_image, (left_card_frame + i * self.card_size[0] + i * 20, 225 - self.card_size[1]))

    def show_n_members_and_p2p_probability(self, screen, n_members, probability):
        # tuning text
        font = pygame.font.Font(self.folder + "/arkhip.ttf", 45)
        font.set_bold(True)
        text = font.render(n_members*"O" + " - " + str(int(probability)) + "%",
                           True,
                           RGB.DARC_BROWN)
        text_width = text.get_rect()[2]
        text_height = text.get_rect()[3]

        # show parchment
        image = pygame.image.load(self.folder + '/parchment.png').convert_alpha()
        scaled_image = pygame.transform.scale(image, (text_width + 60, 80))
        screen.blit(scaled_image, (360 - (text_width + 60) / 2, 260))

        # show text
        screen.blit(text, (360 - text_width / 2, 310 - text_height / 2))

    def show_state(self, screen, game_state, probability, final_probability):
        self.show_final_probability(screen, final_probability)
        self.show_cards(screen, game_state)
        n_members = game_state["members"]
        self.show_n_members_and_p2p_probability(screen, n_members, probability)

    def show_not_in_game(self, screen):
        parchment_image = pygame.image.load(self.folder + '/parchment.png').convert_alpha()
        scaled_parchment_image = pygame.transform.scale(parchment_image, (700, 340))
        screen.blit(scaled_parchment_image, (10, 10))

        font = pygame.font.Font(self.folder + "/arkhip.ttf", 72)
        text_not_in_game = font.render('НЕ В ИГРЕ', True, RGB.DARC_BROWN)
        rect = text_not_in_game.get_rect()
        screen.blit(text_not_in_game, (360 - rect[2]/2, 180 - rect[3]/2))
