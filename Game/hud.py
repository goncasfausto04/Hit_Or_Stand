import pygame
import os
import config
from utils import *


class HUD:
    def __init__(self, screen, config, player):
        self.screen = screen
        self.config = config
        self.player = player

        # Fonts
        self.font_small = pygame.font.Font(None, 20)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 30)

        # Colors
        self.colors = {
            "deep_black": (0, 0, 0),
            "green": (0, 255, 0),
            "white": (255, 255, 255),
            "red": (255, 0, 0),
            "gold": (255, 223, 0),
            "gray": (50, 50, 50),
            "dark_gray": (80, 80, 80),
        }

        # Level-up bar dimensions
        self.bar_x = 0.2 * 1280
        self.bar_y = 720 - 40
        self.bar_width = 0.6 * 1280
        self.bar_height = 15

        # Weapon slot dimensions
        self.slot_size = 50
        self.slot_spacing = 10
        self.slot_start_x = self.bar_x
        self.slot_y = 720 - 95

        # Dash cooldown bar dimensions
        self.dash_bar_width = 0.09 * config.width
        self.dash_bar_height = 0.006 * 720
        self.dash_bar_x = 0.485 * 1280 - (self.dash_bar_width / 2)
        self.dash_bar_y = 0.9 * 720

        #load spell images
        basic_path = os.path.join(base_path, "extras", "basic_spell.png")
        shatterblast_path = os.path.join(base_path, "extras", "shatterblast.png")
        arcane_cascade_path = os.path.join(base_path, "extras", "arcane_cascade.png")
        rebound_rune_path = os.path.join(base_path, "extras", "bouncing.png")
        astral_beam_path = os.path.join(base_path, "extras", "astral_beam.png")

        self.basic_spell = pygame.image.load(basic_path).convert_alpha()
        self.shatterblast = pygame.image.load(shatterblast_path).convert_alpha()
        self.arcane_cascade = pygame.image.load(arcane_cascade_path).convert_alpha()
        self.rebound_rune = pygame.image.load(rebound_rune_path).convert_alpha()
        self.astral_beam = pygame.image.load(astral_beam_path).convert_alpha()

        self.basic_spell = pygame.transform.scale(self.basic_spell, (self.slot_size, self.slot_size))
        self.shatterblast = pygame.transform.scale(self.shatterblast, (self.slot_size, self.slot_size))
        self.arcane_cascade = pygame.transform.scale(self.arcane_cascade, (self.slot_size, self.slot_size))
        self.rebound_rune = pygame.transform.scale(self.rebound_rune, (self.slot_size, self.slot_size))
        self.astral_beam = pygame.transform.scale(self.astral_beam, (self.slot_size, self.slot_size))

    def draw_text(self, text, font, color, x, y, center=False):
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(x, y) if center else (x, y))
        self.screen.blit(surface, rect.topleft)

    def draw_bar(self, x, y, width, height, progress, color_bg, color_fg):
        pygame.draw.rect(self.screen, color_bg, (x, y, width, height))
        pygame.draw.rect(self.screen, color_fg, (x, y, width * progress, height))

    def draw_weapon_slots(self,player):
        weapon_names = ["1", "2", "3", "4", "5"]
        bullet_types = {
            "1": "Basic Spell",
            "2": "Shatterblast",
            "3": "Arcane Cascade",
            "4": "Rebound Rune",
            "5": "Astral Beam",
        }

        for i, weapon_name in enumerate(weapon_names):
            x = self.slot_start_x + i * (self.slot_size + self.slot_spacing)
            rect = pygame.Rect(x, self.slot_y, self.slot_size, self.slot_size)

            pygame.draw.rect(self.screen, self.colors["dark_gray"], rect)
            if weapon_name == "1":
                self.screen.blit(self.basic_spell, (x, self.slot_y))
            elif weapon_name == "2" and "Shatterblast" in player.weapons_purchased:
                self.screen.blit(self.shatterblast, (x, self.slot_y))
            elif weapon_name == "3" and "Arcane Cascade" in player.weapons_purchased:
                self.screen.blit(self.arcane_cascade, (x, self.slot_y))
            elif weapon_name == "4" and "Rebound Rune" in player.weapons_purchased:
                self.screen.blit(self.rebound_rune, (x, self.slot_y))
            elif weapon_name == "5" and "Astral Beam" in player.weapons_purchased:
                self.screen.blit(self.astral_beam, (x, self.slot_y))
            self.draw_text(
                weapon_name,
                self.font_medium,
                self.colors["white"],
                rect.x + 5,
                rect.y + 15,
            )
            border_color = (
                self.colors["green"]
                if bullet_types[weapon_name] == self.player.bullet_type
                else self.colors["white"]
            )
            pygame.draw.rect(self.screen, border_color, rect, 2)

    def draw_level_up_bar(self):
        progress = self.player.exp / self.player.exp_required
        self.draw_bar(
            self.bar_x,
            self.bar_y,
            self.bar_width,
            self.bar_height,
            progress,
            self.colors["white"],
            self.colors["green"],
        )
        self.draw_text(
            f"EXP: {self.player.exp}/{int(self.player.exp_required)}",
            self.font_medium,
            self.colors["dark_gray"],
            config.width // 2,
            self.bar_y + 8,
            center=True,
        )

    def draw_health_bar(self):
        bar_width = 50
        bar_height = 8
        health_ratio = self.player.health / self.player.max_health
        bar_x = self.player.rect.centerx - bar_width // 2
        bar_y = self.player.rect.bottom + 5
        self.draw_bar(
            bar_x,
            bar_y,
            bar_width,
            bar_height,
            health_ratio,
            self.colors["red"],
            self.colors["green"],
        )

    def draw_player_level(self):
        self.draw_text(
            f"Level: {self.player.level}",
            self.font_large,
            self.colors["white"],
            self.dash_bar_x * 1.07,
            config.height * 0.925,
        )

    def draw_best_time(self):
        minutes, seconds = divmod(self.player.best_time, 60)
        self.draw_text(
            f"Record: {minutes:02}:{seconds:02}",
            self.font_large,
            self.colors["white"],
            1280 * 0.697,
            0.925 * 720,
        )

    def draw_player_money(self):
        self.draw_text(
            f"Coins: {self.player.coins}",
            self.font_large,
            self.colors["gold"],
            1280 * 0.688,
            config.height * 0.89,
        )

    def draw_transparent_bar(self, x, y, width, height, color, alpha):
        """
        Draws a semi-transparent bar.

        :param x: X-coordinate of the bar.
        :param y: Y-coordinate of the bar.
        :param width: Width of the bar.
        :param height: Height of the bar.
        :param color: RGB color tuple for the bar.
        :param alpha: Transparency level (0 to 255).
        """
        # Create a surface with per-pixel alpha
        s = pygame.Surface((width, height), pygame.SRCALPHA)
        s.fill((*color, alpha))  # Add alpha to the color
        self.screen.blit(s, (x, y))

    def draw_dash_cooldown(self):
        self.draw_text(
            "Dash",
            self.font_large,
            self.colors["white"],
            self.dash_bar_x * 1.04,
            self.dash_bar_y - self.dash_bar_height * 2,
            center=True,
        )
        timer = self.player.dash_cooldown
        max_cooldown = fps * 2
        if timer > 0:
            progress = timer / max_cooldown
            self.draw_bar(
                self.dash_bar_x,
                self.dash_bar_y,
                self.dash_bar_width,
                self.dash_bar_height,
                progress,
                self.colors["gray"],
                self.colors["green"],
            )
            self.draw_text(
                f"{timer / fps:.1f}",
                self.font_large,
                self.colors["white"],
                self.dash_bar_x * 1.13,
                self.dash_bar_y - self.dash_bar_height * 2,
                center=True,
            )
        else:
            self.draw_text(
                "Space Bar",
                self.font_small,
                self.colors["white"],
                self.dash_bar_x * 1.15,
                self.dash_bar_y - self.dash_bar_height * 2,
                center=True,
            )
            self.draw_bar(
                self.dash_bar_x,
                self.dash_bar_y,
                self.dash_bar_width,
                self.dash_bar_height,
                0,
                self.colors["gray"],
                self.colors["green"],
            )

    def draw(self):
        self.draw_transparent_bar(
            config.width * 0.19,
            config.height * 0.855,
            800,
            90,
            self.colors["deep_black"],
            150,
        )
        self.draw_health_bar()
        self.draw_level_up_bar()
        self.draw_weapon_slots(self.player)
        self.draw_player_level()
        self.draw_player_money()
        if self.player.has_dash:
            self.draw_dash_cooldown()
        self.draw_best_time()
