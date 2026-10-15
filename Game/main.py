"""Game entry point. Run with the project virtual environment."""
import pygame
import config
import window
from interface import interface
from utils import play_video, video_path, sound_path


def main():
    pygame.init()
    window.restore_preferences()
    try:
        play_video(video_path, config.resolution, sound_path)
        interface()
    finally:
        window.save_preferences()
        pygame.quit()


if __name__ == "__main__":
    main()
