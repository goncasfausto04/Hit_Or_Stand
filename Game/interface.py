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

    play_video(video_path, config.resolution, sound_path)

    while True:
        # Create the screen at the set resolution
        screen = pygame.display.set_mode(config.resolution)

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
        while True:
            mouse = pygame.mouse.get_pos()  # Get mouse position

            # Event detection
            for event in pygame.event.get():
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

                    # Options button
                    if button_clicked(0.25 - (0.125 / 2), 0.833, 0.125, 0.083, mouse):
                        chime_sound.play()
                        options()
                        # Reinitialize the screen and other variables after returning from options
                        screen = pygame.display.set_mode(config.resolution)
                        blockyfont = pygame.font.Font(
                            blockyfontpath, int(config.height * 0.07)
                        )
                        blockyfontsmall = pygame.font.Font(
                            blockyfontpath, int(config.height * 0.035)
                        )
                        wilderness_text = blockyfont.render("Hit Or Stand", True, white)
                        quit_text = blockyfontsmall.render("Quit", True, white)
                        credits_text = blockyfontsmall.render("Credits", True, white)
                        rules_text = blockyfontsmall.render("Tutorial", True, white)
                        options_text = blockyfontsmall.render("Options", True, white)
                        title_text = blockyfont.render(
                            "Computation_3 Project!", True, glowing_yellow
                        )
                        background = pygame.image.load(background_path)
                        background = pygame.transform.scale(
                            background, config.resolution
                        )
                        break  # Exit the inner loop to reinitialize the screen

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
            pygame.display.update()


def wilderness_explorer():
    config.width, config.height = config.resolution[0], config.resolution[1]
    game_loop()


def options():
    # Initialize the screen for options
    screen = pygame.display.set_mode(config.resolution)

    # Set fonts
    blockyfontpath = os.path.join(base_path, "extras", "Pixeboy.ttf")
    blockyfont = pygame.font.Font(blockyfontpath, int(config.height * 0.07))
    blockyfontsmall = pygame.font.Font(blockyfontpath, int(config.height * 0.05))

    # Load current resolution from save
    save_dir = os.path.join(os.getenv('APPDATA'), ".hitorstand") if os.name == 'nt' else os.path.expanduser("~/.hitorstand")
    save_location = os.path.join(save_dir, "player_progress.json")
    try:
        with open(save_location, "r") as file:
            player_progress = json.load(file)
            current_res = tuple(player_progress.get("resolution", config.RESOLUTIONS[0]))
    except (FileNotFoundError, json.JSONDecodeError):
        current_res = config.RESOLUTIONS[0]

    # Sound setup
    chime_path = os.path.join(base_path, "extras", "chime1.mp3")
    chime_sound = pygame.mixer.Sound(chime_path)
    volume_level = pygame.mixer.music.get_volume()

    while True:
        mouse = pygame.mouse.get_pos()
        
        # Create text surfaces
        current_res_text = f"Resolution: {config.resolution[0]}x{config.resolution[1]}"
        resolution_text = blockyfontsmall.render(current_res_text, True, white)
        volume_text = blockyfontsmall.render("Music Volume:", True, white)
        back_text = blockyfont.render("Back", True, white)
        reset_text = blockyfont.render("Reset Progress", True, white)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Resolution button
                if button_clicked(0.3, 0.3, 0.4, 0.1, mouse):
                    chime_sound.play()
                    try:
                        with open(save_location, "r") as file:
                            player_progress = json.load(file)
                    except (FileNotFoundError, json.JSONDecodeError):
                        player_progress = {"resolution": list(config.RESOLUTIONS[0])}
                    
                    # Cycle through resolutions
                    current_res = tuple(player_progress.get("resolution", config.RESOLUTIONS[0]))
                    try:
                        current_index = config.RESOLUTIONS.index(current_res)
                    except ValueError:
                        current_index = 0
                    new_index = (current_index + 1) % len(config.RESOLUTIONS)
                    new_res = config.RESOLUTIONS[new_index]
                    
                    # Save new resolution
                    player_progress["resolution"] = list(new_res)
                    with open(save_location, "w") as file:
                        json.dump(player_progress, file)
                    
                    # Update config and screen
                    config.resolution = new_res
                    screen = pygame.display.set_mode(config.resolution)
                    blockyfont = pygame.font.Font(blockyfontpath, int(config.height * 0.07))
                    blockyfontsmall = pygame.font.Font(blockyfontpath, int(config.height * 0.05))

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

        # Resolution button
        draw_buttonutils(
            dark_red,
            glowing_light_red,
            0.3, 0.3, 0.4, 0.1,
            resolution_text,
            blockyfontsmall,
            mouse,
            screen
        )

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

        pygame.display.update()