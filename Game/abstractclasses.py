import pygame
import random
from config import *
from abc import ABC, abstractmethod
base_path = os.path.dirname(__file__)


class PowerUp(pygame.sprite.Sprite, ABC):
    def __init__(self, x, y, duration=300):
        """
        Base Power-Up class.
        param x: Initial x position
        param y: Initial y position
        param color: Visual color of the power-up
        param duration: Duration in frames the power-up is active
        """
        super().__init__()
        self.image = pygame.Surface((20, 20))  # Default size for power-ups
        self.rect = self.image.get_rect(topleft=(x, y))
        self.duration = duration

    @abstractmethod
    def affect_player(self, player):
        """Apply the effect to the player."""
        pass

    @abstractmethod
    def affect_game(self, enemies):
        """Apply the effect to the game."""
        pass


class Invincibility(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y)
        image_path = os.path.join(base_path, "extras", "golden_star.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (40,40)
        )  # Scale to desired size
        self.duration = fps * 5

    def affect_player(self, player):
        """Make the player invincible."""
        player.invincible = True

    def affect_game(self, enemies):
        pass


class DeSpawner(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y)
        image_path = os.path.join(base_path, "extras", "reaper.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (40, 40))
        self.duration = fps * 5  # Duration in frames

    def affect_game(self, enemies):
        """Remove a random percentage of enemies and reduce spawn rates."""
        # Probabilistically remove some enemies
        if len(enemies) > 0:
            num_to_remove = random.randint(1, max(1, len(enemies) // 2))
            enemies_removed = random.sample(enemies.sprites(), num_to_remove)
            for enemy in enemies_removed:
                enemy.kill()
        else:
            pass

    def affect_player(self, player):
        """Reduce the spawn rate while active."""
        player.spawn_rate_multiplier = 0.5  # Reduce spawn rate by half
        player.de_spawner_active = True
        player.de_spawner_timer = self.duration

 


class Instakill(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y)
        image_path = os.path.join(base_path, "extras", "flameskull.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (40, 40))
        self.duration = fps * 5

    def affect_player(self, player):
        player.oneshotkill = True

    def affect_game(self, enemies):
        pass



class InvertedControls(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y)
        image_path = os.path.join(base_path, "extras", "poison.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (40, 40))

    def affect_player(self, player):
        player.inverted = True

    def affect_game(self, enemies):
        pass


class Teleportation(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y)
        image_path = os.path.join(base_path, "extras", "portal.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (40, 40))

    def affect_player(self, player):
        player.teleport = True

    def affect_game(self, enemies):
        pass

 


class Health_Drop(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y)
        image_path = os.path.join(base_path, "extras", "health_pack.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (40, 40))

    def affect_player(self, player):
        player.health_drop = True

    def affect_game(self, enemies):
        pass
