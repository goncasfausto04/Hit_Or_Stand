import pygame
import os
import random
import config
from utils import *
from player import Player
from enemy import *
from pet import Pet
from shed import shed
from shop import shop
from chest import TreasureChest
from abstractclasses import *


# endless loop that will keep the game running
def game_loop():
    # Initialize player and other game components
    player = Player()
    bullets = pygame.sprite.Group()
    pet = Pet(player, bullets)  # Pass bullets group to the Pet
    current_state = "initial"

    # Play soundtrack
    pygame.mixer.music.load(random.choice(soundtrack))  # Load a random soundtrack
    pygame.mixer.music.set_volume(config.music_volume)  # Set the desired volume
    pygame.mixer.music.play(-1)  # Loop the soundtrack indefinitely

    spawn_interval = 2 * fps  # Intervalo inicial entre spawns (2 segundos)
    phase_duration = 30  # Duração de cada fase em segundos
    current_phase = 0  # Fase inicial do jogo

    while True:
        if current_state == "main":
            current_state = execute_game(player, pet)
        elif current_state == "initial":
            current_state = shed(player, pet, (config.width * 0.5, config.height * 0.5))
        elif current_state == "shed":
            current_state = shed(
                player, pet, ((config.width * 0.01), (config.height * 0.5))
            )
        elif current_state == "shop":
            current_state = shop(player)
        elif current_state == "shedshop":
            current_state = shed(
                player, pet, ((config.width - (config.width * 0.20)), (config.height * 0.25))
            )
        elif current_state == "shedcasino":
            current_state = shed(
                player, pet, ((config.width - (config.width * 0.20)), (config.height * 0.65))
            )


