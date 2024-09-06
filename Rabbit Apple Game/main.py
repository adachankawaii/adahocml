import pygame, sys, os
lib_path = os.path.abspath(os.path.join('data'))
sys.path.append(lib_path)
from level import Level  # Khai báo thư viện
from random import randint, choice

# Single
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        cat_surf_1 = pygame.image.load('data/graphics/cat.png').convert_alpha()
        cat_surf_2 = pygame.image.load('data/graphics/cat2.png').convert_alpha()
        self.cat_jump = pygame.image.load('data/graphics/catj.png').convert_alpha()

        self.cat_walk = [cat_surf_1, cat_surf_2]
        self.cat_index = 0

        self.image = self.cat_walk[self.cat_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('data/audio/jump.mp3')
        self.jump_sound.set_volume(0.01)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300

    def animated(self):
        if self.rect.bottom < 300: self.image = self.cat_jump
        else:
            self.cat_index += 0.1
            if self.cat_index >= len(self.cat_walk): self.cat_index = 0
            self.image = self.cat_walk[int(self.cat_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animated()

# Multiple
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'apple':
            apple_surf_1 = pygame.image.load('data/graphics/apple.png').convert_alpha()
            apple_surf_2 = pygame.image.load('data/graphics/apple2.png').convert_alpha()
            self.walk = [apple_surf_1, apple_surf_2]
            self.y = 200
        if type == 'fox':
            fox_surf_1 = pygame.image.load('data/graphics/fox.png').convert_alpha()
            fox_surf_2 = pygame.image.load('data/graphics/fox2.png').convert_alpha()
            self.walk = [fox_surf_1, fox_surf_2]
            self.y = 300
        self.index = 0
        self.image = self.walk[self.index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1000), self.y))
    
    def animated(self):
            self.index += 0.1
            if self.index >= len(self.walk): self.index = 0
            self.image = self.walk[int(self.index)]

    def movement(self):
        self.rect.x -= 5
        if self.rect.right <= 0: self.kill()
    
    def update(self):
        self.animated()
        self.movement()

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score = font.render(f'Score: {current_time}', 0, 'black')
    score_rect = score.get_rect(center = (400, 50))
    screen.blit(score, score_rect)
    return current_time

def obj_movement(obj_list):
    if obj_list:
        for obj_rect in obj_list:
            obj_rect.x -= 4
            if obj_rect.bottom == 300:
                screen.blit(fox_surf, obj_rect)
            else:
                screen.blit(apple_surf, obj_rect)

        obj_list = [obj_rect for obj_rect in obj_list if obj_rect.x > -50]
        return obj_list
    else:
        return []
    
def collisions(cat, obj_list):
    if obj_list:
        for obj_rect in obj_list:
            if cat.colliderect(obj_rect): return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle, False):
        obstacle.empty()
        return False
    else: return True

def cat_movement():
    global cat_surf, cat_index
    if cat_rect.bottom < 300: cat_surf = cat_jump
    else:
        cat_index += 0.1
        if cat_index >= len(cat_norm): cat_index = 0
        cat_surf = cat_norm[int(cat_index)]

pygame.init() # Bắt đầu

pygame.display.set_caption('Game nì cute') # Tạo tiêu đề game

icon = pygame.image.load('data/graphics/girl.png')
pygame.display.set_icon(icon)

bg_music = pygame.mixer.Sound('data/audio/music.mp3')
bg_music.set_volume(0.2)
bg_music.play()

screen = pygame.display.set_mode((800, 400)) # Tạo màn hình game với kích thước W x H

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle = pygame.sprite.Group()

round = pygame.image.load('data/graphics/ground.png').convert()
sky = pygame.image.load('data/graphics/sky.png').convert()

cat_index = 0
cat_surf_1 = pygame.image.load('data/graphics/cat.png').convert_alpha()
cat_surf_2 = pygame.image.load('data/graphics/cat2.png').convert_alpha()
cat_jump = pygame.image.load('data/graphics/catj.png').convert_alpha()
cat_norm = [cat_surf_1, cat_surf_2]
cat_surf = cat_norm[cat_index]
cat_rect = cat_surf.get_rect(midbottom = (80, 300))

