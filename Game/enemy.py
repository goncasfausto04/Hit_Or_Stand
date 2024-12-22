from config import *
import pygame
import random
import math
import config
from bullet import enemy_bullet


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.health = 10
        self.speed = random.randint(3, 4)
        self.damage = 15
        self.color = None
        # creating a surface for the enemy
        self.image = pygame.Surface(enemy_size)
        # getting rectangle for positioning
        self.rect = self.image.get_rect()

        # starting the enemy at a random valid location on the screen
        # enemy_size[0] because the enemy size is a tupple -> (0,0)
        self.rect.x = random.randint(0, config.width - enemy_size[0])
        self.rect.y = random.randint(0, config.height - enemy_size[-1])

    def draw(self, screen):
        # Draw the enemy using its color attribute
        self.image.fill(self.color)
        screen.blit(self.image, self.rect)

    def update(self, player):
        self.move_towards_player(player)

    def move_towards_player(self, player):
        # Calculate direction vector towards the player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = max(1, (dx**2 + dy**2) ** 0.5)  # Avoid division by zero

        # Normalize the direction and move towards the player
        self.rect.x += int(self.speed * dx / distance)
        self.rect.y += int(self.speed * dy / distance)


class initialEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.health = 10
        self.speed = 2
        self.damage = 10

        sprite_path = os.path.join(base_path, "extras", "sprite", "initialenemy")
        self.frame_count = 0
        self.fps_counter = 0

        self.sprites = []
        for i in range(0, 5):
            self.sprites.append(
                pygame.image.load(os.path.join(sprite_path, f"tile00{i}.png"))
            )

        self.image = self.sprites[self.frame_count]

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x - 15, self.rect.y - 17))
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Red color, 2-pixel border

    def update(self, player):
        self.move_towards_player(player)
        self.fps_counter += 1
        if self.fps_counter % 5 == 0:
            self.frame_count += 1
            if self.frame_count >= len(self.sprites):
                self.frame_count = 0
            self.image = self.sprites[self.frame_count]


class fastEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.health = 7
        self.speed = random.randint(3, 4)
        self.damage = 15
        self.color = (255, 0, 0)  # Red

        sprite_path = os.path.join(base_path, "extras", "sprite", "fastEnemy")
        self.frame_count = 0
        self.fps_counter = 0

        self.sprites = []
        for i in range(0, 4):
            image = pygame.image.load(os.path.join(sprite_path, f"slime-move-{i}.png"))
            scaled_image = pygame.transform.scale(
                image, (enemy_size[0] * 2, enemy_size[1] * 2)
            )  # Set new_width and new_height to desired dimensions
            self.sprites.append(scaled_image)

        self.image = self.sprites[self.frame_count]

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x - 15, self.rect.y - 27))
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Red color, 2-pixel border

    def update(self, player):
        self.move_towards_player(player)
        self.fps_counter += 1
        if self.fps_counter % 5 == 0:
            self.frame_count += 1
            if self.frame_count >= len(self.sprites):
                self.frame_count = 0
            self.image = self.sprites[self.frame_count]


class TankMonster(Enemy):
    def __init__(self):
        super().__init__()
        self.health = 30
        self.speed = 2
        self.damage = 10
        self.color = (0, 0, 255)  # Blue

        sprite_path = os.path.join(base_path, "extras", "sprite", "TankMonster")
        self.frame_count = 0
        self.fps_counter = 0

        self.sprites = []
        for i in range(0, 8):
            image = pygame.image.load(os.path.join(sprite_path, f"tile00{i}.png"))
            scaled_image = pygame.transform.scale(
                image, (enemy_size[0] * 4.5, enemy_size[1] * 3)
            )
            self.sprites.append(scaled_image)

        self.image = self.sprites[self.frame_count]

        # Adjust the size of the hitbox
        self.rect.width = self.rect.width
        self.rect.height = self.rect.height * 2.1  # Increase height by 50%

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x - 55, self.rect.y - 25))
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def update(self, player):
        self.move_towards_player(player)
        self.fps_counter += 1
        if self.fps_counter % 5 == 0:
            self.frame_count += 1
            if self.frame_count >= len(self.sprites):
                self.frame_count = 0
            self.image = self.sprites[self.frame_count]


class RangedMonster(Enemy):
    def __init__(self):
        super().__init__()
        self.health = 20
        self.speed = 0
        self.damage = 10
        self.color = (255, 255, 0)
        self.bullet_cooldown = 0
        self.bullet_type = enemy_bullet
        self.fire_rate = 70

        sprite_path = os.path.join(base_path, "extras", "sprite", "RangedMonster")
        self.frame_count = 0
        self.fps_counter = 0

        self.sprites = []
        for i in range(0, 4):
            image = pygame.image.load(os.path.join(sprite_path, f"tile00{i}.png"))
            scaled_image = pygame.transform.scale(
                image, (enemy_size[0] * 2, enemy_size[1] * 2)
            )
            self.sprites.append(scaled_image)

        self.image = self.sprites[self.frame_count]

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x - 15, self.rect.y - 17))
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Red color, 2-pixel border

    def update(self, player):
        self.move_towards_player(player)
        self.fps_counter += 1
        if self.fps_counter % 5 == 0:
            self.frame_count += 1
            if self.frame_count >= len(self.sprites):
                self.frame_count = 0
            self.image = self.sprites[self.frame_count]

    def enemy_shoot(self, bullets):
        if self.bullet_cooldown <= 0:
            for _ in range(2):  # Fire 2 bullets in random directions
                angle = random.uniform(0, 2 * math.pi)  # Generate a random angle
                bullet = self.bullet_type(
                    self.rect.centerx, self.rect.centery, angle, self
                )
                bullets.add(bullet)

            # Reset cooldown
            self.bullet_cooldown = self.fire_rate

        self.bullet_cooldown -= 1


class DuplicateMonster(Enemy):
    def __init__(self):
        super().__init__()
        self.health = 30
        self.speed = 2
        self.damage = 10
        self.color = (58, 58, 58)  # Blue

        sprite_path = os.path.join(base_path, "extras", "sprite", "initialenemy")
        self.frame_count = 0
        self.fps_counter = 0

        self.rect.width = self.rect.width * 1.8
        self.rect.height = self.rect.height * 1.3

        self.sprites = []
        for i in range(0, 5):
            image = pygame.image.load(os.path.join(sprite_path, f"tile00{i}.png"))
            scaled_image = pygame.transform.scale(
                image, (enemy_size[0] * 2.5, enemy_size[1] * 2.5)
            )  # Set new_width and new_height to desired dimensions
            self.sprites.append(scaled_image)

        self.image = self.sprites[self.frame_count]

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x - 12, self.rect.y - 25))
        # pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # Red color, 2-pixel border

    def update(self, player):
        self.move_towards_player(player)
        self.fps_counter += 1
        if self.fps_counter % 5 == 0:
            self.frame_count += 1
            if self.frame_count >= len(self.sprites):
                self.frame_count = 0
            self.image = self.sprites[self.frame_count]

    def spawn_on_death(self, enemies_group):
        """Spawn two new enemies upon death."""
        for _ in range(2):
            new_enemy = initialEnemy()  # Create a new regular enemy
            new_enemy.rect.x = self.rect.x + random.randint(
                -20, 20
            )  # Spawn near the parent enemy
            new_enemy.rect.y = self.rect.y + random.randint(-20, 20)
            enemies_group.add(new_enemy)
