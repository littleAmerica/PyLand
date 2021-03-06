# -*- coding: utf-8 -*-
__author__ = 'matanaliz'

from weapon import *
from event import *
from common import *


class Player(pygame.sprite.Sprite):
    """
    Player class. I think it's self explaining.
    """
    MIN_SPEED = 2.5
    MAX_SPEED = 3.5
    ACCELERATION = 0.1
    MAX_HEALTH = 100

    def __init__(self, bound):
        pygame.sprite.Sprite.__init__(self)

        #Sprite init
        self.size = (32, 32)

        #Transparent surface
        self.image = pygame.Surface(self.size, pygame.SRCALPHA, 32)
        self.image.convert_alpha()

        pygame.draw.rect(self.image, pygame.Color("#00ffff"), pygame.Rect(0, 0, 32, 24))
        #Saving base image for rotation
        self.base_image = self.image

        self.rect = pygame.Rect(bound.width / 2, bound.height / 2, *self.size)

        self.speed = 0
        self.vector = [0, 0]
        self.bound = bound

        #Event dispatcher
        self.event_dispatcher = 0

        #Health init
        self.curr_health = self.MAX_HEALTH

        self.weapon = 0

    def give_weapon(self, weapon):
        assert isinstance(weapon, Weapon)
        self.weapon = weapon

    def set_event_dispatcher(self, event_dispatcher):
        """
        Setting event dispatcher
        :param event_dispatcher: Dispatcher object
        """
        assert isinstance(event_dispatcher, EventDispatcher)
        self.event_dispatcher = event_dispatcher

        #Setting dispatcher for weapon
        self.weapon.set_event_dispatcher(event_dispatcher)

    def update(self):
        """
        Update player state each frame

        """

        #TODO: Change for action map
        #Ugly code. Should move to base class for enemies and player.
        keys = pygame.key.get_pressed()
        vector = [0, 0]
        key_was_pressed = False
        if keys[pygame.K_LEFT]:
            vector[0] = -1
            key_was_pressed = True
        if keys[pygame.K_RIGHT]:
            vector[0] = 1
            key_was_pressed = True
        if keys[pygame.K_UP]:
            vector[1] = -1
            key_was_pressed = True
        if keys[pygame.K_DOWN]:
            vector[1] = 1
            key_was_pressed = True

        #Tick for gun
        self.weapon.tick()

        #Rotating player to face cursor
        mouse_pos = pygame.mouse.get_pos()
        self.__rotate(angle(normalize(sub(self.rect.center, mouse_pos))))

        mouse_key = pygame.mouse.get_pressed()
        if mouse_key == (1, 0, 0):
            if self.weapon:
                self.weapon.fire(mouse_pos)

        self.__apply_acceleration(key_was_pressed)

        if key_was_pressed:
            self.vector = vector
            self.rect.move_ip(*[x * self.speed for x in vector])
        else:
            self.rect.move_ip(*[x * self.speed for x in self.vector])
        self.rect.clamp_ip(self.bound)

    def apply_damage(self, damage):
        """
        Applying damage to player and checks if it's dead
        :param damage:
        :return: If player dead
        """
        if self.curr_health > damage:
            self.curr_health -= damage
            #Dispatch event to health bar
            if self.event_dispatcher:
                self.event_dispatcher.dispatch_event(GameEvent(GameEvent.DAMAGE_GOT, self))
            return False
        else:
            return True

    def __rotate(self, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = self.rect
        self.image = pygame.transform.rotate(self.base_image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = orig_rect.center

    def __apply_acceleration(self, key_was_pressed):
        if key_was_pressed:
            if self.speed < self.MAX_SPEED:
                self.speed += self.ACCELERATION
        else:
            if self.speed > 0:
                self.speed -= self.ACCELERATION