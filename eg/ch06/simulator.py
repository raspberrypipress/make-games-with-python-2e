import pygame, sys, random, math
import pygame.time as GAME_TIME
import solarsystem

windowWidth = 1024
windowHeight = 768

pygame.init()
clock = pygame.time.Clock()
# surface = pygame.display.set_mode((windowWidth, windowHeight), pygame.FULLSCREEN)
surface = pygame.display.set_mode((windowWidth, windowHeight))

pygame.display.set_caption('Solar System Simulator')

prev_mouse_pos = [0,0]
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
                 (body["pos"][0] - body["radius"],
                  body["pos"][1] - body["radius"]))

def drawPlanets():

    for p in planets:
        p["pos"][0] += p["velocity"][0]
        p["pos"][1] += p["velocity"][1]
        drawBody(p)

def drawCurrentBody():
    currentBody["pos"] = list(mouse_pos)
    drawBody(currentBody)

def calculateMovement():

    for p in planets:

        other_planets = [x for x in planets if x is not p]
        for op in other_planets:
            
            # FIXME: Use Vector2!!!!!!
            # Difference in the X,Y coordinates of the objects
            direction = (op["pos"][0] - p["pos"][0], 
                         op["pos"][1] - p["pos"][1]) 
            direction2 = pygame.math.Vector2(op["pos"]) - pygame.math.Vector2(p["pos"])
            print(direction, direction2)
            # Distance between the two objects
            magnitude = math.hypot(op["pos"][0] - p["pos"][0],
                                   op["pos"][1] - p["pos"][1])
            magnitude2 = pygame.math.Vector2(op["pos"]).distance_to(pygame.math.Vector2(p["pos"]))
            print(magnitude, magnitude2)
            # Normalised Vector pointing in the
            # direction of the force
            nDirection = (direction[0] / magnitude,
                          direction[1] / magnitude)

            # We need to limit the gravity to stop things 
			# flying off to infinity... and beyond!
            if magnitude < 5:
                magnitude = 5
            elif magnitude > 30:
                magnitude = 30

			# How strong should the attraction be?
            strength = ((gravity * p["mass"] * op["mass"]) /
                        (magnitude * magnitude)) / op["mass"]

            appliedForce = (nDirection[0] * strength, 
                            nDirection[1] * strength)

            op["velocity"][0] -= appliedForce[0]
            op["velocity"][1] -= appliedForce[1]

            if drawAttractions is True:
                pygame.draw.line(surface, (255,255,255), 
                                 (p["pos"][0], p["pos"][1]),
                                 (op["pos"][0], op["pos"][1]),
                                 1)

def checkUIForClick(coordinates):

    for tab in UICoordinates:
        tabX = tab["coords"][0]

        if coordinates[0] > tabX and coordinates[0] < tabX + 82:
            return tab["name"]

    return False

def handleMouseDown():
    global mouse_pos, currentBody

    if(mouse_pos[1] >= uitab_coords[1]):
        newPlanet = checkUIForClick(mouse_pos)

        if newPlanet:
            currentBody = solarsystem.makeNewPlanet(newPlanet)

def quitGame():
    pygame.quit()
    sys.exit()

# main loop
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

        if event.type == pygame.QUIT:
            quitGame()

    surface.blit(background, (0,0))

    mouse_pos = pygame.mouse.get_pos()
    pressed = pygame.mouse.get_pressed()[0]
    if pressed:
        handleMouseDown()

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
            currentBody["velocity"][0] = (
                mouse_pos[0] - prev_mouse_pos[0]) / 4
            currentBody["velocity"][1] = (
                mouse_pos[1] - prev_mouse_pos[1]) / 4
            planets.append(currentBody)
            currentBody = None

    # Draw the logo for the first four seconds of the program
    if GAME_TIME.get_ticks() < 4000:
        surface.blit(logo, (108,77))

    # Store the previous mouse coordinates to create a vector
	# when we release a new planet
    prev_mouse_pos = mouse_pos

    clock.tick(60)
    pygame.display.update()