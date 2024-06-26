from pygame import *
from random import randint
from time import time as timer #імпортуємо функцію для засікання часу, щоб інтерпретатор не шукав цю функцію в pygame модулі time, даємо їй іншу назву самі


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('shootsound2.mp3')

font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 80)
win = font2.render('YOU WIN!', True, (255, 255, 255))
lose = font2.render('YOU LOSE!', True, (180, 0, 0))


img_back = "image (1).png"
img_hero = "12.png"
img_enemy = "warrior2.png"
img_non_killable_enemy = "warrior1.0 (1).png"
img_health = "health_kit-removebg-preview.png"
img_superEnemy = "big.png"
ammo = "ammo.png"



score = 0
lost = 0
goal = 100
max_lost = 30
life = 5
isBoss_spawned = False  

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, sixe_y , sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_img),(size_x, sixe_y))
        self.speed = sprite_speed
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 90:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:  
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 90:  
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx - 5, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed ):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)   
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint (80, win_width - 80)
            self.rect.y = 0
            lost +=1

class ShootingEnemy(GameSprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed ):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)
        self.shootTime = timer()
        self.isShooted = False  
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 150:
            self.speed = 0
    def shoot(self):
        enemyBullet = EnemyBullet("pulya (1).png", self.rect.centerx - 5, self.rect.bottom, 25, 30, 15)
        enemyBullets.add(enemyBullet)
        print('spawned')

class Asteroid(GameSprite):
     def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed ):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)  
     def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint (80, win_width - 80)
            self.rect.y = 0
            lost +=1


class SuperEnemy(Enemy):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed, max_hits, isBoss = False):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)
        self.max_hits = max_hits
        self.isBoss = isBoss
    def gotHit(self):
        self.max_hits -= 1
    def isKilled(self):
        if(self.max_hits <= 0):
            self.kill()
            return True
        else: return False


