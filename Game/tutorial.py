import pygame
import os
import config
from player import Player
from enemy import *
from shed import shed
from utils import *
from shop import shop


def tutorial():

    # Play soundtrack
    pygame.mixer.music.load(random.choice(soundtrack))  # Load a random soundtrack
    pygame.mixer.music.set_volume(config.music_volume)  # Set the desired volume
    pygame.mixer.music.play(-1)  # Loop the soundtrack indefinitely

    # creating the player group and adding the player to it
    playertutorial = Player()
    player_group = pygame.sprite.Group()
    player_group.add(playertutorial)

    # setting up the background and the screen
    base_path = os.path.dirname(__file__)
    background_path = os.path.join(base_path, "extras", "shedbg.png")
    background = pygame.image.load(background_path)
    background = pygame.transform.scale(background, config.resolution)
    screen = pygame.display.set_mode(config.resolution)
    clock = pygame.time.Clock()

    blockyfont = pygame.font.Font(os.path.join(base_path, "extras", "Pixeboy.ttf"), 32)

    # set up spawn location
    playertutorial.rect.left = config.width * 0.5

    special_area = pygame.Rect(
        config.width
        - (config.width * 0.109)
        - (config.width * 0.02),  # x-coordinate (right margin of 2% from the edge)
        config.height * 0.19,  # y-coordinate (4.2% of screen height)
        config.width * 0.035,  # width (10.9% of screen width)
        config.height * 0.09,  # height (19.4% of screen height)
    )

    promptcount = 0
    wasd_keys_pressed = set()
    running = True

    while running:
        clock.tick(config.fps)
        screen.blit(background, (0, 0))

        # Update player position based on key presses
        playertutorial.update()

        # Draw the player
        player_group.draw(screen)

        print("promptcount:", promptcount)

        if promptcount == 0:
            prompt(
                screen, config.width, config.height * 1.5, "Welcome to the tutorial!"
            )
            promptcount += 1
        elif promptcount == 1:
            prompt(
                screen, config.width, config.height * 1.5, "Use WASD to move around."
            )
            promptcount += 1
        elif promptcount == 3:
            prompt(
                screen,
                config.width,
                config.height * 1.5,
                "Great!! You are not that dumb after all!",
            )
            promptcount += 1
        elif promptcount == 4:
            prompt(
                screen,
                config.width,
                config.height * 1.5,
                "Now, this place is called your Safe House.",
            )
            promptcount += 1
        elif promptcount == 5:
            prompt(
                screen,
                config.width,
                config.height * 1.5,
                "You can come here to upgrade your arsenal.",
            )
            promptcount += 1
        elif promptcount == 6:
            prompt(
                screen,
                config.width,
                config.height * 1.5,
                "or do more nefarious business.",
            )
            promptcount += 1
        elif promptcount == 7:
            prompt(
                screen,
                config.width,
                config.height * 1.5,
                "But you will find more about that.",
            )
            promptcount += 1
        elif promptcount == 8:
            prompt(
                screen,
                config.width,
                config.height * 1.5,
                "Now, on the top right there is the shop",
            )
            promptcount += 1
        elif promptcount == 9:
            prompt(
                screen,
                config.width,
                config.height * 1.5,
                "You can buy weapons and other stuff there.",
            )
            promptcount += 1
        elif promptcount == 10:
            prompt(
                screen,
                config.width,
                config.height * 1.5,
                "Come on. go there, what are you waiting for?",
            )
            promptcount += 1
        elif promptcount == 80:
            prompt(
                screen,
                config.width,
                config.height * 1.5,
                "HAHA, got you! Not Yet Partner!",
            )
            promptcount += 1
        elif promptcount == 240:
            prompt(
                screen,
                config.width,
                config.height * 1.5,
                "On your left, you can go to the Battlefield.",
            )
            promptcount += 1

        # draw the special area
        pygame.draw.rect(screen, (0, 255, 0), special_area, 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                    wasd_keys_pressed.add(event.key)

                # Check if all WASD keys have been pressed
                if (
                    wasd_keys_pressed
                    == {pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d}
                    and promptcount == 2
                ):
                    promptcount += 1  # Advance to next part when all keys pressed

        # Check if the player collides with the special area
        if special_area.colliderect(playertutorial.rect) and promptcount < 80:
            # Go to the shop area (example of what happens here)
            draw_text_with_outline(
                screen,
                "This is the tutorial",
                special_area.x - config.width * 0.15,
                special_area.y - 50,
                white,
                black,
                blockyfont,
            )
            draw_text_with_outline(
                screen,
                "tf you think would happen?",
                special_area.x - config.width * 0.15,
                special_area.y - 20,
                white,
                black,
                blockyfont,
            )
            promptcount += 1
        if special_area.colliderect(playertutorial.rect) and promptcount >= 80:
            draw_text_with_outline(
                screen,
                "Still here?",
                special_area.x - config.width * 0.15,
                special_area.y - 50,
                white,
                black,
                blockyfont,
            )

        if promptcount >= 81 and promptcount < 240:
            promptcount += 1

        pygame.display.flip()
