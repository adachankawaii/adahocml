import pygame # Khai báo thư viện

class Level: # Tạo class Level
    def __init__(self): # Khởi tạo
        self.display_surface = pygame.display.get_surface() # Lấy màn để vẽ lên

    def run(self):
        self.display_surface.fill((230,210,250)) # Tô màu cho màn (R-G-B), hex, 'color'

