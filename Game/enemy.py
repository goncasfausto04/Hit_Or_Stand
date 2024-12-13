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
        """
        receiving the player as input so that we can assure the enemies have the players' direction
        """

        # determining the direction (in radians) of the movement based on the player's position
        # dx = player.rect.x - self.rect.x
        # dy = player.rect.y - self.rect.y
        # getting the direction in radians
        # direction = math.atan2(dy, dx)

        # moving the enemy towards the player --> like bullet
        # self.rect.x += int(self.speed * math.cos(direction))
        # self.rect.y += int(self.speed * math.sin(direction))

    def move_towards_player(self, player):
        # Calculate direction vector towards the player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = max(1, (dx**2 + dy**2) ** 0.5)  # Avoid division by zero

        # Normalize the direction and move towards the player
        self.rect.x += int(self.speed * dx / distance)
        self.rect.y += int(self.speed * dy / distance)

    """
    def handle_collision_with_player(self, player):
        if self.rect.colliderect(player.rect):
            # Stop enemy from moving inside the player by "pushing it back"
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)

            # Push the enemy away by reversing the movement
            self.rect.x -= int(self.speed * dx / distance)
            self.rect.y -= int(self.speed * dy / distance)
    """


class initialEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.health = 5
        self.speed = 2
        self.damage = 10
        self.color = (0, 255, 0)  # Green


class fastEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.health = 10
        self.speed = random.randint(3, 4)
        self.damage = 15
        self.color = (255, 0, 0)  # Red


class TankMonster(Enemy):
    def __init__(self):
        super().__init__()
        self.health = 30
        self.speed = 2
        self.damage = 10
        self.color = (0, 0, 255)  # Blue


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

    def enemy_shoot(self, bullets):
        if self.bullet_cooldown <= 0:
            for _ in range(2):  # Fire 2 bullets in random directions
                angle = random.uniform(0, 2 * math.pi)  # Generate a random angle
                bullet = self.bullet_type(self.rect.centerx, self.rect.centery, angle, self)
                bullets.add(bullet)
                print(f"Bullet spawned at ({self.rect.centerx}, {self.rect.centery}) with angle {angle:.2f}")

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
