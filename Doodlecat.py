#This code creates a doodle jump - like game but with a cat! 
import pygame, sys
from pygame.locals import *
import random
pygame.init()

#Colours + Background
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
sky = (150, 190, 208)
red = (110, 38, 14)
offWhite = (241, 244, 246)
background = sky

#Library of Game Contants
windowWidth = 400
windowHeight = 500
font = pygame.font.Font('freesansbold.ttf', 16)
player = pygame.transform.scale(pygame.image.load('kityKity.png'), (90, 70))
fishy = pygame.transform.scale(pygame.image.load('kityFish.png'), (20, 10))
fps = 60
timer = pygame.time.Clock()
score = 0
high_score = 0
score_last = 0
game_over = False
super_jumps = 2

#Game Variables
player_x = 153
player_y = 400
platforms = [[175, 480, 70, 10], [85, 370, 70, 10], [265, 370, 70, 10], [175, 260, 70, 10], [85, 150, 70, 10], [265, 150, 70, 10], [175, 40, 70, 10]]
jump = False
y_change = 0
x_change = 0
player_speed = 3

#Create Screen
screen = pygame.display.set_mode([windowWidth, windowHeight])
pygame.display.set_caption('Kitty Jump')

#When player collides with blocks (defining check_collisions)
def check_collisions(rect_list, j):
    global player_x
    global player_y
    global y_change
    for i in range(len(rect_list)):
        if rect_list[i].colliderect([player_x + 30, player_y + 61, 44, 2]) and jump == False and y_change > 0:
            j = True
    return j


#Updating Player position(y), every loop, includes defining gravity and the jump height
def update_player(y_pos):
    global jump
    global y_change
    jump_height = 10
    gravity = 0.4
    if jump:
        y_change = -jump_height
        jump = False
    y_pos += y_change
    y_change += gravity
    return y_pos

#Movement of Platforms as the Game Progresses
def update_platforms(my_list, y_pos, change):
    global score
    if y_pos < 250 and change < 0:
        for i in range(len(my_list)):
            my_list[i][1] -= change
    else:
        pass
    for item in range(len(my_list)):
        if my_list[item][1] > 500:
            my_list[item] = [random.randint(10, 320), random.randint(-50, -10), 70, 10]
            score += 1
    return my_list

#While the game is running...
running = True
while running == True:
    timer.tick(fps)
    screen.fill(background)
    screen.blit(player,(player_x, player_y))
    blocks = []
    #Score/HighScore Text
    score_text = font.render('Score: '+ str(score), True, black, background)
    screen.blit(score_text, (320, 40))
    high_score_text = font.render('High Score: '+ str(high_score), True, black, background)
    screen.blit(high_score_text, (280, 20))
    #Lets player know to hit SPACE to play again
    if game_over:
        game_over_text = font.render('Game Over: Spacebar to Restart!', True, black, background)
        screen.blit(game_over_text, (80, 80))
    #Platforms!
    for i in range(len(platforms)):
        block = pygame.draw.rect(screen, offWhite, platforms[i], 0, 3)
        blocks.append(block)

    #Quitting Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
       
        #Movement!
        if event.type == pygame.KEYDOWN:
            #Game Over and Restart
            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                score = 0
                player_x = 153
                player_y = 400
                background = sky
                score_last = 0
                super_jumps = 2
                platforms = [[175, 480, 70, 10], [85, 370, 70, 10], [265, 370, 70, 10], [175, 260, 70, 10], [85, 150, 70, 10], [265, 150, 70, 10], [175, 40, 70, 10]]
            #Right and Left Movement
            if event.key == pygame.K_a:
                x_change = -player_speed
            if event.key == pygame.K_d:
                x_change = player_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                x_change = 0
            if event.key == pygame.K_d:
                x_change = 0

    jump = check_collisions(blocks, jump)
    player_x += x_change

    #Game is Over when...
    if player_y < 440:
        player_y = update_player(player_y)
    else:
        game_over = True
        y_change = 0
        x_change = 0

    #Keeping within x boundaries
    if player_x < -20:
        player_x = -20
    elif player_x > 330:
        player_x = 330

    platforms = update_platforms(platforms, player_y, y_change)
   
   #Face Direction of Movement
    if x_change > 0:
        player = pygame.transform.scale(pygame.image.load('kityKity.png'), (90, 70))
    elif x_change < 0:
        player = pygame.transform.flip(pygame.transform.scale(pygame.image.load('kityKity.png'), (90, 70)), 1, 0)
  
   #High Score Tracking
    if score > high_score:
        high_score = score
 
    #Colour Change as the Player Progresses
    if score - score_last > 10:
        score_last = score
        background = (random.randint(2, 253), random.randint(2, 253), random.randint(2, 253))
    pygame.display.flip()
pygame.quit()
