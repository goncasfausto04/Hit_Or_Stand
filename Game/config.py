"""Logical game dimensions, shared colors and default settings."""
import os

base_path = os.path.dirname(__file__)

black = (0, 0, 0)
blue = (0, 0, 255)
dark_green = (0, 100, 0)
olive_green = (107, 142, 35)
green_ish = (0, 215, 10)
green = (34, 139, 34)
dark_red = (138, 0, 0)
red = (150, 0, 24)
grey = (59, 60, 60)
light_grey = (100, 100, 100)
light_gray = (200, 200, 200)
glowing_light_red = (239, 128, 128)
glowing_yellow = (255, 255, 0)
yellow = (255, 255, 0)
gold = (255, 215, 0)
white = (254, 255, 255)
deep_black = (19, 20, 20)
pink = (255, 105, 180)

# Window scaling does not alter the simulation's coordinate system.
resolution = (1280, 720)
width, height = resolution
fps = 60

pet_image = "dog_pet_comp.png"
pet_image_change = False
music_volume = 0.2

player_size = (int(width * 0.0475), int(width * 0.0475))
enemy_size = (int(width * 0.025), int(height * 0.045))
bullet_size = int(width * 0.006)
chest_size = (int(width * 0.03), int(height * 0.055))
pet_size = (int(width * 0.035), int(height * 0.065))
soundtrack = [os.path.join(base_path, "extras", f"soundtrack{i}.mp3") for i in range(1, 5)]
