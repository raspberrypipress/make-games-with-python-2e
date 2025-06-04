import pygame, copy
from pygame.math import Vector2

planets = {
    "mercury": {"radius" : 15.0, "mass" : 0.6},
    "venus":   {"radius" : 23.0, "mass" : 0.95},
    "earth":   {"radius" : 24.0, "mass" : 1.0},
    "mars":    {"radius" : 15.0, "mass" : 0.4},
    "jupiter": {"radius" : 37.0, "mass" : 15.0},
    "saturn":  {"radius" : 30.0, "mass" : 4},
    "neptune": {"radius" : 30.0, "mass" : 4.2},
    "uranus":  {"radius" : 30.0, "mass" : 3.8}
}

# Load the planet images
images = {}
for name in planets:
    images[name] = pygame.image.load(f"assets/{name}.png")

# Set the starting position/velocity for each planet
for p in planets.values():
    p["velocity"] = Vector2()
    p["pos"] = Vector2()

# Create a new planet.
def make_new_planet(name):
    p = copy.deepcopy(planets[name])
    p["image"] = images[name]
    return p
