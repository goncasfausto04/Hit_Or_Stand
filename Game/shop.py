from utils import under_construction
import pygame
from utils import *  # no need to import pygame because the import is in utils
from config import *  # importing colors and the like
import os
from game import *
from player import Player


def shop(player):
    # Initialize pygame
    pygame.init()

    # Create the screen at the set resolution
    screen = pygame.display.set_mode(config.resolution)

    # Set fonts
    blockyfontpath = os.path.join(base_path, "extras", "Pixeboy.ttf")
    blockyfont = pygame.font.Font(blockyfontpath, int(config.height * 0.07))
    blockyfontsmall = pygame.font.Font(blockyfontpath, int(config.height * 0.035))

    # Render the text
    skins_text = blockyfontsmall.render("Skins Shop", True, white)
    bullets_text = blockyfontsmall.render("Weapons Shop", True, white)
    pets_text = blockyfontsmall.render("Pet Shop", True, white)
    goback_text = blockyfontsmall.render("Go Back", True, white)
    title_text = blockyfont.render("Shopping Street", True, glowing_light_red)

    # Render background
    background_path = os.path.join(base_path, "extras", "loja.jpeg")
    background = pygame.image.load(background_path)
    background = pygame.transform.scale(background, config.resolution)

    # Main loop
    while True:
        mouse = pygame.mouse.get_pos()  # Get mouse position

        # Event detection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Skins button
                if button_clicked(0.125, 0.167, 0.125, 0.083, mouse):
                    under_construction()

                # Weapons button
                if button_clicked(0.125, 0.333, 0.125, 0.083, mouse):
                    weapons_shop(player)

                # Pets button
                if button_clicked(0.125, 0.5, 0.125, 0.083, mouse):
                    under_construction()

                # Go back button
                if button_clicked(0.625, 0.833, 0.125, 0.083, mouse):
                    return "shedshop"  # Exit the shop

        # Fill the screen with background
        screen.blit(background, (0, 0))

        # Skins button
        draw_buttonutils(
            dark_red,
            red,
            0.125,
            0.167,
            0.125,
            0.083,
            skins_text,
            blockyfontsmall,
            mouse,
            screen,
        )

        # Weapons button
        draw_buttonutils(
            dark_red,
            red,
            0.125,
            0.333,
            0.125,
            0.083,
            bullets_text,
            blockyfontsmall,
            mouse,
            screen,
        )

        # Pets button
        draw_buttonutils(
            dark_red,
            red,
            0.125,
            0.5,
            0.125,
            0.083,
            pets_text,
            blockyfontsmall,
            mouse,
            screen,
        )

        # Go back button
        draw_buttonutils(
            dark_red,
            red,
            0.625,
            0.833,
            0.125,
            0.083,
            goback_text,
            blockyfontsmall,
            mouse,
            screen,
        )

        # Update the screen
        pygame.display.update()


