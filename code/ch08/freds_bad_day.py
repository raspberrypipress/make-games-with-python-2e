import pygame, random
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME
import objects

# FIXME: pass fred GAME_TIME not the time itself
# FIXME: use the kill function to remove sprites

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
Fred = objects.Fred(win_width, win_height, GAME_TIME)
all_sprites = pygame.sprite.Group()
all_sprites.add(Fred)

lastBarrel = 0
barrelInterval = 1500
goLeft = False
goRight = False

def quitGame():
    pygame.quit()
    raise SystemExit

def newBarrel():
    global all_sprites, lastBarrel
    theBarrel = objects.Barrel(win_width, win_height, GAME_TIME)
    all_sprites.add(theBarrel)
    lastBarrel = GAME_TIME.get_ticks()

# 'main' loop
while True:
    
    timeTick = GAME_TIME.get_ticks()
    if gameStarted and not gameOver:

        window.blit(background, (0, 0))
        all_sprites.update()

        for barrel in all_sprites:
            if not isinstance(barrel, objects.Barrel):
                continue

            if not barrel.isBroken:

                # FIXME: could we move this into the barrel class and check for collision there? 
                # By definition, a barrel will never collide with a barrel.
                hasCollided = barrel.checkForCollision(Fred);
                
                if hasCollided is True:
                    barrel.split()
                    Fred.isHit = True
                    Fred.timeHit = timeTick
                    if Fred.health >= 10:
                        Fred.health -= 10
                    else:
                        gameOver = True
                        gameFinishedTime = timeTick
        
        pygame.draw.rect(window, (175,59,59), (0, win_height - 10, (win_width / 100) * Fred.health, 10))
        all_sprites.draw(window)

        if goLeft:
            Fred.moveLeft(0)
        
        if goRight:
            Fred.moveRight(win_width)

    elif not gameStarted and not gameOver:
        window.blit(startScreen, (0, 0))

    elif gameStarted and gameOver:
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

                    for barrel in all_sprites:
                        if isinstance(barrel, objects.Barrel):
                            barrel.kill()
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
