import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

WIDTH = 864
HEIGHT = 936

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

font = pygame.font. SysFont("Algerian", 60)

white = (255, 255, 255)

#Defining the game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

#Loading the images
bg = pygame.image.load("images/backgroung.png")
ground_img = pygame.image.load("images/ground.png")
button_img = pygame.image.load("images/restart_button.png")

#Function to display text on the screen
def draw_text(text, font, white, x, y):
    img = font.render(text, True, white)
    screen.blit(img, (x, y))