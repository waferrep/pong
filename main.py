import pygame, sys
import random
import os

def ball_animation():
    global ball_speed_x, ball_speed_y
    #ball goes faster
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    #collisions
    if ball.top <= 0 or ball.bottom >= screen_height:
        pygame.mixer.Sound.play(sfx)
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        ball_restart()
    #collision with paddle
    if ball.colliderect(player) or ball.colliderect(opponent):
        pygame.mixer.Sound.play(sfx)
        ball_speed_x *= -1


def player_animation():
    player.y += player_speed
    #tp player to top or bottom if they hit border
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_animation():
    #follows ball up and down depending on its position
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.top > ball.y:
        opponent.top -= opponent_speed
    #tp player top or bottom if border touched
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_restart():
    global ball_speed_x, ball_speed_y, score, score_opponent
    #tp to center
    ball.center = (screen_width/2, screen_height/2)
    score += 1
    score_opponent += 1
    #randomly select direction
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))

pygame.init() #required for pygame 
pygame.mixer.init() #audio
clock = pygame.time.Clock()

#set up window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

#game rectangles
#pygame.rect renders from left corner, so to center need to do half screen dimensions - half ball dimensions
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30) 
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10,140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10,140)

#colors
bg_color = (31,31,31)
white = (255,255,255)

#ball speed
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))

#player speed
player_speed = 0
opponent_speed = 7

#score
score = 0
score_opponent = 0

#sound assignment
sfx = pygame.mixer.Sound("sounds/pong.mp3")


while True: #updates game
    #this loop just checks if the user quit the window or not on a loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_w:
                player_speed += 7
            if event.key == pygame.K_UP or event.key == pygame.K_s:
                player_speed -= 7
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN or event.key == pygame.K_w:
                player_speed -= 7
            if event.key == pygame.K_UP or event.key == pygame.K_s:
                player_speed += 7    


    ball_animation()
    player_animation()
    opponent_animation()

    #visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen,white, player)
    pygame.draw.rect(screen,white, opponent)
    pygame.draw.ellipse(screen,white, ball)
    pygame.draw.aaline(screen, white, (screen_width / 2, 0),(screen_width / 2, screen_height))

    #scoreboard
    font = pygame.font.Font('fonts/CaviarDreams.ttf', 32)
    text = font.render(f'Score: {score_opponent}', True, white)
    screen.blit(text, (screen_width/1.99, screen_height/2)) #1.99 cus it Looks just a little bit better than 2

    font2 = pygame.font.Font('fonts/CaviarDreams.ttf', 32)
    text2 = font.render(f'Score: {score}', True, white)
    screen.blit(text2, (screen_width/2.9, screen_height/2))



    #updates window
    pygame.display.flip()
    clock.tick(60) #fps