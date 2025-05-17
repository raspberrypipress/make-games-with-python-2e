import pygame, sys, math, random
from pygame.math import Vector2

pygame.init()
clock = pygame.time.Clock()
fps = 60

win_width = 1024
win_height = 768
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Collisions')

prev_mouse_pos = Vector2()
mouse_pos = None
mouse_down = False

collidables = []
current_obj = None
expanding = True

draw_attractions = False

gravity = 1.0

def draw_collidables():

    for obj in collidables:
        obj["pos"] += obj["velocity"]
        pygame.draw.circle(window, obj["colour"], 
                           obj["pos"], int(obj["radius"]), 0)

def draw_current_object():

    global expanding, current_obj

    current_obj["pos"] = mouse_pos

    if expanding is True and current_obj["radius"] < 60:
        current_obj["radius"] += 0.2

        if current_obj["radius"] >= 60:
            expanding = False
            current_obj["radius"] = 9.9

    elif expanding is False and current_obj["radius"] > 1:
        current_obj["radius"] -= 0.2

        if current_obj["radius"] <= 1:
            expanding = True
            current_obj["radius"] = 1.1

    current_obj["mass"] = current_obj["radius"]

    pygame.draw.circle(window, (255,0,0), 
                       current_obj["pos"], 
                       int(current_obj["radius"]), 0)

def calculate_movement():

    for o in collidables:

        other_objs = [x for x in collidables if x is not o]
        for other in other_objs:
                
            direction = other["pos"] - o["pos"]
            magnitude = other["pos"].distance_to(o["pos"])
            n_direction = direction / magnitude

            if magnitude < 5:
                magnitude = 5
            elif magnitude > 15:
                magnitude = 15

            strength = ((gravity * o["mass"] * other["mass"]) /
                        (magnitude * magnitude)) / other["mass"]

            applied_force = n_direction * strength
            other["velocity"] -= Vector2(applied_force)

            if draw_attractions is True:
                pygame.draw.line(window, (255,255,255), 
                                 o["pos"], other["pos"], 1)

def handle_collisions():

    for o in collidables:

        other_objs = [x for x in collidables if x is not o]
        for other in other_objs:

            distance = other["pos"].distance_to(o["pos"])
            if distance < other["radius"] + o["radius"]:
                print(other["radius"]+o["radius"]-distance)

                # Angle of the collision between the two
                coll_angle = math.atan2( 
                    *reversed(o["pos"] - other["pos"]))

                # Calculate the speed of each object
                obj_speed = o["velocity"].magnitude()
                other_speed = other["velocity"].magnitude()

                # Get direction of the objects in radians
                obj_dir = math.atan2(
                    *reversed(o["velocity"]))
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
                mass = o["mass"]
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
                o["velocity"] = obj_final_vel
                other["velocity"] = other_final_vel

def handle_mouse_down():
    global current_obj

    current_obj = {
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

    window.fill((0,0,0))
    mouse_pos = Vector2(pygame.mouse.get_pos())

    # Handle user and system events 
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                quitGame()

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_r:
                collidables = []
            if event.key == pygame.K_a:
                if draw_attractions is True:
                    draw_attractions = False
                elif draw_attractions is False:
                    draw_attractions = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            handle_mouse_down()

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False

        if event.type == pygame.QUIT:
            quitGame()

    calculate_movement()
    handle_collisions()
    draw_collidables()

    if current_obj is not None:
        draw_current_object()

        # If our user has released the mouse, add the new obj
        # to the collidables list and let gravity do its thing
        if mouse_down is False:
            v = (mouse_pos - prev_mouse_pos) / 4
            current_obj["velocity"] = v 
            collidables.append(current_obj)
            current_obj = None

    # Store the previous mouse coordinates to create a vector
    # when we release a new obj
    prev_mouse_pos = mouse_pos

    clock.tick(60)
    pygame.display.update()