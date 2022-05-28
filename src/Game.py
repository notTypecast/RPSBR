import pygame
from src.GameObject import GameObject
from src.ObjectType import ObjectType


class Game:

    beats = {ObjectType.ROCK: ObjectType.SCISSORS, ObjectType.PAPER: ObjectType.ROCK, ObjectType.SCISSORS: ObjectType.PAPER}

    def __init__(self, width, height, hitboxes=False):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))

        self.game_objects = []

        GameObject.images[ObjectType.ROCK] = pygame.image.load("img/rock.png")
        GameObject.images[ObjectType.PAPER] = pygame.image.load("img/paper.png")
        GameObject.images[ObjectType.SCISSORS] = pygame.image.load("img/scissors.png")

        GameObject.mass_by_type[ObjectType.ROCK] = 15
        GameObject.mass_by_type[ObjectType.PAPER] = 1
        GameObject.mass_by_type[ObjectType.SCISSORS] = 4

        GameObject.screen_dimensions = (width, height)

        self.running = True
        self.clock = pygame.time.Clock()
        self.hitboxes = hitboxes

    def calculateNext(self):
        for game_object in self.game_objects:
            for game_object_2 in self.game_objects:
                if game_object is game_object_2:
                    continue
                if Game.rangeOverlap(game_object.xrange(), game_object_2.xrange()) and \
                        Game.rangeOverlap(game_object.yrange(), game_object_2.yrange()):
                    # TODO change speed based on collision
                    # change object type if types are different
                    if game_object.object_type is not game_object_2.object_type:
                        if Game.beats[game_object.object_type] is game_object_2.object_type:
                            game_object_2.object_type = game_object.object_type
                        else:
                            game_object.object_type = game_object_2.object_type
                    break

            game_object.nextMove()

    def gameLoop(self):

        paused = False

        while self.running:
            if not paused:
                self.calculateNext()

                self.screen.fill((0, 0, 0))

                for game_object in self.game_objects:
                    self.screen.blit(GameObject.images[game_object.object_type],
                                     (game_object.pos[0], game_object.pos[1]))

                    if self.hitboxes:
                        pygame.draw.rect(self.screen, (255, 0, 0), (game_object.pos[0], game_object.pos[1],
                                                                    GameObject.image_dimensions[0],
                                                                    GameObject.image_dimensions[1]), width=1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    paused ^= 1

            self.clock.tick(30)

            pygame.display.flip()

    def addGameObject(self, object_type, pos):
        if type(object_type) is not ObjectType:
            raise ValueError("object type should be of type Game.ObjectType")

        if type(pos) is not tuple or len(pos) != 2:
            raise ValueError("invalid coordinate")

        self.game_objects.append(GameObject(object_type, pos))

    @staticmethod
    def rangeOverlap(r1, r2):
        return r1[0] <= r2[1] and r2[0] <= r1[1]
