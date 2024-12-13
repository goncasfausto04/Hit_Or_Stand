from utils import *
from config import *
import pygame
import math
from bullet import Bullet
from bullet import pistol, shotgun, machinegun


# making Player a child of the Sprite class
class Player(pygame.sprite.Sprite):

    def __init__(self):
        # calling the mother class init
        super().__init__()

        # VISUAL VARIABLES
        # we call surface to represent the player image
        sprites_path = os.path.join(base_path, "extras", "sprite")

        self.sprites_idle = []
        self.frame_count = 0
        self.exp_required = 10
        self.dash_cooldown = 0
        self.has_dash = False
        for i in range(0, 9):
            path = os.path.join(sprites_path, f"Idle__00{i}.png")
            image = pygame.image.load(path)
            self.sprites_idle.append(pygame.transform.scale(image, (player_size)))

        self.sprites_run = []
        for i in range(0, 9):
            path = os.path.join(sprites_path, f"Run__00{i}.png")
            image = pygame.image.load(path)
            self.sprites_run.append(
                pygame.transform.scale(image, (player_size[0] * 1.8, player_size[1]))
            )

        self.curernt_sprite_idle = 0
        self.curernt_sprite_run = 0

        self.image = self.sprites_idle[self.curernt_sprite_idle]
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

        # GAMEPLAY VARIABLES
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.bullet_cooldown = 0
        self.bullet_type = "pistol"
        self.fire_rate = {
            "pistol": 50,
            "shotgun": 90,
            "machinegun": 20,
        }  # Cooldown in frames
        self.coins = 20000
        self.powerup_active = False
        self.powerup_timer = 0
        self.level = 1
        self.exp = 0
        self.spawn_rate_multiplier = 1.0  # Default spawn rate multiplier
        self.de_spawner_active = False
        self.de_spawner_timer = 0
        self.invincible = False
        self.spawn_rate_multiplier = 1
        self.oneshotkill = False
        self.inverted = False
 

    def activate_powerup(self):
        """
        Activates the invincibility power-up for 15 seconds.
        """
        self.powerup_active = True
        self.powerup_timer = 15 * fps  # 15 seconds worth of frames
        # self.image.fill(dark_red)

    def update(self):

        # getting the keys input:
        self.frame_count += 1

        keys = pygame.key.get_pressed()

        if self.inverted == False:  # Normal controls
            if keys[pygame.K_w] and self.rect.top > 0:
                self.rect.y -= self.speed
            if keys[pygame.K_s] and self.rect.bottom < config.height:
                self.rect.y += self.speed
            if keys[pygame.K_a] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[pygame.K_d] and self.rect.right < config.width:
                self.rect.x += self.speed
        else:  # Inverted controls
            if keys[pygame.K_w] and self.rect.bottom < config.height:
                self.rect.y += self.speed
            if keys[pygame.K_s] and self.rect.top > 0:
                self.rect.y -= self.speed
            if keys[pygame.K_a] and self.rect.right < config.width:
                self.rect.x += self.speed
            if keys[pygame.K_d] and self.rect.left > 0:
                self.rect.x -= self.speed

        # Power-up timer logic
        if self.powerup_active:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                self.powerup_active = False  # Deactivate power-up
                # self.image.fill(cute_purple)  # Revert to original color

                self.rect.x -= self.speed
            if self.powerup_active:
                self.powerup_timer -= 1
                if self.powerup_timer <= 0:
                    self.powerup_active = False  # Deactivate power-up
                # self.image.fill(cute_purple)  # Revert to original color



        if self.frame_count % 8 == 0:
            if not any(keys):
                self.curernt_sprite_idle += 1
            if self.curernt_sprite_idle >= len(self.sprites_idle):
                self.curernt_sprite_idle = 0
            self.image = self.sprites_idle[int(self.curernt_sprite_idle)]

        if self.frame_count % 2 == 0:
            if (
                keys[pygame.K_d]
                or keys[pygame.K_w]
                or keys[pygame.K_s]
                or keys[pygame.K_a]
            ):
                self.curernt_sprite_run += 1
                if self.curernt_sprite_run >= len(self.sprites_run):
                    self.curernt_sprite_run = 0
                if keys[pygame.K_a]:
                    self.image = pygame.transform.flip(
                        self.sprites_run[int(self.curernt_sprite_run)], True, False
                    )
                else:
                    self.image = self.sprites_run[int(self.curernt_sprite_run)]
        if self.de_spawner_active:
            self.de_spawner_timer -= 1
            if self.de_spawner_timer <= 0:
                self.spawn_rate_multiplier = 1.0  # Reset spawn rate multiplier
                self.de_spawner_active = False

        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        # Check for dash input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.has_dash:
            self.dash()

    def change_bullet_type(self, keys):
        if keys[pygame.K_1]:
            self.bullet_type = "pistol"
        elif keys[pygame.K_2]:
            self.bullet_type = "shotgun"
        elif keys[pygame.K_3]:
            self.bullet_type = "machinegun"

    def shoot(self, bullets):
        """
        bullets --> pygame group where i will add bullets
        """
        # cooldown ==> how many frames i need to wait until i can shoot again
        if self.bullet_cooldown <= 0:
            bullet_class = {
                "pistol": pistol,
                "shotgun": shotgun,
                "machinegun": machinegun,
            }[self.bullet_type]

            # === defining the directions in wich the bullets will fly ===
            # These 4 directions are, in order, right, left, up, down
            for angle in [0, math.pi, math.pi / 2, 3 * math.pi / 2]:

                # === creating a bullet for each angle ===

                # I will use self.rect.centerx to make the x position of the bullet the same as the x position of the player, thus making the bullet come out of them.
                # finally, the directtion of the bullet is the angle
                bullet = bullet_class(self.rect.centerx, self.rect.centery, angle)
                # adding the bullet to the bullets pygame group
                bullets.add(bullet)

            # resetting the cooldown
            self.bullet_cooldown = self.fire_rate[self.bullet_type]

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
        pygame.draw.rect(
            screen, green, (bar_x, bar_y, int(bar_width * health_ratio), bar_height)
        )

    def dash(self):
        """
        Makes the player dash in the direction they are currently moving.
        """
        if self.dash_cooldown <= 0:  # Check if dash is off cooldown
            dash_distance = 100  # Distance to dash
            direction = pygame.Vector2(0, 0)

            # Determine the direction based on the keys pressed
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                direction.y = -1
            if keys[pygame.K_s]:
                direction.y = 1
            if keys[pygame.K_a]:
                direction.x = -1
            if keys[pygame.K_d]:
                direction.x = 1

            # Normalize the direction to avoid faster diagonal dashes
            if direction.length() > 0:
                direction = direction.normalize()

            # Dash to direction
            self.rect.x += direction.x * dash_distance
            self.rect.y += direction.y * dash_distance

            self.dash_cooldown = fps * 2  # 2 seconds cooldown (adjust as needed)
