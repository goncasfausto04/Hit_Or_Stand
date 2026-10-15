"""Enemy types with shared animation frames."""
from functools import lru_cache
import math
import os
import random

import pygame

import config
from assets import load_image
from bullet import enemy_bullet


@lru_cache(maxsize=8)
def _animation_frames(folder, pattern, count, size):
    path = os.path.join(config.base_path, "extras", "sprite", folder)
    return tuple(load_image(os.path.join(path, pattern.format(i)), size)
                 for i in range(count))


class Enemy(pygame.sprite.Sprite):
    animation_folder = None
    animation_pattern = "tile00{}.png"
    animation_count = 0
    animation_scale = None
    draw_offset = (0, 0)

    def __init__(self):
        super().__init__()
        self.health = 10
        self.speed = random.randint(3, 4)
        self.damage = 15
        self.rect = pygame.Rect((0, 0), config.enemy_size)
        self.rect.x = random.randint(0, config.width - self.rect.width)
        self.rect.y = random.randint(0, config.height - self.rect.height)
        self.frame_count = 0
        self.fps_counter = 0

        if self.animation_folder is not None:
            size = None
            if self.animation_scale is not None:
                size = tuple(int(dimension * scale) for dimension, scale in
                             zip(config.enemy_size, self.animation_scale))
            self.sprites = _animation_frames(self.animation_folder,
                                            self.animation_pattern,
                                            self.animation_count, size)
            self.image = self.sprites[0]
        else:
            self.sprites = ()
            self.image = pygame.Surface(config.enemy_size)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x + self.draw_offset[0],
                                 self.rect.y + self.draw_offset[1]))

    def update(self, player):
        self.move_towards_player(player)
        self.fps_counter += 1
        if self.sprites and self.fps_counter % 5 == 0:
            self.frame_count = (self.frame_count + 1) % len(self.sprites)
            self.image = self.sprites[self.frame_count]

    def move_towards_player(self, player):
        if not self.speed:
            return
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = max(1, math.hypot(dx, dy))
        self.rect.move_ip(int(self.speed * dx / distance),
                          int(self.speed * dy / distance))


class initialEnemy(Enemy):
    animation_folder = "initialenemy"
    animation_count = 5
    draw_offset = (-15, -17)

    def __init__(self):
        super().__init__()
        self.speed = 2
        self.damage = 10


class fastEnemy(Enemy):
    animation_folder = "fastEnemy"
    animation_pattern = "slime-move-{}.png"
    animation_count = 4
    animation_scale = (2, 2)
    draw_offset = (-15, -27)

    def __init__(self):
        super().__init__()
        self.health = 7


class TankMonster(Enemy):
    animation_folder = "TankMonster"
    animation_count = 8
    animation_scale = (4.5, 3)
    draw_offset = (-55, -25)

    def __init__(self):
        super().__init__()
        self.health = 30
        self.speed = 2
        self.damage = 10
        self.rect.height = int(self.rect.height * 2.1)


class RangedMonster(Enemy):
    animation_folder = "RangedMonster"
    animation_count = 4
    animation_scale = (2, 2)
    draw_offset = (-15, -17)

    def __init__(self):
        super().__init__()
        self.health = 20
        self.speed = 0
        self.damage = 10
        self.bullet_cooldown = 0
        self.bullet_type = enemy_bullet
        self.fire_rate = 70

    def enemy_shoot(self, bullets):
        if self.bullet_cooldown <= 0:
            for _ in range(2):
                angle = random.uniform(0, 2 * math.pi)
                bullets.add(self.bullet_type(self.rect.centerx, self.rect.centery,
                                             angle, self))
            self.bullet_cooldown = self.fire_rate
        self.bullet_cooldown -= 1


class DuplicateMonster(Enemy):
    animation_folder = "initialenemy"
    animation_count = 5
    animation_scale = (2.5, 2.5)
    draw_offset = (-12, -25)

    def __init__(self):
        super().__init__()
        self.health = 30
        self.speed = 2
        self.damage = 10
        self.rect.width = int(self.rect.width * 1.8)
        self.rect.height = int(self.rect.height * 1.3)

    def spawn_on_death(self, enemies_group):
        """Add and return the two children so collision indexes can track them."""
        children = []
        for _ in range(2):
            enemy = initialEnemy()
            enemy.rect.topleft = (self.rect.x + random.randint(-20, 20),
                                  self.rect.y + random.randint(-20, 20))
            enemies_group.add(enemy)
            children.append(enemy)
        return children
