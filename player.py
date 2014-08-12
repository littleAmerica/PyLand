# -*- coding: utf-8 -*-
__author__ = 'matanaliz'

from weapon import *
from event import *


class Player(pygame.sprite.Sprite):

    SPEED = 3.5

    def __init__(self, group, bound):
        pygame.sprite.Sprite.__init__(self, group)

        self.weapon = Shotgun(self, group)

        self.size = (32, 32)
        self.image = pygame.Surface(self.size)
        self.rect = pygame.Rect(bound.width / 2, bound.height / 2, *self.size)
        self.image.fill(pygame.Color("#00ffff"))
        self.vector = (0, 0)

        self.bound = bound

        self.event_dispatcher = 0

    def set_event_dispatcher(self, event_dispatcher):
        assert isinstance(event_dispatcher, EventDispatcher)
        self.event_dispatcher = event_dispatcher

        #Setting dispatcher for weapon
        self.weapon.set_event_dispatcher(event_dispatcher)


    def update(self):
        #TODO: Change for action map
        keys = pygame.key.get_pressed()
        vector = [0, 0]
        if keys[pygame.K_LEFT]:
            vector[0] = -1
        if keys[pygame.K_RIGHT]:
            vector[0] = 1
        if keys[pygame.K_UP]:
            vector[1] = -1
        if keys[pygame.K_DOWN]:
            vector[1] = 1

        #Tick for gun
        self.weapon.tick()

        mouse_key = pygame.mouse.get_pressed()
        if mouse_key == (1, 0, 0):
            mouse_pos = pygame.mouse.get_pos()
            self.weapon.fire(mouse_pos)

        self.rect.move_ip(*[x * self.SPEED for x in vector])
        self.rect.clamp_ip(self.bound)