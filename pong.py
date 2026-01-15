# Original version by Vinoth Pandian
# Modified for lzscc.200 by Marco Caminati
# You might need to install pygame:
# python3 -m pip install --user pygame
# If the command above doesn't work, try venv:
# python3 -m venv ~/pongenv
# source ~/pongenv/bin/activate
# python3 -m pip install pygame

import pygame, random, sys
from pygame.locals import *

pygame.init()
fps = pygame.time.Clock()

#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255, 255, 0)
BLACK = (0,0,0)
BRIGHTBLUE = (0, 150, 255)


#globals
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
ABILITY_COOLDOWN = 3.5
CD_RIGHT=0.0
CD_LEFT=0.0
balls = []
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0



#canvas declaration
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Hello World')

class Ball:
    def __init__(self, x, y, vx, vy, type = RED, radius = BALL_RADIUS, score = 1):
        self.pos = pygame.Vector2(x,y)
        self.vel = pygame.Vector2(vx,vy)
        self.radius = radius
        self.type = type
        self.score = score
        
    def update(self):
        self.pos += self.vel

        if int(self.pos.y) <= self.radius:
            self.vel.y = -self.vel.y
        if int(self.pos.y) >= HEIGHT + 1 - self.radius:
            self.vel.y = -self.vel.y

    def draw(self, canvas):
        pygame.draw.circle(canvas, self.type, (int(self.pos.x), int(self.pos.y)), self.radius, 0)
        


# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global balls# these are vectors stored as lists
    horz = random.randrange(2,4)
    vert = random.randrange(1,3)
    
    if right == False:
        horz = - horz
        
    balls = [Ball(WIDTH//2, HEIGHT//2, horz, -vert)]


def ability(right):
    global balls # these are vectors stored as lists

    horz = random.randrange(2,4)
    vert = random.randrange(1,3)
    
    if right == False:
        horz = - horz
        
    balls.append(Ball(WIDTH//2, HEIGHT//2, horz, -vert, type=YELLOW, score = 0.5))

# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,l_score,r_score  # these are floats
    global score1, score2  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH - 1,HEIGHT//2]
    paddle2_pos = [WIDTH +1 - HALF_PAD_WIDTH,HEIGHT//2]
    l_score = 0
    r_score = 0
    if random.randrange(0,2) == 0:
        ball_init(True)
    else:
        ball_init(False)


#draw function of canvas
def draw(canvas):
    global paddle1_pos, paddle2_pos, balls, l_score, r_score
           
    canvas.fill(BLACK)
    pygame.draw.line(canvas, WHITE, [WIDTH // 2, 0],[WIDTH // 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
    pygame.draw.circle(canvas, WHITE, [WIDTH//2, HEIGHT//2], 70, 1)

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos[1] += paddle1_vel
    
    if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos[1] += paddle2_vel

    for ball in balls[:]:
        ball.update()
        ball.draw(canvas)

        if int(ball.pos.x) <= ball.radius + PAD_WIDTH and int(ball.pos.y) in range(paddle1_pos[1] - HALF_PAD_HEIGHT, paddle1_pos[1] + HALF_PAD_HEIGHT,1):
            ball.vel.x = -ball.vel.x
            ball.vel.x *= 1.1
            ball.vel.y *= 1.1
        elif int(ball.pos.x) <= ball.radius + PAD_WIDTH:
            r_score += ball.score
            balls.remove(ball)
            if getattr(ball, "type") == RED:
                ball_init(True)
            continue

        if int(ball.pos.x) >= WIDTH + 1 - ball.radius - PAD_WIDTH and int(ball.pos.y) in range(paddle2_pos[1] - HALF_PAD_HEIGHT,paddle2_pos[1] + HALF_PAD_HEIGHT,1):
            ball.vel.x = -ball.vel.x
            ball.vel.x *= 1.1
            ball.vel.y *= 1.1
        elif int(ball.pos.x) >= WIDTH + 1 - ball.radius - PAD_WIDTH:
            l_score += ball.score
            balls.remove(ball)
            if getattr(ball, "type") == RED:
                ball_init(False)
            continue

    #draw paddles and ball
    pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)

    #update scores
    myfont1 = pygame.font.SysFont("Times New Roman", 16)
    label_l_score = myfont1.render(f"Score: {l_score:.1f}", True, YELLOW)
    canvas.blit(label_l_score, (15, 10))

    label_r_score = myfont1.render(f"Score: {r_score:.1f}", True, YELLOW)
    canvas.blit(label_r_score, (430, 10))  
    
    label_l_cd = myfont1.render(f"player 1 Cooldown: {CD_LEFT:.1f}", 1, BRIGHTBLUE)
    canvas.blit(label_l_cd, (15, 40))

    label_r_cd = myfont1.render(f"player 2 Cooldown: {CD_RIGHT:.1f}", 1, BRIGHTBLUE)
    canvas.blit(label_r_cd, (430, 40))
    
#keydown handler
def keydown(event):
    global paddle1_vel, paddle2_vel, balls, CD_LEFT, CD_RIGHT, ABILITY_COOLDOWN
    
    if event.key == K_UP:
        paddle2_vel = -8
    elif event.key == K_DOWN:
        paddle2_vel = 8
    elif event.key == K_w:
        paddle1_vel = -8
    elif event.key == K_s:
        paddle1_vel = 8
    elif event.key == K_e:
        if CD_LEFT == 0:
            ability(True)
            CD_LEFT = ABILITY_COOLDOWN
    elif event.key == K_l:
        if CD_RIGHT == 0:
            ability(False)
            CD_RIGHT = ABILITY_COOLDOWN
    elif event.key == K_LEFT or event.key == K_d:
        for ball in balls:
            ball.vel.x *= 1.3
            ball.vel.y *= 1.3
    elif event.key == K_RIGHT or event.key == K_a:
        for ball in balls:
            ball.vel.x *= 0.8
            ball.vel.y *= 0.8

#keyup handler
def keyup(event):
    global paddle1_vel, paddle2_vel
    
    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_UP, K_DOWN):
        paddle2_vel = 0

init()

#game loop
while True:
    downtime = fps.get_time() / 1000

    if CD_RIGHT > 0:
        CD_RIGHT -= downtime
        if CD_RIGHT < 0:
            CD_RIGHT = 0

    if CD_LEFT > 0:
        CD_LEFT -= downtime
    if CD_LEFT < 0:
        CD_LEFT = 0

    
    draw(window)

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()
    fps.tick(60)