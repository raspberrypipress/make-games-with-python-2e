import pygame, sys, math
import solarsystem
from pygame.math import Vector2

windowWidth = 1024
windowHeight = 768

pygame.init()
clock = pygame.time.Clock()
# surface = pygame.display.set_mode((windowWidth, windowHeight), pygame.FULLSCREEN)
surface = pygame.display.set_mode((windowWidth, windowHeight))

pygame.display.set_caption('Solar System Simulator')

prev_mouse_pos = Vector2()
mouse_pos = None

background = pygame.image.load("assets/background.jpg")
logo = pygame.image.load("assets/logo.png")
UITab = pygame.image.load("assets/tabs.png")

uitab_coords = (131, 687)
x = uitab_coords[0] + 1
UICoordinates = []
for name in solarsystem.images.keys():
    UICoordinates.append({"name": name,
                          "coords": (x, uitab_coords[1])})
    x += 97

planets = []
currentBody = None
drawAttractions = True
gravity = 10.0

def drawUI():
    surface.blit(UITab, uitab_coords)
    x = uitab_coords[0]
    for p in solarsystem.planets:
        rect = pygame.Rect(x, uitab_coords[1], 82, 82)
        img = solarsystem.images[p["name"]]
        surface.blit(img, img.get_rect(center=rect.center))
        x += 97

def drawBody(body):
    surface.blit(solarsystem.images[body["name"]], 
                 body["pos"] - Vector2(body["radius"]))

def drawPlanets():

    for p in planets:
        p["pos"] += p["velocity"]
        drawBody(p)

def drawCurrentBody():
    currentBody["pos"] = mouse_pos
    drawBody(currentBody)

def calculateMovement():

    for p in planets:

        other_planets = [x for x in planets if x is not p]
        for op in other_planets:
            
            # Difference in the X,Y coordinates of the objects
            direction = op["pos"] - p["pos"]
            # Distance between the two objects
            magnitude = op["pos"].distance_to(p["pos"])
            # Normalised Vector pointing in the
            # direction of the force
            nDirection = direction / magnitude

            # We need to limit the gravity to stop things 
            # flying off to infinity... and beyond!
            if magnitude < 5:
                magnitude = 5
            elif magnitude > 30:
                magnitude = 30

            # How strong should the attraction be?
            strength = ((gravity * p["mass"] * op["mass"]) /
                        (magnitude * magnitude)) / op["mass"]

            appliedForce = nDirection * Vector2(strength)

            op["velocity"] -= Vector2(appliedForce)

            if drawAttractions is True:
                pygame.draw.line(surface, (255,255,255), 
                                 p["pos"],
                                 op["pos"],
                                 1)

def checkUIForClick(coordinates):

    for tab in UICoordinates:
        tabX = tab["coords"][0]

        if coordinates[0] > tabX and coordinates[0] < tabX + 82:
            return tab["name"]

    return False

def handleMouseDown():
    global currentBody

    if(mouse_pos[1] >= uitab_coords[1]):
        newPlanet = checkUIForClick(mouse_pos)

        if newPlanet:
            currentBody = solarsystem.makeNewPlanet(newPlanet)

def quitGame():
    pygame.quit()
    sys.exit()

# main loop
pressed = False
while True:

    # Handle user and system events 
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitGame()

        # FIXME: explain why we use KEYUP here instead of get_pressed()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                planets = []
            if event.key == pygame.K_a:
                drawAttractions = not drawAttractions

        mouse_pos = Vector2(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = True
            handleMouseDown()

        if event.type == pygame.MOUSEBUTTONUP:
            pressed = False

        if event.type == pygame.QUIT:
            quitGame()

    surface.blit(background, (0,0))

    # Draw the UI, update the movement of the planets,
    # then draw the planets in their new positions.
    drawUI()
    calculateMovement()
    drawPlanets()

    # If our user has created a new planet,
    # draw it where the mouse is.
    if currentBody:
        drawCurrentBody()

        # If they've released the mouse, add the new planet to
        # the planets list and let gravity do its thing
        if not pressed:
            v = (mouse_pos - prev_mouse_pos) / 4
            currentBody["velocity"] = v
            planets.append(currentBody)
            currentBody = None

    # Draw the logo for the first four seconds of the program
    if pygame.time.get_ticks() < 4000:
        surface.blit(logo, (108,77))

    # Store the previous mouse coordinates to create a vector
    # when we release a new planet
    prev_mouse_pos = mouse_pos

    clock.tick(60)
    pygame.display.update()