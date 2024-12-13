import pygame
import os
import cv2
from config import *
import config


# Function to draw a stick figure with a construction hat
def draw_stick_figure_with_hat(screen, x, y):
    # head
    pygame.draw.circle(screen, (255, 255, 255), (x, y), 20, 2)  # White head outline

    # body
    pygame.draw.line(screen, (255, 255, 255), (x, y + 20), (x, y + 60), 2)  # Body

    # arms
    pygame.draw.line(
        screen, (255, 255, 255), (x, y + 40), (x - 30, y + 40), 2
    )  # Left arm
    pygame.draw.line(
        screen, (255, 255, 255), (x, y + 40), (x + 30, y + 40), 2
    )  # Right arm

    # legs
    pygame.draw.line(
        screen, (255, 255, 255), (x, y + 60), (x - 20, y + 100), 2
    )  # Left leg
    pygame.draw.line(
        screen, (255, 255, 255), (x, y + 60), (x + 20, y + 100), 2
    )  # Right leg

    # hat
    hat_color = (255, 215, 0)

    # drawing the construction hat
    pygame.draw.rect(screen, hat_color, [x - 25, y - 30, 50, 10])  # Hat's brim
    pygame.draw.rect(screen, hat_color, [x - 20, y - 40, 40, 20])  # Hat's dome


# Function to draw a normal stick figure (without a hat)
def draw_normal_stick_figure(screen, x, y):
    # head
    pygame.draw.circle(screen, (255, 255, 255), (x, y), 20, 2)  # White head outline

    # body
    pygame.draw.line(screen, (255, 255, 255), (x, y + 20), (x, y + 60), 2)  # Body

    # arms
    pygame.draw.line(
        screen, (255, 255, 255), (x, y + 40), (x - 30, y + 40), 2
    )  # Left arm
    pygame.draw.line(
        screen, (255, 255, 255), (x, y + 40), (x + 30, y + 40), 2
    )  # Right arm

    # legs
    pygame.draw.line(
        screen, (255, 255, 255), (x, y + 60), (x - 20, y + 100), 2
    )  # Left leg
    pygame.draw.line(
        screen, (255, 255, 255), (x, y + 60), (x + 20, y + 100), 2
    )  # Right leg


def under_construction():

    # creating the screen at 720x720 pixels
    screen = pygame.display.set_mode(config.resolution)

    # setting up the fonts
    corbelfont = pygame.font.SysFont("Corbel", 50)
    conversationfont = pygame.font.SysFont("Ariel", 25)

    # setting my texts:
    back_text = corbelfont.render("Back", True, white)
    construction_text = corbelfont.render("Under Construction", True, white)
    first_speech = conversationfont.render("Can we fix it?", True, white)
    second_speech = conversationfont.render("Probably not...", True, white)

    # setting up the "images" positions
    bob_x_position = 460
    bob_y_position = 450

    normal_x_position = 260
    normal_y_position = 450

    # same old, same old while true loop

    while True:
        # getting the mouse position
        mouse = pygame.mouse.get_pos()

        # event detection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # checking if the user clicked the back button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 450 <= mouse[0] <= 590 and 600 <= mouse[1] <= 660:
                    return

        # displaying the screen
        screen.fill(deep_black)

        # displaying the main UNDER CONSTRUCTION text
        construction_rect = construction_text.get_rect(center=(760 // 2, 300))
        screen.blit(construction_text, construction_rect)

        # drawing the back button
        pygame.draw.rect(screen, dark_red, [450, 600, 140, 60])
        back_rect = back_text.get_rect(center=(450 + 140 // 2, 600 + 60 // 2))
        screen.blit(back_text, back_rect)

        # stick figures text and "images"
        draw_normal_stick_figure(screen, normal_x_position, normal_y_position)
        draw_stick_figure_with_hat(screen, bob_x_position, bob_y_position)

        screen.blit(first_speech, (normal_x_position - 60, normal_y_position - 80))
        screen.blit(second_speech, (bob_x_position - 60, bob_y_position - 80))

        # finally, as always, updating the screen
        pygame.display.update()


def pause_game(screen, width, height):
    """Pauses the game and displays a 'Paused' message."""

    # Set up the font
    font_path = os.path.join(base_path, "extras", "Pixeboy.ttf")
    font = pygame.font.Font(font_path, 100)
    text = font.render("Paused", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height // 2))

    # Display the 'Paused' message
    screen.blit(text, text_rect)
    pygame.display.flip()

    # Infinite loop until the user unpauses
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


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
