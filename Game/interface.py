from game import game_loop
import pygame
from utils import *  # no need to import pygame because the import is in utils
from config import *  # importing colors and the like
import os
from credits import credits_
import config
from tutorial import tutorial
import json


def interface():

    play_video(video_path, config.resolution, sound_path)

    while True:
        # Initialize pygame
        pygame.init()

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

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Quit button
                    if button_clicked(0.75 - (0.125 / 2), 0.833, 0.125, 0.083, mouse):
                        chime_sound.play()
                        pygame.quit()

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

    # Render texts
    volume_text = blockyfontsmall.render("Music Volume:", True, white)
    back_text = blockyfont.render("Back", True, white)
    reset_text = blockyfont.render("Reset Progress", True, white)

    # Volume level
    volume_level = pygame.mixer.music.get_volume()  # Get current volume (0.0 to 1.0)
    max_volume = 1  # Set the maximum volume for the slider

    chime_path = os.path.join(base_path, "extras", "chime1.mp3")
    chime_sound = pygame.mixer.Sound(chime_path)

    def reset_progress():
        save_location = os.path.join(base_path, "player_progress.json")
        default_data = {
            "has_dash": False,
            "level": 1,
            "exp": 0,
            "coins": 0,
            "weapons_purchased": ["Basic Spell"],
            "pets_purchased": ["Dog"],
            "best_time": 0,
            "exp_required": 10,
            "max_health": 100
            # Add other default attributes as needed
        }
        with open(save_location, "w") as file:
            json.dump(default_data, file)

    # Main loop
    while True:
        # Get mouse position
        mouse = pygame.mouse.get_pos()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Volume adjustment
            if event.type == pygame.MOUSEBUTTONDOWN:
                volume_bar = pygame.Rect(
                    config.width * 0.3, config.height * 0.7, config.width * 0.4, 20
                )
                if volume_bar.collidepoint(mouse):
                    # Map the mouse x-position to the volume level within the range [0, max_volume]
                    relative_position = (mouse[0] - volume_bar.x) / volume_bar.width
                    volume_level = max(
                        0, min(relative_position * max_volume, max_volume)
                    )
                    config.music_volume = volume_level
                    pygame.mixer.music.set_volume(volume_level)

                # Back button click
                back_button = pygame.Rect(
                    config.width * 0.3,
                    config.height * 0.8,
                    config.width * 0.4,
                    config.height * 0.1,
                )
                if back_button.collidepoint(mouse):
                    chime_sound.play()
                    # reload the game with the new resolution
                    return

                # Reset button click
                if button_clicked(0.3, 0.5, 0.4, 0.1, mouse):
                    chime_sound.play()
                    reset_progress()

        # Drawing the background
        screen.fill(deep_black)

        # Draw volume bar
        volume_bar = pygame.Rect(
            config.width * 0.3, config.height * 0.7, config.width * 0.4, 20
        )
        pygame.draw.rect(screen, grey, volume_bar)
        filled_bar = pygame.Rect(
            volume_bar.x,
            volume_bar.y,
            volume_bar.width * (volume_level / max_volume),
            volume_bar.height,
        )
        pygame.draw.rect(screen, dark_red, filled_bar)

        # Draw reset button
        draw_buttonutils(
            dark_red,
            glowing_light_red,
            0.3,
            0.5,
            0.4,
            0.1,
            reset_text,
            blockyfont,
            mouse,
            screen,
        )

        # Draw Back button
        draw_buttonutils(
            dark_red,
            glowing_light_red,
            0.3,
            0.8,
            0.4,
            0.1,
            back_text,
            blockyfont,
            mouse,
            screen,
        )

        # Draw static texts
        screen.blit(volume_text, (config.width * 0.1, config.height * 0.7))

        # Update the screen
        pygame.display.update()
