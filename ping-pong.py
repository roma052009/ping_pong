from pygame import*
from random import*

class GameSprite(sprite.Sprite):
    def __init__(self, player_width, player_height, player_image, player_x, player_y, player_speed):
        self.width = player_width
        self.height = player_height
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
class Player(GameSprite):
    def update(self, p):
        keys = key.get_pressed()
        if p == "l":
            if keys[K_w] and self.rect.y > 20:
                self.rect.y -= self.speed
            if keys[K_s] and self.rect.y < win_height - 20:
                self.rect.y += self.speed
        elif p == "r":
            if keys[K_UP] and self.rect.y > 20:
                self.rect.y -= self.speed
            if keys[K_DOWN] and self.rect.y < win_height - 20:
                self.rect.y += self.speed

class Ball(GameSprite):
    def set_route(self, ruh_po_x, ruh_po_y):
        self.ruh_po_x = ruh_po_x
        self.ruh_po_y = ruh_po_y
    def update(self):
        global game
        global game_not_finished
        global text_lose
        if self.rect.y <= 0 or self.rect.y >= win_height - 10:
            self.ruh_po_y = self.ruh_po_y * -1
        
        if sprite.collide_rect(self , player_l) or sprite.collide_rect(self , player_r):
            self.ruh_po_x = self.ruh_po_x * -1

        if self.rect.x <= 0:
            font.init()
            font1 = font.SysFont('Arial', 50)
            text_lose = font1.render("Програв синій", 1, (0, 0, 255))
            game_not_finished = False
        elif self.rect.x >= win_width:
            font.init()
            font1 = font.SysFont('Arial', 50)
            text_lose = font1.render("Програв червоний", 1, (255, 0, 0))
            game_not_finished = False

        self.rect.x += self.ruh_po_x
        self.rect.y += self.ruh_po_y
        
        

        

clock = time.Clock()
FPS = 60

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Пінг понг")

background = transform.scale(image.load("background_ping_pong.png"), (win_width, win_height))

player_l = Player(10, 100, "l_ping_pong.png", 5, win_height / 2 - 25, 5)

player_r = Player(10, 100, "r_ping_pong.png", win_width - 13, win_height / 2 - 25, 5)

ball = Ball(20, 20, "ball_ping_pong.png", win_width / 2 - 10, win_height / 2 - 10, 0)
ball.set_route(randint(3, 5), randint(3, 5))




game_not_finished = True
game = True
while game:
    if game_not_finished == True:
        window.blit(background, (0, 0))
        player_l.update("l")
        player_r.update("r")
        ball.update()

    else:
        window.blit(background, (0, 0))
        window.blit(text_lose, (win_width / 4, win_height / 2))


    
    player_l.reset()
    player_r.reset()
    ball.reset()
    
    display.update()
    clock.tick(FPS)
    
    for e in event.get():
        if e.type == QUIT:
            game = False