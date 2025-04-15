import pygame
from pygame import image, mixer
import sys

pygame.init()
clock = pygame.time.Clock()
fps = 60

win_width = 600
win_height = 650
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Soundboard")

imgs = "assets/images"
snds = "assets/sounds"

buttons = []
stop_button = {"image" : image.load(f"{imgs}/stop.png"),
               "pos" : (275, 585)}

volume = 0.2
volume_slider_rect = pygame.Rect(450, 610, 100, 5)

flashed = None
CLEAR_FLASH = pygame.USEREVENT + 0
flash_button_timer = 250

pygame.mixer.init()
pygame.mixer.music.load(f"{snds}/OGG/farm.ogg")
pygame.mixer.music.play(-1)

def flash_button(img):    
    inv = pygame.Surface(img.get_rect().size, pygame.SRCALPHA)
    inv.blit(img, (0,0), None)
    inv.fill((255, 255, 255, 128), special_flags=pygame.BLEND_RGBA_MULT) 
    return inv

def draw_buttons():
    for button in buttons + [stop_button]:
        img = button["image"]
        if flashed == img:
            img = flash_button(img)
        window.blit(img, button["pos"])       

def draw_volume():
    pygame.draw.rect(window, (229, 229, 229), 
                     volume_slider_rect)

    volume_pos = (100 / 100) * (volume * 100)

    pygame.draw.rect(window, (204, 204, 204), 
                     (450 + volume_pos, 600, 10, 25))

def handle_click():
    global flashed

    for button in buttons:
        rect = button["image"].get_rect(topleft=button["pos"])

        if rect.collidepoint(pygame.mouse.get_pos()):
            flashed = button["image"]
            pygame.time.set_timer(CLEAR_FLASH, flash_button_timer)
            button["sound"].set_volume(volume)
            button["sound"].play()

    rect = stop_button["image"].get_rect(topleft=stop_button["pos"])
    if rect.collidepoint(pygame.mouse.get_pos()):
        flashed = stop_button["image"]
        pygame.time.set_timer(CLEAR_FLASH, flash_button_timer)
        mixer.stop()

def checkVolume():
    global volume

    if pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()
        if volume_slider_rect.collidepoint(pygame.mouse.get_pos()):
            volume = float((mouse_pos[0] - 450)) / 100

def quitGame():
    pygame.quit()
    raise SystemExit


# Create Buttons
animals = ["sheep", "rooster", "pig",
           "mouse", "horse", "dog",
           "cow", "chicken", "cat"]
for y in [25, 225, 425]:
    for x in [25, 225, 425]:
        animal = animals.pop(0)
        img = image.load(f"{imgs}/{animal}.png")
        snd = mixer.Sound(f"{snds}/OGG/{animal}.ogg")
        buttons.append({"image": img,
                        "pos": (x, y),
                        "sound": snd})

# main loop
while True:

    window.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitGame()
        if event.type == pygame.QUIT:
            quitGame()
        if event.type == pygame.MOUSEBUTTONUP:
            handle_click()
        if event.type == CLEAR_FLASH:
            flashed = None

    draw_buttons()
    checkVolume()
    draw_volume()

    pygame.display.update()
