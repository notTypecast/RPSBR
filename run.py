from src.Game import Game
from src.ObjectType import ObjectType
from random import randint

width, height = 800, 800

game = Game(width, height)

for i in range(10):
    game.addGameObject(ObjectType.ROCK, (randint(0, width), randint(0, height)))
    game.addGameObject(ObjectType.PAPER, (randint(0, width), randint(0, height)))
    game.addGameObject(ObjectType.SCISSORS, (randint(0, width), randint(0, height)))


game.gameLoop()
