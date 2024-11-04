import pygame
import random

class Item:
    def __init__(self):
        self.image = pygame.image.load("Assets/Other/Reset.png")  # Đường dẫn đến hình ảnh item
        self.rect = self.image.get_rect()
        self.reset()  # Gọi phương thức reset để khởi tạo vị trí

    def reset(self):
        self.rect.x = 1200  # Vị tríx
        self.rect.y = random.randint(000, 300)  # Vị tríy
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