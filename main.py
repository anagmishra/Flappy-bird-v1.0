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
    image = font.render(text, True, white)
    screen.blit(image, (x, y)) #Helps to actually add the background image

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(HEIGHT/2)
    score = 0
    return score

class Bird(pygame.sprite.Sprite):

    def __init__(self, x, y): #First method that gets called
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f"images/bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center[x, y]
        self.vel = 0
        self.click = False

    def update(self):
        if flying == True:
            self.vel += 0.5
            if self.vel> 8:
                self.vel = 8
            if self.rect.bottom<768:
                self.rect.y += int(self.vel)

        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                self.click = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.click == False
            #Handling animation of the bird
            flap_cooldown = 5 #Total number of frames per each image
            self.counter += 1
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]
            self.image = pygame.transform.rotate(self.images[self.index], self.vel*-2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect < 0:
            self.kill()
    
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image,(self.rect.x, self.rect.y))
        return action

pipe_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()

flappy = Bird(100, int(HEIGHT/2))

bird_group.add(flappy)

button = Button(WIDTH//2-50, HEIGHT//2-100, button_img)

run = True
while run:
    clock.tick(fps)
    screen.blit(bg, (0,0))
    pipe_group.draw(screen)
    bird_group.draw(screen)
    bird_group.update()

    screen.blit(ground_img, (ground_scroll, 768))
    if len(pipe_group) > 0:
        if (bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe == False):
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score+=1
                pass_pipe = False
    draw_text(str(score), font, white, int(WIDTH/2), 20)
    if (pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0):
        game_over = True
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False
    