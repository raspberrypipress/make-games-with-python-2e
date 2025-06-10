import pygame
import math
import random
from pygame.math import Vector2

pygame.init()
clock = pygame.time.Clock()
FPS = 60

WIN_WIDTH = 1024
WIN_HEIGHT = 768
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Collisions')

def draw_collidables():
    for obj in collidables:
        obj["pos"] += obj["velocity"]
        pygame.draw.circle(window, obj["colour"], 
                           obj["pos"], int(obj["radius"]), 0)

def calculate_movement():
    for o in collidables:
        other_objs = [x for x in collidables if x is not o]
        for other in other_objs:
                
            direction = other["pos"] - o["pos"]
            magnitude = other["pos"].distance_to(o["pos"])
            if magnitude == 0:
                continue
            n_direction = direction.normalize()

            clamped_mag = max(5, min(15, magnitude))

            strength = ((gravity * o["mass"] * other["mass"]) /
                        (clamped_mag ** 2)) / other["mass"]

            applied_force = Vector2(n_direction * strength)
            other["velocity"] -= applied_force

            if draw_attractions:
                pygame.draw.line(window, (255,255,255), 
                                 o["pos"], other["pos"], 1)

def draw_current_object():
    global current_obj, expansion

    current_obj["pos"] = mouse_pos

    # If we've exceeded either bound, reverse the expansion
    if not (1 < current_obj["radius"] < 20):
        expansion *= -1

    # Increase the radius by the expansion factor, and set
    # the mass equal to the radius.
    current_obj["radius"] += expansion
    current_obj["mass"] = current_obj["radius"]

    pygame.draw.circle(window, (255,0,0), 
                       current_obj["pos"], 
                       int(current_obj["radius"]), 0)

def handle_collisions():
    for o in collidables:
        other_objs = [x for x in collidables if x is not o]
        for other in other_objs:

            distance = other["pos"].distance_to(o["pos"])
            if distance < other["radius"] + o["radius"]:

                # Angle of the collision between the two
                coll = o["pos"] - other["pos"]
                coll_angle = math.atan2(-coll.y, coll.x)

                # Calculate the speed of each object
                obj_speed = o["velocity"].magnitude()
                other_speed = other["velocity"].magnitude()

                # Get direction of the objects in radians
                obj_dir = math.atan2(-o["velocity"].y,
                                     o["velocity"].x)
                other_dir = math.atan2(-other["velocity"].y,
                                       other["velocity"].x)

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
    global current_obj, expansion

    # Initialise a new circle and set current_obj to it.
    current_obj = {
        "radius" : 3,
        "mass" : 3,
        "velocity" : Vector2(),
        "pos" : Vector2(),
        "colour" : random.choices(range(256), k=3)
    }
    expansion = 0.2

def quit_game():
    pygame.quit()
    raise SystemExit

# main loop
prev_mouse_pos = Vector2()
mouse_pos = None
mouse_down = False
collidables = []
current_obj = None
draw_attractions = False
gravity = 1.0
expansion = 0.2
while True:

    # Handle events 
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_game()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                collidables = []
            if event.key == pygame.K_a:
                draw_attractions = not draw_attractions

        mouse_pos = Vector2(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            handle_mouse_down()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False

        if event.type == pygame.QUIT:
            quit_game()

    window.fill((0,0,0))
    calculate_movement()
    handle_collisions()
    draw_collidables()

    if current_obj:
        draw_current_object()

        # If our user has released the mouse, add the new obj
        # to the collidables list and let gravity do its thing
        if not mouse_down:
            v = (mouse_pos - prev_mouse_pos) / 4
            current_obj["velocity"] = v 
            collidables.append(current_obj)
            current_obj = None

    # Store the previous mouse coordinates to create a vector
    # when we release a new obj
    prev_mouse_pos = mouse_pos

    clock.tick(FPS)
    pygame.display.update()