"""Scale the whole game canvas to a resizable native window.

Game coordinates stay fixed, while rendering and mouse input use inverse
transforms. All scenes share the canvas, including across fullscreen changes.
"""
import pygame
from pygame._sdl2.video import Window
import config

_screen = None
_display = None
_fullscreen = False
_windowed_size = config.resolution
_scaled_frame = None
_resize_drag = None
_native_window = None
_pending_size = None
_cursor = None


def get_screen():
    global _screen, _display, _fullscreen, _scaled_frame, _resize_drag
    global _native_window, _pending_size, _cursor
    if _screen is None or pygame.display.get_surface() is None:
        _display = pygame.display.set_mode(_windowed_size, 0)
        _native_window = Window.from_display_module()
        _pending_size = None
        _cursor = None
        _screen = pygame.Surface(config.resolution).convert()
        _fullscreen = False
        _resize_drag = None
        _scaled_frame = None
        pygame.display.set_caption("Hit or Stand")
    return _screen


def is_fullscreen():
    return _fullscreen


def toggle_fullscreen():
    """Change only the native display; scene references to the canvas stay valid."""
    global _display, _fullscreen, _windowed_size, _scaled_frame, _resize_drag
    global _native_window, _pending_size
    get_screen()
    _resize_drag = None
    _pending_size = None
    size = pygame.display.get_window_size()
    target_fullscreen = not _fullscreen
    try:
        display = pygame.display.set_mode(
            (0, 0) if target_fullscreen else _windowed_size,
            pygame.FULLSCREEN if target_fullscreen else 0,
        )
    except pygame.error:
        return False
    if target_fullscreen:
        _windowed_size = size
    _display = display
    _native_window = Window.from_display_module()
    if not target_fullscreen:
        # SDL may ignore set_mode's size until it has left fullscreen.
        _native_window.size = _windowed_size
        _display = pygame.display.get_surface()
    _fullscreen = target_fullscreen
    _scaled_frame = None
    return True


def corner_rect():
    """A visible in-window grip, separate from the operating system's border."""
    width, height = pygame.display.get_window_size()
    return pygame.Rect(width - 36, height - 36, 36, 36)


def proportional_size(size, previous_size=None):
    """Project the corner position onto the 16:9 diagonal with a usable minimum."""
    units = max(40, round((size[0] * 16 + size[1] * 9) / 337))
    return (units * 16, units * 9)


def resize_window(size):
    """Resize the same SDL window, preserving focus, pointer capture and canvas."""
    global _display, _windowed_size, _scaled_frame
    if _fullscreen or min(size) <= 0:
        return
    target = proportional_size(size)
    if target != pygame.display.get_window_size():
        _native_window.size = target
        _display = pygame.display.get_surface()
        _scaled_frame = None
    _windowed_size = pygame.display.get_window_size()


def handle_corner_drag(event):
    """Track raw window pixels before converting pointer events for the game."""
    global _resize_drag, _pending_size
    if _fullscreen:
        return False
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if corner_rect().collidepoint(event.pos):
            _resize_drag = (event.pos, pygame.display.get_window_size())
            return True
    if _resize_drag is not None:
        if event.type == pygame.WINDOWFOCUSLOST:
            _resize_drag = None
            _pending_size = None
        elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP):
            if event.type == pygame.MOUSEBUTTONUP and event.button != 1:
                return False
            start, size = _resize_drag
            _pending_size = (size[0] + event.pos[0] - start[0],
                             size[1] + event.pos[1] - start[1])
            if event.type == pygame.MOUSEBUTTONUP:
                _resize_drag = None
            return True
    return False


def update_cursor():
    global _cursor
    over_grip = not _fullscreen and corner_rect().collidepoint(pygame.mouse.get_pos())
    cursor = pygame.SYSTEM_CURSOR_SIZENWSE if over_grip or _resize_drag else pygame.SYSTEM_CURSOR_ARROW
    if cursor != _cursor:
        try:
            pygame.mouse.set_cursor(cursor)
        except pygame.error:
            pass  # Headless video drivers may not provide system cursors.
        _cursor = cursor


def viewport(window_size=None):
    """Fit the canvas uniformly, including on monitors with another aspect ratio."""
    width, height = window_size or pygame.display.get_window_size()
    scale = min(width / config.width, height / config.height)
    size = (max(1, round(config.width * scale)), max(1, round(config.height * scale)))
    return pygame.Rect((width - size[0]) // 2, (height - size[1]) // 2, *size)


def to_game_position(position, window_size=None):
    """Inverse of the uniform presentation transform, including viewport offset."""
    view = viewport(window_size)
    if not view.collidepoint(position):
        return (-1, -1)
    return (int((position[0] - view.x) * config.width / view.width),
            int((position[1] - view.y) * config.height / view.height))


def mouse_position():
    return to_game_position(pygame.mouse.get_pos())


def present():
    """Scale the game and UI uniformly, without stretching."""
    global _display, _scaled_frame
    get_screen()
    _display = pygame.display.get_surface()
    view = viewport(_display.get_size())
    size = view.size
    _display.fill((0, 0, 0))
    if size == _screen.get_size():
        _display.blit(_screen, view.topleft)
    else:
        if _scaled_frame is None or _scaled_frame.get_size() != size:
            _scaled_frame = pygame.Surface(size).convert()
        pygame.transform.scale(_screen, size, _scaled_frame)
        _display.blit(_scaled_frame, view.topleft)
    if not _fullscreen:
        grip = corner_rect()
        pygame.draw.rect(_display, (40, 45, 52), grip)
        for inset in (8, 16, 24):
            pygame.draw.line(_display, (230, 230, 230),
                             (grip.right - inset, grip.bottom - 3),
                             (grip.right - 3, grip.bottom - inset), 2)
    update_cursor()
    pygame.display.flip()


def get_events():
    """Handle global shortcuts and translate pointer events to game coordinates."""
    global _pending_size
    events = []
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and (
            event.key == pygame.K_F11
            or (event.key == pygame.K_RETURN and getattr(event, "mod", 0) & pygame.KMOD_ALT)
        ):
            toggle_fullscreen()
            continue
        if handle_corner_drag(event):
            continue
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            data = event.dict.copy()
            if 'pos' in data:
                data['pos'] = to_game_position(data['pos'])
            if 'rel' in data:
                view = viewport()
                data['rel'] = (round(data['rel'][0] * config.width / view.width),
                               round(data['rel'][1] * config.height / view.height))
            event = pygame.event.Event(event.type, data)
        events.append(event)
    if _pending_size is not None:
        resize_window(_pending_size)
        _pending_size = None
    update_cursor()
    return events
