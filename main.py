from pygame import *
from random import randint
from time import time as timer
window = display.set_mode((750,500))
display.set_caption('Шутер')

mixer.init()
mixer.music.load('дуло.mp3')
mixer.music.play()
fire_sound = mixer.Sound('pusk.mp3')
damage_sound = mixer.Sound('попадание.mp3')
vzriv_sound = mixer.Sound('взрыв.mp3')
#шрифты
font.init()
font1 = font.Font(None,70)
win = font1.render('YOU WIN', True, (0,255,0))
lose = font1.render('YOU LOSE', True, (255,0,0))
font2 = font.Font(None, 40)

clock = time.Clock()
FPS = 60
game = True

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_size_x, player_size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_size_x, player_size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height,):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height

        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        global last_time
        global num_fire
        global rel_time
        key_pressed = key.get_pressed()
        if key_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.x < 670:
            self.rect.x += self.speed
        if key_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if key_pressed[K_s] and self.rect.y < 410:
            self.rect.y += self.speed
        
        if key_pressed[K_SPACE]:
            if num_fire < 3 and rel_time == False:
                num_fire += 1
                fire_sound.play()
                self.fire()
            if num_fire >= 3 and rel_time == False:
                last_time = timer()
                rel_time = True


        
    def fire(self):
        bullet = Bullet('m-20.png', self.rect.centerx, self.rect.top, 12, 20, 20)
        bullets.add(bullet)
        
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        #сколько прошло кораблей
        global lost
        #проверка выхода за Игрока
        if self.rect.x < 50:
            self.rect.x = randint(1,670)
            self.rect.y = 0
            lost = lost + 1
class Boss(GameSprite):
    def update(self):
        self.rect.x -= self.speed


class Moved_Enemy(GameSprite):
    direct = 'left'
    def update(self):
        if self.rect.x <= 410:
            self.direct = 'right'
        if self.rect.x >= 610:
            self.direct = 'left'
        

        if self.direct == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x <= 0:
            self.kill()

background = GameSprite('bg.jpg', 0,0,0,750,500)
m_h = Player('pvo.png', 100,100,10,80,80)
boss = Boss('boss.png', randint(50, 650), 10, 100, 100, 2)
rocket = GameSprite('m-20.png', 300,400,10,20,20)
dulo = mixer.Sound('pusk.mp3')
enemy1 = Moved_Enemy('zlodey.png', 400, 250,5,80,80)
enemys = sprite.Group()
for i in range(1, 8):
    enemy = Enemy('самолёт пригожина.png', 700, randint(50, 500), 1, 100,105)
    enemys.add(enemy)
#spisok pul`
bullets = sprite.Group()
score = 0
goal = 1000
finish = False
run = True
last_time = 0
num_fire = 0
rel_time = False
life = 3
boss_hp = 15

w1 = Wall(255, 0, 0, 400, 20, 450, 10)
w2 = Wall(255, 0, 0, 100, 20, 300, 10)
w3 = Wall(255, 0, 0, 300, 10, 20 , 400)
w4 = Wall(255, 0, 0, 400, 10, 10, 400)
w5 = Wall(255, 0, 0, 200, 400, 300, 5)
win_s = GameSprite('pobeda.jpg', 550, 100, 7,90,90)


start_game = timer()


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    text_score = font2.render('Самолётов сбито: '+str(score), True, (255,255,255))
    text_lose = font2.render('Потерь: ' +str(lost),True,(255,255,255))
    text_life = font2.render('Жизни: ' +str(life),True,(255,0,0))

    collides = sprite.groupcollide(enemys, bullets, True, True)
    if collides:
        vzriv_sound.play()
    for c in collides:
        score = score + 1
        enemy = Enemy('самолёт пригожина.png', 700, randint(50, 650), 1, 100,105)
        enemys.add(enemy)
        



    if not finish:
        background.reset()
        window.blit(text_score, (10,10))
        window.blit(text_lose, (10,50))
        window.blit(text_life, (600,50))
        m_h.reset()
        if score > 30:
            boss.reset()

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 0.5:
                ammo_now = font2.render('нет ракет', 1, (255, 0, 0))
                window.blit(ammo_now, (260,460))
            else:
                num_fire = 0
                rel_time = False


        
        m_h.update()
        enemys.draw(window)
        bullets.draw(window)
        enemys.update()
        enemy1.reset()
        enemy1.update()
        boss.update()
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        win_s.reset()
        key_pressed = key.get_pressed()
        if key_pressed[K_SPACE]:
            dulo.play()
        bullets.update()
        if sprite.spritecollide(boss, bullets, True):
            boss_hp -= 1
        if sprite.spritecollide(m_h, enemys, True) or lost >= 10:
            life -= 1
            enemy = Enemy('самолёт пригожина.png', 10, randint(50, 650), 1, 100,105)
            enemys.add(enemy)
            damage_sound.play()
        if sprite.collide_rect(m_h, enemy) or sprite.collide_rect(m_h, w1)  or sprite.collide_rect(m_h, w2) or sprite.collide_rect(m_h, w3)  or sprite.collide_rect(m_h, w4) or sprite.collide_rect(m_h, w5):
            window.blit(lose, (300, 300))
            m_h.rect.x = 100
            m_h.rect.y = 70


        if life <= 0:
            finish = True
            window.blit(lose,(200, 200))
        if score >= goal:
            finish = True
            window.blit(win, (750/2, 500/2))

        if sprite.collide_rect(m_h, win_s):
            window.blit(win, (300, 300))
            m_h.rect.x = 100
            m_h.rect.y = 70
        
        
    
        


        if boss_hp <= 0:
            boss.kill()
        display.update()
    clock.tick(FPS)