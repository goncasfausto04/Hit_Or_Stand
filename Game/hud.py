import pygame
import os
import random
import config
from utils import *
from player import Player
from enemy import *
from pet import Pet
from shed import shed
from shop import shop
from chest import TreasureChest
from abstractclasses import *
class HUD:
    def __init__(self, screen, config, player):
        self.screen = screen
        self.config = config
        self.player = player
        self.font = pygame.font.Font(None, 36)  # Default font
        self.deep_black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.white = (255, 255, 255)

        # Timer tracking in milliseconds
        self.start_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        self.elapsed_time = 0  # Time elapsed since the game started

        # Positioning and size for level-up bar
        self.bar_x = 0.1 * config.width
        self.bar_y = 0.05 * config.height
        self.bar_width = 0.8 * config.width
        self.bar_height = 20

        # Load dash slot image
        self.dash_image_path = os.path.join("extras", "dash.png")
        self.dash_image = pygame.image.load(self.dash_image_path)
        self.dash_image = pygame.transform.scale(
            self.dash_image,
            (int(0.06 * config.width), int(0.06 * config.width))
        )

    def draw_weapon_slots(self):
        slot_size = 50  # Diminuir o tamanho dos slots
        spacing = 10  # Diminuir o espaçamento
        start_x = self.bar_x + 130
        y_position = self.config.height - 95  # Ajuste a posição vertical

        weapon_names = list(self.player.fire_rate.keys())

        for i in range(5):
            slot_rect = pygame.Rect(start_x + i * (slot_size + spacing), y_position, slot_size, slot_size)

            # Retângulo de fundo do slot
            pygame.draw.rect(self.screen, (80, 80, 80), slot_rect)

            # Nome da arma
            if i < len(weapon_names):
                weapon_text = self.font.render(weapon_names[i], True, self.white)
                self.screen.blit(weapon_text, (slot_rect.x + 5, slot_rect.y + 15))

    def draw_level_up_bar(self):
        bar_width = 0.6 * self.config.width  # Reduzindo a largura
        bar_height = 15  # Reduzindo a altura
        bar_x = 0.2 * self.config.width
        bar_y = self.config.height - 40  # Ajustando a posição vertical

        # Desenho da borda
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4), 2)
        # Desenho do preenchimento
        fill_width = (self.player.exp / self.player.exp_required) * bar_width
        pygame.draw.rect(self.screen, self.green, (bar_x, bar_y, fill_width, bar_height))

        # Texto da barra de XP
        # Criando uma fonte menor
        small_font = pygame.font.Font(None, 24)  # Tamanho 24 (ajuste conforme necessário)

        level_text = small_font.render(
            f"EXP: {self.player.exp}/{int(self.player.exp_required)}", True, self.white
        )

        # Exibindo o texto no centro da barra de XP

        self.screen.blit(level_text,
                         (self.config.width // 2 - level_text.get_width() // 2, bar_y))  # Ajuste vertical
    def draw_health_bar(self):
        """
        Draw the health bar below the player's sprite.
        """
        bar_width = 50  # Width of the health bar
        bar_height = 8  # Height of the health bar
        health_ratio = self.player.health / self.player.max_health

        # Positioning the health bar just below the player
        bar_x = self.player.rect.centerx - bar_width // 2
        bar_y = self.player.rect.bottom + 5

        pygame.draw.rect(self.screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, (0, 255, 0), (bar_x, bar_y, int(bar_width * health_ratio), bar_height))

    def draw_player_level(self):
        """
        Draw the player's current level as a large number just above the end of the Level-Up bar.
        """
        large_font = pygame.font.Font(None, 80)
        # Position the level number at the end of the Level-Up bar
        level_text = large_font.render(f"{self.player.level}", True, (255, 255, 255))

        text_x = self.bar_x + 900
        text_y = self.config.height - 78# Above the Level-Up bar

        self.screen.blit(level_text, (text_x, text_y))

    def draw_dash_slot(self):
        if self.player.has_dash:
            self.screen.blit(
                self.dash_image,
                (0.012 * self.config.width, 0.87 * self.config.height)
            )

            timer = self.player.dash_cooldown
            if timer > 0:
                semi_transparent_green = (0, 255, 0)
                pygame.draw.rect(
                    self.screen,
                    semi_transparent_green,
                    (
                        0.012 * self.config.width,
                        0.87 * self.config.height,
                        0.06 * self.config.width * (timer / (60 * 2)),
                        0.06 * self.config.width
                    )
                )

    def draw_player_money(self):
        """
        Draw the player's current coins on the HUD.
        """
        # Fonte para o texto das moedas
        money_font = pygame.font.Font(None, 40)  # Um pouco maior para destaque
        money_text = money_font.render(f"Coins: {self.player.coins}", True, (255, 223, 0))  # Texto em amarelo ouro

        # Posiciona o texto acima do lado esquerdo da barra de Level-Up
        text_x = self.bar_x + 440
        text_y = self.config.height - 90  # Um pouco acima da barra de Level-Up

        # Desenha o texto na tela
        self.screen.blit(money_text, (text_x, text_y))

    def draw(self):
        self.draw_health_bar()  # Player health bar that follows the player
        self.draw_level_up_bar()  # Level-up progress bar at the bottom
        self.draw_weapon_slots()
        self.draw_player_level()
        self.draw_player_money()
        if self.player.has_dash:
            self.draw_dash_slot()  # Dash slot visual
        current_time = pygame.time.get_ticks()  # Current time in milliseconds
        self.elapsed_time = (current_time - self.start_time) // 1000  # Convert to seconds

        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60

        timer_text = self.font.render(f"Time: {minutes:02}:{seconds:02}", True, self.white)
        self.screen.blit(timer_text, (10, 10))  # Draw timer text on the top-left corner