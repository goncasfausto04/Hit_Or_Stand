import pygame
import os
import cv2
from config import *
import config
import sys
import json


def pause_game(screen, width, height,player):
    """Pauses the game and displays a 'Paused' message."""

    # Set up the font
    font_path = os.path.join(base_path, "extras", "Pixeboy.ttf")
    font = pygame.font.Font(font_path, 100)
    font1 = pygame.font.Font(font_path, 50)
    text = font.render("Paused", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    main_menu = font1.render("Main Menu", True, (255, 255, 255))

    # Display the 'Paused' message
    screen.blit(text, text_rect)

    import interface

    # Infinite loop until the user unpauses
    while True:
        draw_buttonutils(dark_red, red, 0.4, 0.6, 0.2, 0.1 ,main_menu, font1, pygame.mouse.get_pos(), screen)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_clicked(0.4, 0.6, 0.2, 0.1, pygame.mouse.get_pos()):
                    player.save_progress()
                    interface.interface()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()

                


def play_video(video_path, resolution, sound_path):
    """Play a video using Pygame and OpenCV."""

    # Initialize Pygame
    pygame.init()

    # Load the video using OpenCV
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Set up the Pygame window
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Video Player")

    # Main loop
    running = True
    clock = pygame.time.Clock()

    # play sound
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()

    pygame.display.set_caption("Hit or Stand")

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if (
                    event.key == pygame.K_ESCAPE
                    or event.key == pygame.K_RETURN
                    or event.key == pygame.K_SPACE
                ):
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame to fit the resolution
        frame = cv2.resize(frame, resolution)

        # Convert the frame to RGB format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.rotate(frame, -90)
        frame = pygame.transform.flip(frame, True, False)

        # Display the frame
        screen.blit(frame, (0, 0))
        pygame.display.update()

        # Control the frame rate
        clock.tick(fps)

    # Clean up
    cap.release()


base_path = os.path.dirname(__file__)
video_path = os.path.join(base_path, "extras", "intro.mp4")
sound_path = os.path.join(base_path, "extras", "wind.mp3")


def render_text_wrapped_from_surface(screen, text, font, color, x, y, max_width):
    """Renders text dynamically across multiple lines if it exceeds max_width."""

    words = text.split()  # Split the text into individual words
    lines = []  # Store lines of text
    current_line = ""  # Current line being built

    for word in words:
        # Check if adding the next word exceeds the maximum width
        if font.size(current_line + word)[0] <= max_width:
            current_line += word + " "
        else:
            lines.append(current_line)  # Save the current line
            current_line = word + " "  # Start a new line

    # Add the last line if there’s leftover text
    if current_line:
        lines.append(current_line)

    # Render each line of text
    for i, line in enumerate(lines):
        line_surface = font.render(line, True, color)
        screen.blit(
            line_surface, (x, y + i * font.size(line)[1])
        )  # Offset each line by its height


def button_clicked(x_frac, y_frac, w_frac, h_frac, mouse):
    x = config.width * x_frac
    y = config.height * y_frac
    w = config.width * w_frac
    h = config.height * h_frac
    return x <= mouse[0] <= x + w and y <= mouse[1] <= y + h


def draw_buttonutils(
    color, hover_color, x_frac, y_frac, w_frac, h_frac, text, font, mouse, screen
):
    x = config.width * x_frac
    y = config.height * y_frac
    w = config.width * w_frac
    h = config.height * h_frac
    current_color = (
        hover_color if button_clicked(x_frac, y_frac, w_frac, h_frac, mouse) else color
    )

    # Draw rounded rectangle for the button
    pygame.draw.rect(screen, current_color, [x, y, w, h], border_radius=10)

    # Draw border for the button
    border_color = (
        white if button_clicked(x_frac, y_frac, w_frac, h_frac, mouse) else black
    )
    pygame.draw.rect(screen, border_color, [x, y, w, h], 2, border_radius=10)

    # Draw the text on the button
    text_rect = text.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text, text_rect)


def prompt(screen, width, height, content):

    # Set up the font
    font_path = os.path.join(base_path, "extras", "Pixeboy.ttf")
    font = pygame.font.Font(font_path, 25)
    text = font.render(content, True, (0, 0, 0))  # Black text
    text_rect = text.get_rect(center=(width // 2, height // 2))

    # Define the background box (padding around the text)
    box_padding = 20
    box_rect = pygame.Rect(
        text_rect.left - box_padding,
        text_rect.top - box_padding,
        text_rect.width + 2 * box_padding,
        text_rect.height + 2 * box_padding,
    )

    # Draw the box with white fill and black outline
    pygame.draw.rect(screen, (255, 255, 255), box_rect)  # White box
    pygame.draw.rect(screen, (0, 0, 0), box_rect, 3)  # Black outline (3 px thick)

    # Draw the text on top of the box
    screen.blit(text, text_rect)
    pygame.display.flip()

    # Infinite loop until the user unpauses
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and (
                event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN
            ):
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                exit()


def draw_text(screen, text, x, y, font, color=white, center=False):
    """Draws text on the screen, with optional centering."""
    label = font.render(text, True, color)
    if center:
        x -= label.get_width() // 2  # Adjust x to center the text
    screen.blit(label, (x, y))


def draw_text_with_outline(surface, text, x, y, color, outline_color, font):
    """Draws text with an outline."""
    text_surface = font.render(text, True, color)
    outline_surface = font.render(text, True, outline_color)
    for dx in [-1, 1]:
        for dy in [-1, 1]:
            surface.blit(outline_surface, (x + dx, y + dy))
    surface.blit(text_surface, (x, y))



def handle_collision(player, collision_rects):
    for rect in collision_rects:
        if player.rect.colliderect(rect):
            # Resolve collision by checking movement direction
            dx = player.rect.centerx - rect.centerx
            dy = player.rect.centery - rect.centery

            if abs(dx) > abs(dy):  # Horizontal collision
                if dx > 0:  # Colliding from the left
                    player.rect.left = rect.right
                else:  # Colliding from the right
                    player.rect.right = rect.left
            else:  # Vertical collision
                if dy > 0:  # Colliding from above
                    player.rect.top = rect.bottom
                else:  # Colliding from below
                    player.rect.bottom = rect.top

def reset_progress():
        """Reset progress to default values."""
        if os.name == 'nt':  # Windows
            save_dir = os.path.join(os.getenv('APPDATA'), ".hitorstand")
        else:  # macOS/Linux
            save_dir = os.path.expanduser("~/.hitorstand")
        
        # Ensure the directory exists
        os.makedirs(save_dir, exist_ok=True)

        save_location = os.path.join(save_dir, "player_progress.json")

        # Define default progress data
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

        # Save the default data to the save file
        with open(save_location, "w") as file:
            json.dump(default_data, file)
        
        print(f"Progress reset to default and saved to {save_location}")

def draw_fps(screen, clock):
    """Draw the FPS (frames per second) on the screen."""
    font=pygame.font.Font(None, 25)
    fps = int(clock.get_fps())
    draw_text(screen, f"FPS: {fps}", 2, config.height*0.97, font, white)

