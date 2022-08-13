# Jim Moriarty
Program for determining the win probability in Poker

## Project architecture
WATCHER -> RECOGNIZER -> PROBABILIST -> DECIDER -> NOTIFYER

### Watcher
Do screenshot

![Иллюстрация к проекту](https://github.com/hnedenko/Jim-Moriarty/blob/main/a_watcher/screenshot.png)

### Recognizer
Cut screenshot.
Get player cards, board cards, enemy's card images.
Reading player cards recognize game state.
Convert player cards, board cards, enemy's card images to digital format.

![Иллюстрация к проекту](https://github.com/hnedenko/Jim-Moriarty/blob/main/b_recognizer/cards/10_grey.jpg)
![Иллюстрация к проекту](https://github.com/hnedenko/Jim-Moriarty/blob/main/b_recognizer/cards/K_red.jpg)

### Probabilist
Using digital player cards and board cards count win probability (Monte Carlo method) when playing pvp (RMS = 8).
Using pvp probability end info about enemies number count final win probability.

### Decider
Unrealized module.
Should make the final decision in the current situation of the game, using all getted info.

### Notifyer
Visualizes current game state, player cards, board cards, enemies number,  win probability when playing pvp, final win probability.

![Иллюстрация к проекту](https://github.com/hnedenko/Jim-Moriarty/blob/main/screen.png)

## Testing
The program does its job - count win probability - quite well.
Average analysis time for one situation - 1 sec.
Playing poker considering only win probability and bank leads to a loss of 7.9% per minute.

The supposed reason - that the leadership in poker is not only and not so much a mathematical component, but also a psychological one.
