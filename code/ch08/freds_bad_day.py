import pygame, sys, random, math
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME
import objects


pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
fps = 60

win_width = 1000
win_height = 768
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Fred\'s Bad Day')
textFont = pygame.font.SysFont("monospace", 50)

gameStarted = False
gameStartedTime = 0
gameFinishedTime = 0
gameOver = False

startScreen = pygame.image.load("assets/startgame.png")
endScreen = pygame.image.load("assets/gameover.png")

background = pygame.image.load("assets/background.png")
Fred = objects.Fred(window)
Barrels = []
lastBarrel = 0
lastBarrelSlot = 0
barrelInterval = 1500

goLeft = False
goRight = False

def quitGame():
	pygame.quit()
	sys.exit()

def newBarrel():
	global Barrels, lastBarrel, lastBarrelSlot

	slot = random.randint(0, 12)

	while slot == lastBarrelSlot:
		slot = random.randint(0, 12)

	theBarrel = objects.Barrel(slot)
	theBarrel.loadImages()

	Barrels.append(theBarrel)
	lastBarrel = GAME_TIME.get_ticks()
	lastBarrelSlot = slot

Fred.loadImages()

# 'main' loop
while True:
	
	timeTick = GAME_TIME.get_ticks()

	if gameStarted is True and gameOver is False:

		window.blit(background, (0, 0))

		Fred.draw(timeTick)

		barrelsToRemove = []

		for idx, barrel in enumerate(Barrels):
			barrel.move(win_height)
			barrel.draw(window)

			if barrel.isBroken is False:

				hasCollided = barrel.checkForCollision(Fred);
				
				if hasCollided is True:
					barrel.split(timeTick)
					Fred.isHit = True
					Fred.timeHit = timeTick
					if Fred.health >= 10:
						Fred.health -= 10
					else :
						gameOver = True
						gameFinishedTime = timeTick

			elif timeTick - barrel.timeBroken > 1000:

				barrelsToRemove.append(idx)
				continue

			if barrel.needsRemoving is True:
				barrelsToRemove.append(idx)
				continue
		
		pygame.draw.rect(window, (175,59,59), (0, win_height - 10, (win_width / 100) * Fred.health , 10))

		for index in barrelsToRemove:
			del Barrels[index]

		if goLeft is True:
			Fred.moveLeft(0)
		
		if goRight is True:
			Fred.moveRight(win_width)

	elif gameStarted is False and gameOver is False:
		window.blit(startScreen, (0, 0))

	elif gameStarted is True and gameOver is True:
		window.blit(endScreen, (0, 0))
		timeLasted = (gameFinishedTime - gameStartedTime) / 1000
	
		if timeLasted < 10:
			timeLasted = "0" + str(timeLasted)
		else:
			timeLasted = str(timeLasted)

		renderedText = textFont.render(timeLasted, 1, (175,59,59))
		window.blit(renderedText, (495, 430))

	# Handle user and system events 
	for event in GAME_EVENTS.get():

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_ESCAPE:
				quitGame()
			elif event.key == pygame.K_LEFT:
				goLeft = True
				goRight = False
			elif event.key == pygame.K_RIGHT:
				goLeft = False
				goRight = True
			elif event.key == pygame.K_RETURN:
				if gameStarted is False and gameOver is False:
					gameStarted = True
					gameStartedTime = timeTick
				elif gameStarted is True and gameOver is True:
					Fred.reset()
					
					Barrels = []
					barrelInterval = 1500

					gameOver = False

	if event.type == pygame.KEYUP:

		if event.key == pygame.K_LEFT:
			goLeft = False
		if event.key == pygame.K_RIGHT:
			goRight = False

		if event.type == GAME_GLOBALS.QUIT:
			quitGame()

	clock.tick(60)
	pygame.display.update()

	if GAME_TIME.get_ticks() - lastBarrel > barrelInterval and gameStarted is True:
		newBarrel()
		if barrelInterval > 150:
			barrelInterval -= 50
