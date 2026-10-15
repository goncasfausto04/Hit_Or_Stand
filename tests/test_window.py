"""Headless regression checks: python -m unittest discover -s tests."""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import warnings

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'Game'))
import pygame
import config
import window


class WindowTests(unittest.TestCase):
    def setUp(self):
        window._windowed_size = config.resolution
        pygame.init()
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            self.screen = window.get_screen()
        pygame.event.clear()

    def tearDown(self):
        pygame.quit()

    def test_scene_changes_reuse_display(self):
        with patch.object(pygame.display, 'set_mode') as create:
            self.assertIs(window.get_screen(), self.screen)
            create.assert_not_called()

    def test_resize_preserves_game_geometry_and_surface(self):
        original = (config.width, config.height, config.player_size, config.enemy_size)
        for size in ((960, 540), (1600, 900), (1000, 800)):
            event = pygame.event.Event(pygame.VIDEORESIZE, size=size, w=size[0], h=size[1])
            pygame.event.post(event)
            self.assertIn(event, window.get_events())
            self.assertIs(window.get_screen(), self.screen)
            self.assertEqual(self.screen.get_size(), config.resolution)
            self.assertEqual(original, (config.width, config.height,
                                        config.player_size, config.enemy_size))
            window.present()

    def test_creates_native_resizable_window(self):
        pygame.display.quit()
        pygame.display.init()
        with patch.object(pygame.display, 'set_mode', wraps=pygame.display.set_mode) as create:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                window.get_screen()
            create.assert_called_once_with(window._windowed_size, 0)

    def test_presentation_fills_window_and_maps_pointer(self):
        for size in ((960, 540), (1600, 900), (1000, 800)):
            pygame.display.set_mode(size, pygame.RESIZABLE)
            self.screen.fill((30, 70, 110))
            pygame.draw.rect(self.screen, (220, 90, 40), (640, 360, 640, 360))
            window.present()
            display = pygame.display.get_surface()
            self.assertEqual(display.get_size(), size)
            view = window.viewport(size)
            self.assertEqual(tuple(display.get_at(view.topleft))[:3], (30, 70, 110))
            self.assertEqual(tuple(display.get_at((view.right-45, view.bottom-45)))[:3], (220, 90, 40))
            self.assertAlmostEqual(view.width / view.height, 16 / 9, delta=0.005)
            if view.top > 0:
                self.assertEqual(tuple(display.get_at((0, 0)))[:3], (0, 0, 0))
                self.assertEqual(window.to_game_position((0, 0)), (-1, -1))
            center = (size[0] // 2, size[1] // 2)
            self.assertEqual(window.to_game_position(center), (640, 360))
            with patch.object(pygame.mouse, 'get_pos', return_value=center):
                self.assertEqual(window.mouse_position(), (640, 360))
            click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=center, button=1)
            pygame.event.clear()
            pygame.event.post(click)
            translated = window.get_events()
            self.assertEqual(translated[0].pos, (640, 360))

    def test_corner_drag_resizes_proportionally_and_consumes_clicks(self):
        start = (config.width - 5, config.height - 5)
        events = [pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=start, button=1),
                  pygame.event.Event(pygame.MOUSEMOTION, pos=(start[0]+320, start[1]+180), rel=(320,180)),
                  pygame.event.Event(pygame.MOUSEBUTTONUP, pos=(1595,895), button=1)]
        with patch.object(pygame.event, 'get', return_value=events):
            self.assertEqual(window.get_events(), [])
        self.assertEqual(pygame.display.get_window_size(), (1600, 900))
        self.assertIs(window.get_screen(), self.screen)
        self.assertIsNone(window._resize_drag)

    def test_drag_across_frames_keeps_native_window_and_focus(self):
        native_id = window._native_window.id
        start = (1270, 710)
        batches = [
            [pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=start, button=1)],
            [pygame.event.Event(pygame.MOUSEMOTION, pos=(1430, 800), rel=(160,90))],
            [pygame.event.Event(pygame.MOUSEMOTION, pos=(1590, 890), rel=(160,90))],
            [pygame.event.Event(pygame.MOUSEMOTION, pos=(1110, 620), rel=(-480,-270))],
            [pygame.event.Event(pygame.MOUSEBUTTONUP, pos=(1110, 620), button=1)],
        ]
        sizes = [(1280,720), (1440,810), (1600,900), (1120,630), (1120,630)]
        with patch.object(pygame.display, 'set_mode', wraps=pygame.display.set_mode) as recreate:
            for events, expected in zip(batches, sizes):
                with patch.object(pygame.event, 'get', return_value=events):
                    self.assertEqual(window.get_events(), [])
                window.present()
                self.assertEqual(pygame.display.get_window_size(), expected)
                self.assertEqual(pygame.display.get_surface().get_size(), expected)
                self.assertEqual(window._native_window.id, native_id)
                self.assertIs(window.get_screen(), self.screen)
            recreate.assert_not_called()
        self.assertIsNone(window._resize_drag)

    def test_focus_loss_cancels_pending_resize(self):
        events = [pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(1270,710), button=1),
                  pygame.event.Event(pygame.MOUSEMOTION, pos=(1590,890), rel=(320,180)),
                  pygame.event.Event(pygame.WINDOWFOCUSLOST)]
        with patch.object(pygame.event, 'get', return_value=events):
            window.get_events()
        self.assertIsNone(window._resize_drag)
        self.assertEqual(pygame.display.get_window_size(), (1280,720))

    def test_resize_then_fullscreen_restores_last_size(self):
        window.resize_window((960,540))
        self.assertTrue(window.toggle_fullscreen())
        window.resize_window((1600,900))
        self.assertTrue(window.toggle_fullscreen())
        self.assertEqual(pygame.display.get_window_size(), (960,540))
        window.resize_window((1120,630))
        self.assertEqual(pygame.display.get_window_size(), (1120,630))

    def test_sides_do_not_start_resize_and_notifications_do_not_snap(self):
        for pos in ((1279, 360), (640, 719), (1, 360)):
            event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pos, button=1)
            self.assertFalse(window.handle_corner_drag(event))
            self.assertIsNone(window._resize_drag)
        with patch.object(pygame.display, 'set_mode') as resize:
            with patch.object(pygame.event, 'get', return_value=[
                pygame.event.Event(pygame.WINDOWSIZECHANGED, x=1500, y=720)
            ]):
                window.get_events()
            resize.assert_not_called()

    def test_fullscreen_round_trip_reuses_surface(self):
        with patch.object(pygame.display, 'set_mode', wraps=pygame.display.set_mode):
            self.assertTrue(window.toggle_fullscreen())
            self.assertTrue(window.is_fullscreen())
            self.assertIs(window.get_screen(), self.screen)
            self.assertTrue(window.toggle_fullscreen())
            self.assertFalse(window.is_fullscreen())

    def test_failed_toggle_does_not_change_state(self):
        with patch.object(pygame.display, 'set_mode', side_effect=pygame.error('unsupported')):
            self.assertFalse(window.toggle_fullscreen())
            self.assertFalse(window.is_fullscreen())

    def test_shortcuts_are_consumed_and_other_events_preserved(self):
        click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(640, 360), button=1)
        quit_event = pygame.event.Event(pygame.QUIT)
        for event in (pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F11, mod=0),
                      pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN, mod=pygame.KMOD_ALT),
                      click, quit_event):
            pygame.event.post(event)
        with patch.object(window, 'toggle_fullscreen') as toggle:
            self.assertEqual(window.get_events(), [click, quit_event])
            self.assertEqual(toggle.call_count, 2)

    def test_options_fullscreen_button_and_back(self):
        import interface
        events = [pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1),
                  pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)]
        with patch.object(window, 'get_events', side_effect=([events[0]], [events[1]])), \
             patch.object(window, 'mouse_position', side_effect=((640, 252), (640, 576))), \
             patch.object(window, 'toggle_fullscreen') as toggle:
            interface.options()
            toggle.assert_called_once()
        self.assertIs(window.get_screen(), self.screen)


if __name__ == '__main__':
    unittest.main()