cat_surf_scaled = pygame.transform.scale2x(cat_surf)
cat_scaled_rect = cat_surf_scaled.get_rect(center = (400, 200))

fox_index = 0
fox_surf_1 = pygame.image.load('data/graphics/fox.png').convert_alpha()
fox_surf_2 = pygame.image.load('data/graphics/fox2.png').convert_alpha()
fox_norm = [fox_surf_1, fox_surf_2]
fox_surf = fox_norm[fox_index]

apple_index = 0
apple_surf_1 = pygame.image.load('data/graphics/apple.png').convert_alpha()
apple_surf_2 = pygame.image.load('data/graphics/apple2.png').convert_alpha()
apple_norm = [apple_surf_1, apple_surf_2]
apple_surf = apple_norm[apple_index]

font = pygame.font.Font('data/font/Pixeltype.ttf', 50)

game_name = font.render('Ada Ada', 0, (100, 50, 100))
game_name_rect = game_name.get_rect(center = (400, 80))

game_mess = font.render('Press Space to continue ...', 0, (100, 50, 100))
game_mess_rect = game_mess.get_rect(center = (400, 320))

clock = pygame.time.Clock() # Tạo clock
level = Level() # Khởi tạo level
gravity = 0
start_time = 0
score = 0
game_active = False
    
obj = pygame.USEREVENT + 1
pygame.time.set_timer(obj, 1500)
obj_list = []

fox_ev = pygame.USEREVENT + 2
pygame.time.set_timer(fox_ev, 300)

apple_ev = pygame.USEREVENT + 2
pygame.time.set_timer(apple_ev, 200)


while True: 
    for event in pygame.event.get(): # Scan qua các event trong game
        if event.type == pygame.QUIT: # Nếu bấm nút ‘X’ – kết thúc
            pygame.quit() # Thoát pygame
            sys.exit() # Thoát toàn bộ chương trình
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and cat_rect.bottom >= 300:
                    gravity = -20

            if event.type == obj:
                obstacle.add(Obstacle(choice(['apple', 'fox', 'apple', 'fox', 'apple'])))
                # if randint(0, 2):
                #     obj_list.append(fox_surf.get_rect(bottomright = (randint(900, 1000), 300)))
                # else:
                #     obj_list.append(apple_surf.get_rect(bottomright = (randint(900, 1000), 200)))

            if event.type == fox_ev:
                if fox_index == 0: fox_index = 1
                else: fox_index = 0
                fox_surf = fox_norm[fox_index]

            if event.type == apple_ev:
                if apple_index == 0: apple_index = 1
                else: apple_index = 0
                apple_surf = apple_norm[apple_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)

    if game_active:
        level.run() # Chạy hàm run() trong level
        screen.blit(round, (0, 300))
        screen.blit(sky, (0, 0))
        score = display_score()

        # obj_list = obj_movement(obj_list)

        # gravity += 1
        # cat_rect.y += gravity
        # if cat_rect.bottom >= 300:
        #     cat_rect.bottom = 300
        
        # cat_movement()
        # screen.blit(cat_surf, cat_rect)

        player.draw(screen)
        player.update()

        obstacle.draw(screen)
        obstacle.update()

        # fox_rect.x -= 5
        # if fox_rect.right <= 0: fox_rect.left = 800
        # screen.blit(fox_surf, fox_rect)

        game_active = collision_sprite()

    else:
        screen.fill((200, 190, 230))
        screen.blit(cat_surf_scaled, cat_scaled_rect)

        score_mess = font.render(f'Your Score: {score}', 0, (100, 50, 100))
        score_mess_rect = score_mess.get_rect(center = (400, 320))

        obj_list.clear()
        cat_rect.bottom = 300
        gravity = 0

        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(game_mess, game_mess_rect)
        else:
            screen.blit(score_mess, score_mess_rect)

    pygame.display.update() # Cập nhật frame
    clock.tick(60) # Cân bằng FPS