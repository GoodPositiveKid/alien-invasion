import sys
import time
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
class Game:
  def __init__(self):
    pygame.init()
    self.settings=Settings()
    self.screen=pygame.display.set_mode((self.settings.width,self.settings.height))
    pygame.display.set_caption('Aliens!')
    self.player = Ship(self)
    self.bullets = pygame.sprite.Group()
    self.aliens= pygame.sprite.Group()
    self.score=0
    self.create_aliens()

  def run(self):
    while True:
      self.check()
      self.update_screen()
      self.player.update()
      self.update_bullets()
      self.update_aliens()
      for bullet in self.bullets.copy():
        if bullet.rect.top <= 0:
          time.sleep(0.05)
          self.bullets.remove(bullet)

  def keydown(self, event):
    if event.key == pygame.K_RIGHT:
      self.player.right=True
    if event.key == pygame.K_LEFT:
      self.player.left=True
    elif event.key == pygame.K_q:
      exit()
    elif event.key == pygame.K_SPACE:
      self.fire_bullet()

  def keyup(self, event):
    if event.key == pygame.K_RIGHT:
      self.player.right = False
    if event.key == pygame.K_LEFT:
      self.player.left = False
  
  def fire_bullet(self):
    if len(self.bullets) < self.settings.most_bullets:
      new_bullet= Bullet(self)
      self.bullets.add(new_bullet)

  def check(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        exit()
      elif event.type == pygame.KEYDOWN:
        self.keydown(event)
      elif event.type == pygame.KEYUP:
        self.keyup(event)
    if self.score == 66:
      print('you win!')
  
  def update_screen(self):
    self.screen.fill(self.settings.bg_color)
    self.player.show()
    for bullet in self.bullets.sprites():
      bullet.bullet()
    self.aliens.draw(self.screen)
    pygame.display.flip()
  
  def update_bullets(self):
    self.bullets.update()
    number_aliens = len(self.aliens)
    collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)
    number_aliens2 = len(self.aliens)
    if number_aliens2 < number_aliens:
      self.score += number_aliens - number_aliens2
      print(self.score)

  def create_aliens(self):
    alien1 = Alien(self)
    alien_width, alien_height = alien1.rect.size
    available_width_x = self.settings.width - (2 * alien_width)
    number_aliens_x = available_width_x // (2 * alien_width)

    ship_height = self.player.rect.height
    available_width_y = (self.settings.height - (3 * alien_height) - ship_height)
    number_rows = available_width_y // (2 * alien_height)
    for rowNumber in range(number_rows):
      for alienNumber in range(number_aliens_x):
        self.make_alien(alienNumber,rowNumber)
      
  def make_alien(self,alien_Number,row_number):
    alien = Alien(self)
    alien_width,alien_height = alien.rect.size
    alien.x = alien_width + 2 * alien_width * alien_Number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    self.aliens.add(alien)

  def update_aliens(self):
    self.aliens.update()

    self.check_fleet_edges()

  def check_fleet_edges(self):
    for alien in self.aliens.sprites():
      if alien.check_edges():
        self.change_direction()
        break

  def change_direction(self):
    for alien in self.aliens.sprites():
      alien.rect.y += self.settings.drop_speed
    self.settings.direction *= -1

  
if __name__ =='__main__':
  ai=Game()
  ai.run()