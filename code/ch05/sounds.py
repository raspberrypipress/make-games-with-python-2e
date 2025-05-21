import pygame
from pygame import image, mixer, Vector2
import itertools

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
stop_btn = {"image" : image.load(f"{imgs}/stop.png"),
            "pos" : (275, 585)}

volume = 0.2
volume_slider_rect = pygame.Rect(450, 610, 100, 5)

flashed = None
CLEAR_FLASH = pygame.USEREVENT + 0
flash_timer = 250

# Initialise the mixer and play a sound
pygame.mixer.init()
pygame.mixer.music.load(f"{snds}/OGG/farm.ogg")
pygame.mixer.music.play(-1)

# Create buttons
animals = ["sheep", "rooster", "pig", "mouse",
           "horse", "dog", "cow", "chicken", "cat"]
coords = itertools.product([0,1,2], repeat=2)
offset = Vector2(25, 25)
for animal in animals:
    position = Vector2(next(coords)) * 200 + offset
    img = image.load(f"{imgs}/{animal}.png")
    snd = mixer.Sound(f"{snds}/OGG/{animal}.ogg")
    buttons.append({"image": img,
                    "pos": position,
                    "sound": snd})

def draw_buttons():
    for button in buttons + [stop_btn]:
        img = button["image"]
        if flashed == img:
            img = flash_button(img)
        window.blit(img, button["pos"])       

def flash_button(img):    
    inv = pygame.Surface(img.get_rect().size, pygame.SRCALPHA)
    inv.blit(img, (0,0), None)
    inv.fill((255, 255, 255, 128), None, 
             pygame.BLEND_RGBA_MULT)
    return inv

def handle_click():
    global flashed

    for button in buttons:
        rect = button["image"].get_rect(topleft=button["pos"])

        if rect.collidepoint(pygame.mouse.get_pos()):
            flashed = button["image"]
            pygame.time.set_timer(CLEAR_FLASH, flash_timer)
            button["sound"].set_volume(volume)
            button["sound"].play()

    rect = stop_btn["image"].get_rect(topleft=stop_btn["pos"])
    if rect.collidepoint(pygame.mouse.get_pos()):
        flashed = stop_btn["image"]
        pygame.time.set_timer(CLEAR_FLASH, flash_timer)
        mixer.stop()

def draw_volume():
    pygame.draw.rect(window, (229, 229, 229), 
                     volume_slider_rect)

    volume_pos = (100 / 100) * (volume * 100)

    pygame.draw.rect(window, (204, 204, 204), 
                     (450 + volume_pos, 600, 10, 25))

def check_volume():
    global volume

    if pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()
        if volume_slider_rect.collidepoint(mouse_pos):
            volume = float((mouse_pos[0] - 450)) / 100

def quit_game():
    pygame.quit()
    raise SystemExit

# main loop
while True:
    window.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_game()
        if event.type == pygame.QUIT:
            quit_game()
        if event.type == pygame.MOUSEBUTTONUP:
            handle_click()
        if event.type == CLEAR_FLASH:
            flashed = None

    draw_buttons()
    check_volume()
    draw_volume()

    pygame.display.update()
    clock.tick(fps)