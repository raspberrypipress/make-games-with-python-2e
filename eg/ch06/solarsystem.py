import pygame, copy
from pygame.math import Vector2

images = {
    "mercury" : pygame.image.load("assets/mercury.png"),
    "venus" : pygame.image.load("assets/venus.png"),
    "earth" : pygame.image.load("assets/earth.png"),
    "mars" : pygame.image.load("assets/mars.png"),
    "jupiter" : pygame.image.load("assets/jupiter.png"),
    "saturn" : pygame.image.load("assets/saturn.png"),
    "neptune" : pygame.image.load("assets/neptune.png"),
    "uranus" : pygame.image.load("assets/uranus.png"),
}

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

def makeNewPlanet(which):

    for pieceOfRock in planets:

        if pieceOfRock["name"] == which:
            return copy.deepcopy(pieceOfRock)

    return False

