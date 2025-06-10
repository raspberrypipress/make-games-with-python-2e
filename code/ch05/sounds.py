import pygame
from pygame import image, mixer, Vector2
import itertools

pygame.init()
FPS = 60
WIN_WIDTH = 600
WIN_HEIGHT = 650
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Soundboard")

DEFAULT_VOLUME = 0.2
IMAGES_PATH = "assets/images"
SOUNDS_PATH = "assets/sounds"
FLASH_TIMER = 250
FLASH_COLOUR = (255, 255, 255, 128)
ANIMALS = ["sheep", "rooster", "pig", "mouse",
           "horse", "dog", "cow", "chicken", "cat"]

buttons = []
stop_btn = {"image": image.load(f"{IMAGES_PATH}/stop.png"),
            "pos": (275, 585)}
flashed = None
CLEAR_FLASH = pygame.USEREVENT + 0

volume = DEFAULT_VOLUME
volume_slider_rect = pygame.Rect(450, 610, 100, 5)

pygame.mixer.init()
pygame.mixer.music.load(f"{SOUNDS_PATH}/OGG/farm.ogg")
pygame.mixer.music.play(-1)

# Create animal sound buttons
coords = itertools.product([0, 1, 2], repeat=2)
offset = Vector2(25, 25)
for animal in ANIMALS:
    position = Vector2(next(coords)) * 200 + offset
    img = image.load(f"{IMAGES_PATH}/{animal}.png")
    snd = mixer.Sound(f"{SOUNDS_PATH}/OGG/{animal}.ogg")
    buttons.append({"image": img,
                    "pos": position,
                    "sound": snd})

def draw_buttons():
    for button in buttons + [stop_btn]:
        img = button["image"]
        if flashed == img:
            img = create_flashed_button(img)
        window.blit(img, button["pos"])

def create_flashed_button(img):
    flashed = pygame.Surface(img.get_rect().size, 
                             pygame.SRCALPHA)
    flashed.blit(img, (0, 0))
    flashed.fill(FLASH_COLOUR, None, pygame.BLEND_RGBA_MULT)
    return flashed

def handle_button_click():
    global flashed
    mouse_pos = pygame.mouse.get_pos()

    for button in buttons:
        rect = button["image"].get_rect(topleft=button["pos"])
        if rect.collidepoint(mouse_pos):
            flashed = button["image"]
            pygame.time.set_timer(CLEAR_FLASH, FLASH_TIMER)
            button["sound"].set_volume(volume)
            button["sound"].play()
            return

    # Check stop button
    rect = stop_btn["image"].get_rect(topleft=stop_btn["pos"])
    if rect.collidepoint(mouse_pos):
        flashed = stop_btn["image"]
        pygame.time.set_timer(CLEAR_FLASH, FLASH_TIMER)
        mixer.stop()

def draw_volume_slider():
    # Draw slider background
    pygame.draw.rect(window, (229, 229, 229), 
                     volume_slider_rect)
    
    # Draw slider handle
    volume_pos = volume * 100
    handle_rect = pygame.Rect(450 + volume_pos, 600, 10, 25)
    pygame.draw.rect(window, (204, 204, 204), handle_rect)

def update_volume():
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
        elif event.type == pygame.MOUSEBUTTONUP:
            handle_button_click()
        elif event.type == CLEAR_FLASH:
            flashed = None

    draw_buttons()
    update_volume()
    draw_volume_slider()

    pygame.display.update()
    clock.tick(FPS)