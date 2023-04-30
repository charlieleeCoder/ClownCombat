import pygame
import sys
from pygame import mixer
from fighterTypes import Fighter


pygame.init()
mixer.init()

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Clown Combat')

#set framerate
clock = pygame.time.Clock()
FPS = 50

#colours
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0] # player scores [p1, p2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#load music & sounds
try:
    pygame.mixer.music.load('Music\ld32.mp3')
    pygame.mixer.music.play(-1, 0.0, 5000)
except KeyboardInterrupt:
    sys.exit()
except:
    music="failed"

#load background
bg_image = pygame.image.load('Art\Circuspixelart.jpg').convert_alpha()

#define font
count_font = pygame.font.Font('Fonts\RockwellNova.ttf', 100)
score_font = pygame.font.Font('Fonts\RockwellNova.ttf', 30)
victory_font = pygame.font.Font('Fonts\RockwellNova.ttf', 100)

#function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH,SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0,0))

#define fighter variables
juggling_clown_size = 64
juggling_clown_scale = 3.5
juggling_clown_offset = [21, 10]
juggling_clown_data = [juggling_clown_size, juggling_clown_scale, juggling_clown_offset]
fat_clown_size = 64
fat_clown_scale = 3.5
fat_clown_offset = [21, 10]
fat_clown_data = [fat_clown_size, fat_clown_scale, fat_clown_offset]

#load spritesheet
juggling_clown = pygame.image.load('Art\sprite 5-Sheet.png').convert_alpha()
fat_clown = pygame.image.load('Art\\fat clown-Sheet.png').convert_alpha()

# define number of steps in each animation
juggling_clown_animation_steps = [5, 7, 7, 5]
fat_clown_animation_steps = [2, 2, 2, 5]

# function for drawing health bar
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, BLACK, (x - 2, y - 2, 406, 36))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

# create two instances of fighters
fighter_1 = Fighter (1, 200, 310, juggling_clown_data, juggling_clown, juggling_clown_animation_steps) #add animation deets
fighter_2 = Fighter (2, 700, 310, fat_clown_data, fat_clown, fat_clown_animation_steps) #add animation deets

# game loop
run = True
while run:

    # frame rate
    clock.tick(FPS)

    # draw background
    draw_bg ()

    # show player health
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text('P1: ' + str(score[0]), score_font, RED, 20, 60)
    draw_text('P2: ' + str(score[1]), score_font, RED, 580, 60)

    # update fighters
    fighter_1.update()
    fighter_2.update()

    # draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # check for player defeat
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over =  True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] += 1
            round_over =  True
            round_over_time = pygame.time.get_ticks()
    else:
        ## display Victory ## duplicate
        draw_text('Victory!', victory_font, RED, int(SCREEN_WIDTH/2 - 175), int(SCREEN_HEIGHT)/3)
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter (1, 200, 310, juggling_clown_data, juggling_clown, juggling_clown_animation_steps) #add animation deets
            fighter_2 = Fighter (2, 700, 310, fat_clown_data, fat_clown, fat_clown_animation_steps) #add animation deets

    # update countdown
    if intro_count <= 0:
        # move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        # display count timer
        draw_text(str(intro_count), count_font, RED, int(SCREEN_WIDTH/2 - 25), int(SCREEN_HEIGHT)/3)
        # update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display
    pygame.display.update()

# exit pygame
pygame.quit()
