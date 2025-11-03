import pygame as g
import random as r
import sys as s
import math as m
from pygame.math import Vector2

g.init()

WIDTH, HEIGHT = 720,720
WIN = g.display.set_mode((WIDTH,HEIGHT))
start = False

settingname = ["worm speed", "field size", "max apple n."]
settings = [2,3,1]
selected = 0

def drawtext(text,size,color,centerx,centery):
    font = g.font.Font('HERCULESPIXELFONTREGULAR-OVAX0.OTF', size)
    rtext = font.render(str(text),True,color)
    textrect = rtext.get_rect(center = (centerx, centery))
    WIN.blit(rtext, textrect)


while(start == False):
    WIN.fill((0,100,10))
    
    for i in range (len(settings)):

        if selected == i:
            drawtext(settingname[i],30,"yellow",WIDTH/2-250+i*250,90)
            drawtext(settings[i],50,"yellow",WIDTH/2-250+i*250,150)
        else:
            drawtext(settingname[i],30,"black",WIDTH/2-250+i*250,90)
            drawtext(settings[i],50,"black",WIDTH/2-250+i*250,150)

    drawtext("Use arrow keys to change settings",30,"black",WIDTH/2,220)
    drawtext("Press SPACE to start",30,"black",WIDTH/2,500)
    
    g.display.update()

    for event in g.event.get():
        if event.type == g.QUIT:
            s.exit()
        elif event.type == g.KEYDOWN:
            if event.key == g.K_SPACE:
                start = True
            if event.key == g.K_UP:
                if selected < 2 and settings[selected] < 5:
                    settings[selected] += 1
                elif selected == 2 and settings[2] < 15:
                    settings[2] += 1
            if event.key == g.K_DOWN and settings[selected] > 1:
                settings[selected] -= 1
            if event.key == g.K_LEFT and selected > 0:
                selected -= 1
            if event.key == g.K_RIGHT and selected < len(settings)-1:
                selected += 1

gsize = [9,80,12,60,18,40,24,30,36,20]

settings[0] -= 1; settings[1] -= 1

cellnum, cellsize = gsize[settings[1]*2],gsize[settings[1]*2+1]

clock = g.time.Clock()
g.display.set_caption("Worm Game")

ferrari = g.mixer.Sound("ferrari.mp3")
ferraritimer = 1080

class FRUIT:
    def __init__(self):
        self.x = []
        for i in range(settings[2]): self.x.append(r.randint(0,cellnum-1))
        self.y = []
        for i in range(settings[2]): self.y.append(r.randint(0,cellnum-1))
        self.pos = []
        for i in range(settings[2]): self.pos.append(Vector2(self.x[i],self.y[i]))
        self.longcrunch = g.mixer.Sound("longcrunch.wav")
        self.shortcrunch = g.mixer.Sound("shortcrunch.wav")

    def draw(self):
        for i in range(settings[2]):
            fruit_rect = g.Rect(self.x[i]*cellsize,self.y[i]*cellsize,cellsize,cellsize)
            WIN.blit(apple,fruit_rect)

    def eaten(self,fi):
        self.x[fi] = r.randint(0,cellnum-1)
        self.y[fi] = r.randint(0,cellnum-1)
        self.pos[fi] = Vector2(self.x[fi],self.y[fi])
        
        if r.randint(0,1) == 0:
            self.longcrunch.play()
        else:
            self.shortcrunch.play()

class SNAKE:
    def __init__(self):
        self.snakebody = g.transform.scale(g.image.load('snakebody.png').convert_alpha(), (cellsize,cellsize))
        self.snakecorner = g.transform.scale(g.image.load('snakecornertr.png').convert_alpha(), (cellsize,cellsize))
        self.snakehead = g.transform.scale(g.image.load('snakeheadright.png').convert_alpha(), (cellsize,cellsize))
        self.snaketail = g.transform.scale(g.image.load('snaketail.png').convert_alpha(), (cellsize,cellsize))
        self.initxy = m.floor(cellnum/2)-1
        self.body = [Vector2(self.initxy,self.initxy),Vector2(self.initxy+1,self.initxy),Vector2(self.initxy+2,self.initxy)]
        self.direction = Vector2(0,0)
        self.addblock = False

    def draw(self):
        for index,block in enumerate(self.body):
            block_rect = g.Rect(block.x*cellsize,block.y*cellsize,cellsize,cellsize)

            if index == 0:
                if self.direction == (0,1):
                    WIN.blit(g.transform.rotate(self.snakehead,270),block_rect)
                elif self.direction == (0,-1):
                    WIN.blit(g.transform.rotate(self.snakehead,90),block_rect)
                elif self.direction == (1,0):
                    WIN.blit(self.snakehead,block_rect)
                elif self.direction == (-1,0):
                    WIN.blit(g.transform.rotate(self.snakehead,180),block_rect)
            elif index == len(self.body)-1:
                taildir = self.body[-2] - self.body[-1]
                if taildir == (1,0):
                    WIN.blit(self.snaketail,block_rect)
                elif taildir == (-1,0):
                    WIN.blit(g.transform.rotate(self.snaketail, 180),block_rect)
                elif taildir == (0,1):
                    WIN.blit(g.transform.rotate(self.snaketail, 270),block_rect)
                elif taildir == (0,-1):
                    WIN.blit(g.transform.rotate(self.snaketail, 90),block_rect)
            else:
                previous = self.body[index+1] - block 
                next = self.body[index-1] - block
                bodydir = self.body[index] - self.body[index + 1]

                if previous.x == next.x:
                    if bodydir == (0,-1):
                        WIN.blit(g.transform.rotate(self.snakebody, 90),block_rect)
                    elif bodydir == (0,1):
                        WIN.blit(g.transform.rotate(self.snakebody, 270),block_rect)
                elif previous.y == next.y:
                    if bodydir == (-1, 0):
                        WIN.blit(g.transform.rotate(self.snakebody, 180),block_rect)
                    elif bodydir == (1,0):
                        WIN.blit(self.snakebody,block_rect)    
                else:
                    if previous.x == -1 and next.y == -1 or previous.y == -1 and next.x == -1:
                        WIN.blit(g.transform.rotate(self.snakecorner, 270),block_rect)
                    if previous.x == -1 and next.y == 1 or previous.y == 1 and next.x == -1:
                        WIN.blit(self.snakecorner,block_rect)
                    if previous.x == 1 and next.y == -1 or previous.y == -1 and next.x == 1:
                        WIN.blit(g.transform.rotate(self.snakecorner, 180),block_rect)
                    if previous.x == 1 and next.y == 1 or previous.y == 1 and next.x == 1:
                        WIN.blit(g.transform.rotate(self.snakecorner, 90),block_rect)

    
    def move(self):
        if self.addblock:   
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.addblock = False    
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

