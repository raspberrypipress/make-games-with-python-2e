import pygame
import solarsystem
from pygame.math import Vector2

pygame.init()
clock = pygame.time.Clock()
fps = 60

win_width = 1024
win_height = 768
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Solar System Simulator')

background = pygame.image.load("assets/background.jpg")
logo = pygame.image.load("assets/logo.png")
uitab = pygame.image.load("assets/tabs.png")

# Prepare the user interface metadata
uitab_pos = (int((win_width-uitab.get_width())/2),
              win_height-uitab.get_height())
num_planets = len(solarsystem.planets)
ui_spacing = int(uitab.get_width()/num_planets + 2)
ui_coords = []  # Name and location of each planet button
tab_height = win_height - uitab_pos[1]
def draw_ui():
    global ui_coords

    window.blit(uitab, uitab_pos) # Draw the UI tab graphic
    x = uitab_pos[0]
    for name in solarsystem.planets:
        print(type(x))

        # Draw the planet on the tab
        rect = pygame.Rect(x, uitab_pos[1], 
                           tab_height, tab_height)
        img = solarsystem.images[name]
        window.blit(img, img.get_rect(center=rect.center))

        # Calculate the click zones for each tab
        ui_coords.append({"name": name,
                          "coords": (x + 1, uitab_pos[1])})
        x += ui_spacing

def draw_body(body):
    window.blit(body["image"], 
                body["pos"] - Vector2(body["radius"]))

def draw_bodies():
    # Update the position of the bodies and draw them
    for p in bodies:
        p["pos"] += p["velocity"]
        draw_body(p)

def draw_current_body():
    current_body["pos"] = mouse_pos
    draw_body(current_body)

def calculate_movement():
    for p in bodies:
        other_bodies = [x for x in bodies if x is not p]
        for op in other_bodies:
            
            # Difference in the X,Y coordinates of the objects
            direction = op["pos"] - p["pos"]

            # Distance between the two objects
            magnitude = op["pos"].distance_to(p["pos"])

            # Normalised vector pointing in the
            # direction of the force
            n_direction = direction / magnitude

            # We need to limit the gravity to stop things 
            # flying off to infinity... and beyond!
            if magnitude < 5:
                magnitude = 5
            elif magnitude > 30:
                magnitude = 30

            # How strong should the attraction be?
            strength = ((gravity * p["mass"] * op["mass"]) /
                        (magnitude * magnitude)) / op["mass"]
            applied_force = n_direction * strength

            op["velocity"] -= Vector2(applied_force)
            if draw_attractions:
                pygame.draw.line(window, (255,255,255), 
                                 p["pos"], op["pos"], 1)

def check_ui_for_click(coords):
    for tab in ui_coords:
        x = tab["coords"][0]
        if coords[0] in range(x + 1, x + tab_height):
            return tab["name"]
    return False

def handle_mouse_down():
    global current_body

    if(mouse_pos[1] >= uitab_pos[1]):
        name = check_ui_for_click(mouse_pos)

        if name:
            current_body = solarsystem.make_new_planet(name)

def quitGame():
    pygame.quit()
    raise SystemExit

# main loop
prev_mouse_pos = Vector2()
mouse_pos = None
bodies = []
current_body = None
draw_attractions = True
gravity = 10.0
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
                bodies = []
            if event.key == pygame.K_a:
                draw_attractions = not draw_attractions

        mouse_pos = Vector2(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = True
            handle_mouse_down()

        if event.type == pygame.MOUSEBUTTONUP:
            pressed = False

        if event.type == pygame.QUIT:
            quitGame()

    window.blit(background, (0,0))

    # Draw the UI, update the movement of the bodies,
    # then draw the bodies in their new positions.
    draw_ui()
    calculate_movement()
    draw_bodies()

    # If our user has created a new planet,
    # draw it where the mouse is.
    if current_body:
        draw_current_body()

        # If they've released the mouse, add the new planet to
        # the bodies list and let gravity do its thing
        if not pressed:
            v = (mouse_pos - prev_mouse_pos) / 4
            current_body["velocity"] = v
            bodies.append(current_body)
            current_body = None

    # Draw the logo for the first four seconds of the program
    if pygame.time.get_ticks() < 4000:
        window.blit(logo, (108,77))

    # Store the previous mouse coordinates to create a vector
    # when we release a new planet
    prev_mouse_pos = mouse_pos

    clock.tick(fps)
    pygame.display.update()