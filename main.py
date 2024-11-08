import pygame
import os
import random
from item import Item

pygame.init()
pygame.mixer.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Khủng long vượt ngàn chông gai")

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "run1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "run2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "jump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "duck.png")),
           pygame.image.load(os.path.join("Assets/Dino", "duck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]
ROCK = [pygame.image.load(os.path.join("Assets/Rock", "Rock1.png")),
         pygame.image.load(os.path.join("Assets/Rock", "Rock2.png")),
         pygame.image.load(os.path.join("Assets/Rock", "Rock3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

JUMP_SOUND = pygame.mixer.Sound(os.path.join("Assets/Sounds", "jump.mp3"))
DIE_SOUND = pygame.mixer.Sound(os.path.join("Assets/Sounds", "die.mp3"))
CHECKPOINT_SOUND = pygame.mixer.Sound(os.path.join("Assets/Sounds", "point.mp3"))
ITEM_COLLECT_SOUND = pygame.mixer.Sound(os.path.join("Assets/Sounds", "item_collect.mp3"))

SPIKES = [pygame.image.load(os.path.join("Assets/Spikes", "spikes1.png")),
          pygame.image.load(os.path.join("Assets/Spikes", "spikes1.png")),
          pygame.image.load(os.path.join("Assets/Spikes", "spikes1.png"))]

class Dinosaur:
    X_POS = 80
    Y_POS = 305
    Y_POS_DUCK = 330
    JUMP_VEL = 8.5
    MOVE_VEL = 25

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.using_item = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
            
        if self.using_item:
            if userInput[pygame.K_LEFT]:
                self.dino_rect.x -= self.MOVE_VEL  
            if userInput[pygame.K_RIGHT]:
                self.dino_rect.x += self.MOVE_VEL  

    def activate_item(self):
        self.using_item = True

    def deactivate_item(self):
        self.using_item = False


    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect.y = self.Y_POS_DUCK 
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect.y = self.Y_POS  
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            if self.dino_rect.y == self.Y_POS:
                JUMP_SOUND.play()
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Rock(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)      
        super().__init__(image, self.type)      
        self.rect.y = 395 - self.rect.height

class Spikes(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 315
class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1
        
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, item_visible
    run = True
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
    
    def score():
        global points, game_speed, item_visible
        points += 1
        if points % 1000 == 0:
            CHECKPOINT_SOUND.play()
            game_speed += 1
            
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

        if day_night_cycle % 2 == 0:
            SCREEN.fill((255, 255, 255))
        else:
            SCREEN.fill((0, 0, 0)) 

        if points >= 500:
            day_night_cycle = (points // 500) % 2
        userInput = pygame.key.get_pressed()


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
            if pygame.time.get_ticks() - item_start_time >= 2000:  
                item_active = False
                player.deactivate_item()

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

def menu(death_count):
    global points
    run = True
    button_start_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)  # Nút bắt đầu
    button_exit_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120, 200, 50)  # Nút thoát

    while run:
        SCREEN.fill((255, 255, 255))  # Làm mới màn hình với màu trắng
        font = pygame.font.Font('Roboto-Bold.ttf', 30)  # Phông chữ cho menu

        # Nếu đây là lần chơi đầu tiên
        if death_count == 0:
            text = font.render("Thánh Long K'uhul Ajaw Toàn Năng!", True, (0, 0, 0))
        # Nếu người chơi đã thua ít nhất 1 lần
        elif death_count > 0:
            text = font.render("Nhấn nút bên dưới để chơi lại", True, (0, 0, 0))
            score = font.render("Điểm của bạn: " + str(points), True, (0, 0, 0))  # Hiển thị điểm
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)  # Vị trí của điểm
            SCREEN.blit(score, scoreRect)

        # Vẽ thông báo trên màn hình
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Vị trí của thông báo
        SCREEN.blit(text, textRect)

        # Vẽ nút "Bắt đầu"
        pygame.draw.rect(SCREEN, (0, 150, 0), button_start_rect)  # Vẽ hình chữ nhật cho nút
        button_start_text = font.render("Bắt đầu", True, (255, 255, 255))  # Văn bản cho nút
        button_start_text_rect = button_start_text.get_rect(center=button_start_rect.center)  # Vị trí văn bản
        SCREEN.blit(button_start_text, button_start_text_rect)

        # Vẽ nút "Thoát"
        pygame.draw.rect(SCREEN, (150, 0, 0), button_exit_rect)  # Vẽ hình chữ nhật cho nút thoát
        button_exit_text = font.render("Thoát", True, (255, 255, 255))  # Văn bản cho nút thoát
        button_exit_text_rect = button_exit_text.get_rect(center=button_exit_rect.center)  # Vị trí văn bản
        SCREEN.blit(button_exit_text, button_exit_text_rect)

        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))  # Vẽ khủng long trên menu
        pygame.display.update()  # Cập nhật màn hình

        # Kiểm tra sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Thoát nếu nhấn nút thoát
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # Kiểm tra nhấn chuột
                if button_start_rect.collidepoint(event.pos):  # Bắt đầu trò chơi nếu nhấn nút bắt đầu
                    main()
                elif button_exit_rect.collidepoint(event.pos):  # Thoát trò chơi nếu nhấn nút thoát
                    pygame.quit()
                    run = False

# Gọi menu với số lần chết ban đầu là 0
menu(death_count=0)