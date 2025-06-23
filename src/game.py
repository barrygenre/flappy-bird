import pygame
import random
from pygame.locals import *

pygame.init()

# Game settings
clock = pygame.time.Clock()
fps = 60
screen_width = 864
screen_height = 936
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# Game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 200
pipe_frequency = 1500  # ms
last_pipe = pygame.time.get_ticks()
score = 0
pass_pipe = False

# Load images
bg = pygame.image.load("assets/bg.png")
ground = pygame.image.load("assets/ground.png")
restart_img = pygame.image.load("assets/restart.png")

# Font
font = pygame.font.SysFont("Arial", 48)


def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [pygame.image.load(f"assets/bird{n}.png") for n in range(1, 4)]
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 0
        self.clicked = False

    def update(self):
        if flying:
            self.velocity += 0.5
            if self.velocity > 8:
                self.velocity = 8
            if self.rect.bottom < screen_height - ground.get_height():
                self.rect.y += int(self.velocity)

        if pygame.mouse.get_pressed()[0] == 1 and not self.clicked and not game_over:
            self.clicked = True
            self.velocity = -10
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Animation
        self.counter += 1
        flap_cooldown = 5
        if self.counter > flap_cooldown:
            self.counter = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

        self.image = pygame.transform.rotate(
            self.images[self.index], -self.velocity * 2
        )
        self.rect = self.image.get_rect(center=self.rect.center)


# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__()
        self.image = pygame.image.load("assets/pipe.png")
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


# Button class
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


# Groups
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
flappy = Bird(100, screen_height // 2)
bird_group.add(flappy)

button = Button(screen_width // 2, screen_height // 2, restart_img)

# Game loop
run = True
while run:
    clock.tick(fps)
    screen.blit(bg, (0, 0))
    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update()

    # Draw and scroll ground
    screen.blit(ground, (ground_scroll, screen_height - ground.get_height()))
    if not game_over and flying:
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        # Create new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            top_pipe = Pipe(screen_width, screen_height // 2 + pipe_height, 1)
            bottom_pipe = Pipe(screen_width, screen_height // 2 + pipe_height, -1)
            pipe_group.add(top_pipe)
            pipe_group.add(bottom_pipe)
            last_pipe = time_now

        pipe_group.update()

        # Score
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

    # Collision
    if (
        pygame.sprite.groupcollide(bird_group, pipe_group, False, False)
        or flappy.rect.top < 0
    ):
        game_over = True

    if flappy.rect.bottom >= screen_height - ground.get_height():
        flying = False
        game_over = True

    # Restart
    if game_over:
        if button.draw():
            game_over = False
            score = 0
            pipe_group.empty()
            flappy.rect.center = (100, screen_height // 2)
            flappy.velocity = 0

    # Events
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True

    pygame.display.update()

pygame.quit()
