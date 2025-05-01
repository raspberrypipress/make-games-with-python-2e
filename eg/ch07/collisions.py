import pygame, sys, random, math
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME
from pygame.math import Vector2

windowWidth = 1024
windowHeight = 768

pygame.init()
clock = pygame.time.Clock()
surface = pygame.display.set_mode((windowWidth, windowHeight))

pygame.display.set_caption('Collisions')

previousMousePosition = [0,0]
mousePosition = None
mouseDown = False

collidables = []
currentObject = None
expanding = True

drawAttractions = False

gravity = 1.0

def drawCollidables():

	for obj in collidables:
		obj["pos"] += obj["velocity"]

		pygame.draw.circle(surface, (255,255,255), obj["pos"], int(obj["radius"]), 0)

def drawCurrentObject():

	global expanding, currentObject

	currentObject["pos"] = Vector2(mousePosition)

	if expanding is True and currentObject["radius"] < 30:
		currentObject["radius"] += 0.2

		if currentObject["radius"] >= 30:
			expanding = False
			currentObject["radius"] = 9.9

	elif expanding is False and currentObject["radius"] > 1:
		currentObject["radius"] -= 0.2

		if currentObject["radius"] <= 1:
			expanding = True
			currentObject["radius"] = 1.1

	currentObject["mass"] = currentObject["radius"]

	pygame.draw.circle(surface, (255,0,0), currentObject["pos"], int(currentObject["radius"]), 0)

def calculateMovement():

	for obj in collidables:

		other_objs = [x for x in collidables if x is not obj]
		for other_obj in other_objs:
				
			direction = other_obj["pos"] - obj["pos"]
			magnitude = other_obj["pos"].distance_to(obj["pos"])
			nDirection = direction / magnitude

			if magnitude < 5:
				magnitude = 5
			elif magnitude > 15:
				magnitude = 15

			strength = ((gravity * obj["mass"] * other_obj["mass"]) / (magnitude * magnitude)) / other_obj["mass"]
			appliedForce = nDirection * strength
			other_obj["velocity"] -= Vector2(appliedForce)

			if drawAttractions is True:
				pygame.draw.line(surface, (255,255,255), obj["pos"], other_obj["pos"], 1)

def handleCollisions():

	for obj in collidables:

		other_objs = [x for x in collidables if x is not obj]
		for other_obj in other_objs:

			distance = other_obj["pos"].distance_to(obj["pos"])
			if distance < other_obj["radius"] + obj["radius"]:

				# First we get the angle of the collision between the two objects
				collisionAngle = math.atan2(obj["pos"][1] - other_obj["pos"][1], obj["pos"][0] - other_obj["pos"][0])

				#Then we need to calculate the speed of each object
				obj_speed = obj["velocity"].magnitude()
				other_obj_speed = other_obj["velocity"].magnitude()

				# Now, we work out the direction of the objects in radians
				objDirection = math.atan2(obj["velocity"][1], obj["velocity"][0])
				other_objDirection = math.atan2(other_obj["velocity"][1], other_obj["velocity"][0])

				# Now we calculate the new X/Y values of each object for the collision
				objsNewVelocityX = obj_speed * math.cos(objDirection - collisionAngle)
				objsNewVelocityY = obj_speed * math.sin(objDirection - collisionAngle)

				other_objsNewVelocityX = other_obj_speed * math.cos(other_objDirection - collisionAngle)
				other_objsNewVelocityY = other_obj_speed * math.sin(other_objDirection - collisionAngle)
				
				# We adjust the velocity based on the mass of the objects
				objsFinalVelocityX = ((obj["mass"] - other_obj["mass"]) * objsNewVelocityX + (other_obj["mass"] + other_obj["mass"]) * other_objsNewVelocityX)/(obj["mass"] + other_obj["mass"])
				other_objsFinalVelocityX = ((obj["mass"] + obj["mass"]) * objsNewVelocityX + (other_obj["mass"] - obj["mass"]) * other_objsNewVelocityX)/(obj["mass"] + other_obj["mass"])

				# Now we set those values
				obj["velocity"][0] = objsFinalVelocityX
				other_obj["velocity"][0] = other_objsFinalVelocityX

def handleMouseDown():
	global currentObject

	currentObject = {
		"radius" : 3,
		"mass" : 3,
		"velocity" : Vector2(),
		"pos" : Vector2()
	}

def quitGame():
	pygame.quit()
	sys.exit()

# 'main' loop
while True:

	surface.fill((0,0,0))
	mousePosition = pygame.mouse.get_pos()

	# Handle user and system events 
	for event in GAME_EVENTS.get():

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_ESCAPE:
				quitGame()

		if event.type == pygame.KEYUP:

			if event.key == pygame.K_r:
				collidables = []
			if event.key == pygame.K_a:
				if drawAttractions is True:
					drawAttractions = False
				elif drawAttractions is False:
					drawAttractions = True

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouseDown = True
			handleMouseDown()

		if event.type == pygame.MOUSEBUTTONUP:
			mouseDown = False

		if event.type == GAME_GLOBALS.QUIT:
			quitGame()

	calculateMovement()
	handleCollisions()
	drawCollidables()

	if currentObject is not None:
		drawCurrentObject()

		# If our user has released the mouse, add the new obj to the collidables list and let gravity do its thing
		if mouseDown is False:
			currentObject["velocity"] = (Vector2(mousePosition) - Vector2(previousMousePosition)) / 4
			collidables.append(currentObject)
			currentObject = None

	# Store the previous mouse coordinates to create a vector when we release a new obj
	previousMousePosition = mousePosition

	clock.tick(60)
	pygame.display.update()