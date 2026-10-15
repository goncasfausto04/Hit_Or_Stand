"""Player movement, animation, weapons and persistent upgrades."""
from functools import lru_cache
import math
import os
import pygame
import config
from config import base_path, player_size, fps, width, height, red, green
from assets import load_image
from bullet import pistol, shotgun, machinegun, bouncing, sniper
from progress import DEFAULT_PROGRESS, read_progress, save_path, write_progress


@lru_cache(maxsize=32)
def glow_image(radius, color):
    image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(image, color, (radius, radius), radius)
    return image


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

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
            self.sprites_idle.append(load_image(path, player_size))

        self.sprites_run = []
        for i in range(0, 7):
            path = os.path.join(sprites_path_run, f"Run__00{i}.png")
            self.sprites_run.append(load_image(path, player_size))

        self.sprites_dead = []
        for i in range(0, 8):
            path = os.path.join(sprites_path_dead, f"die__00{i}.png")
            self.sprites_dead.append(load_image(path, player_size))

        self.sprites_run_left = [pygame.transform.flip(image, True, False) for image in self.sprites_run]

        self.current_sprite_idle = 0
        self.current_sprite_run = 0
        self.current_sprite_dead = 0

        self.image = self.sprites_idle[self.current_sprite_idle]
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

        self.rect.height = self.rect.height * 0.9
        self.rect.width = self.rect.width * 0.8

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
        self.level = 1
        self.exp = 0
        self.de_spawner_active = False
        self.de_spawner_timer = 5 * fps
        self.invincible = False
        self.oneshotkill = False
        self.inverted = False
        self.teleport = False
        self.weapons_purchased = ["Basic Spell"]
        self.pets_purchased = ["Dog"]
        self.dying = False
        self.dead = False
        self.health_drop = False
        self.best_time = 0
        self.load_progress()

    def get_save_path(self):
        return str(save_path())

    def save_progress(self):
        write_progress({key: getattr(self, key) for key in DEFAULT_PROGRESS}, self.get_save_path())

    def load_progress(self):
        for key, value in read_progress(self.get_save_path()).items():
            setattr(self, key, value)
        self.health = self.max_health

    def reset_combat_state(self):
        """Temporary battlefield effects must not leak into another run."""
        self.invincible = False
        self.oneshotkill = False
        self.inverted = False
        self.teleport = False
        self.health_drop = False
        self.de_spawner_active = False
        self.de_spawner_timer = 0

    def update(self):

        if self.dead:
            return
        self.frame_count += 1

        keys = pygame.key.get_pressed()

        if not self.dying:
            movement = [0, 0]  # [dx, dy]

            if not self.inverted:  # Normal controls
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
                if self.current_sprite_dead >= len(self.sprites_dead):
                    self.dying = False
                    self.current_sprite_dead = 0
                    self.health = self.max_health
                    self.dead = True
                else:
                    self.image = self.sprites_dead[self.current_sprite_dead]
                    self.current_sprite_dead += 1
            return

        if self.frame_count % 12 == 0:
            if not any(keys[key] for key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d)):
                self.current_sprite_idle += 1
            if self.current_sprite_idle >= len(self.sprites_idle):
                self.current_sprite_idle = 0
            self.image = self.sprites_idle[int(self.current_sprite_idle)]

        if not self.dying:
            if self.frame_count % 3 == 0:
                if (
                    keys[pygame.K_d]
                    or keys[pygame.K_w]
                    or keys[pygame.K_s]
                    or keys[pygame.K_a]
                ):
                    self.current_sprite_run += 1
                    if self.current_sprite_run >= len(self.sprites_run):
                        self.current_sprite_run = 0
                    if keys[pygame.K_a]:
                        self.image = self.sprites_run_left[self.current_sprite_run]
                    else:
                        self.image = self.sprites_run[int(self.current_sprite_run)]
            if self.de_spawner_active:
                self.de_spawner_timer -= 1
                if self.de_spawner_timer <= 0:
                    self.de_spawner_active = False

            if self.dash_cooldown > 0:
                self.dash_cooldown -= 1

            # Check for dash input
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
        glow_surface = glow_image(radius, tuple(color))

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

    def shoot(self, bullets):
        """
        bullets --> pygame group where i will add bullets
        """
        if self.dying or self.dead:
            return
        if self.bullet_cooldown <= 0:
            bullet_class = {
                "Basic Spell": pistol,
                "Shatterblast": shotgun,
                "Arcane Cascade": machinegun,
                "Rebound Rune": bouncing,
                "Astral Beam": sniper,
            }[self.bullet_type]

            for angle in [0, math.pi, math.pi / 2, 3 * math.pi / 2]:


                # finally, the directtion of the bullet is the angle
                bullet = bullet_class(self.rect.centerx, self.rect.centery, angle)
                bullets.add(bullet)

            self.bullet_cooldown = self.fire_rate[self.bullet_type]

        self.bullet_cooldown -= 1

    def draw_health_bar(self, screen):
        """
        Draws a health bar below the player's sprite.
        """
        bar_width = 50  # Width of the health bar
        bar_height = 8  # Height of the health bar
        health_ratio = max(0, min(1, self.health / self.max_health))  # Fraction of health remaining

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
                if self.inverted:
                    direction = -direction
                self.rect.move_ip(direction * dash_distance)
                self.rect.clamp_ip(pygame.Rect(0, 0, config.width, config.height))
                self.dash_cooldown = config.fps * 2  # Cooldown in seconds
                # Add visual/audio feedback here
