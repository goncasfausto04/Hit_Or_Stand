from utils import *
from config import *
import pygame
import math
from bullet import Bullet

# making Player a child of the Sprite class
class Player(pygame.sprite.Sprite):

    def __init__(self):
        #calling the mother class init
        super().__init__()

        # VISUAL VARIABLES
        # we call surface to represent the player image
        self.image = pygame.Surface(player_size)
        # drawing the image of the player
        self.image.fill(cute_purple)
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

        # GAMEPLAY VARIABLES
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.bullet_cooldown = 0

        self.powerup_active = False
        self.powerup_timer = 0

    def activate_powerup(self):
        """
        Activates the invincibility power-up for 15 seconds.
        """
        self.powerup_active = True
        self.powerup_timer = 15 * fps  # 15 seconds worth of frames
        self.image.fill(dark_red)
    def update(self):

        # getting the keys input:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < height:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < width:
            self.rect.x += self.speed
        if self.powerup_active:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                self.powerup_active = False  # Deactivate power-up
                self.image.fill(cute_purple)  # Revert to original color


    def shoot(self, bullets):
        """
        bullets --> pygame group where i will add bullets
        """
        # cooldown ==> how many frames i need to wait until i can shoot again
        if self.bullet_cooldown <= 0:
            # === defining the directions in wich the bullets will fly ===
            # These 4 directions are, in order, right, left, up, down
            for angle in [0, math.pi, math.pi / 2, 3 * math.pi / 2]:

                # === creating a bullet for each angle ===

                # I will use self.rect.centerx to make the x position of the bullet the same as the x position of the player, thus making the bullet come out of them.
                # finally, the directtion of the bullet is the angle
                bullet = Bullet(self.rect.centerx, self.rect.centery, angle)
                # adding the bullet to the bullets pygame group
                bullets.add(bullet)

            # resetting the cooldown
            self.bullet_cooldown = fps

        self.bullet_cooldown -= 1

    def draw_health_bar(self, screen):
        """
        Draws a health bar below the player's sprite.
        """
        bar_width = 50  # Width of the health bar
        bar_height = 8  # Height of the health bar
        health_ratio = self.health / self.max_health  # Fraction of health remaining

        # Positioning the health bar below the player
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.bottom + 5  # Just below the bottom of the player sprite

        # Draw the red background (full bar)
        pygame.draw.rect(screen, red, (bar_x, bar_y, bar_width, bar_height))
        # Draw the green foreground (current health)
        pygame.draw.rect(screen, green, (bar_x, bar_y, int(bar_width * health_ratio), bar_height))
