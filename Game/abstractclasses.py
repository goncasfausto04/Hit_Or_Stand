import pygame
import random
from config import *
from abc import ABC, abstractmethod
import time


class PowerUp(pygame.sprite.Sprite, ABC):
    def __init__(self, x, y, duration=300):
        """ 
        Base Power-Up class. 
        :param x: Initial x position 
        :param y: Initial y position 
        :param color: Visual color of the power-up 
        :param duration: Duration in frames the power-up is active 
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

    @abstractmethod
    def deactivate(self, player):
        """Remove the power-ups effect when it expires."""
        player.powerup_active = False


class Invincibility(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill((0, 20, 0))  # Fill the power-up with blue to represent invincibility.
        self.duration = fps * 5
    def affect_player(self, player):
        """Make the player invincible."""
        player.invincible = True

    def affect_game(self, enemies):
        """Invincibility doesn't directly affect enemies, but it could if you wanted."""
        # For now, no game-wide effects, just the player's invincibility. 
        pass

    def deactivate(self, player):
        """End the invincibility effect."""
        player.invincible = False
       


class DeSpawner(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.Surface((40, 40))  # Set the size of the power-up 
        self.image.fill((255, 0, 0))  # Red color to indicate the De-spawner 
        self.rect = self.image.get_rect(center=(x, y))
        self.duration = fps * 5  # Duration in frames (e.g., 5 seconds at 60 FPS) 

    def affect_game(self, enemies):
        """Remove a random percentage of enemies and reduce spawn rates."""
        # Probabilistically remove some enemies 
        if len(enemies) > 0:
            num_to_remove = random.randint(1, max(1, len(enemies) // 2))
            enemies_removed = random.sample(enemies.sprites(), num_to_remove)
            for enemy in enemies_removed:
                enemy.kill()
                print(f"De-spawner removed {len(enemies_removed)} enemies!")
        else:
            print("No enemies to remove")

        

    def affect_player(self, player):
        """Reduce the spawn rate while active."""
        player.spawn_rate_multiplier = 0.5  # Reduce spawn rate by half 
        player.de_spawner_active = True
        player.de_spawner_timer = self.duration

    def deactivate(self, player):
        pass


class Instakill(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill((0, 0, 200))
    def affect_player(self, player):
        player.oneshotkill = True

    def affect_game(self, enemies):
        pass
    def deactivate(self, player):
        player.oneshotkill = False

class InvertedControls(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill((0, 100, 100))
    def affect_player(self, player):
        player.inverted = True

    def affect_game(self, enemies):
        pass
    def deactivate(self, player):
        player.inverted = False


class HealthDrop(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface(powerup_size)  # Half size of an enemy
        self.image.fill(green_ish)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
