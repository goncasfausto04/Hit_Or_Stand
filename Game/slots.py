"""Slot machine with pre-rendered background, reels and static labels."""
import os
import random
import sys

import pygame

import config
import window
from ui import TextCache, prompt_bet
from utils import wait_with_events


def _gradient(size, top, bottom):
    surface = pygame.Surface(size).convert()
    width, height = size
    for y in range(height):
        blend = y / max(1, height - 1)
        color = tuple(round(start + (end - start) * blend) for start, end in zip(top, bottom))
        pygame.draw.line(surface, color, (0, y), (width - 1, y))
    return surface


def slots(player):
    width, height = config.resolution
    screen = window.get_screen()
    pygame.display.set_caption("Slot Machine")
    font_path = os.path.join(config.base_path, "extras", "Pixeboy.ttf")
    font = pygame.font.Font(font_path, int(width * 0.04))
    small_font = pygame.font.Font(font_path, int(width * 0.03))
    text = TextCache(font)
    small_text = TextCache(small_font)
    slot_size = (100, 100)
    slot_x = [width // 4 - 50, width // 2 - 50, 3 * width // 4 - 50]
    slot_y = height // 2 - 50
    symbols = (config.red, config.green, config.blue)
    reels = {color: _gradient(slot_size, config.light_gray, color) for color in (*symbols, config.white)}
    for surface in reels.values():
        pygame.draw.rect(surface, config.black, surface.get_rect(), 5)

    background = _gradient(config.resolution, config.dark_green, config.olive_green)
    backing_rect = pygame.Rect(slot_x[0] - 20, slot_y - 20, slot_x[-1] + 140 - slot_x[0], 140)
    pygame.draw.rect(background, config.light_grey, backing_rect)
    pygame.draw.rect(background, config.black, backing_rect, 5)
    for x in slot_x:
        pygame.draw.rect(background, config.black, (x + 5, slot_y + 5, *slot_size))
    for label, y in (("Press SPACE to Spin!", slot_y - height * 0.1), ("Press Esc to go back", height - 50)):
        surface = text.render(label)
        outline = text.render(label, config.black)
        x = width // 2 - surface.get_width() // 2
        for dx, dy in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            background.blit(outline, (x + dx, y + dy))
        background.blit(surface, (x, y))

    bet = prompt_bet(screen, player, small_font)
    if bet is None:
        return "shedcasino"
    bet_surface = small_text.render(f"Bet: ${bet}", config.gold)

    def draw_slot_machine(results, message=None):
        screen.blit(background, (0, 0))
        for x, color in zip(slot_x, results):
            screen.blit(reels[color], (x, slot_y))
        screen.blit(bet_surface, (width * 0.039, height * 0.1))
        if message:
            message_surface = text.render(message)
            screen.blit(message_surface, message_surface.get_rect(midtop=(width // 2, height - 100)))
        screen.blit(text.render(f"Money: ${player.coins}"), (20, 20))

    results = [config.white] * 3
    message = None
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for event in window.get_events():
            if event.type == pygame.QUIT:
                player.save_progress()
                pygame.quit()
                sys.exit()
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                return "shedcasino"
            if event.key != pygame.K_SPACE:
                continue
            if player.coins < bet:
                message = "Insufficient Funds!"
                continue
            for frame in range(15):
                results = [random.choice(symbols) for _ in range(3)]
                draw_slot_machine(results)
                window.present()
                wait_with_events(100 + frame * 5, player)
            won = results[0] == results[1] == results[2]
            message = "You Win!" if won else "You Lose!"
            player.coins += bet * 3 if won else -bet
            player.save_progress()

        draw_slot_machine(results, message)
        window.present()
