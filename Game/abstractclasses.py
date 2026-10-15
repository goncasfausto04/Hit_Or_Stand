"""Collectible power-up effects and their shared artwork."""
from abc import ABC, abstractmethod
import os
import random

import pygame

from assets import load_image
from config import base_path, fps


class PowerUp(pygame.sprite.Sprite, ABC):
    icon = None

    def __init__(self, x, y, duration=300):
        super().__init__()
        self.image = load_image(os.path.join(base_path, "extras", self.icon), (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.duration = duration

    @abstractmethod
    def affect_player(self, player):
        """Apply the effect to the player."""

    def affect_game(self, enemies):
        """Optionally apply an immediate effect to the enemy group."""


class Invincibility(PowerUp):
    icon = "golden_star.png"

    def affect_player(self, player):
        player.invincible = True


class DeSpawner(PowerUp):
    icon = "reaper.png"

    def affect_game(self, enemies):
        if enemies:
            num_to_remove = random.randint(1, max(1, len(enemies) // 2))
            for enemy in random.sample(enemies.sprites(), num_to_remove):
                enemy.kill()

    def affect_player(self, player):
        player.de_spawner_active = True
        player.de_spawner_timer = 5 * fps


class Instakill(PowerUp):
    icon = "flameskull.png"

    def affect_player(self, player):
        player.oneshotkill = True


class InvertedControls(PowerUp):
    icon = "poison.png"

    def affect_player(self, player):
        player.inverted = True


class Teleportation(PowerUp):
    icon = "portal.png"

    def affect_player(self, player):
        player.teleport = True


class Health_Drop(PowerUp):
    icon = "health_pack.png"

    def affect_player(self, player):
        player.health_drop = True
