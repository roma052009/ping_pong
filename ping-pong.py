from pygame import*
from random import*

font.init()

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
            
class Button(GameSprite):
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

class Ball(GameSprite):
    def set_route(self, ruh_po_x, ruh_po_y):
        self.ruh_po_x = ruh_po_x
        self.ruh_po_y = ruh_po_y
    def update(self):
        global game
        global game_not_finished
        global text_lose
        global balls_missed_l
        global balls_missed_r
        global text_l
        global text_r
        if self.rect.y <= 0 or self.rect.y >= win_height - 10:
            self.ruh_po_y = self.ruh_po_y * -1
        
        if sprite.collide_rect(self , player_l) or sprite.collide_rect(self , player_r):
            self.ruh_po_x = self.ruh_po_x * -1

        if self.rect.x <= 0:
            
            font1 = font.SysFont('Arial', 50)
            reset_position()
            balls_missed_l += 1
            text_l = font2.render("Пропущено " + str(balls_missed_l), 1, (0, 0, 255))
            

        elif self.rect.x >= win_width:
            
            font1 = font.SysFont('Arial', 50)
            reset_position()
            balls_missed_r += 1
            text_r = font2.render("Пропущено " + str(balls_missed_r), 1, (255, 0, 0))
            
            

        self.rect.x += self.ruh_po_x
        self.rect.y += self.ruh_po_y

def reset_game():
    global balls_missed_l
    global balls_missed_r
    global text_lose
    global text_l
    global text_r

    balls_missed_l = 0
    balls_missed_r = 0
    text_lose = font1.render(" ", 1, (255, 0, 0))
    text_r = font2.render("Пропущено " + str(balls_missed_r), 1, (255, 0, 0))
    text_l = font2.render("Пропущено " + str(balls_missed_l), 1, (0, 0, 255))

def reset_position():
    player_l.rect.y = win_height / 2 - 25
    player_r.rect.y = win_height / 2 - 25
    ball.rect.x = win_width / 2 - 10
    ball.rect.y = win_height / 2 - 10      
        

        

clock = time.Clock()
FPS = 60

win_width = 700
win_height = 500
balls_missed_l = 0
balls_missed_r = 0



font1 = font.SysFont('Arial', 50)
text_lose = font1.render(" ", 1, (255, 0, 0))

font2 = font.SysFont('Arial', 20)
text_l = font2.render("Пропущено " + str(balls_missed_l), 1, (0, 0, 255))
text_r = font2.render("Пропущено " + str(balls_missed_r), 1, (255, 0, 0))

window = display.set_mode((win_width, win_height))
display.set_caption("Пінг понг")

background = transform.scale(image.load("background_ping_pong.png"), (win_width, win_height))

player_l = Player(10, 100, "l_ping_pong.png", 5, win_height / 2 - 25, 5)

player_r = Player(10, 100, "r_ping_pong.png", win_width - 13, win_height / 2 - 25, 5)

ball = Ball(20, 20, "ball_ping_pong.png", win_width / 2 - 10, win_height / 2 - 10, 0)
ball.set_route(randint(3, 5), randint(3, 5))

b_play = Button(100, 30, "b_play.jpg", win_width / 2 - 50, win_height / 2 - 45, 0)
b_restart = Button(100, 30, "b_restart.jpg", win_width / 2 - 50, win_height / 2 - 15, 0)
b_exit = Button(100, 30, "b_exit.jpg", win_width / 2 - 50, win_height / 2 + 15, 0)


game_not_finished = True
game = True
while game:

    window.blit(background, (0, 0))
    player_l.reset()
    player_r.reset()
    ball.reset()
    window.blit(text_l, (0, 0))
    window.blit(text_r, (win_width - 120, 0))

    if game_not_finished == True:
        player_l.update("l")
        player_r.update("r")
        ball.update()

    else:
        window.blit(text_lose, (win_width / 4, 25))
        b_play.reset()
        b_restart.reset()
        b_exit.reset()
        
    if balls_missed_l == 5:
        font1 = font.SysFont('Arial', 50)
        text_lose = font1.render("Виграв червоний", 1, (255, 0, 0))
        game_not_finished = False

    if balls_missed_r == 5:
        font1 = font.SysFont('Arial', 50)
        text_lose = font1.render("Виграв синій", 1, (0, 0, 255))
        game_not_finished = False
    
    keys = key.get_pressed()
    if keys[K_ESCAPE]:
        game_not_finished = False


    
    display.update()
    clock.tick(FPS)
    
    for e in event.get():
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            x, y = e.pos
            if b_play.collidepoint(x, y):
                game_not_finished = True
            if b_restart.collidepoint(x, y):
                reset_position()
                reset_game()
                game_not_finished = True
            if b_exit.collidepoint(x, y):
                game = False

        if e.type == QUIT:
            game = False