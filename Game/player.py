from utils import *
from config import *
import pygame
import math
from bullet import *
import json


# making Player a child of the Sprite class
class Player(pygame.sprite.Sprite):

    def __init__(self):
        # calling the mother class init
        super().__init__()

        # VISUAL VARIABLES
        # we call surface to represent the player image
        sprites_path_idle = os.path.join(base_path, "extras", "sprite", "idle")
        sprites_path_run = os.path.join(base_path, "extras", "sprite", "run")
        sprites_path_dead = os.path.join(base_path, "extras", "sprite", "die")

        self.frame_count = 0
        self.exp_required = 10
        self.dash_cooldown = 0
        self.has_dash = False

        self.sprites_idle = []
        for i in range(0, 9):
            path = os.path.join(sprites_path_idle, f"Idle__00{i}.png")
            image = pygame.image.load(path)
            self.sprites_idle.append(pygame.transform.scale(image, (player_size)))

        self.sprites_run = []
        for i in range(0, 7):
            path = os.path.join(sprites_path_run, f"Run__00{i}.png")
            image = pygame.image.load(path)
            self.sprites_run.append(
                pygame.transform.scale(image, (player_size[0], player_size[1]))
            )

        self.sprites_dead = []
        for i in range(0, 8):
            path = os.path.join(sprites_path_dead, f"die__00{i}.png")
            image = pygame.image.load(path)
            self.sprites_dead.append(
                pygame.transform.scale(image, (player_size[0], player_size[1]))
            )

        self.curernt_sprite_idle = 0
        self.curernt_sprite_run = 0
        self.curernt_sprite_dead = 0

        self.image = self.sprites_idle[self.curernt_sprite_idle]
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

        self.rect.height = self.rect.height * 0.9
        self.rect.width = self.rect.width * 0.8

        # GAMEPLAY VARIABLES
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.bullet_cooldown = 0
        self.bullet_type = "Basic Spell"
        self.fire_rate = {
            "Basic Spell": 50,
            "Shatterblast": 90,
            "Arcane Cascade": 35,
            "Rebound Rune": 75,
            "Astral Beam": 100,
        }  # Cooldown in frames

        self.coins = 0
        self.powerup_active = False
        self.powerup_timer = 0
        self.level = 1
        self.exp = 0
        self.spawn_rate_multiplier = 1.0  # Default spawn rate multiplier
        self.de_spawner_active = False
        self.de_spawner_timer = 5 * fps
        self.invincible = False
        self.spawn_rate_multiplier = 1
        self.oneshotkill = False
        self.inverted = False
        self.teleport = False
        self.weapons_purchased = ["Basic Spell"]
        self.pets_purchased = ["Dog"]
        self.dying = False
        self.dead = False
        self.enemies_spawn_multiplier = 1.1
        self.health_drop = False
        self.best_time = 0
        self.load_progress()

    def save_progress(self):
        save_location = os.path.join(base_path, "player_progress.json")
        player_data = {
            "has_dash": self.has_dash,
            "level": self.level,
            "exp": self.exp,
            "coins": self.coins,
            "weapons_purchased": self.weapons_purchased,
            "pets_purchased": self.pets_purchased,
            "best_time": self.best_time,
            "exp_required": self.exp_required,
            "max_health": self.max_health,
            # Add other attributes you want to save
        }
        with open(save_location, "w") as file:
            json.dump(player_data, file)

    def load_progress(self):
        save_location = os.path.join(base_path, "player_progress.json")
        if os.path.exists(save_location):
            with open(save_location, "r") as file:
                player_data = json.load(file)
                self.has_dash = player_data["has_dash"]
                self.level = player_data["level"]
                self.exp = player_data["exp"]
                self.coins = player_data["coins"]
                self.weapons_purchased = player_data["weapons_purchased"]
                self.pets_purchased = player_data["pets_purchased"]
                self.best_time = player_data["best_time"]
                self.exp_required = player_data["exp_required"]
                self.max_health = player_data["max_health"]
                # Load other attributes as needed
        else:
            pass

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

        if self.dying != True:
            movement = [0, 0]  # [dx, dy]

            if self.inverted == False:  # Normal controls
                if keys[pygame.K_w] and self.rect.top > 0:
                    movement[1] -= self.speed
                if keys[pygame.K_s] and self.rect.bottom < config.height:
                    movement[1] += self.speed
                if keys[pygame.K_a] and self.rect.left > 0:
                    movement[0] -= self.speed
                if keys[pygame.K_d] and self.rect.right < config.width:
                    movement[0] += self.speed
            else:  # Inverted controls
                if keys[pygame.K_w] and self.rect.bottom < config.height:
                    movement[1] += self.speed
                if keys[pygame.K_s] and self.rect.top > 0:
                    movement[1] -= self.speed
                if keys[pygame.K_a] and self.rect.right < config.width:
                    movement[0] += self.speed
                if keys[pygame.K_d] and self.rect.left > 0:
                    movement[0] -= self.speed

            # Normalize the  vector so that the player moves at the same speed in all directions
            magnitude = (movement[0] ** 2 + movement[1] ** 2) ** 0.5
            if magnitude > 0:  # Avoid division by zero
                movement[0] = movement[0] / magnitude * self.speed
                movement[1] = movement[1] / magnitude * self.speed

            # Apply movement to the player
            self.rect.x += movement[0]
            self.rect.y += movement[1]

        if self.dying:
            if self.frame_count % 12 == 0:
                if self.curernt_sprite_dead >= len(self.sprites_dead):
                    self.dying = False
                    self.curernt_sprite_dead = 0
                    self.health = self.max_health
                    self.dead = True
                self.image = self.sprites_dead[int(self.curernt_sprite_dead)]
                self.curernt_sprite_dead += 1
                return

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

        if self.frame_count % 12 == 0:
            if not any(keys):
                self.curernt_sprite_idle += 1
            if self.curernt_sprite_idle >= len(self.sprites_idle):
                self.curernt_sprite_idle = 0
            self.image = self.sprites_idle[int(self.curernt_sprite_idle)]

        if self.dying != True:
            if self.frame_count % 3 == 0:
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
            if self.de_spawner_active == True:
                self.de_spawner_timer -= 1
                if self.de_spawner_timer <= 0:
                    self.de_spawner_active = False

            if self.dash_cooldown > 0:
                self.dash_cooldown -= 1

            # Check for dash input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and self.has_dash:
                self.dash()

    def change_bullet_type(self, keys):
        if keys[pygame.K_1]:
            self.bullet_type = "Basic Spell"
        elif keys[pygame.K_2] and "Shatterblast" in self.weapons_purchased:
            self.bullet_type = "Shatterblast"
        elif keys[pygame.K_3] and "Arcane Cascade" in self.weapons_purchased:
            self.bullet_type = "Arcane Cascade"
        elif keys[pygame.K_4] and "Rebound Rune" in self.weapons_purchased:
            self.bullet_type = "Rebound Rune"
        elif keys[pygame.K_5] and "Astral Beam" in self.weapons_purchased:
            self.bullet_type = "Astral Beam"

    def glow(self, surface, radius, color):
        # Create a surface for the glow
        glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

        # Draw concentric circles with decreasing opacity
        for i in range(radius, 0, -1):
            pygame.draw.circle(glow_surface, color, (radius, radius), i)

        # Blit the glow onto the main surface at the player's center
        surface.blit(
            glow_surface, (self.rect.centerx - radius, self.rect.centery - radius)
        )

    def death(self):
        """
        Called when the player dies.
        """
        self.dying = True

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # Draw the hitbox
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Red color, 2-pixel border

    def shoot(self, bullets):
        """
        bullets --> pygame group where i will add bullets
        """
        # cooldown ==> how many frames i need to wait until i can shoot again
        if self.bullet_cooldown <= 0:
            bullet_class = {
                "Basic Spell": pistol,
                "Shatterblast": shotgun,
                "Arcane Cascade": machinegun,
                "Rebound Rune": bouncing,
                "Astral Beam": sniper,
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
        if self.dash_cooldown <= 0:
            dash_distance = 100
            direction = pygame.Vector2(0, 0)
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                direction.y = -1
            if keys[pygame.K_s]:
                direction.y = 1
            if keys[pygame.K_a]:
                direction.x = -1
            if keys[pygame.K_d]:
                direction.x = 1

            if direction.length() > 0:
                direction = direction.normalize()
                self.rect.move_ip(direction * dash_distance)
                self.dash_cooldown = config.fps * 2  # Cooldown in seconds
                # Add visual/audio feedback here
