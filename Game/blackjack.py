import pygame
import random
import time
import os
from config import *
from player import Player
import config


def blackjack(player):
    pygame.init()

    width, height = config.resolution[0], config.resolution[1]

    WIDTH = config.resolution[0]
    HEIGHT = config.resolution[1]
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Blackjack")

    blockyfontpath = os.path.join(base_path, "extras", "Pixeboy.ttf")
    FONT = pygame.font.Font(blockyfontpath, int(WIDTH * 0.04))
    SMALL_FONT = pygame.font.Font(blockyfontpath, int(WIDTH * 0.03))

    SUITS = ["Spades", "Hearts", "Diamonds", "Clubs"]
    SUIT_COLORS = {"Spades": black, "Clubs": black, "Hearts": red, "Diamonds": red}
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def criar_deck():
        deck = [{"rank": rank, "suit": suit} for suit in SUITS for rank in RANKS]
        random.shuffle(deck)
        return deck

    def draw_text(text, x, y, font=FONT, color=white, center=False):
        """Draws text on the screen, with optional centering."""
        label = font.render(text, True, color)
        if center:
            x -= label.get_width() // 2  # Adjust x to center the text
        screen.blit(label, (x, y))

    def get_card_value(card):
        if card["rank"] in ["J", "Q", "K"]:
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
        rank_text = SMALL_FONT.render(card["rank"], True, black)
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

    deck, player_hand, dealer_hand, player_stands = restart_game()
    game_over_message = None
    bet = 0

    def set_bet():
        nonlocal bet
        bet = 0
        typing = True
        input_box_width = 200
        input_box_height = 40
        input_box = pygame.Rect(
            WIDTH // 2 - input_box_width // 2,
            HEIGHT // 2 - input_box_height // 2,
            input_box_width,
            input_box_height,
        )
        input_text = ""

        while typing:

            screen.fill(green)

            # Display available money
            draw_text(
                f"Available Money: ${player.coins}",
                WIDTH // 2,
                HEIGHT // 2 - 100,
                SMALL_FONT,
                gold,
                True,
            )
            draw_text(
                "Set your bet:", WIDTH // 2, HEIGHT // 2 - 50, SMALL_FONT, white, True
            )
            draw_text(
                "Press Enter to Confirm",
                WIDTH // 2,
                HEIGHT // 2 + 50,
                SMALL_FONT,
                white,
                True,
            )
            draw_text(
                "Type 0 to play just for fun",
                WIDTH // 2,
                HEIGHT // 2 + 100,
                SMALL_FONT,
                white,
                True,
            )

            pygame.draw.rect(screen, white, input_box)
            txt_surface = SMALL_FONT.render(input_text, True, black)
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            input_box.w = max(input_box_width, txt_surface.get_width() + 10)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if input_text.isdigit() and int(input_text) <= player.coins:
                            bet = int(input_text)
                            typing = False
                        else:
                            draw_text(
                                "Invalid Bet! Must be a number within available funds.",
                                WIDTH // 2 - 220,
                                HEIGHT // 2 + 70,
                                SMALL_FONT,
                                red,
                                True,
                            )
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        typing = (
                            False  # Exit the bet input screen without setting a bet.
                        )
                        return
                    else:
                        input_text += event.unicode

    set_bet()

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
            pygame.display.flip()
            time.sleep(2)
            set_bet()
            deck, player_hand, dealer_hand, player_stands = restart_game()
            game_over_message = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and not game_over_message:
                if event.key == pygame.K_h:
                    player_hand.append(deal_card(deck))
                elif event.key == pygame.K_s:
                    player_stands = True
                    while calculate_hand_value(dealer_hand) < 17:
                        dealer_hand.append(deal_card(deck))
                elif event.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
