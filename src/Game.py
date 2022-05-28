import pygame
from src.GameObject import GameObject
from src.ObjectType import ObjectType
from math import acos, sqrt, sin, cos, pi, floor


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

        GameObject.mass_by_type[ObjectType.ROCK] = 4
        GameObject.mass_by_type[ObjectType.PAPER] = 1
        GameObject.mass_by_type[ObjectType.SCISSORS] = 2

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
                    ### change speed based on collision ###

                    # masses of objects
                    m1 = GameObject.mass_by_type[game_object.object_type]
                    m2 = GameObject.mass_by_type[game_object_2.object_type]
                    # speeds of objects
                    v1 = game_object.speed
                    v2 = game_object_2.speed
                    # centers of objects
                    x1 = (game_object.pos[0] + GameObject.image_dimensions[0]/2,
                          game_object.pos[1] + GameObject.image_dimensions[1]/2)
                    x2 = (game_object_2.pos[0] + GameObject.image_dimensions[0]/2,
                          game_object_2.pos[1] + GameObject.image_dimensions[1]/2)

                    dx1x2 = (x1[0] - x2[0], x1[1] - x2[1])
                    dx2x1 = (x2[0] - x1[0], x2[1] - x1[1])

                    dv1v2 = (v1[0] - v2[0], v1[1] - v2[1])
                    dv2v1 = (v2[0] - v1[0], v2[1] - v1[1])

                    v1_sclr = 2*m2/(m1+m2)*(dv1v2[0]*dx1x2[0] + dv1v2[1]*dx1x2[1])/(dx1x2[0]**2 + dx1x2[1]**2)
                    v1_new = (v1[0] - v1_sclr*dx1x2[0], v1[1] - v1_sclr*dx1x2[1])

                    v2_sclr = 2*m1/(m1+m2)*(dv2v1[0]*dx2x1[0] + dv2v1[1]*dx2x1[1])/(dx2x1[0]**2 + dx2x1[1]**2)
                    v2_new = (v2[0] - v2_sclr*dx2x1[0], v2[1] - v2_sclr*dx2x1[1])

                    game_object.speed = v1_new
                    game_object_2.speed = v2_new

                    #######################################

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
                    if event.key == pygame.K_p:
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
