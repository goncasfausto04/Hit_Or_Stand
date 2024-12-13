# Config file used to set global variables and other settings
import os

base_path = os.path.dirname(__file__)

# COLORS
black = (0, 0, 0)
blue = (0, 0, 255)
dark_green = (0, 100, 0)
olive_green = (107, 142, 35)
green_ish = (0, 215, 10)
green = (34, 139, 34)
dark_red = (138, 0, 0)
red = (150, 0, 24)
grey = (59, 60, 60)
dark_gray = (50, 50, 50)
light_grey = (100, 100, 100)
light_gray = (200, 200, 200)
cute_purple = (128, 0, 128)
glowing_light_red = (239, 128, 128)
glowing_yellow = (255, 255, 0)
yellow = (255, 255, 0)
gold = (255, 215, 0)
white = (254, 255, 255)
deep_black = (19, 20, 20)
pink = (255, 105, 180)

# SCREEN RESOLUTION
resolution = (1280, 720)
width, height = resolution[0], resolution[1]
fps = 60

# SIZES
player_size = (int(width * 0.025), int(height * 0.08))  # Smaller player size
enemy_size = (int(width * 0.025), int(height * 0.045))  # Smaller enemy size
bullet_size = int(width * 0.006)  # Smaller bullet size
powerup_size = (int(width * 0.025), int(height * 0.045))  # Smaller power-up size
chest_size = (int(width * 0.025), int(height * 0.045))  # Smaller chest size

# music volume
music_volume = 0.2
pet_size = (int(width * 0.035), int(height * 0.065))  # Smaller pet size

# soundtrack list
soundtrack1_path = os.path.join(base_path, "extras", "soundtrack1.mp3")
soundtrack2_path = os.path.join(base_path, "extras", "soundtrack2.mp3")
soundtrack3_path = os.path.join(base_path, "extras", "soundtrack3.mp3")
soundtrack4_path = os.path.join(base_path, "extras", "soundtrack4.mp3")

soundtrack = [soundtrack1_path, soundtrack2_path, soundtrack3_path, soundtrack4_path]
