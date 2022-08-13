from PIL import Image
from support import CARD_FRAMES as CF
import os


class Recognizer:

    def __init__(self):
        self.folder_card_samples = 'b_recognizer/cards'
        self.cuted_screens = 'b_recognizer/cuted_screens'

    def recognize_game_state(self, screen, is_saving_cuted):
        # crop input screen and init output dict
        game_state = dict()
        game_state["status"] = True
        h_01 = screen.crop(CF.HAND_01)
        h_02 = screen.crop(CF.HAND_02)
        b_01 = screen.crop(CF.BOARD_01)
        b_02 = screen.crop(CF.BOARD_02)
        b_03 = screen.crop(CF.BOARD_03)
        b_04 = screen.crop(CF.BOARD_04)
        b_05 = screen.crop(CF.BOARD_05)
        e_02 = screen.crop(CF.ENEMY_02)
        e_03 = screen.crop(CF.ENEMY_03)
        e_04 = screen.crop(CF.ENEMY_04)
        e_05 = screen.crop(CF.ENEMY_05)
        e_06 = screen.crop(CF.ENEMY_06)
        game_state["hand"] = [h_01, h_02]
        game_state["board"] = [b_01, b_02, b_03, b_04, b_05]
        game_state["members"] = [e_02, e_03, e_04, e_05, e_06]

        # save cuted cards to files
        if is_saving_cuted:
            h_01.save(self.cuted_screens + "/hand_01.jpg")
            h_02.save(self.cuted_screens + "/hand_02.jpg")
            b_01.save(self.cuted_screens + "/board_01.jpg")
            b_02.save(self.cuted_screens + "/board_02.jpg")
            b_03.save(self.cuted_screens + "/board_03.jpg")
            b_04.save(self.cuted_screens + "/board_04.jpg")
            b_05.save(self.cuted_screens + "/board_05.jpg")

            e_02.save(self.cuted_screens + "/enemy_02.jpg")
            e_03.save(self.cuted_screens + "/enemy_03.jpg")
            e_04.save(self.cuted_screens + "/enemy_04.jpg")
            e_05.save(self.cuted_screens + "/enemy_05.jpg")
            e_06.save(self.cuted_screens + "/enemy_06.jpg")

        # load card samples
        card_samples = dict()
        card_samples_names = os.listdir(self.folder_card_samples)
        for name in card_samples_names:
            card_samples[name] = Image.open(self.folder_card_samples + "/" + name)

        # load enemy_in_game sample
        enemy_in_game = Image.open('b_recognizer/enemy_in_game.jpg')

        # recognize hand_01 card
        for name in card_samples_names:
            distance = self._get_distance_between_images(card_samples[name], game_state["hand"][0])
            if distance < 1500:
                game_state["hand"][0] = name

        # recognize hand_02 card
        for name in card_samples_names:
            distance = self._get_distance_between_images(card_samples[name], game_state["hand"][1])
            if distance < 1500:
                game_state["hand"][1] = name

        # recognize board_01 card
        for name in card_samples_names:
            distance = self._get_distance_between_images(card_samples[name], game_state["board"][0])
            if distance < 1500:
                game_state["board"][0] = name

        # recognize board_02 card
        for name in card_samples_names:
            distance = self._get_distance_between_images(card_samples[name], game_state["board"][1])
            if distance < 1500:
                game_state["board"][1] = name

        # recognize board_03 card
        for name in card_samples_names:
            distance = self._get_distance_between_images(card_samples[name], game_state["board"][2])
            if distance < 1500:
                game_state["board"][2] = name

        # recognize board_04 card
        for name in card_samples_names:
            distance = self._get_distance_between_images(card_samples[name], game_state["board"][3])
            if distance < 1500:
                game_state["board"][3] = name

        # recognize board_05 card
        for name in card_samples_names:
            distance = self._get_distance_between_images(card_samples[name], game_state["board"][4])
            if distance < 1500:
                game_state["board"][4] = name

        # recognize enemy_02 status
        distance = self._get_distance_between_images(enemy_in_game, game_state["members"][0])
        if distance < 1500:
            game_state["members"][0] = 1
        else:
            game_state["members"][0] = 0

        # recognize enemy_03 status
        distance = self._get_distance_between_images(enemy_in_game, game_state["members"][1])
        if distance < 1500:
            game_state["members"][1] = 1
        else:
            game_state["members"][1] = 0

        # recognize enemy_04 status
        distance = self._get_distance_between_images(enemy_in_game, game_state["members"][2])
        if distance < 1500:
            game_state["members"][2] = 1
        else:
            game_state["members"][2] = 0

        # recognize enemy_05 status
        distance = self._get_distance_between_images(enemy_in_game, game_state["members"][3])
        if distance < 1500:
            game_state["members"][3] = 1
        else:
            game_state["members"][3] = 0

        # recognize enemy_06 status
        distance = self._get_distance_between_images(enemy_in_game, game_state["members"][4])
        if distance < 1500:
            game_state["members"][4] = 1
        else:
            game_state["members"][4] = 0

        # set non-recognizer card to output dict
        if type(game_state["hand"][0]) != str:
            game_state["hand"][0] = None
        if type(game_state["hand"][1]) != str:
            game_state["hand"][1] = None
        if type(game_state["board"][0]) != str:
            game_state["board"][0] = None
        if type(game_state["board"][1]) != str:
            game_state["board"][1] = None
        if type(game_state["board"][2]) != str:
            game_state["board"][2] = None
        if type(game_state["board"][3]) != str:
            game_state["board"][3] = None
        if type(game_state["board"][4]) != str:
            game_state["board"][4] = None

        # recognize game status
        if (game_state["hand"][0] == "0.jpg")\
                or (game_state["hand"][0] is None)\
                or (game_state["hand"][1] == "0.jpg")\
                or (game_state["hand"][1] is None)\
                or (game_state["board"][0] is None)\
                or (game_state["board"][1] is None)\
                or (game_state["board"][2] is None)\
                or (game_state["board"][3] is None)\
                or (game_state["board"][4] is None):
            game_state["status"] = False

        # count N memberss
        game_state["members"] = sum(game_state["members"]) + 1

        return game_state

    def _get_distance_between_images(self, image_01, image_02):
        rezult = 0
        if type(image_01) != str and type(image_02) != str:
            width, height = image_01.size

            pixel_image_01 = image_01.load()
            pixel_image_02 = image_02.load()

            summ = 0
            for x in range(width):
                for y in range(height):
                    summ += (pixel_image_01[x, y][0] - pixel_image_02[x, y][0]) ** 2
                    summ += (pixel_image_01[x, y][1] - pixel_image_02[x, y][1]) ** 2
                    summ += (pixel_image_01[x, y][2] - pixel_image_02[x, y][2]) ** 2
            rezult = summ ** 0.5
        else:
            rezult = 2 ** (86 + 60)
        return rezult

    def generate_cards(self, screen):
        # cut cards from screen
        read_cards = list()
        read_cards.append(screen.crop(CF.HAND_01))
        read_cards.append(screen.crop(CF.HAND_01))
        read_cards.append(screen.crop(CF.HAND_02))
        read_cards.append(screen.crop(CF.BOARD_01))
        read_cards.append(screen.crop(CF.BOARD_02))
        read_cards.append(screen.crop(CF.BOARD_03))
        read_cards.append(screen.crop(CF.BOARD_04))
        read_cards.append(screen.crop(CF.BOARD_05))

        # read saved sample cards
        card_samples = list()
        card_samples_names = os.listdir(self.folder_card_samples)
        for name in card_samples_names:
            card_samples.append(Image.open(self.folder_card_samples + "/" + name))
        counter = len(card_samples_names)

        # compare read cards and sample
        for read_image in read_cards:
            distances = list()
            for sample_image in card_samples:
                distances.append(self._get_distance_between_images(read_image, sample_image))
            min_dist = min(distances)
            if min_dist > 1500:
                read_image.save(self.folder_card_samples + "/" + str(counter) + ".jpg")
                counter += 1
