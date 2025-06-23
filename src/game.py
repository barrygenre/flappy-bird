import pygame
import random
import os

# import json  # For high scores

from pygame.locals import *

BASE_DIR = os.path.dirname(__file__)
ASSET_PATH = lambda name: os.path.join(BASE_DIR, "assets", name)
HIGHSCORE_PATH = os.path.join(BASE_DIR, "highscore.txt")

pygame.init()
clock = pygame.time.Clock()
fps = 60
screen_width = 864
screen_height = 936
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 200
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks()
score = 0
highscore = 0
pass_pipe = False

# Uncomment to enable sound
# pygame.mixer.init()
# flap_sound = pygame.mixer.Sound(ASSET_PATH("flap.wav"))
# hit_sound = pygame.mixer.Sound(ASSET_PATH("hit.wav"))

# Load images
bg = pygame.image.load(ASSET_PATH("bg.png"))
# dark_bg = pygame.image.load(ASSET_PATH("bg_dark.png"))  # Uncomment for dark mode
ground = pygame.image.load(ASSET_PATH("ground.png"))
restart_img = pygame.image.load(ASSET_PATH("restart.png"))

font = pygame.font.SysFont("Arial", 48)


def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


# Uncomment to load high score from file
# if os.path.exists(HIGHSCORE_PATH):
#     with open(HIGHSCORE_PATH, "r") as f:
#         highscore = int(f.read())


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [
            pygame.image.load(ASSET_PATH(f"bird{n}.png")) for n in range(1, 4)
        ]
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0
        self.clicked = False

    def update(self):
        if flying:
            self.velocity += 0.5  # Original gravity
            # self.velocity += 1.2  # Uncomment for higher gravity (Git task)
            if self.velocity > 8:
                self.velocity = 8
            if self.rect.bottom < screen_height - ground.get_height():
                self.rect.y += int(self.velocity)

        if pygame.mouse.get_pressed()[0] == 1 and not self.clicked and not game_over:
            self.clicked = True
            self.velocity = -10
            # flap_sound.play()

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.counter += 1
        if self.counter > 5:
            self.counter = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

        self.image = pygame.transform.rotate(
            self.images[self.index], -self.velocity * 2
        )
        self.rect = self.image.get_rect(center=self.rect.center)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__()
        self.image = pygame.image.load(ASSET_PATH("pipe.png"))
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y - pipe_gap // 2)
        else:
            self.rect.topleft = (x, y + pipe_gap // 2)

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self):
        screen.blit(self.image, self.rect)
        return (
            self.rect.collidepoint(pygame.mouse.get_pos())
            and pygame.mouse.get_pressed()[0]
        )


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
flappy = Bird(100, screen_height // 2)
bird_group.add(flappy)
button = Button(screen_width // 2, screen_height // 2, restart_img)

run = True
while run:
    clock.tick(fps)

    # Background toggle (feature)
    screen.blit(bg, (0, 0))
    # screen.blit(dark_bg, (0, 0))  # Uncomment to enable dark mode

    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update()
    screen.blit(ground, (ground_scroll, screen_height - ground.get_height()))

    if not game_over and flying:
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            pipe_group.add(Pipe(screen_width, screen_height // 2 + pipe_height, 1))
            pipe_group.add(Pipe(screen_width, screen_height // 2 + pipe_height, -1))
            last_pipe = time_now

        pipe_group.update()

        if len(pipe_group) > 0:
            pipe = pipe_group.sprites()[0]
            if (
                flappy.rect.left > pipe.rect.left
                and flappy.rect.right < pipe.rect.right
                and not pass_pipe
            ):
                pass_pipe = True
            if pass_pipe and flappy.rect.left > pipe.rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, (255, 255, 255), screen_width // 2, 20)
    # draw_text(f"High: {highscore}", font, (255, 255, 0), screen_width - 200, 20)

    if (
        pygame.sprite.groupcollide(bird_group, pipe_group, False, False)
        or flappy.rect.top < 0
    ):
        game_over = True
        # hit_sound.play()

    if flappy.rect.bottom >= screen_height - ground.get_height():
        flying = False
        game_over = True

    if game_over:
        if button.draw():
            game_over = False
            score = 0
            pipe_group.empty()
            flappy.rect.center = (100, screen_height // 2)
            flappy.velocity = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True

    pygame.display.update()

pygame.quit()

# Uncomment to save highscore
# if score > highscore:
#     with open(HIGHSCORE_PATH, "w") as f:
#         f.write(str(score))
