import pygame, sys, math, random
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

		pygame.draw.circle(surface, obj["colour"], obj["pos"], int(obj["radius"]), 0)

def drawCurrentObject():

	global expanding, currentObject

	currentObject["pos"] = Vector2(mousePosition)

	if expanding is True and currentObject["radius"] < 60:
		currentObject["radius"] += 0.2

		if currentObject["radius"] >= 60:
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
		for other in other_objs:
				
			direction = other["pos"] - obj["pos"]
			magnitude = other["pos"].distance_to(obj["pos"])
			nDirection = direction / magnitude

			if magnitude < 5:
				magnitude = 5
			elif magnitude > 15:
				magnitude = 15

			strength = ((gravity * obj["mass"] * other["mass"]) / (magnitude * magnitude)) / other["mass"]
			appliedForce = nDirection * strength
			other["velocity"] -= Vector2(appliedForce)

			if drawAttractions is True:
				pygame.draw.line(surface, (255,255,255), obj["pos"], other["pos"], 1)

def handleCollisions():

	for obj in collidables:

		other_objs = [x for x in collidables if x is not obj]
		for other in other_objs:

			distance = other["pos"].distance_to(obj["pos"])
			if distance < other["radius"] + obj["radius"]:
				print(other["radius"] + obj["radius"] - distance)

				# Angle of the collision between the two
				coll_angle = math.atan2( 
					*reversed(obj["pos"] - other["pos"]))

				# Calculate the speed of each object
				obj_speed = obj["velocity"].magnitude()
				other_speed = other["velocity"].magnitude()

				# Get direction of the objects in radians
				obj_dir = math.atan2(
					*reversed(obj["velocity"]))
				other_dir = math.atan2(
					*reversed(other["velocity"]))

				# Calculate the post-collision velocity
				obj_angle = obj_dir - coll_angle
				obj_new_ang = Vector2(math.cos(obj_angle),
				                      math.sin(obj_angle))
				obj_new_vel = obj_new_ang * obj_speed

				other_angle = other_dir - coll_angle
				other_new_ang = Vector2(math.cos(other_angle),
								        math.sin(other_angle))
				other_new_vel = other_new_ang * other_speed
				
				# Adjust velocity based on object masses
				mass = obj["mass"]
				other_mass = other["mass"]

				obj_final_vel = (
					((mass - other_mass) * obj_new_vel
					 + (other_mass * 2) * other_new_vel)
					/ (mass + other_mass)
				)
				other_final_vel = (
					((mass * 2) * obj_new_vel
					 + (other_mass - mass) * other_new_vel)
					/ (mass + other_mass)
				)

				# Set the final velocities
				obj["velocity"] = obj_final_vel
				other["velocity"] = other_final_vel

def handleMouseDown():
	global currentObject

	currentObject = {
		"radius" : 3,
		"mass" : 3,
		"velocity" : Vector2(),
		"pos" : Vector2(),
		"colour" : random.choices(range(256), k=3)
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