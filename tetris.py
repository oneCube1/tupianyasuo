import pygame
import random
import os

# 初始化pygame和音频
pygame.init()
pygame.mixer.init()

# 加载音效
try:
    # 设置音效文件路径
    MUSIC_FILE = "tetris_music.mp3"  # 请确保这个文件存在
    if os.path.exists(MUSIC_FILE):
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.play(-1)  # -1表示循环播放
        pygame.mixer.music.set_volume(0.3)  # 设置音量
except:
    print("音乐文件加载失败")

# 修改游戏尺寸和方块大小
SIZE = (800, 1000)  # 放大窗口
GAME_RES = (20, 10)
TILE = 35  # 放大方块尺寸

# 修改颜色，移除黑色边框
COLORS = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

# 定义方块形状
SHAPES = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],  # I
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # J
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # L
    [[1, 2, 5, 6]],  # O
    [[6, 7, 9, 10], [1, 5, 6, 10]],  # S
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # T
    [[4, 5, 9, 10], [2, 6, 5, 9]]  # Z
]

class Tetris:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        self.figure = None
        self.x = 200  # 调整游戏区域位置
        self.y = 100
        
        self.clear_field()
        
    def clear_field(self):
        self.field = []
        for i in range(self.height):
            new_line = []
            for j in range(self.width):
                new_line.append(0)
            self.field.append(new_line)
            
    def new_figure(self):
        self.figure = Figure(3, 0)
        
    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if (i + self.figure.y > self.height - 1 or
                        j + self.figure.x > self.width - 1 or
                        j + self.figure.x < 0 or
                        self.field[i + self.figure.y][j + self.figure.x] > 0):
                        intersection = True
        return intersection
    
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"
            
    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1-1][j]
        self.score += lines ** 2
        
    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()
        
    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()
            
    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x
            
    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    def reset_game(self):
        """重置游戏状态"""
        self.field = []
        self.score = 0
        self.state = "start"
        self.figure = None
        self.clear_field()

class Figure:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(SHAPES) - 1)
        self.color = random.randint(1, len(COLORS) - 1)
        self.rotation = 0
        
    def image(self):
        return SHAPES[self.type][self.rotation]
    
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(SHAPES[self.type])

# 创建按钮类
class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# 创建游戏窗口
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("俄罗斯方块")
clock = pygame.time.Clock()

# 创建重新开始按钮
restart_button = Button(SIZE[0]//2 - 100, SIZE[1]//2 + 50, 200, 50, "重新开始", (0, 128, 0))

# 创建游戏对象
game = Tetris(GAME_RES[0], GAME_RES[1])
counter = 0
pressing_down = False

# 主游戏循环
while True:
    if game.figure is None:
        game.new_figure()
        
    counter += 1
    if counter > 100000:
        counter = 0
        
    if counter % (5 if pressing_down else 25) == 0:
        if game.state == "start":
            game.go_down()
            
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.state == "gameover" and restart_button.is_clicked(event.pos):
                game.reset_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
                
    screen.fill((255, 255, 255))
    
    # 绘制游戏区域
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, COLORS[game.field[i][j]],
                           [game.x + j * TILE,
                            game.y + i * TILE,
                            TILE, TILE], 0)
            
    # 绘制当前方块
    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, COLORS[game.figure.color],
                                   [game.x + (j + game.figure.x) * TILE,
                                    game.y + (i + game.figure.y) * TILE,
                                    TILE, TILE], 0)
                    
    # 显示分数
    font = pygame.font.Font(None, 48)  # 放大字体
    text = font.render(f"得分: {game.score}", True, (0, 0, 0))
    screen.blit(text, [20, 20])
    
    if game.state == "gameover":
        game_over_text = font.render("游戏结束!", True, (255, 0, 0))
        screen.blit(game_over_text, [SIZE[0]//3, SIZE[1]//2])
        restart_button.draw(screen)
        
    pygame.display.flip()
    clock.tick(60) 