def execute_game(player, pet):
    base_path = os.path.dirname(__file__)
    background_path = os.path.join(base_path, "extras", "Battleground.png")
    background = pygame.image.load(background_path)
    background = pygame.transform.scale(background, config.resolution)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(config.resolution)
    blockyfontpath = os.path.join(base_path, "extras", "Pixeboy.ttf")
    blockyfont = pygame.font.Font(blockyfontpath, int(config.height * 0.05))
    mouse = pygame.mouse.get_pos()  # Get mouse position
    pygame.display.set_caption("Hit or Stand")

    leave_text = blockyfont.render("Leave", True, white)
    not_leave_text = blockyfont.render("Stay", True, white)

    player_group = pygame.sprite.Group()
    player_group.add(player)
    pet_group = pygame.sprite.Group()  # Create a group for the pet
    pet_group.add(pet)  # Add the pet to the group
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    chests = pygame.sprite.Group()

    enemy_cooldown = 0
    running = True
    powerups_group = pygame.sprite.Group()  # Group to hold power-up sprites
    abspowerups_group =  pygame.sprite.Group()
    powerup_spawn_timer = 0  # Timer for power-ups
    despawner_spawn_time = 0
    beforeinstakill = 0
    invencibility_spawn_time = 0
    oneshot_spawn_time = 0
    invencibility_time = 300
    reverse_spawn_time = 0
    health_drop_spawn_timer = 0  # Timer for health drops
    reverse_time = 120
    spawn_rate = (
        fps * 6 
    )  # Spawn a health drop every 6 seconds (60 frames per second)
    spawn_chance = 100  # Percentage rarity of power-up (lower is rarer)
    exp_multiplier = 1.2

    bar_width = 300
    bar_height = 10
    bar_x = (config.width - bar_width) // 2
    bar_y = height - bar_height - 50

    game_time = 0
    game_time_frames = 0  # Tracks elapsed time in seconds
    kills = 0  # Tracks the number of kills
    font = pygame.font.SysFont("Arial", 30)  # Font for rendering text

    damage_cooldown = 35  # Cooldown in frames (1 second at 60 FPS (if it was 60))
    player_cooldown = 0  # Tracks the remaining cooldown time for the player

    def draw_level_up_bar(screen):
        # Draw the background bar (empty)
        pygame.draw.rect(screen, deep_black, (bar_x, bar_y, bar_width, bar_height))

        # Calculate the width of the filled part of the bar
        fill_width = (player.exp / player.exp_required) * bar_width
        pygame.draw.rect(screen, green, (bar_x, bar_y, fill_width, bar_height))

        # Draw the text showing the current level and experience
        level_text = font.render(
            f"Level: {player.level}  EXP: {player.exp}/{int(player.exp_required)}",
            True,
            white,
        )
        screen.blit(
            level_text,
            (config.width // 2 - level_text.get_width() // 2, bar_y + bar_height + 10),
        )
    def draw_slot(screen):
        # Load and scale the image to make it smaller
        dash_image_path = os.path.join(base_path, "extras", "dash.png")
        dash_image = pygame.image.load(dash_image_path)
        dash_image = pygame.transform.scale(dash_image, (int(0.06 * config.width), int(0.06 * config.width)))  # Smaller size

        # Draw the image as the background for the slot
        screen.blit(
            dash_image,
            (
                0.012 * config.width,
                0.87 * config.height,
            ),
        )
        
        timer = player.dash_cooldown
        # draw the timer on the slot with less opacity
        if timer > 0:
            # Modify the green color to include less opacity (e.g., 100 out of 255)
            semi_transparent_green = (0, 255, 0)  # 100 is the alpha (opacity)
            
            pygame.draw.rect(
                screen,
                semi_transparent_green,
                (
                    0.012 * config.width,
                    0.87 * config.height,
                    0.06 * config.width * (timer / (fps * 2)),  # Adjusted to match the new size
                    0.06 * config.width,  # Adjusted to match the new size
                ),
            )


    while running:
        clock.tick(fps)

        game_time_frames += 1  # Increment the timer based on frames
        total_seconds = game_time_frames // fps  # Convert frames to seconds
        minutes = total_seconds // 60  # Calculate minutes
        seconds = total_seconds % 60  # Calculate seconds
        timer_text = font.render(
            f"Time: {minutes:02}:{seconds:02}", True, white
        )  # Format MM:SS

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_game(screen, config.width, config.height)

        # Handle changing bullet type (check for 1, 2, or 3 key press)
        keys = pygame.key.get_pressed()
        player.change_bullet_type(keys)

        # Update game logic
        screen.blit(background, (0, 0))
        player.shoot(bullets)
        pet.update()  # Update the pet's behavior (follows player, fires randomly)
        pet_group.update()  # Update the pet group
        pet.pet_shoot(bullets)  # Pet shoots bullets

        for enemy in enemies:
            enemy.draw(screen)  # Call the draw method for each enemy

        if player.exp >= player.exp_required:
            x = random.randint(50, config.width - 50)
            y = random.randint(50, config.height - 50)
            chest = TreasureChest(x, y, player)
            chests.add(chest)
            player.level += 1
            player.exp -= player.exp_required
            player.exp_required = int(
                player.exp_required * exp_multiplier
            )  # Increase the XP required for the next level

        # Detect collision and apply damage
        for enemy in enemies:
            enemy.move_towards_player(player)  # Move towards the player

        collided_enemies = pygame.sprite.spritecollide(player, enemies, False)

        if collided_enemies and player_cooldown <= 0 and player.invincible == False:
            # Apply damage once for all collisions in the frame if player is not invincible
            total_damage = sum(enemy.damage for enemy in collided_enemies)
            player.health -= total_damage
            player_cooldown = damage_cooldown  # Reset the player's cooldown

        if player_cooldown > 0:
            player_cooldown -= 1  # Reduce player's cooldown by 1 each frame

        invencibility_spawn_time += 1  # change
        if invencibility_spawn_time >= random.randint(fps * 40, fps * 80):  # Spawn a power-up every 5 seconds
            x, y = random.randint(50, 1230), random.randint(50, 650)
            powerup_type = Invincibility
            powerup1 = powerup_type(x, y)
            abspowerups_group.add(powerup1)
            invencibility_spawn_time = 0
        abspowerups_group.update()

        despawner_spawn_time += 1
        if despawner_spawn_time >= random.randint(fps * 40, fps * 80):  # Spawn a power-up every 5 seconds
            x, y = random.randint(50, 1230), random.randint(50, 650)
            powerup_type = DeSpawner
            powerup2 = DeSpawner(x, y)
            abspowerups_group.add(powerup2)
            despawner_spawn_time = 0
        abspowerups_group.update()

        oneshot_spawn_time += 1  # change
        if oneshot_spawn_time >= random.randint(fps * 40, fps * 80):  # Spawn a power-up every 5 seconds
            x, y = random.randint(50, 1230), random.randint(50, 650)
            powerup_type = Instakill
            powerup3 = powerup_type(x, y)
            abspowerups_group.add(powerup3)
            oneshot_spawn_time = 0
        abspowerups_group.update()

        reverse_spawn_time += 1  # change
        if reverse_spawn_time >= random.randint(fps * 40, fps * 80):  # Spawn a power-up every 5 seconds
            x, y = random.randint(50, 1230), random.randint(50, 650)
            powerup_type = InvertedControls
            powerup4 = powerup_type(x, y)
            abspowerups_group.add(powerup4)
            reverse_spawn_time = 0
        abspowerups_group.update()

        abspowerups_group.update()
        # Check for collisions between player and power-ups
        collected_powerups = pygame.sprite.spritecollide(player, abspowerups_group, True)
        for powerup in collected_powerups:
            powerup.affect_player(player)
            powerup.affect_game(enemies)

        if invencibility_time > 0 and player.invincible == True:
            invencibility_time -= 1
        if invencibility_time <= 0:
            player.invincible = False
            invencibility_time = 300
        if player.oneshotkill == True:
            beforeinstakill = kills
        if reverse_time > 0 and player.inverted == True:
            reverse_time -= 1
        if reverse_time <= 0:
            player.inverted = False
            reverse_time = 120

        enemy_types = [initialEnemy, fastEnemy, TankMonster, RangedMonster, DuplicateMonster]
        spawn_configs = [
            (60, [70, 20, 10, 0, 0], 1, 2),
            (120, [50, 30, 15, 5, 0], 1, 1.8),
            (180, [40, 30, 20, 10, 5], 2, 1.5),
            (240, [30, 30, 25, 15, 5], 2, 1.3),
            (300, [25, 25, 30, 20, 10], 3, 1.1),
            (360, [20, 25, 30, 25, 15], 3, 1),
            (420, [20, 20, 30, 30, 20], 4, 1),
            (480, [15, 15, 35, 35, 20], 4, 1),
            (540, [10, 10, 40, 40, 25], 4, 1),
            (float('inf'), [5, 5, 45, 45, 35], 5, 0.8)
        ]

        if enemy_cooldown <= 0:
            for max_time, weights, num_spawn, cooldown_factor in spawn_configs:
                if total_seconds < max_time:
                    spawn_weights = weights
                    num_enemies_to_spawn = num_spawn
                    enemy_cooldown = int(cooldown_factor * fps)
                    break

            for _ in range(num_enemies_to_spawn):
                enemy_type = random.choices(enemy_types, weights=spawn_weights, k=1)[0]
                new_enemy = enemy_type()
                enemies.add(new_enemy)

        enemy_cooldown -= 1


        # === Health Drop Spawn Logic ===
        health_drop_spawn_timer += 1
        if health_drop_spawn_timer >= spawn_rate:  # Health drop spawn timer
            if random.randint(1, spawn_chance // 2) <= 20:  # 20% chance for health drop
                x = random.randint(50, config.width - 50)
                y = random.randint(50, config.height - 50)
                health_drop = HealthDrop(x, y)
                powerups_group.add(health_drop)
            health_drop_spawn_timer = 0  # Reset health drop timer

        # Handle collisions with power-ups and health drops
        collected_powerups = pygame.sprite.spritecollide(player, powerups_group, True)
        for item in collected_powerups:
            if isinstance(item, PowerUp):  # Activate power-up
                player.activate_powerup()
            elif isinstance(
                item, HealthDrop
            ):  # Increase health, but not above max health
                player.health = min(player.health + 20, player.max_health)

        if pygame.sprite.spritecollide(
            player, powerups_group, True
        ):  # True removes power-up
            player.activate_powerup()  # Activate invincibility for the player

        for enemy in enemies:
            if isinstance(enemy, RangedMonster):  # Check if the enemy is a RangedMonster
                enemy.enemy_shoot(bullets)  # Call the shoot method

        # updating positions and visuals
        player_group.update()
        bullets.update()
        enemies.update(player)

        if player.powerup_active:  # If the player is invincible
            collided_enemies = pygame.sprite.spritecollide(
                player, enemies, True
            )  # True removes enemy

            #for enemy in collided_enemies:
                #enemy.kill()  # Remove enemy on collision
                #kills += 1
                #player.exp += 1

        # drawing the player and enemies sprites on the screen
        powerups_group.draw(screen)
        chests.draw(screen)

        # Handle collisions
        for bullet in bullets:
            # Verificar se a bala é de um inimigo
            if getattr(bullet, 'is_enemy_bullet', False):  # Verifica se é uma bala inimiga
                # Detectar colisão com o jogador
                if player.rect.colliderect(bullet.rect):
                    player.health -= bullet.damage
                    bullet.kill()  # Remove a bala após a colisão
            else:
                # Verificar colisão com todos os inimigos
                for enemy in enemies:
                    if enemy.rect.colliderect(bullet.rect):
                        enemy.health -= 10  # Aplica dano no inimigo
                        bullet.kill()  # Remove a bala após a colisão
                        if enemy.health <= 0:
                            enemy.kill()
                            kills += 1
                            player.exp += 1
                        # Se a vida do inimigo chegar a 0, ele morre
                        break  # Sai do loop interno após processar o inimigo atual


        if beforeinstakill < kills:
            player.oneshotkill = False
        # Draw game objects
        draw_level_up_bar(screen)
        if player.has_dash:
            draw_slot(screen)
        player_group.draw(screen)
        pet_group.draw(screen)
        abspowerups_group.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        player.draw_health_bar(screen)
        timer_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, white)
        kills_text = font.render(f"Kills: {kills}", True, white)
        screen.blit(timer_text, (10, 10))  # Timer at top-left corner
        screen.blit(kills_text, (10, 40))  # Kill counter below timer

        collected_chests = pygame.sprite.spritecollide(player, chests, True)
        for chest in collected_chests:
            chest.open_chest(screen)

        if player.rect.right >= config.width:
            out = True
            while out:
                mouse = pygame.mouse.get_pos()
                draw_buttonutils(
                    dark_green,
                    (0, 255, 0),
                    0.4 - (0.125 / 2),
                    0.667,
                    0.125,
                    0.083,
                    not_leave_text,
                    blockyfont,
                    mouse,
                    screen,
                )
                draw_buttonutils(
                    dark_red,
                    glowing_light_red,
                    0.6 - (0.125 / 2),
                    0.667,
                    0.125,
                    0.083,
                    leave_text,
                    blockyfont,
                    mouse,
                    screen,
                )
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if button_clicked(
                            0.4 - (0.125 / 2), 0.667, 0.125, 0.083, mouse
                        ):
                            player.rect.right = config.width - 20
                            out = False
                        elif button_clicked(
                            0.6 - (0.125 / 2), 0.667, 0.125, 0.083, mouse
                        ):
                            return "shed"

        pygame.display.flip()
