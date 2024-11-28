import random
import pygame
import math
import os  # Import os module
from bullet import *  # Import all bullet classes
from config import *  # Assuming you have the config file with the resolution, pet size, etc.

# Define base_path
base_path = os.path.dirname(__file__)


class Pet(pygame.sprite.Sprite):
    def __init__(self, player, bullets, min_distance=50):
        super().__init__()

        # VISUAL VARIABLES
        self.image = os.path.join(base_path, "extras", "dog_pet_comp.png")
        self.image = pygame.image.load(self.image)  # Load image without resizing first
        self.image = pygame.transform.scale(
            self.image, pet_size
        )  # Resize to the pet's size
        self.rect = self.image.get_rect()
        self.rect.center = (
            player.rect.centerx + 50,
            player.rect.centery + 50,
        )  # Initial position relative to player

        # GAMEPLAY VARIABLES
        self.player = player  # Reference to the player
        self.speed = 2.1  # Speed at which the pet moves towards the player
        self.health = 180
        self.max_health = 180
        self.min_distance = (
            min_distance  # Minimum distance the pet will keep from the player
        )
        self.bullet_cooldown = 0  # Cooldown for firing bullets
        self.fire_rate = 120  # Cooldown in frames (you can adjust)
        self.bullet_type = pet_bullet
        self.bullets = bullets  # Pass the bullets group

    def update(self):
        # Calculate direction to the player
        dx = self.player.rect.x - self.rect.x
        dy = self.player.rect.y - self.rect.y
        distance = math.sqrt(dx**2 + dy**2)

        # Move the pet towards the player if it's farther than the minimum distance
        if distance > self.min_distance:
            direction = math.atan2(dy, dx)
            self.rect.x += int(self.speed * math.cos(direction))
            self.rect.y += int(self.speed * math.sin(direction))

        # Make pet go back when colliding with player
        if self.rect.colliderect(self.player.rect):
            direction = math.atan2(dy, dx)  # Calculate direction again
            self.rect.x -= int(self.speed * math.cos(direction))
            self.rect.y -= int(self.speed * math.sin(direction))

    def pet_shoot(self, bullets):
        """
        Shoots bullets in four directions (right, left, up, down) if cooldown allows.
        """
        if self.bullet_cooldown <= 0:
            bullet_class = self.bullet_type

            for _ in range(2):  # Fire 4 bullets in random directions
                angle = random.uniform(
                    0, 2 * math.pi
                )  # Generate a random angle in radians
                bullet = bullet_class(self.rect.centerx, self.rect.centery, angle)
                bullets.add(bullet)

            # resetting the cooldown
            self.bullet_cooldown = self.fire_rate

        self.bullet_cooldown -= 1

    def draw_health_bar(self, screen):
        """
        Draws a health bar below the player's sprite.
        """
        bar_width = 25  # Width of the health bar
        bar_height = 4  # Height of the health bar
        health_ratio = self.health / self.max_health  # Fraction of health remaining

        # Positioning the health bar below the player
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.bottom + 5  # Just below the bottom of the player sprite

        # Draw the red background (full bar)
        pygame.draw.rect(screen, red, (bar_x, bar_y, bar_width, bar_height))
        # Draw the green foreground (current health)
        pygame.draw.rect(
            screen, green, (bar_x, bar_y, int(bar_width * health_ratio), bar_height)
        )
