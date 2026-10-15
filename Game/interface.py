"""Main menu and settings."""
import os
import sys

import pygame

import config
import window
from assets import load_image
from credits import credits_
from game import game_loop
from tutorial import tutorial
from ui import TextCache
from utils import button_clicked, draw_buttonutils, reset_progress


def interface():
    screen = window.get_screen()
    font_path = os.path.join(config.base_path, "extras", "Pixeboy.ttf")
    font = pygame.font.Font(font_path, int(config.height * 0.07))
    small_font = pygame.font.Font(font_path, int(config.height * 0.035))
    background = load_image(
        os.path.join(config.base_path, "extras", "menubg.jpg"), config.resolution
    )
    title = font.render("Computation_3 Project!", True, config.glowing_yellow)
    chime = pygame.mixer.Sound(os.path.join(config.base_path, "extras", "chime1.mp3"))
    game_chime = pygame.mixer.Sound(os.path.join(config.base_path, "extras", "chime2.mp3"))
    buttons = (
        ((0.125, 0.333, 0.75, 0.083), font.render("Hit Or Stand", True, config.white), font, game_loop),
        ((0.1875, 0.667, 0.125, 0.083), small_font.render("Tutorial", True, config.white), small_font, tutorial),
        ((0.6875, 0.667, 0.125, 0.083), small_font.render("Credits", True, config.white), small_font, credits_),
        ((0.1875, 0.833, 0.125, 0.083), small_font.render("Options", True, config.white), small_font, options),
        ((0.6875, 0.833, 0.125, 0.083), small_font.render("Quit", True, config.white), small_font, None),
    )

    def play_menu_music():
        pygame.display.set_caption("Hit Or Stand")
        pygame.mixer.music.load(os.path.join(config.base_path, "extras", "mainmusic.mp3"))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_pos(5)
        pygame.mixer.music.set_volume(config.music_volume)

    play_menu_music()
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        mouse = window.mouse_position()
        for event in window.get_events():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
                continue
            for bounds, _, _, action in buttons:
                if not button_clicked(*bounds, event.pos):
                    continue
                sound = game_chime if action is game_loop else chime
                sound.set_volume(config.music_volume)
                sound.play()
                if action is None:
                    pygame.quit()
                    sys.exit()
                action()
                if action in (game_loop, tutorial):
                    play_menu_music()
                break

        screen.blit(background, (0, 0))
        for bounds, label, button_font, action in buttons:
            game_button = action is game_loop
            draw_buttonutils(
                config.dark_red if game_button else config.grey,
                config.glowing_light_red if game_button else config.light_grey,
                *bounds, label, button_font, mouse, screen,
            )
        screen.blit(title, (config.width * 0.05, config.height * 0.02))
        window.present()


def options():
    screen = window.get_screen()
    font_path = os.path.join(config.base_path, "extras", "Pixeboy.ttf")
    font = pygame.font.Font(font_path, int(config.height * 0.07))
    small_font = pygame.font.Font(font_path, int(config.height * 0.05))
    text = TextCache(small_font)
    back_text = font.render("Back", True, config.white)
    reset_text = font.render("Reset Progress", True, config.white)
    resize_text = text.render("Drag the bottom-right corner to resize")
    volume_text = text.render("Music Volume:")
    chime = pygame.mixer.Sound(os.path.join(config.base_path, "extras", "chime1.mp3"))
    chime.set_volume(config.music_volume)
    volume_bar = pygame.Rect(config.width * 0.3, config.height * 0.6, config.width * 0.4, 20)
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        mouse = window.mouse_position()
        for event in window.get_events():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
                continue
            if button_clicked(0.3, 0.3, 0.4, 0.1, event.pos):
                chime.play()
                window.toggle_fullscreen()
            elif volume_bar.collidepoint(event.pos):
                config.music_volume = max(0, min((event.pos[0] - volume_bar.x) / volume_bar.width, 1))
                pygame.mixer.music.set_volume(config.music_volume)
                chime.set_volume(config.music_volume)
                window.save_preferences()
            elif button_clicked(0.3, 0.45, 0.4, 0.1, event.pos):
                chime.play()
                reset_progress()
            elif button_clicked(0.3, 0.75, 0.4, 0.1, event.pos):
                chime.play()
                return

        size = pygame.display.get_window_size()
        fullscreen_text = text.render(
            "Exit Fullscreen (F11)" if window.is_fullscreen() else "Fullscreen (F11)"
        )
        size_text = text.render(f"Window: {size[0]} x {size[1]}")
        screen.fill(config.deep_black)
        draw_buttonutils(
            config.dark_red, config.glowing_light_red, 0.3, 0.3, 0.4, 0.1,
            fullscreen_text, small_font, mouse, screen,
        )
        screen.blit(size_text, size_text.get_rect(center=(config.width * 0.5, config.height * 0.15)))
        screen.blit(resize_text, resize_text.get_rect(center=(config.width * 0.5, config.height * 0.23)))
        screen.blit(volume_text, (config.width * 0.1, config.height * 0.6))
        pygame.draw.rect(screen, config.grey, volume_bar)
        filled_bar = pygame.Rect(volume_bar.x, volume_bar.y, volume_bar.width * config.music_volume, volume_bar.height)
        pygame.draw.rect(screen, config.dark_red, filled_bar)
        for bounds, label in (((0.3, 0.45, 0.4, 0.1), reset_text), ((0.3, 0.75, 0.4, 0.1), back_text)):
            draw_buttonutils(
                config.dark_red, config.glowing_light_red, *bounds, label, font, mouse, screen
            )
        window.present()
