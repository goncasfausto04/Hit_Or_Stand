"""Shared rendering and input for small menu screens."""
from functools import lru_cache

import pygame

import config
import window


class TextCache:
    """Keep a bounded set of text surfaces for one font and scene."""

    def __init__(self, font):
        self.render = lru_cache(maxsize=128)(
            lambda text, color=config.white: font.render(text, True, color)
        )


def prompt_bet(screen, player, font):
    """Return an affordable nonnegative bet, or None when cancelled."""
    text = TextCache(font)
    center_x, center_y = config.width // 2, config.height // 2
    input_box = pygame.Rect(center_x - 100, center_y - 20, 200, 40)
    input_text = ""
    error = None
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        for event in window.get_events():
            if event.type == pygame.QUIT:
                player.save_progress()
                pygame.quit()
                raise SystemExit
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                return None
            if event.key == pygame.K_RETURN:
                if input_text and int(input_text) <= player.coins:
                    return int(input_text)
                error = "Enter a bet within your available funds."
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
                error = None
            elif (
                event.unicode
                and all(character in "0123456789" for character in event.unicode)
                and len(input_text) + len(event.unicode) <= len(str(max(0, player.coins)))
            ):
                input_text += event.unicode
                error = None

        screen.fill(config.green)
        for label, y, color in (
            (f"Available Money: ${player.coins}", center_y - 100, config.gold),
            ("Set your bet:", center_y - 50, config.white),
            ("Press Enter to Confirm", center_y + 50, config.white),
            ("Type 0 to play just for fun", center_y + 100, config.white),
            ("Esc to return", center_y + 150, config.white),
        ):
            surface = text.render(label, color)
            screen.blit(surface, surface.get_rect(midtop=(center_x, y)))

        input_surface = text.render(input_text, config.black)
        input_box.width = max(200, input_surface.get_width() + 10)
        input_box.centerx = center_x
        pygame.draw.rect(screen, config.white, input_box)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))
        if error:
            surface = text.render(error, config.red)
            screen.blit(surface, surface.get_rect(midtop=(center_x, center_y + 200)))
        window.present()
