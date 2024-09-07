from pygame import *
from random import randint

#background music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN', True, (255, 255, 255))
lose = font1.render('YOU LOSE', True, (255, 0, 0))
font2 = font.Font(None, 36)

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_asteroid = 'asteroid.png'

score = 0
lost = 0
goal = 20
max_lost = 5

# parent class for other sprites
class GameSprite(sprite.Sprite):
  # class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # We call the class constructor (Sprite):
        sprite.Sprite.__init__(self)

        # each sprite must store an image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # each sprite must store the rect property it is inscribed in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
  # method that draws the character in the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Player class
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet) 
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed  
        if self.rect.y < 0:
            self.kill()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0 
            lost += 1

# Create the window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# create sprites
ship = Player('rocket.png', 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range (1, 5):
    monster = Enemy(img_enemy, randint(70, win_width-70), -40, 70, 50, randint(1, 3))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range (1):          
    asteroid = Enemy(img_asteroid, randint(70, win_width-70), -40, 70, 50, randint(1, 2))
    asteroids.add(asteroid)

bullets = sprite.Group()
clock = time.Clock()
# the "game over" variable: as soon as it is True, the sprites stop working in the main loop
finish = False
# main game loop
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()
            
    if not finish:
        window.blit(background, (0,0))
        
        text_score = font2.render('Score: ' + str(score), True, (255, 255, 255))
        window.blit(text_score, (10, 20))

        text_missed = font2.render('Missed: ' + str(lost), True, (255, 255, 255))
        window.blit(text_missed, (10, 50))

        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        
        sprite.groupcollide(asteroids, bullets, False, True)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1

            monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost or sprite.spritecollide(ship, asteroids, False):
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()
        
    clock.tick(60)