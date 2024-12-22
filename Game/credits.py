import pygame
import os
from utils import *
import config


def credits_():
    """Displays the credits screen of the game."""

    screen = pygame.display.set_mode(config.resolution)

    blockyfontpath = os.path.join(base_path, "extras", "Pixeboy.ttf")
    blockyfont = pygame.font.Font(blockyfontpath, int(config.height * 0.05))

    chime = os.path.join(base_path, "extras", "chime1.mp3")
    chime_sound = pygame.mixer.Sound(chime)

    professors_text = blockyfont.render("Professors:", True, white)
    augusto_text = blockyfont.render(
        "Augusto Santos, ajrsantos@novaims.unl.pt", True, white
    )
    diogo_text = blockyfont.render(
        "Diogo Rastreio, drasteiro@novaims.unl.pt", True, white
    )
    liah_text = blockyfont.render(
        "Liah Rosenfeld, lrosenfeld@novaims.unl.pt", True, white
    )

    students_text = blockyfont.render("Students:", True, white)
    goncalo_text = blockyfont.render("Goncalo Faustino 20231721", True, white)
    bernardo_text = blockyfont.render("Bernardo Coelho 20231736", True, white)
    henrique_text = blockyfont.render("Henrique Esteves 20231717", True, white)
    luis_text = blockyfont.render("Luis Duarte 20231621", True, white)

    body_text = "This game was developed as a project for the course of Computation 3, we hope you envjoy the gameplay as much we enjoyed to develop it!"

    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (
                    config.width * 0.625 <= mouse[0] <= config.width * 0.75
                    and config.height * 0.833 <= mouse[1] <= config.height * 0.916
                ):
                    chime_sound.play()
                    return

        screen.fill(deep_black)
        screen.blit(professors_text, (config.width * 0.1, config.height * 0.07))
        screen.blit(augusto_text, (config.width * 0.1, config.height * 0.13))
        screen.blit(diogo_text, (config.width * 0.1, config.height * 0.19))
        screen.blit(liah_text, (config.width * 0.1, config.height * 0.25))

        screen.blit(students_text, (config.width * 0.1, config.height * 0.4))
        screen.blit(goncalo_text, (config.width * 0.1, config.height * 0.46))
        screen.blit(bernardo_text, (config.width * 0.1, config.height * 0.52))
        screen.blit(henrique_text, (config.width * 0.1, config.height * 0.58))
        screen.blit(luis_text, (config.width * 0.1, config.height * 0.64))

        render_text_wrapped_from_surface(
            screen,
            body_text,
            blockyfont,
            white,
            x=config.width * 0.1,
            y=config.height * 0.71,
            max_width=config.width * 0.8,
        )
        draw_buttonutils(
            dark_red,
            glowing_light_red,
            0.625,
            0.833,
            0.125,
            0.083,
            blockyfont.render("Back", True, white),
            blockyfont,
            mouse,
            screen,
        )

        pygame.display.update()
