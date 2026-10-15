"""Shared immutable image surfaces; callers must not modify cached surfaces."""
from functools import lru_cache
import pygame


@lru_cache(maxsize=256)
def load_image(path, size=None):
    image = pygame.image.load(path).convert_alpha()
    if size is not None:
        image = pygame.transform.scale(image, size)
    return image
