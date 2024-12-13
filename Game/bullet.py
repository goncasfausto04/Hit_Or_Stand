# sprit -> everything that is appearing in 2D

from config import *
import config
import pygame
import math


# class Bullet is a child of the Sprite class from pygame
class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, direction):
        super().__init__()

        self.radius = bullet_size
        self.direction = direction
        self.speed = 7
        # updating the x and y position to fit the circles
        self.rect = pygame.Rect(
            x - self.radius, y - self.radius, self.radius * 2, self.radius * 2
        )

    def update(self):

        # updating the bullet's position based on the speed and the direction
        # (x, y) --> (cos, sin)
        self.rect.x += int(self.speed * math.cos(self.direction))
        self.rect.y += int(self.speed * math.sin(self.direction))

        # killing the bullet if it goes off screen
        if (
            self.rect.x < 0
            or self.rect.x > config.width
            or self.rect.y < 0
            or self.rect.y > config.height
        ):
            self.kill()

    def draw(self, screen):
        # drawing the bullet on the screen
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)


# creating 3 different types of bullets
class pistol(Bullet):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.color = red
        self.speed = 7


class shotgun(Bullet):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.color = blue
        self.speed = 7


class machinegun(Bullet):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.color = green
        self.speed = 7


class pet_bullet(Bullet):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.color = yellow
        self.speed = 8
        self.radius = 6.5
class enemy_bullet(Bullet):
    def __init__(self, x, y, direction, shooter=None):
        super().__init__(x, y, direction)
        self.color = dark_red
        self.speed = 5
        self.radius = 10
        self.shooter = shooter
        self.damage = 15
        self.is_enemy_bullet = True  # Mark as an enemy bullet