import pygame
import solarsystem
from pygame.math import Vector2

pygame.init()
clock = pygame.time.Clock()
FPS = 60

WIN_WIDTH = 1024
WIN_HEIGHT = 768
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Solar System Simulator')

background = pygame.image.load("assets/background.jpg")
logo = pygame.image.load("assets/logo.png")
ui = pygame.image.load("assets/tabs.png")

# Initialise the user interface metadata
UI_POS = (int((WIN_WIDTH-ui.get_width())/2),
          WIN_HEIGHT-ui.get_height())
NUM_PLANETS = len(solarsystem.PLANETS)
UI_SPACING = int(ui.get_width()/NUM_PLANETS + 2)

ui_coords = []  # Name and location of each planet button
x = UI_POS[0]
for name in solarsystem.PLANETS:
    # Calculate the click zones for each tab
    ui_coords.append({"name": name,
                      "coords": (x + 1, UI_POS[1])})
    x += UI_SPACING

def draw_ui():
    global ui_coords

    window.blit(ui, UI_POS) # Draw the UI tab graphic
    x = UI_POS[0]
    for name in solarsystem.PLANETS:

        # Draw the planet on the tab
        rect = pygame.Rect(x, UI_POS[1], 
                           ui.get_height(), ui.get_height())
        img = solarsystem.IMAGES[name]
        window.blit(img, img.get_rect(center=rect.center))
        x += UI_SPACING

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
            
            # Difference in the X,Y coordinates of the planets
            direction = op["pos"] - p["pos"]

            # Distance between the two
            magnitude = op["pos"].distance_to(p["pos"])
            if magnitude == 0: # Two planets atop each other!
                continue

            # Normalised vector pointing in the
            # direction of the force
            n_direction = direction.normalize()

            # We need to limit the gravity to stop things 
            # flying off to infinity... and beyond!
            clamped_mag = max(5, min(30, magnitude))

            # How strong should the attraction be?
            strength = ((gravity * p["mass"] * op["mass"]) /
                        (clamped_mag ** 2)) / op["mass"]
            applied_force = Vector2(n_direction * strength)

            op["velocity"] -= applied_force
            if draw_attractions:
                pygame.draw.line(window, (255,255,255), 
                                 p["pos"], op["pos"], 1)

def check_ui_for_click(coords):
    h = ui.get_height()
    for tab in ui_coords:
        x = tab["coords"][0]
        if coords[0] >= x + 1 and coords[0] < x + h:
            return tab["name"]
    return False

def handle_mouse_down():
    global current_body

    if(mouse_pos[1] >= UI_POS[1]):
        name = check_ui_for_click(mouse_pos)

        if name:
            current_body = solarsystem.make_new_planet(name)

def quit_game():
    pygame.quit()
    raise SystemExit

# main loop
prev_mouse_pos = Vector2()
mouse_pos = None
bodies = []
current_body = None
draw_attractions = True
gravity = 10.0
mouse_down = False
while True:

    # Handle events 
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_game()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                bodies = []
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
        if not mouse_down:
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

    clock.tick(FPS)
    pygame.display.update()