def weapons_shop(player):
    pygame.init()
    screen = pygame.display.set_mode(config.resolution)
    blockyfontpath = os.path.join(base_path, "extras", "Pixeboy.ttf")
    blockyfont = pygame.font.Font(
        blockyfontpath, int(config.height * 0.035)
    )  # Smaller font size
    font = blockyfont
    background_path = os.path.join(base_path, "extras", "weaponshop.png")
    background = pygame.image.load(background_path)
    background = pygame.transform.scale(background, config.resolution)

    # Weapon prices
    weapon_prices = {
        "Pistol": 100,
        "Shotgun": 300,
        "Machine Gun": 500,
        "Exploding Bullets Weapon": 800,
        "Stalker Gun": 800,
        "Bouncing Bullets Weapon": 800,
        "Freezing Bullets Weapon": 900,
        "Cluster Bullet Weapon": 1000,
        "Poison Weapon": 1000,
        "Gravity Weapon": 1200,
    }

    while True:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Purchase logic
                if (
                    button_clicked(0.1, 0.2, 0.4, 0.06, mouse)
                    and player.coins >= weapon_prices["Pistol"]
                ):
                    print("Pistol Purchased")
                    player.coins -= weapon_prices["Pistol"]
                    player.weapons_purchased.append("Pistol")
                elif button_clicked(0.1, 0.2, 0.4, 0.06, mouse):
                    print("Not enough money for Pistol")

                if (
                    button_clicked(0.55, 0.2, 0.4, 0.06, mouse)
                    and player.coins >= weapon_prices["Shotgun"]
                ):
                    print("Shotgun Purchased")
                    player.coins -= weapon_prices["Shotgun"]
                    player.weapons_purchased.append("Shotgun")
                elif button_clicked(0.55, 0.2, 0.4, 0.06, mouse):
                    print("Not enough money for Shotgun")

                if (
                    button_clicked(0.1, 0.3, 0.4, 0.06, mouse)
                    and player.coins >= weapon_prices["Machine Gun"]
                ):
                    print("Machine Gun Purchased")
                    player.coins -= weapon_prices["Machine Gun"]
                    player.weapons_purchased.append("Machine Gun")
                elif button_clicked(0.1, 0.3, 0.4, 0.06, mouse):
                    no_money_messaege(screen)

                if (
                    button_clicked(0.55, 0.3, 0.4, 0.06, mouse)
                    and player.coins >= weapon_prices["Exploding Bullets Weapon"]
                ):
                    print("Exploding Bullets Weapon Purchased")
                    player.coins -= weapon_prices["Exploding Bullets Weapon"]
                    player.weapons_purchased.append("Exploding Bullets Weapon")
                elif button_clicked(0.55, 0.3, 0.4, 0.06, mouse):
                    no_money_messaege(screen)

                if (
                    button_clicked(0.1, 0.4, 0.4, 0.06, mouse)
                    and player.coins >= weapon_prices["Stalker Gun"]
                ):
                    print("Stalker Gun Purchased")
                    player.coins -= weapon_prices["Stalker Gun"]
                    player.weapons_purchased.append("Stalker Gun")
                elif button_clicked(0.1, 0.4, 0.4, 0.06, mouse):
                    no_money_messaege(screen)

                if (
                    button_clicked(0.55, 0.4, 0.4, 0.06, mouse)
                    and player.coins >= weapon_prices["Freezing Bullets Weapon"]
                ):
                    print("Freezing Bullets Weapon Purchased")
                    player.coins -= weapon_prices["Freezing Bullets Weapon"]
                    player.weapons_purchased.append("Freezing Bullets Weapon")
                elif button_clicked(0.55, 0.4, 0.4, 0.06, mouse):
                    no_money_messaege(screen)

                if (
                    button_clicked(0.1, 0.5, 0.4, 0.06, mouse)
                    and player.coins >= weapon_prices["Bouncing Bullets Weapon"]
                ):
                    print("Bouncing Bullets Weapon Purchased")
                    player.coins -= weapon_prices["Bouncing Bullets Weapon"]
                    player.weapons_purchased.append("Bouncing Bullets Weapon")
                elif button_clicked(0.1, 0.5, 0.4, 0.06, mouse):
                    no_money_messaege(screen)

                if (
                    button_clicked(0.55, 0.5, 0.4, 0.06, mouse)
                    and player.coins >= weapon_prices["Cluster Bullet Weapon"]
                ):
                    print("Cluster Bullet Weapon Purchased")
                    player.coins -= weapon_prices["Cluster Bullet Weapon"]
                    player.weapons_purchased.append("Cluster Bullet Weapon")
                elif button_clicked(0.55, 0.5, 0.4, 0.06, mouse):
                    no_money_messaege(screen)

                if (
                    button_clicked(0.1, 0.6, 0.4, 0.06, mouse)
                    and player.coins >= weapon_prices["Poison Weapon"]
                ):
                    print("Poison Weapon Purchased")
                    player.coins -= weapon_prices["Poison Weapon"]
                    player.weapons_purchased.append("Poison Weapon")
                elif button_clicked(0.1, 0.6, 0.4, 0.06, mouse):
                    no_money_messaege(screen)

                if (
                    button_clicked(0.55, 0.6, 0.4, 0.06, mouse)
                    and player.coins >= weapon_prices["Gravity Weapon"]
                ):
                    print("Gravity Weapon Purchased")
                    player.coins -= weapon_prices["Gravity Weapon"]
                    player.weapons_purchased.append("Gravity Weapon")
                elif button_clicked(0.55, 0.6, 0.4, 0.06, mouse):
                    no_money_messaege(screen)

                if button_clicked(0.55, 0.7, 0.4, 0.06, mouse):
                    return  # Go back to main shop

        # Drawing
        screen.blit(background, (0, 0))
        money_text = font.render(f"Money: ${player.coins}", True, white)
        screen.blit(money_text, (config.width * 0.05, config.height * 0.05))

        pistol_text = font.render("Pistol - $100", True, white)
        shotgun_text = font.render("Shotgun - $300", True, white)
        machinegun_text = font.render("Machine Gun - $500", True, white)
        explodingbullets_text = font.render(
            "Exploding Bullets Weapon - $800", True, white
        )
        homing_text = font.render("Stalker Gun - $800", True, white)
        freezingbullets_text = font.render(
            "Freezing Bullets Weapon - $900", True, white
        )
        bouncingbullets_text = font.render(
            "Bouncing Bullets Weapon - $800", True, white
        )
        clusterbullets_text = font.render("Cluster Bullet Weapon - $1000", True, white)
        poison_text = font.render("Poison Weapon - $1000", True, white)
        gravity_text = font.render("Gravity Gun - $1200", True, white)
        goback_text = font.render("Go Back", True, white)

        draw_buttonutils(
            dark_red, red, 0.1, 0.2, 0.4, 0.06, pistol_text, blockyfont, mouse, screen
        )
        draw_buttonutils(
            dark_red, red, 0.55, 0.2, 0.4, 0.06, shotgun_text, blockyfont, mouse, screen
        )
        draw_buttonutils(
            dark_red,
            red,
            0.1,
            0.3,
            0.4,
            0.06,
            machinegun_text,
            blockyfont,
            mouse,
            screen,
        )
        draw_buttonutils(
            dark_red,
            red,
            0.55,
            0.3,
            0.4,
            0.06,
            explodingbullets_text,
            blockyfont,
            mouse,
            screen,
        )
        draw_buttonutils(
            dark_red, red, 0.1, 0.4, 0.4, 0.06, homing_text, blockyfont, mouse, screen
        )
        draw_buttonutils(
            dark_red,
            red,
            0.55,
            0.4,
            0.4,
            0.06,
            freezingbullets_text,
            blockyfont,
            mouse,
            screen,
        )
        draw_buttonutils(
            dark_red,
            red,
            0.1,
            0.5,
            0.4,
            0.06,
            bouncingbullets_text,
            blockyfont,
            mouse,
            screen,
        )
        draw_buttonutils(
            dark_red,
            red,
            0.55,
            0.5,
            0.4,
            0.06,
            clusterbullets_text,
            blockyfont,
            mouse,
            screen,
        )
        draw_buttonutils(
            dark_red, red, 0.1, 0.6, 0.4, 0.06, poison_text, blockyfont, mouse, screen
        )
        draw_buttonutils(
            dark_red, red, 0.55, 0.6, 0.4, 0.06, gravity_text, blockyfont, mouse, screen
        )
        draw_buttonutils(
            dark_red, red, 0.55, 0.7, 0.4, 0.06, goback_text, blockyfont, mouse, screen
        )

        pygame.display.update()


def no_money_messaege(screen):
    """Displays a 'Not enough money' message for a short duration."""

    # Set up the font
    font_path = os.path.join(base_path, "extras", "Pixeboy.ttf")
    font = pygame.font.Font(font_path, 100)
    text = font.render("Not enough money", True, (255, 255, 255))
    text_rect = text.get_rect(center=(config.width // 2, config.height // 2))

    # Display the message for 120 frames
    for _ in range(75):
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(int(1000 / 60))  # Delay to maintain 60 FPS
