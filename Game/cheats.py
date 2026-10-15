"""Recognize hidden keyboard codes without consuming normal game input."""
from contextlib import contextmanager

import pygame

from progress import read_progress, write_progress

CODE = "motherload"
REWARD = 10_000
_prefix = ""
_active_player = None


def set_player(player):
    """Use a live player's balance while their game session is running."""
    global _active_player, _prefix
    _active_player = player
    _prefix = ""


@contextmanager
def player_session(player):
    """Restore the previous recipient even when a scene exits unexpectedly."""
    previous = _active_player
    set_player(player)
    try:
        yield
    finally:
        set_player(previous)


def _award_tokens():
    if _active_player is not None:
        _active_player.coins += REWARD
        _active_player.save_progress()
    else:
        progress = read_progress()
        progress["coins"] += REWARD
        write_progress(progress)


def process_event(event):
    """Award once per complete code, leaving every event available to its scene."""
    global _prefix
    if event.type == pygame.WINDOWFOCUSLOST:
        _prefix = ""
        return False
    if event.type != pygame.KEYDOWN or getattr(event, "repeat", False):
        return False
    if (
        getattr(event, "key", None) in (pygame.K_ESCAPE, pygame.K_BACKSPACE)
        or getattr(event, "mod", 0) & (pygame.KMOD_CTRL | pygame.KMOD_ALT | pygame.KMOD_GUI)
    ):
        _prefix = ""
        return False

    awarded = False
    for character in getattr(event, "unicode", "").casefold():
        _prefix += character
        while _prefix and not CODE.startswith(_prefix):
            _prefix = _prefix[1:]
        if _prefix == CODE:
            _prefix = ""
            _award_tokens()
            awarded = True
    return awarded
