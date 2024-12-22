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
from hud import HUD


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
                player,
                pet,
                ((config.width - (config.width * 0.22)), (config.height * 0.25)),
            )
        elif current_state == "shedcasino":
            current_state = shed(
                player,
                pet,
                ((config.width - (config.width * 0.27)), (config.height * 0.65)),
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
    hud = HUD(screen, config, player)

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
    abspowerups_group = pygame.sprite.Group()
    despawner_spawn_time = 0
    beforeinstakill = 0
    invencibility_spawn_time = 0
    oneshot_spawn_time = 0
    invencibility_time = 300
    health_drop_spawn_time = 0
    reverse_spawn_time = 0
    teleport_spawn_time = 0
    invencibility_spawn_interval = random.randint(fps * 50, fps * 100)
    despawner_spawn_interval = random.randint(fps * 30, fps * 70)
    oneshot_spawn_interval = random.randint(fps * 25, fps * 50)
    reverse_spawn_interval = random.randint(fps * 40, fps * 80)
    teleport_spawn_interval = random.randint(fps * 30, fps * 70)
    health_drop_spawn_interval = random.randint(fps * 30, fps * 60)
    reverse_time = 120
    exp_multiplier = 1.2

    game_time_frames = 0  # Tracks elapsed time in seconds
    kills = 0  # Tracks the number of kills
    font = pygame.font.SysFont("Arial", 30)  # Font for rendering text

    damage_cooldown = 35  # Cooldown in frames (1 second at 60 FPS (if it was 60))
    player_cooldown = 0  # Tracks the remaining cooldown time for the player

    colission_rect1 = pygame.Rect(
            0,
            config.height * 0.94,
            config.width ,
            config.height*0.01 ,
        )

    colission_rect2 = pygame.Rect(
            config.width * 0.02,
            0,
            config.width * 0.01,
            config.height * 0.94,
        )


    while running:

        clock.tick(fps)
        game_time_frames += 1  # Increment the timer based on frames
        total_seconds = game_time_frames // fps  # Convert frames to seconds
        minutes = total_seconds // 60  # Calculate minutes
        seconds = total_seconds % 60  # Calculate seconds
        time = minutes * 60 + seconds  # Calculate total time in seconds
        timer_text = font.render(
            f"Time: {minutes:02}:{seconds:02}", True, white
        )  # Format MM:SS

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.save_progress()
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_game(screen, config.width, config.height)

        # Handle changing bullet type (check for 1, 2, or 3 key press)
        keys = pygame.key.get_pressed()
        player.change_bullet_type(keys)

        # Update game logic
        pet_group.update()  # Update the pet's position
        abspowerups_group.update()
        player_group.update()
        bullets.update()
        enemies.update(player)

        # drawing the player and enemies sprites on the screen
        screen.blit(background, (0, 0))
        chests.draw(screen)
        # draw_level_up_bar(screen, player)
        abspowerups_group.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        pet_group.draw(screen)
        player.draw_health_bar(screen)
        draw_fps(screen, clock)
        player_group.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)  # Call the draw method for each enemy
        hud.draw()

        timer_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, white)
        kills_text = font.render(f"Kills: {kills}", True, white)
        screen.blit(timer_text, (10, 10))  # Timer at top-left corner
        screen.blit(kills_text, (10, 40))  # Kill counter below timer

        player.shoot(bullets)
        pet.pet_shoot(bullets)  # Pet shoots bullets

        def teleport_player(self):
            # Generate random position within the screen bounds
            new_x = random.randint(60, config.width - 60)
            new_y = random.randint(60, config.height - 60)

            # Update the player's position
            self.rect.x = new_x
            self.rect.y = new_y

        if player.exp >= player.exp_required:
            x = random.randint(50, config.width - 50)
            y = random.randint(50, config.height - 50)
            if player.has_dash == True:
                chest = TreasureChest(x, y, player, ["100", "200", "300", "400", "500"])
            else:
                chest = TreasureChest(
                    x, y, player, ["100", "200","Dash","300", "400"]
                )
            chests.add(chest)
            player.level += 1
            player.exp -= player.exp_required
            player.exp_required = int(
                player.exp_required * exp_multiplier
            )  # Increase the XP required for the next level
            if player.level % 5 == 0:
                player.max_health += 5

        # Detect collision and apply damage
        collided_enemies = pygame.sprite.spritecollide(player, enemies, False)

        if collided_enemies and player_cooldown <= 0 and player.invincible == False:
            # Apply damage once for all collisions in the frame if player is not invincible
            total_damage = sum(enemy.damage for enemy in collided_enemies)
            player.health -= total_damage
            player_cooldown = damage_cooldown  # Reset the player's cooldown

        if player_cooldown > 0:
            player_cooldown -= 1  # Reduce player's cooldown by 1 each frame

        invencibility_spawn_time += 1  # change
        if invencibility_spawn_time >= invencibility_spawn_interval:
            x, y = random.randint(50, 1230), random.randint(50, 650)
            powerup_type = Invincibility
            powerup1 = powerup_type(x, y)
            abspowerups_group.add(powerup1)
            invencibility_spawn_time = 0
            invencibility_spawn_interval = random.randint(fps * 50, fps * 100)


        despawner_spawn_time += 1
        if despawner_spawn_time >= despawner_spawn_interval:
            x, y = random.randint(50, 1230), random.randint(50, 650)
            powerup_type = DeSpawner
            powerup2 = DeSpawner(x, y)
            abspowerups_group.add(powerup2)
            despawner_spawn_time = 0
            despawner_spawn_interval = random.randint(fps * 30, fps * 70)



        oneshot_spawn_time += 1  # change
        if oneshot_spawn_time >= oneshot_spawn_interval:  # Spawn a power-up every 5 seconds
            x, y = random.randint(50, 1230), random.randint(50, 650)
            powerup_type = Instakill
            powerup3 = powerup_type(x, y)
            abspowerups_group.add(powerup3)
            oneshot_spawn_time = 0
            oneshot_spawn_interval = random.randint(fps * 25, fps * 50)


        reverse_spawn_time += 1  # change
        if reverse_spawn_time >= reverse_spawn_interval:
            x, y = random.randint(50, 1230), random.randint(50, 650)
            powerup_type = InvertedControls
            powerup4 = powerup_type(x, y)
            abspowerups_group.add(powerup4)
            reverse_spawn_time = 0

        teleport_spawn_time += 1
        if teleport_spawn_time >= teleport_spawn_interval:  # Spawn a power-up every 5 seconds
            x, y = random.randint(50, 1230), random.randint(50, 650)
            powerup_type = Teleportation
            powerup5 = powerup_type(x, y)
            abspowerups_group.add(powerup5)
            teleport_spawn_time = 0
            teleport_spawn_interval = random.randint(fps * 30, fps * 70)

        health_drop_spawn_time += 1
        if health_drop_spawn_time >= health_drop_spawn_interval:
            x, y = random.randint(50, 1230), random.randint(50, 650)
            powerup_type = Health_Drop
            powerup6 = powerup_type(x, y)
            abspowerups_group.add(powerup6)
            health_drop_spawn_time = 0
            health_drop_spawn_interval = random.randint(fps * 30, fps * 60)
        abspowerups_group.update()

        abspowerups_group.update()
        # Check for collisions between player and power-ups
        collected_powerups = pygame.sprite.spritecollide(
            player, abspowerups_group, True
        )

        
        if player.rect.colliderect(colission_rect1):
            player.rect.y -= 5
        #pygame.draw.rect(screen, (0, 0, 0), colission_rect1)

        if player.rect.colliderect(colission_rect2):
            player.rect.x += 5
        #pygame.draw.rect(screen, (0, 0, 0), colission_rect2)


 
        for powerup in collected_powerups:
            powerup.affect_player(player)
            powerup.affect_game(enemies)

        if invencibility_time > 0 and player.invincible == True:
            invencibility_time -= 1
            player.glow(screen, radius=60, color=(0, 20, 0, 50))
        if invencibility_time <= 0:
            player.invincible = False
            invencibility_time = 300
        if player.oneshotkill == True:
            beforeinstakill = kills
            player.glow(screen, radius=60, color=(0, 0, 200, 50))
        if reverse_time > 0 and player.inverted == True:
            reverse_time -= 1
            player.glow(screen, radius=60, color=(0, 100, 100, 50))
        if reverse_time <= 0:
            player.inverted = False
            reverse_time = 120
        if player.de_spawner_active == True:
            player.glow(screen, radius=60, color=(255, 0, 0, 50))

        if player.teleport == True:
            teleport_player(player)
            player.teleport = False

        if player.health_drop == True:
            player.health = min(player.health + 20, player.max_health)
            player.health_drop = False

        enemy_types = [
            initialEnemy,
            fastEnemy,
            TankMonster,
            RangedMonster,
            DuplicateMonster,
        ]
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
            (float("inf"), [5, 5, 45, 45, 35], 5, 0.8),
        ]

        if enemy_cooldown <= 0:
            for max_time, weights, num_spawn, cooldown_factor in spawn_configs:
                if total_seconds < max_time:
                    spawn_weights = weights
                    num_enemies_to_spawn = num_spawn
                    enemy_cooldown = int(cooldown_factor * fps)
                    break

            for _ in range(num_enemies_to_spawn):
                if player.de_spawner_active == False:
                    enemy_type = random.choices(
                        enemy_types, weights=spawn_weights, k=1
                    )[0]
                    new_enemy = enemy_type()
                    enemies.add(new_enemy)
                elif (
                    player.de_spawner_active == True
                ):  # now when despawner is activated enemies only have 75% chance of spawning
                    if random.randint(1, 100) <= 75:
                        enemy_type = random.choices(
                            enemy_types, weights=spawn_weights, k=1
                        )[0]
                        new_enemy = enemy_type()
                        enemies.add(new_enemy)

        enemy_cooldown -= 1

        for enemy in enemies:
            if isinstance(
                enemy, RangedMonster
            ):  # Check if the enemy is a RangedMonster
                enemy.enemy_shoot(bullets)  # Call the shoot method

        # updating positions and visuals

        if player.powerup_active:  # If the player is invincible
            collided_enemies = pygame.sprite.spritecollide(player, enemies, True)

        # Handle collisions
        for bullet in bullets:
            # Verificar se a bala é de um inimigo
            if getattr(
                bullet, "is_enemy_bullet", False
            ):  # Verifica se é uma bala inimiga
                # Detectar colisão com o jogador
                if player.rect.colliderect(bullet.rect):
                    if player.invincible == False:
                        player.health -= bullet.damage
                    bullet.kill()  # Remove a bala após a colisão
            else:
                # Verificar colisão com todos os inimigos
                for enemy in enemies:
                    if enemy.rect.colliderect(bullet.rect):
                        if player.oneshotkill == True:
                            enemy.health -= bullet.damage * 100000  # Aplica dano no inimigo que os mata automaticamente
                            bullet.kill()  # Remove a bala após a colisão
                        else:
                            enemy.health -= bullet.damage  # Aplica dano no inimigo
                            bullet.kill()  # Remove a bala após a colisão
                        if enemy.health <= 0:
                            if isinstance(enemy, DuplicateMonster):
                                enemy.spawn_on_death(enemies)  # Spawn new enemies
                            enemy.kill()
                            kills += 1
                            player.exp += 1
                        # Se a vida do inimigo chegar a 0, ele morre
                        break  # Sai do loop interno após processar o inimigo atual

        if beforeinstakill < kills:
            player.oneshotkill = False

        collected_chests = pygame.sprite.spritecollide(player, chests, True)
        for chest in collected_chests:
            chest.open_chest(screen, player)

        # kill player

        if player.health <= 0:
            player.death()
            if time > player.best_time:
                player.best_time = time

        if player.dead:
            dead = True
            dead_text = blockyfont.render("Respawn?", True, white)

            while dead:
                mouse = pygame.mouse.get_pos()

                draw_buttonutils(
                    dark_red,
                    green_ish,
                    0.5 - (0.125 / 2),
                    0.5 - (0.125 / 2),
                    0.125,
                    0.125,
                    dead_text,
                    blockyfont,
                    mouse,
                    screen,
                )

                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        player.save_progress()
                        pygame.quit()
                        exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if button_clicked(
                            0.5 - (0.125 / 2), 0.5 - (0.125 / 2), 0.125, 0.125, mouse
                        ):
                            player.dead = False
                            return "initial"

        if player.rect.right >= config.width:
            out = True
            while out:
                mouse = pygame.mouse.get_pos()
                draw_buttonutils(
                    dark_green,
                    (0, 255, 0),
                    0.4 - (0.125 / 2),
                    0.5 - (0.083 / 2),
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
                    0.5 - (0.083 / 2),
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
                        player.save_progress()
                        pygame.quit()
                        exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if button_clicked(
                            0.4 - (0.125 / 2), 0.5 - (0.083 / 2), 0.125, 0.083, mouse
                        ):
                            player.rect.right = config.width - 20
                            out = False
                        elif button_clicked(
                            0.6 - (0.125 / 2), 0.5 - (0.083 / 2), 0.125, 0.083, mouse
                        ):
                            player.health = 100
                            if player.best_time < time:
                                player.best_time = time
                            return "shed"

        pygame.display.flip()