class HealthPack(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint (80, win_width - 80)
            self.rect.y = 0 
    def apply(self):
        global life
        life += 1
        self.kill()

class Ammo(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint (80, win_width - 80)
            self.rect.y = 0 
    def apply(self):
        global num_fire
        num_fire +=10
        self.kill()

class Bullet(GameSprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)
        # self.image = transform.rotate(self.image, 90)
    def update(self):
        self.rect.y += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.y < 0:
            self.kill()

class EnemyBullet(GameSprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)
        # self.image = transform.rotate(self.image, 180)
    def update(self):
        self.rect.y += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.y > 500:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (win_width, win_height))

player = Player(img_hero, 7, win_height - 100, 65, 75, 12)
# health_pack = HealthPack(img_health, randint(30, win_width - 30), -40, 30, 30, 7)



health_packs = sprite.Group()
bullets = sprite.Group()
enemyBullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
superMonsters = sprite.Group()
ammo_packs = sprite.Group()
shootingEnemies = sprite.Group()
# health_packs.add(health_pack)

for i in range(1, 4):
    monster = Enemy(img_enemy, randint(0, win_width - 100), randint(-200, 0), 80, 80, 1 )
    monsters.add(monster)
for i in range(1, 3):
    shootingEnemy = ShootingEnemy(img_enemy, randint(0, win_width - 100), randint(-200, 0), 80, 80, 2 )
    shootingEnemies.add(shootingEnemy)
for i in range(1, 4):
    asteroid = Asteroid(img_non_killable_enemy, randint(0, win_width - 100), randint(-150,  0), 80, 80, 7,)
    asteroids.add(asteroid)
for i in range(1, 3):
    superMonster = SuperEnemy(img_superEnemy, randint(0, win_width - 100), randint(-110,  0) , 80, 50, randint(1, 3), 3)
    superMonsters.add(superMonster)


run = True
finish = False
clock = time.Clock()
FPS = 30
num_fire = 20  # змінна для підрахунку пострілів    


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN and not finish: ###
            if e.key == K_SPACE:
                if num_fire > 0:   
                    num_fire -= 1
                    fire_sound.play()
                    player.fire()
                   
              

    if not finish:
        window.blit(background, (0, 0))
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        health_packs.update()
        superMonsters.update()
        ammo_packs.update()
        shootingEnemies.update()
        enemyBullets.update()
        
        health_packs.draw(window)
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        superMonsters.draw(window)
        ammo_packs.draw(window)
        shootingEnemies.draw(window)
        enemyBullets.draw(window)

        if life == 1 and len(health_packs) == 0:
            health_pack = HealthPack(img_health, randint(30, win_width - 30), -40, 30, 30, 7)
            health_packs.add(health_pack)

        if num_fire <=5 and len(ammo_packs) == 0:
            ammo_pack = Ammo(ammo, randint(80, win_width - 80), -40, 30, 30, 5)
            ammo_packs.add(ammo_pack)
        if score >= 10:
            if isBoss_spawned == False:
                superMonster = SuperEnemy(img_superEnemy, 350, -110 , 160, 100, randint(1, 3), 5,True)
                superMonsters.add(superMonster)
                isBoss_spawned = True

     

        

        # перевірка зіткнення кулі та монстрів (і монстр, і куля при зіткненні зникають)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            # цей цикл повториться стільки разів, скільки монстрів збито
            score = score + 1
            if isBoss_spawned ==False:
                monster = Enemy(img_enemy, randint(0, win_width - 100), randint(-200, 0), 80, 80, 1 )
                monsters.add(monster)

        collides = sprite.groupcollide(asteroids, bullets, True, True)
        for collide in collides:
              score = score + 2
              if isBoss_spawned ==False:
                asteroid = Asteroid(img_non_killable_enemy, randint(0, win_width - 100), randint(-150,  0), 80, 80, 5,)
                asteroids.add(asteroid)

        collides = sprite.groupcollide(shootingEnemies, bullets, True, True)
        for collide in collides:
            score = score + 2
            if isBoss_spawned ==False:
                shootingEnemy = ShootingEnemy(img_enemy, randint(0, win_width - 100), randint(-200, 0), 80, 80, 2 )
                shootingEnemies.add(shootingEnemy)



        for superMonster in superMonsters:
            if sprite.spritecollide(superMonster, bullets, True):
                superMonster.gotHit()
                if superMonster.isKilled():
                    if superMonster.isBoss == False:
                        score = score + 4
                        if isBoss_spawned ==False:
                            superMonster = SuperEnemy(img_superEnemy, randint(0, win_width - 100), randint(-110,  0) , 80, 50, randint(1, 3), 3)
                            superMonsters.add(superMonster)
                    else:
                        score=score+70
            now_time = timer()
            
            for shootingEnemy in shootingEnemies: 
                if shootingEnemy.rect.y > 150:
                    if(shootingEnemy.isShooted == False):
                        shootingEnemy.shoot()
                        shootingEnemy.isShooted = True
                        shootingEnemy.shootTime = timer()
                        print('shot!')
                    if(shootingEnemy.shootTime + 1 < now_time):
                        shootingEnemy.isShooted = False

       
            
                    
                    

     
            


        # якщо спрайт торкнувся ворога зменшує життя
        if sprite.spritecollide(player, monsters, False):
            life = life - 1
            if sprite.spritecollide(player, monsters, True):
                monster = Enemy(img_enemy, randint(0, win_width - 100), randint(-200, 0), 80, 80, 1 )
                monsters.add(monster)

        if sprite.spritecollide(player, asteroids, False):
            life = life - 2
            if sprite.spritecollide(player, asteroids,True):
                asteroid = Asteroid(img_non_killable_enemy, randint(0, win_width - 100), randint(-150,  0), 80, 80, 5,)
                asteroids.add(asteroid)

        if sprite.spritecollide(player, shootingEnemies, False):
             life = life - 2
             if sprite.spritecollide(player, shootingEnemies, True):
                  shootingEnemy = ShootingEnemy(img_enemy, randint(0, win_width - 100), randint(-200, 0), 80, 80, 2 )
                  shootingEnemies.add(shootingEnemy)

        if sprite.spritecollide(player, superMonsters, False):
             life = life - 2
             if sprite.spritecollide(player, superMonsters, True):
                superMonster = SuperEnemy(img_superEnemy, randint(0, win_width - 100), randint(-110,  0) , 80, 50, randint(1, 3), 3)
                superMonsters.add(superMonster)
    
           

        if sprite.spritecollide(player, enemyBullets, False):
            life = life - 3
            sprite.spritecollide(player, enemyBullets, True)
            
           
            

        if sprite.spritecollide(player, health_packs, True):
            health_pack.apply()

        if sprite.spritecollide(player, ammo_packs, True):
            ammo_pack.apply()



        #програш
        if life <= 0 or lost >= max_lost:
            finish = True 
            window.blit(lose, (200, 200))


        # перевірка виграшу: скільки очок набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font1.render("Рахунок: " + str(score),1, (255,255,255))
        window.blit(text,(10, 20))

        text_lose = font1.render("Пропущенно: " + str(lost),1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text2 = font1.render("Набої: " + str(num_fire),1, (255,255,255))
        window.blit(text2,(10, 85))
        
    
        
        text_life = font1.render(str(life), 1, (0, 150, 0))
        window.blit(text_life, (650, 10))
        display.update()

    clock.tick(FPS)
