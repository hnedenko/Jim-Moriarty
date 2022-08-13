import pygame
import sys
from support import RGB
from a_watcher import watcher
from b_recognizer import recognizer
from c_probabilist import probabilist
from d_decider import decider
from e_notifyer import notifyer

pygame.init()

FPS = 1

"♥ ♠ ♦ ♣"

screen = pygame.display.set_mode((720, 360))

# Create all modules
watcher = watcher.Watcher()
recognizer = recognizer.Recognizer()
probabilist = probabilist.Probabilist()
decider = decider.Decider()
notifyer = notifyer.Notifyer()

while True:
    # Redraw display
    screen.fill(RGB.PARCHMENT)
    pygame.time.Clock().tick(FPS)

    # Watcher (getting screens)
    screenshot = watcher.get_screen()

    # Recognizer (getting digital cards) + Notifyer (visualization)
    game_state = recognizer.recognize_game_state(screenshot, True)
    # recognizer.generate_cards(screenshot)
    if game_state["status"]:

        # Probabilist (getting win probability)
        probability, final_probability = probabilist.get_win_probability(game_state)

        # Decider (getting ordered recommendations)
        recommendation = decider.get_recommendations(probability)

        # Notifyer(visualization)
        notifyer.show_state(screen, game_state, probability, final_probability)
    else:
        # Notifyer (show not in game UI)
        notifyer.show_not_in_game(screen)

    # Main loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Redraw display
    pygame.display.flip()
