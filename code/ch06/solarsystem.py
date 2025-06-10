import pygame
import copy
from pygame.math import Vector2

# Planet data
PLANETS = {
    "mercury": {"radius": 15.0, "mass": 0.6},
    "venus":   {"radius": 23.0, "mass": 0.95},
    "earth":   {"radius": 24.0, "mass": 1.0},
    "mars":    {"radius": 15.0, "mass": 0.4},
    "jupiter": {"radius": 37.0, "mass": 15.0},
    "saturn":  {"radius": 30.0, "mass": 4.0},
    "neptune": {"radius": 30.0, "mass": 4.2},
    "uranus":  {"radius": 30.0, "mass": 3.8}
}

# Load the planet images
IMAGES = {}
for name in PLANETS:
    IMAGES[name] = pygame.image.load(f"assets/{name}.png")

# Set starting position and velocity for each planet
for planet in PLANETS.values():
    planet["velocity"] = Vector2(0, 0)
    planet["pos"] = Vector2(0, 0)

def make_new_planet(name):
    planet = copy.deepcopy(PLANETS[name])
    planet["image"] = IMAGES[name]
    return planet