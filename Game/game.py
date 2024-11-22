from config import *
import pygame
from player import Player
from enemy import Enemy
from shed import shed
from powerup import *
import random
#endless loop that will keep the game running
def game_loop():
    #create player from the game
    player = Player()
    #by default star game in main area
    current_state = "main"

    while True:
        if current_state == "main":
            current_state = execute_game(player)
        elif current_state == "shed":
            current_state = shed(player)

def execute_game(player):

    #SETUP

    # setting up the background
    background = pygame.image.load("ImageBackground.jpg")
    background = pygame.transform.scale(background, (width, height))

    # using the clock to control the time frame.
    clock = pygame.time.Clock()

    # screen setup
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Endless Wilderness Explorer")


    # creating an empty group for the player received as input
    player_group = pygame.sprite.Group()

    # adding the player to the group
    player_group.add(player)

    #creating an empty bullet group that will be given as input to the player.shoot method
    bullets = pygame.sprite.Group()

    # creating the enemy group
    enemies = pygame.sprite.Group()

    # before starting our main loop, setup the enemy cooldown variable
    enemy_cooldown = 0
    
    # MAING GAME LOOP

    running = True
    powerups_group = pygame.sprite.Group()  # Group to hold power-up sprites
    spawn_timer = 0  # Timer to track power-up spawn opportunities
    spawn_rate = 200  # Frames between spawn attempts (e.g., every ~3.3 seconds at 60 FPS)
    spawn_chance = 100  # Percentage rarity of power-up (lower is rarer, e.g., 10% here)
    while running:

        # controlling the frame rate
        clock.tick(fps)

        # setting up the background
        screen.blit(background, (0, 0)) # if you put (0,0), it will fill the whole screen

        # handlng events:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        #automatically shoot bullets from the player
        player.shoot(bullets)

        # spawning enemies every two seconds
        if enemy_cooldown <= 0:
            # creating an enemy... would be so cool if there were more than one type... oh well...
            enemy = Enemy()

            # adding the enemy to the group
            enemies.add(enemy)
            
            # in bullets, we use the fps to spawn every second. Here we double that, to spawn every two seconds
            enemy_cooldown = 2 * fps

        # updating the enemy cooldown
        enemy_cooldown -= 1

        spawn_timer += 1  # Increment spawn timer
        if spawn_timer >= spawn_rate:
            # Spawn power-up if chance allows
            if random.randint(1, spawn_chance) <= 10:  # 10% chance to spawn
                x = random.randint(50, width - 50)
                y = random.randint(50, height - 50)
                powerup = PowerUp(x, y)
                powerups_group.add(powerup)
            spawn_timer = 0  # Reset spawn timer
        if pygame.sprite.spritecollide(player, powerups_group, True):  # True removes power-up
            player.activate_powerup()  # Activate invincibility for the player

        # updating positions and visuals
        #calling the .update() method of all the instances in the player group
        player_group.update()

        #check if player moved off screen
        if player.rect.right >= width:
            return "shed" 

        # updating the bullets group
        bullets.update()
        enemies.update(player)

        if player.powerup_active:  # If the player is invincible
            collided_enemies = pygame.sprite.spritecollide(player, enemies, True)  # True removes enemy
            for enemy in collided_enemies:
                enemy.kill()  # Remove enemy on collision

        # drawing the player and enemies sprites on the screen
        player_group.draw(screen)
        enemies.draw(screen)
        powerups_group.draw(screen)


        # drawing the bullets sprites
        for bullet in bullets:
            bullet.draw(screen)

        # seeing for colisions between player bullets and enemies
        for bullet in bullets:
            # getting the enemies that were hit by a bullet
            collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)

            for enemy in collided_enemies:

                # every hit enemy needs to lose life...
                # every bullet hit will reduce the life by 5 hp
                enemy.health -= 5

                # removing the bullet from the screen (as it's lodged in the enemy's heart)
                bullet.kill()

                # checking if the enemy is ripperino
                if enemy.health <= 0:
                    enemy.kill()
        player.draw_health_bar(screen)
        pygame.display.flip()

    # the main while 
    pygame.quit()