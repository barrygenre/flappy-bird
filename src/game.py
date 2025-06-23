import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60  # Frames per second

screen_width = 864
screen_height = 936
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# game vars
ground_scroll = 0
scroll_speed = 4
# load images for the game
bg = pygame.image.load("assets/bg.png")
ground = pygame.image.load("assets/ground.png")


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0  # Animation counter
        for num in range(1, 4):
            img = pygame.image.load(f"assets/bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]  # Set the initial image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.counter += 1  # Increment the animation counter
        flap_cooldonw = 5  # Control the speed of the animation
        if self.counter > flap_cooldonw:
            self.counter = 0  # Reset the counter
            self.index += 1  # Move to the next image
            if self.index >= len(self.images):
                self.index = 0  # Loop back to the first image
            self.image = self.images[self.index]  # Update the image


bird_group = pygame.sprite.Group()

flappy_bird = Bird(100, screen_height // 2)

bird_group.add(flappy_bird)  # Add the bird to the sprite group


run = True
# The game loop
while run:

    clock.tick(fps)  # Control the frame rate
    screen.blit(bg, (0, 0))  # Draw the background

    bird_group.draw(screen)  # Draw the bird
    bird_group.update()  # Update the bird's animation
    screen.blit(
        ground, (ground_scroll, screen_height - ground.get_height())
    )  # Draw the ground scroll and ground
    ground_scroll -= scroll_speed  # Update ground scroll position
    if abs(ground_scroll) > 35:
        ground_scroll = 0
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    pygame.display.update()  # Update the display

pygame.quit()
# Exit the game
