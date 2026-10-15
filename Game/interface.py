import window
from game import game_loop
import pygame
from utils import *  # no need to import pygame because the import is in utils
from config import *  # importing colors and the like
import os
from credits import credits_
import config
from tutorial import tutorial
import json
import sys


def interface():

    while True:
        # Create the screen at the set resolution
        screen = window.get_screen()

        # Set fonts
        blockyfontpath = os.path.join(base_path, "extras", "Pixeboy.ttf")
        blockyfont = pygame.font.Font(blockyfontpath, int(config.height * 0.07))
        blockyfontsmall = pygame.font.Font(blockyfontpath, int(config.height * 0.035))

        # Render the text
        wilderness_text = blockyfont.render("Hit Or Stand", True, white)
        quit_text = blockyfontsmall.render("Quit", True, white)
        credits_text = blockyfontsmall.render("Credits", True, white)
        rules_text = blockyfontsmall.render("Tutorial", True, white)
        options_text = blockyfontsmall.render("Options", True, white)
        title_text = blockyfont.render("Computation_3 Project!", True, glowing_yellow)

        # Render music
        music_path = os.path.join(base_path, "extras", "mainmusic.mp3")
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_pos(5)
        pygame.mixer.music.set_volume(music_volume)

        # Render background
        background_path = os.path.join(base_path, "extras", "menubg.jpg")
        background = pygame.image.load(background_path)
        background = pygame.transform.scale(background, config.resolution)

        chime_path = os.path.join(base_path, "extras", "chime1.mp3")
        chime_sound = pygame.mixer.Sound(chime_path)
        chime_sound.set_volume(config.music_volume)

        chime2_path = os.path.join(base_path, "extras", "chime2.mp3")
        chime2_sound = pygame.mixer.Sound(chime2_path)
        chime2_sound.set_volume(config.music_volume)

        pygame.display.set_caption("Hit Or Stand")

        # Main loop
        ui_clock = pygame.time.Clock()
        while True:
            ui_clock.tick(60)
            mouse = window.mouse_position()  # Get mouse position

            # Event detection
            for event in window.get_events():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Quit button
                    if button_clicked(0.75 - (0.125 / 2), 0.833, 0.125, 0.083, mouse):
                        chime_sound.play()
                        pygame.quit()
                        sys.exit()

                    # Credits button
                    if button_clicked(0.75 - (0.125 / 2), 0.667, 0.125, 0.083, mouse):
                        chime_sound.play()
                        credits_()

                    # Wilderness game button
                    if button_clicked(0.125, 0.333, 0.75, 0.083, mouse):
                        chime2_sound.play()
                        wilderness_explorer()
                        pygame.mixer.music.load(music_path)
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(config.music_volume)

                    # Options button
                    if button_clicked(0.25 - (0.125 / 2), 0.833, 0.125, 0.083, mouse):
                        chime_sound.play()
                        options()
                    # Rules button
                    if button_clicked(0.25 - (0.125 / 2), 0.667, 0.125, 0.083, mouse):
                        chime_sound.play()
                        tutorial()

                # Escape key to return to main menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            # Fill the screen with background
            screen.blit(background, (0, 0))

            # Wilderness game button
            draw_buttonutils(
                dark_red,
                glowing_light_red,
                0.125,
                0.333,
                0.75,
                0.083,
                wilderness_text,
                blockyfont,
                mouse,
                screen,
            )

            # Rules button
            draw_buttonutils(
                grey,
                light_grey,
                0.25 - (0.125 / 2),
                0.667,
                0.125,
                0.083,
                rules_text,
                blockyfontsmall,
                mouse,
                screen,
            )

            # Quit button
            draw_buttonutils(
                grey,
                light_grey,
                0.75 - (0.125 / 2),
                0.833,
                0.125,
                0.083,
                quit_text,
                blockyfontsmall,
                mouse,
                screen,
            )

            # Options button
            draw_buttonutils(
                grey,
                light_grey,
                0.25 - (0.125 / 2),
                0.833,
                0.125,
                0.083,
                options_text,
                blockyfontsmall,
                mouse,
                screen,
            )

            # Credits button
            draw_buttonutils(
                grey,
                light_grey,
                0.75 - (0.125 / 2),
                0.667,
                0.125,
                0.083,
                credits_text,
                blockyfontsmall,
                mouse,
                screen,
            )

            # Title text
            screen.blit(title_text, (config.width * 0.05, config.height * 0.02))

            # Update the screen
            window.present()


