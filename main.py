import pygame
import os
import random

# Khởi tạo pygame
pygame.init()

# Đặt chiều cao và chiều rộng của màn hình
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100

# Tạo màn hình hiển thị
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Khủng long vượt ngàn chông gai")

# Tải hình ảnh cho các trạng thái của nhân vật
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "run1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "run2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "jump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "duck.png")),
           pygame.image.load(os.path.join("Assets/Dino", "duck2.png"))]

# Tải hình ảnh cho các chướng ngại vật
SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

# Tải hình ảnh cho đám mây
CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

# Tải hình nền mặt đất
BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

# Lớp đại diện cho khủng long
class Dinosaur:
    X_POS = 80  # Vị trí x của khủng long
    Y_POS = 310  # Vị trí y khi chạy
    Y_POS_DUCK = 340  # Vị trí y khi cúi
    JUMP_VEL = 8.5  # Tốc độ nhảy

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

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

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

# Lớp đại diện cho đám mây
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

# Lớp đại diện cho chướng ngại vật
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

# Lớp đại diện cho xương rồng nhỏ
class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

# Lớp đại diện cho xương rồng lớn
class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

# Lớp đại diện cho chim
class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

# Hàm chính để chạy trò chơi
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('Roboto-bold.ttf', 20)
    obstacles = []
    death_count = 0
    day_night_cycle = 0  # Biến để theo dõi chu kỳ ngày đêm

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Điểm: " + str(points), True, (0, 0, 0))
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

    # Vòng lặp chính của trò chơi
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Thay đổi màu nền theo chu kỳ
        if day_night_cycle % 2 == 0:
            SCREEN.fill((255, 255, 255))  # Nền trắng (ban ngày)
        else:
            SCREEN.fill((0, 0, 0))  # Nền đen (ban đêm)

        # Cập nhật chu kỳ ngày đêm dựa trên điểm số
        if points >= 500:
            day_night_cycle = (points // 500) % 2

        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        # Tạo chướng ngại vật ngẫu nhiên
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        # Cập nhật và vẽ chướng ngại vật
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()

# Hàm hiển thị menu trước và sau khi chơi
# def menu(death_count):
#     global points
#     run = True
#     while run:
#         SCREEN.fill((255, 255, 255))  # Làm mới màn hình với màu trắng
#         font = pygame.font.Font('Roboto-Bold.ttf', 30)  # Phông chữ cho menu

#         # Nếu đây là lần chơi đầu tiên
#         if death_count == 0:
#             text = font.render("Nhấn phím bất kỳ để bắt đầu!", True, (0, 0, 0))
#         # Nếu người chơi đã thua ít nhất 1 lần
#         elif death_count > 0:
#             text = font.render("Nhấn phím bất kỳ để chơi lại", True, (0, 0, 0))
#             score = font.render("Điểm của bạn: " + str(points), True, (0, 0, 0))  # Hiển thị điểm
#             scoreRect = score.get_rect()
#             scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)  # Vị trí của điểm
#             SCREEN.blit(score, scoreRect)

#         # Vẽ thông báo trên màn hình
#         textRect = text.get_rect()
#         textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Vị trí của thông báo
#         SCREEN.blit(text, textRect)
#         SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))  # Vẽ khủng long trên menu
#         pygame.display.update()  # Cập nhật màn hình

#         # Kiểm tra sự kiện
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:  # Thoát nếu nhấn nút thoát
#                 pygame.quit()
#                 run = False
#             if event.type == pygame.KEYDOWN:  # Bắt đầu trò chơi nếu nhấn phím
#                 main()
# # Gọi menu với số lần chết ban đầu là 0
# menu(death_count=0)
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

        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 - 140))  # Vẽ khủng long trên menu
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