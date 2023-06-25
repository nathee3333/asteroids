from typing import Any
from pygame import *


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.5)
fire_sound = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, pl_image, x, y, size_x, size_y, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(pl_image), (size_x, size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
width = 700
height = 500
window = display.set_mode((width, height))
background = transform.scale(image.load('galaxy.jpg'), (width, height))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < width-70:
            self.rect.x += self.speed 
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed 
        if keys[K_s] and self.rect.y < height-100:
            self.rect.y += self.speed 
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 50, 50, -15)
        bullets.add(bullet)
bullets = sprite.Group()       

from random import *
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > height:
            self.rect.y = 0
            self.rect.x = randint(0, width-100)
            lost += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

enemies = sprite.Group()
for i in range(1, 6):
    enemy = Enemy("asteroid.png", randint(0, width-100), -40, 50, 50, randint(1,5))
    enemies.add(enemy)


player = Player('rocket.png', 5, height-100, 70, 100, 10)
finish = False
run = True
display.set_caption("Космєтічка")

font.init()
mainfont = font.SysFont(None, 30)
win = mainfont.render("YOU WIN", True, (255,255,255))
lose = mainfont.render("YOU LOSE", True, (255,0,0))
score = 0
lost = 0

rel_time = False
num_fire = 0
from time import time as timer
life = 3
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    player.fire()
                    fire_sound.play()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish:
        window.blit(background, (0,0))
        text_score = mainfont.render("Рахунок: "+str(score), True, (0,255,0))
        text_lost = mainfont.render("Пропущені: "+str(lost), True, (255,0,0))
        window.blit(text_score, (10,10))
        window.blit(text_lost, (10,50))
        player.update()
        player.draw() 
        enemies.update()
        enemies.draw(window)

        bullets.update()
        bullets.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = mainfont.render("Перезарядка!", True, (0,255,0))
                window.blit(reload, (450,height-50))
            else:
                num_fire = 0
                rel_time = False


        collides = sprite.groupcollide(enemies, bullets, True, True)
        for c in collides:
            score += 1
            enemy = Enemy("asteroid.png", randint(0, width-100), -40, 50, 50, randint(1,5))
            enemies.add(enemy)
        if life == 0 or lost>10:
            finish = True
            window.blit(lose, (width-350, height-250))
        if score >= 10:
            finish = True
            window.blit(win, (width-350, height-250))
        
        if sprite.spritecollide(player, enemies, False):
            sprite.spritecollide(player, enemies, True)
            life -= 1

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
        
        text_life = mainfont.render(str(life), True, life_color)
        window.blit(text_life, (650, 10))
        

    display.update()
    time.delay(50)




