import pygame
import math
from pygame import Vector2
from random import randint


class Entity(pygame.sprite.Sprite):
    def __init__(self, type, screenWidht, screenHeight, size, random: bool):
        super().__init__()
        if random:
            self.random_location = (randint(0, screenWidht), randint(0, screenHeight))
        else:
            # to set newbie entities location after one is caught
            self.random_location = (screenWidht, screenHeight)

        self.screenWidht = screenWidht
        self.screenHeight = screenHeight
        if type == 'Rock':
            self.image = pygame.image.load("graphics/the rock original.gif")
        if type == 'Paper':
            self.image = pygame.image.load("graphics/paper no backgorund.png")
        if type == 'Scissor':
            self.image = pygame.image.load("graphics/scissor no backgorund.png")

        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center=self.random_location)
        self.vector = Vector2(self.rect.x, self.rect.y)

    def distance(self, other):
        return (self.vector - other.vector).length()

    def check_window_collisions(self):
        if self.rect.right >= self.screenWidht: self.rect.right = self.screenWidht
        if self.rect.left <= 0: self.rect.left = 0
        if self.rect.top <= 0: self.rect.top = 0
        if self.rect.bottom >= self.screenHeight: self.rect.bottom = self.screenHeight

    def get_closest_target(self, other):
        closest_target = None
        closeset_distance = None

        for current_target in other:
            current_distance = self.distance(current_target)
            if closeset_distance is None or current_distance < closeset_distance:
                closeset_distance = current_distance
                closest_target = current_target

        return (closest_target, closeset_distance)

    def move(self, targets, chasers, chase_speed_multiplier, escape_speed_multiplier):
        if len(targets) != 0:
            self.target_direction = (self.get_closest_target(targets)[0].vector - self.vector)

            self.target_direction.normalize_ip()
            self.vector += self.target_direction * chase_speed_multiplier

        if len(chasers) != 0:
            self.closest = self.get_closest_target(chasers)

            if self.closest[1] <= 250:
                self.away_direction = self.closest[0].vector - self.vector
                self.away_direction.normalize_ip()
                self.vector -= self.away_direction * escape_speed_multiplier

        self.rect.x = self.vector.x
        self.rect.y = self.vector.y

        self.check_window_collisions()

    def update(self):
        pass
