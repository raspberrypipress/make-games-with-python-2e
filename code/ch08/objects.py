import pygame

class Fred():

  leftImage = None
  rightImage = None
  leftImageHit = None
  rightImageHit = None

  def __init__(self, window):
    self.window = window
    self.reset()
    self.x = self.window.get_width() / 2

  def reset(self):
    self.x = self.window.get_width() / 2
    self.y = 625

    self.isHit = False
    self.timeHit = 0
    self.health = 100

    self.direction = 1
    self.speed = 8

  def moveLeft(self, leftBound):

    if self.direction != 0:
      self.direction = 0

    if((self.x - self.speed) > leftBound):
      self.x -= self.speed  

  def moveRight(self, rightBound):

    if self.direction != 1:
      self.direction = 1

    if((self.x + self.speed) + 58 < rightBound):
      self.x += self.speed      

  def loadImages(self):
    self.leftImage = pygame.image.load("assets/Fred-Left.png")
    self.rightImage = pygame.image.load("assets/Fred-Right.png")
    self.leftImageHit = pygame.image.load("assets/Fred-Left-Hit.png")
    self.rightImageHit = pygame.image.load("assets/Fred-Right-Hit.png")

  def draw(self, time):

    if time - self.timeHit > 800:
      self.timeHit = 0
      self.isHit = False

    if self.direction == 1:
      if self.isHit is False:
        self.window.blit(self.rightImage, (self.x, self.y))
      else :
        self.window.blit(self.rightImageHit, (self.x, self.y))
    else :
      if self.isHit is False:
        self.window.blit(self.leftImage, (self.x, self.y))
      else :
        self.window.blit(self.leftImageHit, (self.x, self.y))

class Barrel():

  slots = [(4, 103), (82, 27), (157, 104), (234, 27), (310, 104), (388, 27), (463, 104), (539, 27), (615, 104), (691, 27), (768, 104), (845, 27), (920, 104)]
  slot = 0
  x = 0
  y = 0

  image = None
  brokenImage = None

  isBroken = False
  timeBroken = 0
  needsRemoving = False

  size = [33,22]
  ratio = 0.66

  vy = 1.5
  gravity = 1.05
  maxY = 20

  def split(self, time):
    self.isBroken = True
    self.timeBroken = time
    self.vy = 5
    self.x -= 10

  def checkForCollision(self, fred):

    hitX = False
    hitY = False

    if fred.x > self.x and fred.x < self.x + 75:
      hitX = True
    elif fred.x + 57 > self.x and fred.x + 57 < self.x + 75:
      hitX = True
    if fred.y + 120 > self.y and fred.y < self.y:
      hitY = True
    elif fred.y < self.y + 48:
      hitY = True
    if hitX is True and hitY is True:
      return True

  def loadImages(self):
    self.image = pygame.image.load("assets/Barrel.png")
    self.brokenImage = pygame.image.load("assets/Barrel_break.png")

  def move(self, windowHeight):

    if self.vy < self.maxY:
      self.vy = self.vy * self.gravity
    self.y += self.vy

    if self.y > windowHeight:
      self.needsRemoving = True

  def draw(self, surface):
    if self.isBroken is True:
      surface.blit(self.brokenImage, (self.x, self.y))
    else :
      surface.blit(self.image, (self.x, self.y))

  def __init__(self, slot):
    self.slot = slot
    self.x = self.slots[slot][0]
    self.y = self.slots[slot][1] + 24
