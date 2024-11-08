def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, item_visible
    run = True
    paused = False  # Thêm biến paused
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 370
    points = 0
    font = pygame.font.Font('Roboto-bold.ttf', 20)
    obstacles = []
    death_count = 0
    day_night_cycle = 0
    item = Item()
    item_active = False
    item_start_time = 0
    item_visible = False  
    
    gun = Gun()  
    gun_visible = False  
    gun_spawned = False  
    gun_reset_time = 0  

    def score():
        global points, game_speed, item_visible
        points += 1
        if points % 100 == 0:
            game_speed += 1
            
        if points % 1000 == 0:
            CHECKPOINT_SOUND.play()
            
        if points % 200 == 0 and not item_visible:
            item_visible = True
            item.reset()  

        text = font.render("Điểm: " + str(points), True, (0, 255, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Nhấn P để tạm dừng hoặc tiếp tục
                    paused = not paused

        if paused:
            # Hiển thị thông báo "Tạm dừng"
            pause_text = font.render("Tạm dừng - Nhấn P để tiếp tục", True, (255, 0, 0))
            pause_text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            SCREEN.blit(pause_text, pause_text_rect)
            pygame.display.update()
            clock.tick(5)  # Giảm tốc độ cập nhật màn hình để tiết kiệm tài nguyên khi tạm dừng
            continue

        userInput = pygame.key.get_pressed()
        if userInput[pygame.K_SPACE] and player.can_shoot:
            player.shoot()

        if day_night_cycle % 2 == 0:
            SCREEN.fill((255, 255, 255))
        else:
            SCREEN.fill((0, 0, 0)) 

        if points >= 500:
            day_night_cycle = (points // 500) % 2
        userInput = pygame.key.get_pressed()

        if points % random.randint(200, 500) == 0 and not gun_visible:  
            if random.randint(0, 99) < 90:  
                gun.reset()  
                gun_visible = True  

        if item_visible:
            item.update()
            item.draw(SCREEN)

            if player.dino_rect.colliderect(item.rect):
                ITEM_COLLECT_SOUND.play()
                item.collect()
                item_active = True
                item_start_time = pygame.time.get_ticks()
                player.activate_item()
                item_visible = False 

        if item_active:
            elapsed_time = pygame.time.get_ticks() - item_start_time
            remaining_time = max(0, 4000 - elapsed_time) // 1000  

            time_text = font.render(f"Item Time: {remaining_time}s", True, (255, 0, 0))
            SCREEN.blit(time_text, (10, 10))

            if elapsed_time >= 2000:
                item_active = False
                player.deactivate_item()

        if gun_visible:
            gun.update()
            gun.draw(SCREEN)

            if player.dino_rect.colliderect(gun.rect):
                gun.collect()  
                player.activate_shooting()  
                gun_visible = False  

        if gun_reset_time > 0 and pygame.time.get_ticks() - gun_reset_time >= 5000:  
            gun_visible = False  
            gun_spawned = False  

        for bullet in player.bullet_list:
            bullet.update()
            bullet.draw(SCREEN)

            for obstacle in obstacles[:]:
                if bullet.rect.colliderect(obstacle.rect):
                    player.bullet_list.remove(bullet)  
                    obstacles.remove(obstacle)  
                    break  

            if bullet.rect.x > SCREEN_WIDTH:
                player.bullet_list.remove(bullet)

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            rand_num = random.randint(0, 4)
            if rand_num == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif rand_num == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif rand_num == 2:
                obstacles.append(Bird(BIRD))
            elif rand_num == 3:
                obstacles.append(Spikes(SPIKES))
            elif rand_num == 4:
                obstacles.append(Rock(ROCK))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                DIE_SOUND.play()
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()