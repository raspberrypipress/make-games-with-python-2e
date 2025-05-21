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

# Draw the user interface
ui_spacing = 97
uitab_upperleft = (131, 687)
x = uitab_upperleft[0] + 1
ui_coordinates = []
for name in solarsystem.images.keys():
    ui_coordinates.append({"name": name,
                           "coords": (x, uitab_upperleft[1])})
    x += ui_spacing

prev_mouse_pos = Vector2()
mouse_pos = None
planets = []
current_body = None
draw_attractions = True
gravity = 10.0

def draw_ui():
    window.blit(uitab, uitab_upperleft)
    x = uitab_upperleft[0]
    for p in solarsystem.planets:
        rect = pygame.Rect(x, uitab_upperleft[1], 82, 82)
        img = solarsystem.images[p["name"]]
        window.blit(img, img.get_rect(center=rect.center))
        x += ui_spacing

def draw_body(body):
    window.blit(solarsystem.images[body["name"]], 
                 body["pos"] - Vector2(body["radius"]))

def draw_planets():
    for p in planets:
        p["pos"] += p["velocity"]
        draw_body(p)

def draw_current_body():
    current_body["pos"] = mouse_pos
    draw_body(current_body)

def calculate_movement():

    for p in planets:

        other_planets = [x for x in planets if x is not p]
        for op in other_planets:
            
            # Difference in the X,Y coordinates of the objects
            direction = op["pos"] - p["pos"]
            # Distance between the two objects
            magnitude = op["pos"].distance_to(p["pos"])
            # Normalised Vector pointing in the
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
                                 p["pos"],
                                 op["pos"],
                                 1)

def check_ui_for_click(coordinates):

    for tab in ui_coordinates:
        tabX = tab["coords"][0]

        if coordinates[0] > tabX and coordinates[0] < tabX + 82:
            return tab["name"]

    return False

def handle_mouse_down():
    global current_body

    if(mouse_pos[1] >= uitab_upperleft[1]):
        new_planet = check_ui_for_click(mouse_pos)

        if new_planet:
            current_body = solarsystem.make_new_planet(new_planet)

def quitGame():
    pygame.quit()
    raise SystemExit

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

    # Draw the UI, update the movement of the planets,
    # then draw the planets in their new positions.
    draw_ui()
    calculate_movement()
    draw_planets()

    # If our user has created a new planet,
    # draw it where the mouse is.
    if current_body:
        draw_current_body()

        # If they've released the mouse, add the new planet to
        # the planets list and let gravity do its thing
        if not pressed:
            v = (mouse_pos - prev_mouse_pos) / 4
            current_body["velocity"] = v
            planets.append(current_body)
            current_body = None

    # Draw the logo for the first four seconds of the program
    if pygame.time.get_ticks() < 4000:
        window.blit(logo, (108,77))

    # Store the previous mouse coordinates to create a vector
    # when we release a new planet
    prev_mouse_pos = mouse_pos

    clock.tick(fps)
    pygame.display.update()