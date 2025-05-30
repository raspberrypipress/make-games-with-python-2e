import pygame, copy
from pygame.math import Vector2

planets = [{
    "name" : "mercury",
    "radius" : 15.0,
    "mass" : 0.6,
    "velocity" : Vector2(),
    "pos" : Vector2()
},
{
    "name" : "venus",
    "radius" : 23.0,
    "mass" : 0.95,
    "velocity" : Vector2(),
    "pos" : Vector2()
},
{
    "name" : "earth",
    "radius" : 24.0,
    "mass" : 1.0,
    "velocity" : Vector2(),
    "pos" : Vector2()
},
{
    "name" : "mars",
    "radius" : 15.0,
    "mass" : 0.4,
    "velocity" : Vector2(),
    "pos" : Vector2()
},
{
    "name" : "jupiter",
    "radius" : 37.0,
    "mass" : 15.0,
    "velocity" : Vector2(),
    "pos" : Vector2()
},
{
    "name" : "saturn",
    "radius" : 30.0,
    "mass" : 4,
    "velocity" : Vector2(),
    "pos" : Vector2()
},
{
    "name" : "neptune",
    "radius" : 30.0,
    "mass" : 4.2,
    "velocity" : Vector2(),
    "pos" : Vector2()
},
{
    "name" : "uranus",
    "radius" : 30.0,
    "mass" : 3.8,
    "velocity" : Vector2(),
    "pos" : Vector2()
}]

# Load the planet images
images = {}
for p in planets:
    name = p["name"]
    images[name] = pygame.image.load(f"assets/{name}.png")

def make_new_planet(which):
    for piece_of_rock in planets:

        if piece_of_rock["name"] == which:
            return copy.deepcopy(piece_of_rock)

    return False

