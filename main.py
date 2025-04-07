import pygame_menu
from pygame import *
from time import time as timer
from random import randint
mixer.init()
font.init()
window_y = 900
window_x = 1400
window = display.set_mode((window_x, window_y))
background = transform.scale(image.load('background.jpg'), (window_x, window_y))
living1 = transform.scale(image.load('alive.png'), (60, 80))
living2 = transform.scale(image.load('alive.png'), (60, 80))
living3 = transform.scale(image.load('alive.png'), (60, 80))
dead1 = transform.scale(image.load('dead.png'), (60, 80))
dead2 = transform.scale(image.load('dead.png'), (60, 80))
dead3 = transform.scale(image.load('dead.png'), (60, 80))
showing_tank = transform.scale(image.load('hero.png'), (200, 200))

mixer.music.load('soundtrack.ogg')
mixer.music.set_volume(0.5)
mixer.music.play()
shot = mixer.Sound('shot.ogg')
lose = mixer.Sound('lose.ogg')
win_sound = mixer.Sound('win.ogg')
reloading_sound = mixer.Sound('reloading.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, length):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, length))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < window_x - 100:
            self.rect.x += self.speed
        if keys_pressed[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < window_y - 100:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15, 25, 35)
        bullets.add(bullet)

lost = 0
win = 0
lives = 3

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > window_y + 50:
            self.rect.x = randint(0, window_x - 200)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()

class Barrier(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > window_y + 50:
            self.rect.x = randint(0, window_x - 200)
            self.rect.y = 0

font = font.Font(None, 80)

tanks1 = sprite.Group()
tanks2 = sprite.Group()
tanks3 = sprite.Group()
bullets = sprite.Group()
barriers = sprite.Group()
for _ in range(2):
    tank1 = Enemy('enemy_1.png', randint(0, window_x), -40, randint(1, 2), 100, 100)
    tank2 = Enemy('enemy_2.png', randint(0, window_x), -40, randint(1, 2), 100, 100)
    tank3 = Enemy('enemy_3.png', randint(0, window_x), -40, randint(1, 2), 100, 100)
    tanks1.add(tank1)
    tanks2.add(tank2)
    tanks3.add(tank3)

barrier = Barrier('barrier.png', randint(0, window_x), -40, randint(1, 2), 100, 100)
barriers.add(barrier)

clock = time.Clock()
FPS = 60
game = True
finish = False
rel_time = False
num_fire = 0

main_sprite = Player('hero.png', 700, 600, 5, 100, 100)
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 5 and rel_time == False:
                    main_sprite.fire()
                    shot.play()
                    num_fire += 1
                if num_fire > 5 and rel_time == False:
                    rel_time = True
                    start_time = timer()
                    reloading_sound.play()

    if finish != True:
        window.blit(background, (0, 0))
        main_sprite.reset()
        main_sprite.update()
        text_missed = font.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_missed, (0, 0))
        text_destroyed = font.render("Уничтожено: " + str(win), 1, (255, 255, 255))
        window.blit(text_destroyed, (0, 100))
        bullets.draw(window)
        bullets.update()

        tanks1.draw(window)
        tanks1.update()

        tanks2.draw(window)
        tanks2.update()

        tanks3.draw(window)
        tanks3.update()

        barriers.draw(window)
        barriers.update()

        if rel_time == True:
            finish_time = timer()
            if finish_time - start_time < 3:
                reloading = font.render('reloading...', True, (220, 0, 0))
                window.blit(reloading, (600, 750))
            else:
                rel_time = False
                num_fire = 0

        sprites_list1 = sprite.groupcollide(tanks1, bullets, True, True)
        sprites_list2 = sprite.groupcollide(tanks2, bullets, True, True)
        sprites_list3 = sprite.groupcollide(tanks3, bullets, True, True)

        for _ in sprites_list1:
            win += 1
            tank1 = Enemy('enemy_1.png', randint(0, window_x), -40, randint(1, 2), 100, 100)
            tanks1.add(tank1)
        for _ in sprites_list2:
            win += 1
            tank2 = Enemy('enemy_2.png', randint(0, window_x), -40, randint(1, 2), 100, 100)
            tanks2.add(tank2)
        for _ in sprites_list3:
            win += 1
            tank3 = Enemy('enemy_3.png', randint(0, window_x), -40, randint(1, 2), 100, 100)
            tanks3.add(tank3)
        
        if sprite.spritecollide(main_sprite, barriers, True) or sprite.spritecollide(main_sprite, tanks1, True) or sprite.spritecollide(main_sprite, tanks2, True) or sprite.spritecollide(main_sprite, tanks3, True):
            lives -= 1

        if win >= 10:
            win_sound.play()
            finish = True
            win = font.render('You defended the D point!', 1, (250, 250, 0))
            window.blit(win, (500, 300))
        
        if lost >= 3 or lives == 0:
            lose.play()
            finish = True
            win = font.render('Enemy captured the D point', 1, (255, 0, 0))
            window.blit(win, (500, 300))
        

        window.blit(showing_tank, (1200, 0))
        
        if lives == 3:
            window.blit(living1, (1270, 10))
            window.blit(living2, (1240, 100))
            window.blit(living3, (1300, 100))
        
        if lives == 2:
            window.blit(living1, (1270, 10))
            window.blit(living2, (1240, 100))
            window.blit(dead1, (1300, 100))
        
        if lives == 1:
            window.blit(living1, (1270, 10))
            window.blit(dead1, (1240, 100))
            window.blit(dead2, (1300, 100))
        
        if lives == 0:
            window.blit(dead1, (1270, 10))
            window.blit(dead2, (1240, 100))
            window.blit(dead3, (1300, 100))

        display.update()
        clock.tick(FPS)
