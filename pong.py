import pygame


# Class for the Paddle
class Player(pygame.rect.Rect):
    def __init__(self, x, y, w, h, max_x, min_x):
        super().__init__(x, y, w, h)
        self.max_x = max_x
        self.min_x = min_x


# Initialize pygame Clock
clock = pygame.time.Clock()

# Initialise pygame
pygame.init()

# Define some constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 60


# Function to move player
def move_player(player, keys, controls, pos, speed=0.5):
    # Check for the pressed key and then move the player accordingly
    if keys[controls['up']] and pos[1] > 0:  # 'up' key is pressed
        pos[1] -= speed  # moving player up
    # Repeat for other directions
    if keys[controls['down']] and pos[1] < SCREEN_HEIGHT - player.height:
        pos[1] += speed
    if keys[controls['right']] and pos[0] < player.max_x - player.width:
        pos[0] += speed
    if keys[controls['left']] and pos[0] > player.min_x:
        pos[0] -= speed


# Setting up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")

# Initialize the players
player1 = Player(PLAYER_WIDTH, SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT, SCREEN_WIDTH / 2,
                 0)
player2 = Player(SCREEN_WIDTH - 2 * PLAYER_WIDTH, SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT,
                 SCREEN_WIDTH, SCREEN_WIDTH / 2)

# Setting up the font for the score
font = pygame.font.SysFont(None, 64)

# Initialize both scores to zero and a variable to keep track of who scored last.
player1_score = 0
player2_score = 0
last_scored = 1  # let's say Player One starts

# Define the net parameters
net_colour = pygame.Color('gray')
NET_WIDTH = 5
NET_HEIGHT = 40
GAP_HEIGHT = 20

# Define the ball parameters
ball_colour = pygame.Color('white')
ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
ball_radius = 7.5

# Initialise the player's position on screen
player1_pos = [player1.x, player1.y]
player2_pos = [player2.x, player2.y]

# Define the controls for each player
controls1 = {'up': pygame.K_w, 'down': pygame.K_s, 'right': pygame.K_d, 'left': pygame.K_a}
controls2 = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'right': pygame.K_RIGHT, 'left': pygame.K_LEFT}

# Set the initial speed of the ball
ball_speed = [0.15, 0.15]
ball_direction = 1

# Initialize pygame mixer
pygame.mixer.init()

# Load the sound effects
wall_sound = pygame.mixer.Sound('wall.wav')
paddle_sound = pygame.mixer.Sound('goal.wav')
goal_sound = pygame.mixer.Sound('paddle.wav')

# Game loop
while True:
    quit_game = False

    # Check for keypresses
    for event in pygame.event.get():
        if event.type == pygame.QUIT or player1_score == 10 or player2_score == 10:
            quit_game = True
            break

    # End the game
    if quit_game:
        pygame.quit()
        break

    # clear screen
    screen.fill((0, 0, 0))

    # Draw the net dividing the play area in two halves
    for i in range(0, SCREEN_HEIGHT, NET_HEIGHT + GAP_HEIGHT):
        pygame.draw.rect(screen, net_colour, pygame.Rect(SCREEN_WIDTH // 2 - NET_WIDTH // 2, i, NET_WIDTH, NET_HEIGHT))

    # Move the players as per the keypress
    move_player(player1, pygame.key.get_pressed(), controls1, player1_pos)
    move_player(player2, pygame.key.get_pressed(), controls2, player2_pos)

    # Move the ball
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Hitting the paddle with the ball
    player1_rect = pygame.Rect(player1_pos[0], player1_pos[1], PLAYER_WIDTH, PLAYER_HEIGHT)
    player2_rect = pygame.Rect(player2_pos[0], player2_pos[1], PLAYER_WIDTH, PLAYER_HEIGHT)
    ball_rect = pygame.Rect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, ball_radius * 2, ball_radius * 2)

    # Updating speed when ball touches player's paddle
    if player1_rect.colliderect(ball_rect) and ball_speed[0] < 0:
        ball_speed[0] *= -1.10
        paddle_sound.play()
    elif player2_rect.colliderect(ball_rect) and ball_speed[0] > 0:
        ball_speed[0] *= -1.10
        paddle_sound.play()

    # Ball bouncing off top and bottom
    if ball_pos[1] - ball_radius < 0 or ball_pos[1] + ball_radius > SCREEN_HEIGHT:
        ball_speed[1] *= -1.10
        wall_sound.play()

    # Display scores
    score_text = font.render("{}    {}".format(player1_score, player2_score), True, (200, 200, 200))
    text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
    screen.blit(score_text, text_rect)

    # Goal scored
    if ball_pos[0] - ball_radius < 0:
        player2_score += 1
        ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        last_scored = 2
        goal_sound.play()
        # Decide initial direction of ball for next 'round'
        if last_scored == 1:
            ball_speed = [0.15, -0.15]
        else:
            ball_speed = [-0.15, 0.15]
    elif ball_pos[0] + ball_radius > SCREEN_WIDTH:  # Ball hits right wall
        player1_score += 1
        ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        last_scored = 1
        goal_sound.play()
        if last_scored == 1:
            ball_speed = [0.15, -0.15]
        else:
            ball_speed = [-0.15, 0.15]

    # Draw the players
    pygame.draw.rect(screen, (255, 0, 0),
                     pygame.Rect(round(player1_pos[0]), round(player1_pos[1]), PLAYER_WIDTH, PLAYER_HEIGHT))
    pygame.draw.rect(screen, (0, 255, 0),
                     pygame.Rect(round(player2_pos[0]), round(player2_pos[1]), PLAYER_WIDTH, PLAYER_HEIGHT))

    # Draw the ball
    pygame.draw.circle(screen, ball_colour, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    # Refresh the display
    pygame.display.update()
