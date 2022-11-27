from kandinsky import *
from time import *
from ion import *
from math import sin, cos, radians
from random import randint

class Paddle:
    def __init__(self):
        self.x,self.y=20,100
        self.movement="still"

    def move(self):
        if keydown(KEY_UP) and self.y>20:
            self.y-=8
            self.movement="up"
        elif keydown(KEY_DOWN) and self.y<185:
            self.y+=8
            self.movement="down"
        else:self.movement="still"
    
    def update(self):
        self.move()
        fill_rect(self.x,self.y,8,25,(0,0,0))

class Ball:
    def __init__(self):
        self.velocity=8
        self.angle=randint(-15,15)
        self.angle_update()
        self.x,self.y=40,110
        self.simu_x,self.simu_y=self.x,self.y
    
    def angle_update(self):
        self.vx=self.velocity*cos(radians(self.angle))#calcul each axis velocity in function of velocity and angle
        self.vy=self.velocity*sin(radians(self.angle))
    
    def move(self):
        self.simu_x+=self.vx
        self.simu_y+=self.vy
        
    def collision(self):
        global run
        if self.simu_y<20:#ceilling collided
            self.simu_y=20
            self.angle=-self.angle
            self.angle_update()
        elif self.simu_y>205:#floor collided
            self.simu_y=205
            self.angle=-self.angle
            self.angle_update()
        
        if self.simu_x>245:#right wall collided
            self.simu_x=245
            self.angle=180-self.angle
            self.angle_update()
        elif self.simu_x<0:run=False #ball out (=game over)
        
        if self.simu_x<28 and 28<self.x and self.simu_y<paddle.y+25 and self.simu_y+5>paddle.y:#paddle collided
            self.simu_x=28
            self.angle=180-self.angle+randint(-6,6)#angle caclul +paddle movement factor +random variation
            if paddle.movement=="up":self.angle-=30
            elif paddle.movement=="down":self.angle+=30
            self.angle_update()
            game.score+=1
            self.velocity+=0.5

    def update(self):
        self.move()
        self.collision()
        self.x,self.y=self.simu_x,self.simu_y
        fill_rect(round(self.x),round(self.y),5,5,(0,0,0))

class Game:
    def __init__(self):
        self.score=0
        fill_rect(0,0,300,20,(0,0,0))#ceilling
        fill_rect(250,0,70,230,(0,0,0))#wall
        fill_rect(0,210,300,15,(0,0,0))#floor
        
    def update(self):
        fill_rect(0,20,250,190,(255,255,255))#clear screen
        draw_string("score: "+str(self.score),20,0,(255,255,255),(0,0,0))
        paddle.update()
        ball.update()
        sleep(0.05)
        
while True:
    ok=False
    run=True
    game=Game()
    ball=Ball()
    paddle=Paddle()
    while run: #run the game
        game.update()
    fill_rect(0,0,320,225,(0,0,0)) #death screen
    draw_string("Game Over, Press OK",60,80,(255,0,0),(0,0,0))
    draw_string("Score: "+str(game.score),100,110,(255,0,0),(0,0,0))
    while not ok:
        if keydown(KEY_OK): ok=True#restart the game on keydown