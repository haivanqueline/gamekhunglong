import pygame
import random

class Item:
    def __init__(self):
        self.image = pygame.image.load("Assets/Other/Chicken.png")  # Đường dẫn đến hình ảnh item
        self.rect = self.image.get_rect()
        self.reset()  # Gọi phương thức reset để khởi tạo vị trí

    def reset(self):
        self.rect.x = 1200  # Vị tríx
        self.rect.y = random.randint(0, 300)  # Vị tríy
        self.is_collected = False

    def update(self):
        if not self.is_collected:
            self.rect.x -= 20  # Di chuyển item về phía bên trái
            if self.rect.x < -self.rect.width:
                self.reset()

    def draw(self, screen):
        if not self.is_collected:
            screen.blit(self.image, self.rect)

    def collect(self):
        self.is_collected = True
        
        
class Gun:
    def __init__(self):
        self.image = pygame.image.load("Assets/Other/Gun.png")
        self.image = pygame.transform.scale(self.image, (50, 50))  # Thay đổi kích thước cho phù hợp
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(600, 800)
        self.rect.y = random.randint(200, 300)
        self.visible = False

    def reset(self):
        # Đặt lại vị trí của gun khi hiển thị
        self.rect.x = random.randint(600, 800)
        self.rect.y = random.randint(200, 300)
        self.visible = True

    def update(self):
        # Di chuyển hoặc cập nhật vị trí của gun nếu cần
        self.rect.x -= 5  # Di chuyển từ phải sang trái (điều chỉnh tốc độ)

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)

    def collect(self):
        # Xử lý khi gun được thu thập
        self.visible = False
