import pygame
import pygame.event as GAME_EVENTS
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

startScreen = pygame.image.load("assets/startgame.png")
endScreen = pygame.image.load("assets/gameover.png")
background = pygame.image.load("assets/background.png")

gameStarted = False
gameStartedTime = 0
timeLasted = 0

Fred = objects.Fred(win_width, win_height, pygame.time)
barrels = pygame.sprite.Group()
lastBarrel = 0
barrelInterval = 1500

def quitGame():
    pygame.quit()
    raise SystemExit

def newBarrel():
    global barrels, lastBarrel
    theBarrel = objects.Barrel(win_width, win_height, pygame.time)
    barrels.add(theBarrel)
    lastBarrel = pygame.time.get_ticks()

# 'main' loop
while True:

    timeTick = pygame.time.get_ticks()

    # Handle events    
    for event in GAME_EVENTS.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitGame()
            elif event.key == pygame.K_RETURN:
                if not gameStarted and Fred.health > 0:
                    gameStarted = True
                    gameStartedTime = timeTick
                elif gameStarted and Fred.health <= 0:
                    Fred.reset()
                    for barrel in barrels:
                        barrel.kill()
                    barrelInterval = 1500
                    gameStartedTime = timeTick

        if event.type == pygame.QUIT:
            quitGame()

    if gameStarted and Fred.health > 0:

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
            if Fred.health <= 0:
                timeLasted = (timeTick - gameStartedTime) // 1000
        
        # FIXME: use a timer event to create barrels like we did in the platform chapter?
        if pygame.time.get_ticks() - lastBarrel > barrelInterval:
            newBarrel()
            if barrelInterval > 150:
                barrelInterval -= 50

        pygame.draw.rect(window, (175,59,59), (0, win_height - 10, (win_width / 100) * Fred.health, 10))
        barrels.draw(window)
        window.blit(Fred.image, Fred.rect)

    elif not gameStarted and Fred.health > 0:
        window.blit(startScreen, (0, 0))

    elif gameStarted and Fred.health <= 0:
        window.blit(endScreen, (0, 0))
        renderedText = textFont.render(f"{timeLasted:02}", 1, (175,59,59))
        window.blit(renderedText, (495, 430))

    clock.tick(60)
    pygame.display.update()

