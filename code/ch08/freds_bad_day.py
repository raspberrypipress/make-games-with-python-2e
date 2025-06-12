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
barrels = pygame.sprite.Group()

lastBarrel = 0
barrelInterval = 1500
fred_direction = 0

def quitGame():
    pygame.quit()
    raise SystemExit

def newBarrel():
    global barrels, lastBarrel
    theBarrel = objects.Barrel(win_width, win_height, GAME_TIME)
    barrels.add(theBarrel)
    lastBarrel = GAME_TIME.get_ticks()

# 'main' loop
while True:

    # Handle events    
    for event in GAME_EVENTS.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitGame()
            elif event.key == pygame.K_RETURN:
                if gameStarted is False and gameOver is False:
                    gameStarted = True
                    gameStartedTime = timeTick
                elif gameStarted is True and gameOver is True:
                    Fred.reset()
                    for barrel in barrels:
                        if isinstance(barrel, objects.Barrel):
                            barrel.kill()
                    barrelInterval = 1500
                    gameOver = False

        if event.type == GAME_GLOBALS.QUIT:
            quitGame()

    timeTick = GAME_TIME.get_ticks()
    if gameStarted and not gameOver:

        window.blit(background, (0, 0))

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            Fred.set_direction(-1)
        elif pressed_keys[pygame.K_RIGHT]:
            Fred.set_direction(1)            
        Fred.update()
        barrels.update()

        # check for collisions
        b = pygame.sprite.spritecollideany(Fred, barrels)
        if b and not b.isBroken:
            b.split()
            Fred.hit()
            if Fred.health < 10:
                gameOver = True
                gameFinishedTime = timeTick
        
        pygame.draw.rect(window, (175,59,59), (0, win_height - 10, (win_width / 100) * Fred.health, 10))
        barrels.draw(window)
        window.blit(Fred.image, Fred.rect)

    elif not gameStarted and not gameOver:
        window.blit(startScreen, (0, 0))

    elif gameStarted and gameOver:
        window.blit(endScreen, (0, 0))
        timeLasted = (gameFinishedTime - gameStartedTime) // 1000
        renderedText = textFont.render(f"{timeLasted:02}", 1, (175,59,59))
        window.blit(renderedText, (495, 430))

    clock.tick(60)
    pygame.display.update()

    # FIXME: use a timer event to create barrels like we did in the platform chapter?
    if GAME_TIME.get_ticks() - lastBarrel > barrelInterval and gameStarted is True:
        newBarrel()
        if barrelInterval > 150:
            barrelInterval -= 50
