"""A cached, readable credits scene in the game's pixel-art style."""
import os
import sys

import pygame

import config
import window


PROFESSORS = (
    ("Augusto Santos", "ajrsantos@novaims.unl.pt"),
    ("Diogo Rastreio", "drasteiro@novaims.unl.pt"),
    ("Liah Rosenfeld", "lrosenfeld@novaims.unl.pt"),
)
STUDENTS = (
    ("Goncalo Faustino", "20231721"),
    ("Bernardo Coelho", "20231736"),
    ("Henrique Esteves", "20231717"),
    ("Luis Duarte", "20231621"),
)
PROJECT_MESSAGE = (
    "This game was developed as a project for the course of Computation 3,",
    "we hope you enjoy the gameplay as much as we enjoyed developing it!",
)

_BACKGROUND = (17, 19, 23)
_PANEL = (26, 29, 35)
_BORDER = (47, 52, 61)
_TEXT = (245, 244, 241)
_MUTED = (164, 172, 185)
_ACCENT = (226, 112, 116)


def _build_scene():
    """Render the static scene and both button states once per visit."""
    scale = min(config.width / 1280, config.height / 720)
    font_path = os.path.join(config.base_path, "extras", "Pixeboy.ttf")
    fonts = {
        size: pygame.font.Font(font_path, max(1, round(size * scale)))
        for size in (24, 26, 30, 32, 64)
    }
    content = pygame.Surface(config.resolution).convert()
    content.fill(_BACKGROUND)

    def rect(x, y, width, height):
        return pygame.Rect(*(round(value * scale) for value in (x, y, width, height)))

    def label(text, size, color, position, alignment="topleft", target=content):
        rendered = fonts[size].render(text, True, color)
        bounds = rendered.get_rect()
        setattr(bounds, alignment, tuple(round(value * scale) for value in position))
        target.blit(rendered, bounds)
        return bounds

    # Keep decoration quiet so names remain the focus.
    pygame.draw.rect(content, (93, 43, 49), rect(0, 0, 1280, 5))
    label("COMPUTATION 3  /  CREDITS", 24, _ACCENT, (640, 53), "midtop")
    label("HIT OR STAND", 64, _TEXT, (640, 91), "midtop")
    label("Made by a small team. Built to be played.", 26, _MUTED, (640, 158), "midtop")

    panels = (rect(80, 216, 546, 294), rect(654, 216, 546, 294))
    for panel, title, count in zip(panels, ("Professors", "Students"), ("03", "04")):
        shadow = panel.move(0, round(5 * scale))
        pygame.draw.rect(content, (10, 12, 15), shadow, border_radius=round(10 * scale))
        pygame.draw.rect(content, _PANEL, panel, border_radius=round(10 * scale))
        pygame.draw.rect(content, _BORDER, panel, max(1, round(scale)), border_radius=round(10 * scale))
        left = panel.left / scale
        right = panel.right / scale
        label(title, 32, _TEXT, (left + 28, 239))
        label(count, 26, _ACCENT, (right - 28, 243), "topright")
        pygame.draw.line(content, _BORDER,
                         (panel.left + round(28 * scale), round(281 * scale)),
                         (panel.right - round(28 * scale), round(281 * scale)))

    for index, (name, email) in enumerate(PROFESSORS):
        y = 300 + index * 65
        label(name, 32, _TEXT, (108, y))
        label(email, 24, _MUTED, (108, y + 30))

    for index, (name, student_id) in enumerate(STUDENTS):
        y = 307 + index * 46
        label(name, 32, _TEXT, (682, y))
        label(student_id, 26, _MUTED, (1172, y + 4), "topright")

    for index, line in enumerate(PROJECT_MESSAGE):
        label(line, 26, _MUTED, (640, 541 + index * 27), "midtop")

    back_rect = rect(500, 618, 280, 56)
    buttons = []
    for fill, border in (((53, 32, 38), (118, 58, 66)), ((86, 39, 48), _ACCENT)):
        button = pygame.Surface(back_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(button, fill, button.get_rect(), border_radius=round(8 * scale))
        pygame.draw.rect(button, border, button.get_rect(), max(1, round(scale)), border_radius=round(8 * scale))
        label("Back to menu", 30, _TEXT, (114, 29), "center", button)
        badge = rect(220, 16, 44, 24)
        pygame.draw.rect(button, (31, 26, 32), badge, border_radius=round(3 * scale))
        label("ESC", 24, _MUTED, (242, 28), "center", button)
        buttons.append(button)
    return content, back_rect, buttons


def credits_():
    """Show the credits until Back or Escape, using logical window coordinates."""
    screen = window.get_screen()
    content, back_rect, buttons = _build_scene()
    chime = pygame.mixer.Sound(os.path.join(config.base_path, "extras", "chime1.mp3"))
    chime.set_volume(config.music_volume)
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        for event in window.get_events():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                    and back_rect.collidepoint(event.pos)):
                chime.play()
                return

        screen.blit(content, (0, 0))
        hovered = back_rect.collidepoint(window.mouse_position())
        screen.blit(buttons[hovered], back_rect)
        window.present()
