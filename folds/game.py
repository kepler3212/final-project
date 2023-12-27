#import libraries
import pygame
from pygame import mixer
from pygame import *
from random import randint,choice
import math

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.Font(None, 36)



mixer.init()
mixer.music.load('music.ogg')
mixer.music.play()

#game window

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
window = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Castle Defender')

clock = pygame.time.Clock()
FPS = 60


goal = 20 
score = 0
lost = 0 
health = 300
max_lost = 3



#load images
score_img = pygame.transform.scale(pygame.image.load('score.png'), (50,50))
#missed_img = pygame.transform.scale(pygame.image.load('missed.png'), (80,80))
health_img = pygame.transform.scale(pygame.image.load('health.png'), (50,50))
score_img_rect = score_img.get_rect()


#background
bg = pygame.transform.scale(pygame.image.load('background.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
#castle
castle_img_100 = pygame.image.load('castle.png')

#bullet image
bullet_img = pygame.image.load('arrow.png')
b_w = bullet_img.get_width()
b_h = bullet_img.get_height()
bullet_img = pygame.transform.scale(bullet_img, (int(b_w * 0.075), int(b_h * 0.075)))


WHITE = (255, 255, 255)

#gamesprite class
class GameSprite(pygame.sprite.Sprite):
	def __init__(self,x ,y ,speed, image, w , h):
		pygame.sprite.Sprite.__init__(self)
		self.w = w
		self.h = h
		self.speed = speed 
		self.image = pygame.transform.scale(pygame.image.load(image), (w,h))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def show(self):
		screen.blit(self.image, self.rect)	

	#enemyclass	
class Enemy(GameSprite):
	def update(self):
		self.rect.x += self.speed
		if self.rect.x > SCREEN_WIDTH:
			self.rect.x = 0
			self.rect.y = 0
			lost = lost + 1



#castle class
class Castle():
	def __init__(self, image100, x, y, scale):
		self.health = 30
		self.max_health = self.health
		self.fired = False

		width = image100.get_width()
		height = image100.get_height()

		self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale))) 
		self.rect = self.image100.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.score = 0

				
			

	#shoot function
	def shoot(self):
		pos = pygame.mouse.get_pos()
		x_dist = pos[0] - self.rect.midleft[0]
		y_dist = -(pos[1] - self.rect.midleft[1])
		self.angle = math.degrees(math.atan2(y_dist, x_dist))
		
		if pygame.mouse.get_pressed()[0] and self.fired == False:
			self.fired = True
			bullet = Bullet(bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
			bullet_group.add(bullet)
		#
		if pygame.mouse.get_pressed()[0] == False:
			self.fired = False



	def draw(self):
		self.image = self.image100

		screen.blit(self.image, self.rect)


#bullet class
class Bullet(pygame.sprite.Sprite):
	def __init__(self, image, x, y, angle):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.angle = math.radians(angle)
		self.speed = 20
		
		self.dx = math.cos(self.angle) * self.speed
		self.dy = -(math.sin(self.angle) * self.speed)


	def update(self):
		
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
			self.kill()			

		
		self.rect.x += self.dx
		self.rect.y += self.dy



castle = Castle(castle_img_100, SCREEN_WIDTH - 300, SCREEN_HEIGHT - 500, 0.15)
win_img = pygame.image.load('win.png')
lose_img = pygame.image.load('over.png')


#groups 
 
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
for i in range(1, 8):  
	image = choice([ 'dragon2.png', 'dragon3.png']) 
	enemy = Enemy (-20 ,randint(75, 550 ), randint(5, 10),  image, 100,100 )
	enemy_group.add(enemy)





#game loop
run = True
finish = False 
while run:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	if not finish:
		#blits
		screen.blit(bg, (0, 0))
		window.blit(score_img, (25,8))
		#window.blit(missed_img, (10,50))
		window.blit(health_img,(20,100))

		#score text and show
		text = font2.render('score: ' + str(score), 1, (0, 0, 0))
		window.blit(text, (10, 60))

		#text_lose = font2.render("Missed: " + str(lost), 1, (0, 0, 0))
		#window.blit(text_lose, (10, 110))

		text_hp = font2.render("health: " + str(castle.health), 1, (0,0 ,0))
		window.blit(text_hp, (10, 150))



		#draw castle
		castle.draw()
		castle.shoot()
		enemy_group.update()
		""" for i in enemy_group:
			enemy.show() """

		bullet_group.update()
		bullet_group.draw(screen)
		enemy_group.draw(screen)  
		#print(len(bullet_group)) 

		#collides
		collides = pygame.sprite.groupcollide(bullet_group, enemy_group, True, True)
		for i in collides:
			score = score + 1 
			image = choice([ 'dragon2.png', 'dragon3.png']) 
			enemy = Enemy (-20 ,randint(75, 550 ), randint(5, 10),  image, 100,100 )
			
			enemy_group.add(enemy)
			 

		
		collides2 = pygame.sprite.spritecollide(castle, enemy_group,True)
		for i in collides2:
			castle.health -= 10
			print(castle.health)
			image = choice([   'dragon2.png', 'dragon3.png']) 
			enemy = Enemy (-20 ,randint(75, 550 ), randint(5, 10),  image, 100,100 ) 
			enemy_group.add(enemy)

		if  score >= goal:
			finish = True
			window.blit(win_img, (100,100))


		if   castle.health < 0:

			finish = True
			window.blit(lose_img, (100,70))
		
		
		

		#update display window
		pygame.display.update()

	pygame.time.delay(50)
	