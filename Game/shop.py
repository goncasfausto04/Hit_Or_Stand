"""Shops share one catalog renderer and purchase flow."""
import os
import sys

import pygame

import config
import window
from assets import load_image
from ui import TextCache
from utils import button_clicked, draw_buttonutils, wait_with_events


WEAPONS = (
    ("Shatterblast", 1500),
    ("Arcane Cascade", 2500),
    ("Rebound Rune", 3500),
    ("Astral Beam", 4000),
)
PETS = (("Dog", 100), ("Cat", 600), ("Crab", 600))
PET_IMAGES = {
    "Dog": "dog_pet_comp.png",
    "Cat": "cat_pet_comp.png",
    "Crab": "Crab_pet_comp.png",
}


def shop(player):
    screen = window.get_screen()
    font = pygame.font.Font(
        os.path.join(config.base_path, "extras", "Pixeboy.ttf"),
        int(config.height * 0.035),
    )
    background = load_image(
        os.path.join(config.base_path, "extras", "loja.jpeg"), config.resolution
    )
    buttons = (
        ((0.125, 0.333, 0.125, 0.083), font.render("Spells Shop", True, config.white), weapons_shop),
        ((0.125, 0.5, 0.125, 0.083), font.render("Pet Shop", True, config.white), pet_shop),
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
                return "shedshop"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for bounds, _, action in buttons:
                    if button_clicked(*bounds, event.pos):
                        if action is None:
                            return "shedshop"
                        action(player)
                        break
        screen.blit(background, (0, 0))
        for bounds, label, _ in buttons:
            draw_buttonutils(
                config.dark_red, config.red, *bounds, label, font, mouse, screen
            )
        window.present()


def weapons_shop(player):
    _catalog_shop(player, WEAPONS, "weapons_purchased", "weaponshop.png")


def pet_shop(player):
    _catalog_shop(player, PETS, "pets_purchased", "petshop.png", equip_pet=True)


def _catalog_shop(player, items, purchased_attribute, background_name, equip_pet=False):
    screen = window.get_screen()
    font = pygame.font.Font(
        os.path.join(config.base_path, "extras", "Pixeboy.ttf"),
        int(config.height * 0.035),
    )
    text = TextCache(font)
    background = load_image(
        os.path.join(config.base_path, "extras", background_name), config.resolution
    )
    buttons = tuple(
        (name, price, (0.1, 0.2 + index * 0.16, 0.4, 0.06))
        for index, (name, price) in enumerate(items)
    )
    back_bounds = (0.1, 0.2 + len(items) * 0.16, 0.4, 0.06)
    purchased = getattr(player, purchased_attribute)
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
                return
            if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
                continue
            if button_clicked(*back_bounds, event.pos):
                return
            for name, price, bounds in buttons:
                if not button_clicked(*bounds, event.pos):
                    continue
                if name not in purchased:
                    if player.coins < price:
                        no_money_message(screen, player)
                        break
                    player.coins -= price
                    purchased.append(name)
                    player.save_progress()
                if equip_pet:
                    config.pet_image = PET_IMAGES[name]
                    config.pet_image_change = True
                break

        screen.blit(background, (0, 0))
        screen.blit(
            text.render(f"Money: ${player.coins}"),
            (config.width * 0.05, config.height * 0.05),
        )
        for name, price, bounds in buttons:
            if name in purchased:
                label = name if equip_pet else f"{name} - Purchased"
            else:
                label = f"{name} - ${price}"
            draw_buttonutils(
                config.dark_red, config.red, *bounds, text.render(label), font, mouse, screen
            )
        draw_buttonutils(
            config.dark_red, config.red, *back_bounds,
            text.render("Go Back"), font, mouse, screen,
        )
        window.present()


def no_money_message(screen, player):
    font = pygame.font.Font(os.path.join(config.base_path, "extras", "Pixeboy.ttf"), 100)
    text = font.render("Not enough money", True, config.white)
    screen.blit(text, text.get_rect(center=(config.width // 2, config.height // 2)))
    window.present()
    wait_with_events(1250, player)
