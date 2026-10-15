import window
import pygame
import random
from utils import wait_with_events
import os
from config import base_path, black, gold, green, red, white
from ui import TextCache, prompt_bet
import config
import sys


def blackjack(player):
 
    WIDTH = config.resolution[0]
    HEIGHT = config.resolution[1]
    screen = window.get_screen()
    pygame.display.set_caption("Blackjack")

    blockyfontpath = os.path.join(base_path, "extras", "Pixeboy.ttf")
    FONT = pygame.font.Font(blockyfontpath, int(WIDTH * 0.04))
    SMALL_FONT = pygame.font.Font(blockyfontpath, int(WIDTH * 0.03))
    renderers = {FONT: TextCache(FONT), SMALL_FONT: TextCache(SMALL_FONT)}

    SUITS = ["Spades", "Hearts", "Diamonds", "Clubs"]
    SUIT_COLORS = {"Spades": black, "Clubs": black, "Hearts": red, "Diamonds": red}
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def criar_deck():
        deck = [{"rank": rank, "suit": suit} for suit in SUITS for rank in RANKS]
        random.shuffle(deck)
        return deck

    def draw_text(text, x, y, font=FONT, color=white, center=False):
        """Draws text on the screen, with optional centering."""
        label = renderers[font].render(text, color)
        if center:
            x -= label.get_width() // 2  # Adjust x to center the text
        screen.blit(label, (x, y))

    def get_card_value(card):
        if card["rank"] in ("J", "Q", "K"):
            return 10
        elif card["rank"] == "A":
            return 11
        else:
            return int(card["rank"])

    def calculate_hand_value(hand):
        value = sum(get_card_value(card) for card in hand)
        aces = sum(1 for card in hand if card["rank"] == "A")
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def deal_card(deck):
        return deck.pop()

    def draw_card(card, x, y):
        card_width = WIDTH * 0.0547
        card_height = HEIGHT * 0.1389
        card_rect = pygame.Rect(x, y, card_width, card_height)
        pygame.draw.rect(screen, white, card_rect)
        pygame.draw.rect(screen, black, card_rect, 2)
        rank_text = renderers[SMALL_FONT].render(card["rank"], black)
        suit_color = SUIT_COLORS[card["suit"]]
        pygame.draw.circle(
            screen,
            suit_color,
            (x + card_width // 2, y + card_height * 0.65),
            card_width * 0.1429,
        )
        screen.blit(rank_text, (x + card_width * 0.0714, y + card_height * 0.05))

    def draw_hidden_card(x, y):
        card_width = WIDTH * 0.0547
        card_height = HEIGHT * 0.1389
        card_rect = pygame.Rect(x, y, card_width, card_height)
        pygame.draw.rect(screen, black, card_rect)
        pygame.draw.rect(screen, white, card_rect, 2)
        pygame.draw.line(screen, white, (x, y), (x + card_width, y + card_height), 4)

    def game_logic(player_hand, dealer_hand, player_stands, bet):
        player_value = calculate_hand_value(player_hand)
        dealer_value = calculate_hand_value(dealer_hand)

        if player_value > 21:
            player.coins -= bet
            return "You Bust! Dealer Wins!"
        elif dealer_value > 21:
            player.coins += bet
            return "Dealer Busts! You Win!"
        elif player_stands and dealer_value >= 17:
            if player_value > dealer_value:
                player.coins += bet
                return "You Win!"
            elif player_value < dealer_value:
                player.coins -= bet
                return "Dealer Wins!"
            else:
                return "It's a Tie!"
        return None

    running = True
    clock = pygame.time.Clock()

    def restart_game():
        deck = criar_deck()
        player_hand = [deal_card(deck), deal_card(deck)]
        dealer_hand = [deal_card(deck), deal_card(deck)]
        player_stands = False
        return deck, player_hand, dealer_hand, player_stands

    bet = prompt_bet(screen, player, SMALL_FONT)
    if bet is None:
        return
    deck, player_hand, dealer_hand, player_stands = restart_game()
    game_over_message = None

    while running:
        screen.fill(green)
        draw_text(f"Bet: ${bet}", WIDTH * 0.039, HEIGHT * 0.030, SMALL_FONT, gold)
        draw_text(
            f"Player: {calculate_hand_value(player_hand)}",
            WIDTH * 0.039,
            HEIGHT * 0.069,
        )
        draw_text(
            f"Money: ${player.coins}", WIDTH * 0.508, HEIGHT * 0.028, SMALL_FONT, gold
        )

        for i, card in enumerate(player_hand):
            draw_card(card, WIDTH * 0.039 + i * WIDTH * 0.0625, HEIGHT * 0.139)

        if player_stands:
            draw_text(
                f"Dealer: {calculate_hand_value(dealer_hand)}",
                WIDTH * 0.039,
                HEIGHT * 0.417,
            )
            for i, card in enumerate(dealer_hand):
                draw_card(card, WIDTH * 0.039 + i * WIDTH * 0.0625, HEIGHT * 0.486)
        else:
            draw_text("Dealer: ?", WIDTH * 0.039, HEIGHT * 0.417)
            draw_hidden_card(WIDTH * 0.039, HEIGHT * 0.486)
            draw_card(dealer_hand[1], WIDTH * 0.101, HEIGHT * 0.486)

        draw_text(
            "H to Hit | S to Stand | Esc To Return to Menu", 50, HEIGHT - 50, SMALL_FONT
        )

        if not game_over_message:
            game_over_message = game_logic(player_hand, dealer_hand, player_stands, bet)

        if game_over_message:
            draw_text(game_over_message, WIDTH // 2 - 200, HEIGHT // 2 - 50)
            window.present()
            wait_with_events(2000, player)
            player.save_progress()
            bet = prompt_bet(screen, player, SMALL_FONT)
            if bet is None:
                return
            deck, player_hand, dealer_hand, player_stands = restart_game()
            game_over_message = None

        for event in window.get_events():
            if event.type == pygame.QUIT:
                player.save_progress()
                running = False

            if event.type == pygame.KEYDOWN and not game_over_message:
                if event.key == pygame.K_h and not player_stands:
                    player_hand.append(deal_card(deck))
                elif event.key == pygame.K_s and not player_stands:
                    player_stands = True
                    while calculate_hand_value(dealer_hand) < 17:
                        dealer_hand.append(deal_card(deck))
                elif event.key == pygame.K_ESCAPE:
                    return

        window.present()
        clock.tick(30)

    pygame.quit()
    sys.exit()
