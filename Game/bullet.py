"""Projectiles, their movement, and wall rebounds."""
import config
import pygame
import math
import random


# class Bullet is a child of the Sprite class from pygame
class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, direction, radius=None):
        super().__init__()

        self.radius = config.bullet_size if radius is None else radius
        self.direction = direction
        self.speed = 7
        self._velocity_key = None
        # updating the x and y position to fit the circles
        diameter = round(self.radius * 2)
        self.rect = pygame.Rect(0, 0, diameter, diameter)
        self.rect.center = (x, y)

    def _move(self):
        # updating the bullet's position based on the speed and the direction
        # (x, y) --> (cos, sin)
        key = (self.speed, self.direction)
        if key != self._velocity_key:
            self._velocity_key = key
            self._velocity = (int(self.speed * math.cos(self.direction)),
                              int(self.speed * math.sin(self.direction)))
        self.rect.move_ip(self._velocity)

    def update(self):
        self._move()

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
        self.color = config.red
        self.speed = 7
        self.damage = 5


class shotgun(Bullet):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.color = config.blue
        self.speed = 7
        self.damage = 20


class machinegun(Bullet):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.color = config.green
        self.speed = 7
        self.damage = 9


class bouncing(Bullet):
    def __init__(self, x, y, direction):
        direction = random.uniform(0, 2 * math.pi)
        super().__init__(x, y, direction)
        self.color = config.pink
        self.speed = 7
        self.damage = 15
        self.bounce_count = 2

    def update(self):
        self._move()
        if self.rect.left < 0 or self.rect.right > config.width:
            self.rect.x = max(0, min(self.rect.x, config.width - self.rect.width))
            self.direction = math.pi - self.direction
            self.bounce_count -= 1
        if self.rect.top < 0 or self.rect.bottom > config.height:
            self.rect.y = max(0, min(self.rect.y, config.height - self.rect.height))
            self.direction = -self.direction
            self.bounce_count -= 1
        if self.bounce_count <= 0:
            self.kill()


class sniper(Bullet):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.color = config.glowing_yellow
        self.speed = 15
        self.damage = 25


class pet_bullet(Bullet):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction, radius=6.5)
        self.color = config.yellow
        self.speed = 8
        self.damage = 10


class enemy_bullet(Bullet):
    def __init__(self, x, y, direction, shooter=None):
        super().__init__(x, y, direction, radius=10)
        self.color = config.dark_red
        self.speed = 5
        self.shooter = shooter
        self.damage = 15
        self.is_enemy_bullet = True  # Mark as an enemy bullet
