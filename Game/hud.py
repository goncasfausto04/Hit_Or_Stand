import pygame
import os
import config
from utils import *


class HUD:
    def __init__(self, screen, config, player):
        self.screen = screen
        self.config = config
        self.player = player

        # Fonts using screen percentage
        self.font_small = pygame.font.Font(None, int(config.height * 0.028))
        self.font_medium = pygame.font.Font(None, int(config.height * 0.033))
        self.font_large = pygame.font.Font(None, int(config.height * 0.042))


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
        self.bar_x = 0.2 * config.width
        self.bar_y = config.height * 0.944  # 720-40 equivalent
        self.bar_width = 0.6 * config.width
        self.bar_height = config.height * 0.021  # 15px equivalent

        # Weapon slot dimensions
        self.slot_size = config.width * 0.039  # ~50px at 1280
        self.slot_spacing = config.width * 0.008  # 10px equivalent
        self.slot_start_x = self.bar_x
        self.slot_y = config.height * 0.868  # 720-95 equivalent

        # Dash cooldown bar dimensions
        self.dash_bar_width = 0.09 * config.width
        self.dash_bar_height = 0.008 * config.height
        self.dash_bar_x = 0.5 * config.width - (self.dash_bar_width / 2)  # Centered
        self.dash_bar_y = 0.9 * config.height

        # Load spell images
        basic_path = os.path.join(base_path, "extras", "basic_spell.png")
        shatterblast_path = os.path.join(base_path, "extras", "shatterblast.png")
        arcane_cascade_path = os.path.join(base_path, "extras", "arcane_cascade.png")
        rebound_rune_path = os.path.join(base_path, "extras", "bouncing.png")
        astral_beam_path = os.path.join(base_path, "extras", "astral_beam.png")

        # Scale images dynamically
        self.basic_spell = self.load_scaled_image(basic_path)
        self.shatterblast = self.load_scaled_image(shatterblast_path)
        self.arcane_cascade = self.load_scaled_image(arcane_cascade_path)
        self.rebound_rune = self.load_scaled_image(rebound_rune_path)
        self.astral_beam = self.load_scaled_image(astral_beam_path)

    def load_scaled_image(self, path):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (int(self.slot_size), int(self.slot_size)))

    def draw_text(self, text, font, color, x_ratio, y_ratio, center=False):
        x = x_ratio * self.config.width
        y = y_ratio * self.config.height
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(x, y) if center else (x, y))
        self.screen.blit(surface, rect.topleft)

    def draw_bar(self, x_ratio, y_ratio, width_ratio, height_ratio, progress, color_bg, color_fg):
        x = x_ratio * self.config.width
        y = y_ratio * self.config.height
        width = width_ratio * self.config.width
        height = height_ratio * self.config.height
        pygame.draw.rect(self.screen, color_bg, (x, y, width, height))
        pygame.draw.rect(self.screen, color_fg, (x, y, width * progress, height))

    def draw_weapon_slots(self, player):
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
            images = {
                "1": self.basic_spell,
                "2": self.shatterblast,
                "3": self.arcane_cascade,
                "4": self.rebound_rune,
                "5": self.astral_beam
            }
            
            if weapon_name in images and bullet_types[weapon_name] in player.weapons_purchased:
                self.screen.blit(images[weapon_name], (x, self.slot_y))
            
            self.draw_text(
                weapon_name,
                self.font_medium,
                self.colors["white"],
                (x + 5) / self.config.width,
                (self.slot_y + 15) / self.config.height
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
            0.2,  # x_ratio
            0.944,  # y_ratio
            0.6,  # width_ratio
            0.021,  # height_ratio
            progress,
            self.colors["white"],
            self.colors["green"],
        )
        self.draw_text(
            f"EXP: {self.player.exp}/{int(self.player.exp_required)}",
            self.font_medium,
            self.colors["dark_gray"],
            0.5,
            0.955,
            center=True,
        )

   
    def draw_player_level(self):
        self.draw_text(
            f"Level: {self.player.level}",
            self.font_large,
            self.colors["white"],
            0.465,
            0.925,
        )

    def draw_best_time(self):
        minutes, seconds = divmod(self.player.best_time, 60)
        self.draw_text(
            f"Record: {minutes:02}:{seconds:02}",
            self.font_large,
            self.colors["white"],
            0.7,
            0.925,
        )

    def draw_player_money(self):
        self.draw_text(
            f"Coins: {self.player.coins}",
            self.font_large,
            self.colors["gold"],
            0.688,
            0.89,
        )
    
     # FPS tracking
    

    def update_fps(self, fps):
        """Update the current FPS value"""
        self.fps = fps



    def draw_transparent_bar(self, x_ratio, y_ratio, width_ratio, height_ratio, color, alpha):
        s = pygame.Surface((
            int(width_ratio * self.config.width), 
            int(height_ratio * self.config.height)
        ), pygame.SRCALPHA)
        s.fill((*color, alpha))
        self.screen.blit(s, (
            x_ratio * self.config.width,
            y_ratio * self.config.height
        ))

    def draw_dash_cooldown(self):
        self.draw_text(
            "Dash",
            self.font_large,
            self.colors["white"],
            0.454,
            0.88,
            center=True,
        )
        
        timer = self.player.dash_cooldown
        max_cooldown = fps * 2
        if timer > 0:
            progress = timer / max_cooldown
            self.draw_bar(
                0.485 - (0.09/2),  # x_ratio centered
                0.9,  # y_ratio
                0.09,  # width_ratio
                0.008,  # height_ratio
                progress,
                self.colors["gray"],
                self.colors["green"],
            )
            self.draw_text(
                f"{timer / fps:.1f}",
                self.font_large,
                self.colors["white"],
                0.53,
                0.88,
                center=True,
            )
        else:
            self.draw_text(
                "Space Bar",
                self.font_small,
                self.colors["white"],
                0.5,
                0.88,
                center=True,
            )

    def draw(self):
        self.update_fps(fps)
        self.draw_transparent_bar(
            0.19,
            0.855,
            0.625,  # 800/1280 equivalent
            0.125,  # 90/720 equivalent
            self.colors["deep_black"],
            150,
        )
        self.draw_level_up_bar()
        self.draw_weapon_slots(self.player)
        self.draw_player_level()
        self.draw_player_money()
        if self.player.has_dash:
            self.draw_dash_cooldown()
        self.draw_best_time()