class LOGIC:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.score10sound = g.mixer.Sound("10score.mp3")
        self.dead = False
        self.wilhelmscream = g.mixer.Sound("wilhelmscream.wav")

    def update(self,sdir):
        if self.dead == False:

            if sdir == 0:
                self.snake.direction = Vector2(-1,0)
            if sdir == 1:
                self.snake.direction = Vector2(1,0)
            if sdir == 2:
                self.snake.direction = Vector2(0,-1)
            if sdir == 3:
                self.snake.direction = Vector2(0,1)

            if self.snake.direction.x == 1 and sdir == 0:
                self.snake.direction = Vector2(1,0)
            if self.snake.direction.x == -1 and sdir == 1:
                self.snake.direction = Vector2(-1,0)
            if self.snake.direction.y == 1 and sdir == 2:
                self.snake.direction = Vector2(0,1)
            if self.snake.direction.y == -1 and sdir == 3:
                self.snake.direction = Vector2(0,-1)

            self.snake.move()
            
            for fi in range(settings[2]):
                self.collisioncheck(fi)
            
            self.checkdeath()

    def draw(self):
        if not self.dead:
            WIN.blit(BG, (0,0))
            self.fruit.draw()
            self.snake.draw()
            self.drawscore()
        else:
            WIN.fill((0,100,10))
            drawtext("You Died!",100,"black",WIDTH/2,HEIGHT/2-100)
            drawtext(f"Score: {len(self.snake.body)-3}",100,"black",WIDTH/2,HEIGHT/2)
            drawtext("Press SPACE to restart",50,"black",WIDTH/2,HEIGHT/2+100)
        g.display.update()

    def collisioncheck(self,fi):
        for i,j in enumerate((self.snake.body)):
            if self.fruit.pos[fi] == j and i == 0:
                self.fruit.eaten(fi)
                self.snake.addblock = True
                if (len(self.snake.body)-2) % 10 == 0:
                    self.score10sound.play()
            elif self.fruit.pos[fi] == j:
                self.fruit.x[fi] = r.randint(0,cellnum-1)
                self.fruit.y[fi] = r.randint(0,cellnum-1)
                self.fruit.pos[fi] = Vector2(self.fruit.x[fi],self.fruit.y[fi])
                    
    def checkdeath(self):
        if not ((-1 < self.snake.body[0].x < cellnum) and (-1 < self.snake.body[0].y < cellnum)):
            self.dead = True
            self.wilhelmscream.play()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
               self.dead = True
               self.wilhelmscream.play()

    def drawscore(self):
        drawtext(f"Score: {len(self.snake.body)-3}",25,"black",65,18)


BG = g.transform.scale(g.image.load("grass.jpg"), (WIDTH,HEIGHT))
apple = g.transform.scale(g.image.load('apple.png').convert_alpha(), (cellsize,cellsize))

SCREEN_UPDATE = g.USEREVENT
g.time.set_timer(SCREEN_UPDATE,150 - settings[0]*30)

game = LOGIC()
sdir = 3

ferrarichannel = g.mixer.Channel(5)

while(1):

    if settings[0] > 3:
        if not ferrarichannel.get_busy() :
            ferrarichannel.play(ferrari)

        if game.dead:
            ferrari.stop()


    for event in g.event.get():
        if event.type == g.QUIT:
            s.exit()  
        if event.type == SCREEN_UPDATE:
            game.update(sdir) 

    keys = g.key.get_pressed()
    if (keys[g.K_LEFT] or keys[g.K_a]):
        if game.snake.direction.x != 1:
           sdir = 0
    if (keys[g.K_RIGHT] or keys[g.K_d]):
        if game.snake.direction.x != -1:
            sdir = 1
    if (keys[g.K_UP] or keys[g.K_w]):
        if game.snake.direction.y != 1:
            sdir = 2
    if (keys[g.K_DOWN] or keys[g.K_s]):
        if game.snake.direction.y != -1:
            sdir = 3
    if keys[g.K_SPACE] and game.dead == True:
        game.snake.body = [Vector2(game.snake.initxy,game.snake.initxy),Vector2(game.snake.initxy+1,game.snake.initxy),Vector2(game.snake.initxy+1,game.snake.initxy)]
        sdir = 3
        game.dead = False

    game.draw()
    