def wilderness_explorer():
    game_loop()


def options():
    # Initialize the screen for options
    screen = window.get_screen()

    # Set fonts
    blockyfontpath = os.path.join(base_path, "extras", "Pixeboy.ttf")
    blockyfont = pygame.font.Font(blockyfontpath, int(config.height * 0.07))
    blockyfontsmall = pygame.font.Font(blockyfontpath, int(config.height * 0.05))

    # Sound setup
    chime_path = os.path.join(base_path, "extras", "chime1.mp3")
    chime_sound = pygame.mixer.Sound(chime_path)
    volume_level = pygame.mixer.music.get_volume()
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        mouse = window.mouse_position()
        
        # Create text surfaces
        size = pygame.display.get_window_size()
        fullscreen_text = blockyfontsmall.render(
            "Exit Fullscreen (F11)" if window.is_fullscreen() else "Fullscreen (F11)",
            True, white,
        )
        size_text = blockyfontsmall.render(
            f"Window: {size[0]} x {size[1]}", True, white
        )
        resize_text = blockyfontsmall.render("Drag the bottom-right corner to resize", True, white)
        volume_text = blockyfontsmall.render("Music Volume:", True, white)
        back_text = blockyfont.render("Back", True, white)
        reset_text = blockyfont.render("Reset Progress", True, white)

        # Event handling
        for event in window.get_events():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_clicked(0.3, 0.3, 0.4, 0.1, mouse):
                    chime_sound.play()
                    window.toggle_fullscreen()

                # Volume control
                volume_bar = pygame.Rect(
                    config.width * 0.3, config.height * 0.6, config.width * 0.4, 20
                )
                if volume_bar.collidepoint(mouse):
                    relative_position = (mouse[0] - volume_bar.x) / volume_bar.width
                    volume_level = max(0, min(relative_position, 1))
                    config.music_volume = volume_level
                    pygame.mixer.music.set_volume(volume_level)

                # Reset progress
                if button_clicked(0.3, 0.45, 0.4, 0.1, mouse):
                    chime_sound.play()
                    reset_progress()

                # Back button
                if button_clicked(0.3, 0.75, 0.4, 0.1, mouse):
                    chime_sound.play()
                    return

        # Draw everything
        screen.fill(deep_black)

        # Fullscreen button
        draw_buttonutils(
            dark_red,
            glowing_light_red,
            0.3, 0.3, 0.4, 0.1,
            fullscreen_text,
            blockyfontsmall,
            mouse,
            screen
        )

        screen.blit(size_text, size_text.get_rect(center=(config.width * 0.5, config.height * 0.15)))
        screen.blit(resize_text, resize_text.get_rect(center=(config.width * 0.5, config.height * 0.23)))

        # Volume control
        screen.blit(volume_text, (config.width * 0.1, config.height * 0.6))
        volume_bar = pygame.Rect(
            config.width * 0.3, config.height * 0.6, config.width * 0.4, 20
        )
        pygame.draw.rect(screen, grey, volume_bar)
        filled_bar = pygame.Rect(
            volume_bar.x,
            volume_bar.y,
            volume_bar.width * volume_level,
            volume_bar.height,
        )
        pygame.draw.rect(screen, dark_red, filled_bar)

        # Reset progress button
        draw_buttonutils(
            dark_red,
            glowing_light_red,
            0.3, 0.45, 0.4, 0.1,
            reset_text,
            blockyfont,
            mouse,
            screen
        )

        # Back button
        draw_buttonutils(
            dark_red,
            glowing_light_red,
            0.3, 0.75, 0.4, 0.1,
            back_text,
            blockyfont,
            mouse,
            screen
        )

        window.present()
