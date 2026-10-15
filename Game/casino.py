"""Casino selection screen."""
import os
import sys

import pygame

import config
import window
from assets import load_image
from blackjack import blackjack
from slots import slots
from utils import button_clicked, draw_buttonutils


def casino(player):
    screen = window.get_screen()
    font = pygame.font.Font(
        os.path.join(config.base_path, "extras", "Pixeboy.ttf"),
        int(config.height * 0.035),
    )
    background = load_image(
        os.path.join(config.base_path, "extras", "casinobg.png"), config.resolution
    )
    buttons = (
        ((0.125, 0.167, 0.125, 0.083), font.render("Slot Machine", True, config.white), slots),
        ((0.125, 0.333, 0.125, 0.083), font.render("Blackjack", True, config.white), blackjack),
        ((0.625, 0.833, 0.125, 0.083), font.render("Go Back", True, config.white), None),
    )
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        mouse = window.mouse_position()
        for event in window.get_events():
            if event.type == pygame.QUIT:
                player.save_progress()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "shedcasino"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for bounds, _, action in buttons:
                    if button_clicked(*bounds, event.pos):
                        if action is None:
                            return "shedcasino"
                        action(player)
                        break
        screen.blit(background, (0, 0))
        for bounds, label, _ in buttons:
            draw_buttonutils(
                config.dark_red, config.red, *bounds, label, font, mouse, screen
            )
        window.present()
