"""Guided safe-house and combat tutorial."""
import os
import random
import sys

import pygame

import config
import window
from abstractclasses import Invincibility
from assets import load_image
from config import base_path, black, soundtrack, white
from enemy import initialEnemy
from player import Player
from utils import draw_text_with_outline, prompt


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
    background_path = os.path.join(base_path, "extras", "shedbg.png")
    background = load_image(background_path, config.resolution)
    screen = window.get_screen()
    clock = pygame.time.Clock()

    blockyfont = pygame.font.Font(os.path.join(base_path, "extras", "Pixeboy.ttf"), 32)

    # set up spawn location
    playertutorial.rect.left = config.width * 0.5

    special_area = pygame.Rect(
        config.width * 0.845,  # x-coordinate (right margin of 2% from the edge)
        config.height * 0.248,  # y-coordinate (4.2% of screen height)
        config.width * 0.03,  # width (10.9% of screen width)
        config.height * 0.06,  # height (19.4% of screen height)
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
                "Great! You have the movement controls.",
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

        pygame.draw.rect(screen, (0, 255, 0), special_area, 2)

        for event in window.get_events():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
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

        if 81 <= promptcount < 240:
            promptcount += 1

        if playertutorial.rect.left <= 0:
            playertutorial.rect.left = config.width - playertutorial.rect.width
            return battle()

        window.present()


def battle():
    # creating the player group and adding the player to it
    playertutorial = Player()
    player_group = pygame.sprite.Group()
    player_group.add(playertutorial)
    enemy_group = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    abspowerups_group = pygame.sprite.Group()

    # setting up the background and the screen
    background_path = os.path.join(base_path, "extras", "Battleground.png")
    background = load_image(background_path, config.resolution)
    screen = window.get_screen()
    clock = pygame.time.Clock()

    blockyfont = pygame.font.Font(os.path.join(base_path, "extras", "Pixeboy.ttf"), 32)
    running = True

    playertutorial.rect.right = config.width - 20

    frame_count = 0

    update_enemy = False

    player_shoot = False

    dead_enemy = False

    spawn_powerup = False

    run_frames = True

    while running:
        clock.tick(config.fps)
        screen.blit(background, (0, 0))

        if run_frames:
            frame_count += 1

        # Update player position based on key presses
        playertutorial.update()

        # Draw the player
        player_group.draw(screen)

        # Draw the powerups
        abspowerups_group.draw(screen)

        abspowerups_group.update()
        # Check for collisions between player and power-ups
        collected = pygame.sprite.spritecollide(playertutorial, abspowerups_group, True)
        for powerup in collected:
            powerup.affect_player(playertutorial)
        if collected:
            run_frames = True

        # Draw the enemies
        for enemy in enemy_group:
            enemy.draw(screen)

        if spawn_powerup:
            x = random.randint(50, config.width - 50)
            y = random.randint(50, config.height - 50)
            powerup1 = Invincibility(x, y)
            abspowerups_group.add(powerup1)
            spawn_powerup = False


        if update_enemy:
            enemy_group.update(playertutorial)

        if player_shoot:
            # Draw the bullets

            playertutorial.shoot(bullets)
            bullets.update()

            for bullet in bullets:
                bullet.draw(screen)
                for enemy in enemy_group:
                    if enemy.rect.colliderect(bullet.rect):
                        enemy.health -= bullet.damage  # Apply damage
                        bullet.kill()  # Consume the bullet
                        if enemy.health <= 0:
                            enemy.kill()
                            dead_enemy = True
                        break

        if dead_enemy:
            run_frames = True
            dead_enemy = False

        for event in window.get_events():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        if frame_count == 150:
            prompt(
                screen, config.width, config.height * 1.5, "Welcome to the battlefield!"
            )

        if frame_count == 200:
            prompt(
                screen,
                config.width,
                config.height * 1.5,
                "This is where you will fight your enemies.",
            )

        if frame_count == 250:
            # spawn enemy
            enemy = initialEnemy()
            enemy_group.add(enemy)

        if frame_count == 300:
            prompt(screen, config.width, config.height * 1.5, "Look!! One enemy!.")
            update_enemy = True

        if frame_count == 350:
            prompt(
                screen, config.width, config.height * 1.5, "He will try and Kill You!!"
            )

        if frame_count == 400:
            prompt(screen, config.width, config.height * 1.5, "Kill Him first!!")
            player_shoot = True
            run_frames = False
            frame_count += 1

        if frame_count == 450:
            prompt(screen, config.width, config.height * 1.5, "Great Job!!")
            spawn_powerup = True

        if frame_count == 470:
            prompt(
                screen,
                config.width,
                config.height * 1.5,
                "See that little thing that spawned?",
            )

        if frame_count == 500:
            prompt(
                screen, config.width, config.height * 1.5, "Its a powerup. Catch it!"
            )
            frame_count += 1
            run_frames = False


        if frame_count == 520:
            prompt(screen, config.width, config.height * 1.5, "You are invincible now.")

        if frame_count == 530:
            prompt(
                screen, config.width, config.height * 1.5, "Like this are many others!"
            )

        if frame_count == 570:
            prompt(
                screen,
                config.width,
                config.height * 1.5,
                "Your main objective is to last as long as you can!",
            )

        if frame_count == 600:
            prompt(
                screen, config.width, config.height * 1.5, "Go and try for yourself!"
            )

        if frame_count == 650:
            prompt(
                screen,
                config.width,
                config.height * 1.5,
                "Good Luck! Press ESC to exit.",
            )

        window.present()

    return
