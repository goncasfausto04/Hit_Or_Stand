import random
import pygame
import config
import os
from config import *
from player import Player


class TreasureChest(pygame.sprite.Sprite):
    def __init__(self, x, y, player, rewards):
        super().__init__()

        self.rewards = rewards  # list with 5 inputs
        self.weights = [0.3, 0.3, 0.2, 0.1, 0.1]  # Define weights for each reward
        self.cards = random.choices(
            self.rewards, weights=self.weights, k=3
        )  # Select 3 random rewards based on weights
        self.flipped_cards = [False, False, False]
        # Load the chest image
        image_path = os.path.join(base_path, "extras", "chest.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, chest_size
        )  # Scale to desired size
        self.player = player

        # Load the card image
        card_path = os.path.join(base_path, "extras", "card.png")
        self.card_image = pygame.image.load(card_path).convert_alpha()
        self.card_image = pygame.transform.scale(
            self.card_image, (100, 150)
        )  # Scale to desired size

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.card_size = (100, 150)
        self.player = player
        self.card_positions = [
            ((config.width * (1 / 3)) - 50, config.height * (1 / 2) - 75),
            ((config.width * (1 / 2)) - 50, config.height * (1 / 2) - 75),
            ((config.width * (2 / 3)) - 50, config.height * (1 / 2) - 75),
        ]  # Adjust these positions based on your screen size

    def flip_card(self, card_index):
        if 0 <= card_index < len(self.cards) and not self.flipped_cards[card_index]:
            self.flipped_cards[card_index] = True
            if self.cards[card_index] in ["100", "200", "300","400","500"]:
                self.player.coins += int(self.cards[card_index])
            elif self.cards[card_index] == "Dash":
                self.player.has_dash = True

            return self.cards[card_index]
        else:
            return None

    def draw_cards(self, screen):
        for i in range(3):
            if self.flipped_cards[i]:
                pygame.draw.rect(
                    screen, (255, 255, 255), (*self.card_positions[i], *self.card_size)
                )
                font = pygame.font.Font(None, 36)
                text_surface = font.render(self.cards[i], True, (0, 0, 0))
                coins_surface = font.render("Coins", True, (0, 0, 0))
                text_rect = text_surface.get_rect(
                    center=(
                        self.card_positions[i][0] + 50,
                        self.card_positions[i][1] + 75,
                    )
                )
                coins_rect = coins_surface.get_rect(
                    center=(
                        self.card_positions[i][0] + 50,
                        self.card_positions[i][1] + 100,
                    )
                )
                screen.blit(text_surface, text_rect)
                if self.cards[i] in ["100", "200", "300","400","500"]:
                    screen.blit(coins_surface, coins_rect)
            else:
                screen.blit(self.card_image, self.card_positions[i])

    def open_chest(self, screen, player):
        running = True
        last_loop = True

        while running or last_loop:
            # Clear screen
            self.draw_cards(screen)
            pygame.display.flip()

            if running == False and last_loop == True:
                last_loop = False
                pygame.time.wait(1500)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    player.save_progress()
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, pos in enumerate(self.card_positions):
                        card_rect = pygame.Rect(*pos, *self.card_size)
                        if (
                            card_rect.collidepoint(mouse_pos)
                            and not self.flipped_cards[i]
                        ):
                            self.flip_card(i)
                            if all(self.flipped_cards):
                                running = False
