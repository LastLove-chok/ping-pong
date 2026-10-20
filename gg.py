import pygame
import sys

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("circus.ogg")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_W, PADDLE_H = 15, 100
BALL_SIZE = 15

player_y = float(HEIGHT // 2 - PADDLE_H // 2)
enemy_y = float(HEIGHT // 2 - PADDLE_H // 2)

player = pygame.Rect(30, int(player_y), PADDLE_W, PADDLE_H)
enemy = pygame.Rect(WIDTH - 30 - PADDLE_W, int(enemy_y), PADDLE_W, PADDLE_H)

ball_x = float(WIDTH // 2 - BALL_SIZE // 2)
ball_y = float(HEIGHT // 2 - BALL_SIZE // 2)
ball_rect = pygame.Rect(int(ball_x), int(ball_y), BALL_SIZE, BALL_SIZE)

BALL_SPEED_X = 550.0
BALL_SPEED_Y = 550.0
ball_speed_x = BALL_SPEED_X
ball_speed_y = BALL_SPEED_Y

player_score = 0
enemy_score = 0
font = pygame.font.SysFont("Arial", 40)

PADDLE_SPEED = 800.0
ENEMY_SPEED = 550.0


def reset_ball(direction):
    global ball_x, ball_y, ball_speed_x, ball_speed_y
    ball_x = WIDTH / 2 - BALL_SIZE / 2
    ball_y = HEIGHT / 2 - BALL_SIZE / 2
    ball_speed_x = BALL_SPEED_X * direction
    ball_speed_y = BALL_SPEED_Y if ball_speed_y > 0 else -BALL_SPEED_Y


running = True
while running:
    dt = clock.tick(240) / 1000.0
    if dt > 0.05:
        dt = 0.05

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_y -= PADDLE_SPEED * dt
    if keys[pygame.K_s]:
        player_y += PADDLE_SPEED * dt
    player_y = max(0.0, min(HEIGHT - PADDLE_H, player_y))
    player.y = int(player_y)

    enemy_center = enemy_y + PADDLE_H / 2
    ball_center = ball_y + BALL_SIZE / 2
    if enemy_center < ball_center:
        enemy_y += ENEMY_SPEED * dt
    elif enemy_center > ball_center:
        enemy_y -= ENEMY_SPEED * dt
    enemy_y = max(0.0, min(HEIGHT - PADDLE_H, enemy_y))
    enemy.y = int(enemy_y)

    ball_x += ball_speed_x * dt
    ball_y += ball_speed_y * dt
    ball_rect.x = int(ball_x)
    ball_rect.y = int(ball_y)

    if ball_y <= 0:
        ball_y = 0.0
        ball_speed_y = abs(ball_speed_y)
    elif ball_y + BALL_SIZE >= HEIGHT:
        ball_y = float(HEIGHT - BALL_SIZE)
        ball_speed_y = -abs(ball_speed_y)

    if ball_rect.colliderect(player) and ball_speed_x < 0:
        ball_speed_x = abs(ball_speed_x)
        ball_x = float(player.right)

    if ball_rect.colliderect(enemy) and ball_speed_x > 0:
        ball_speed_x = -abs(ball_speed_x)
        ball_x = float(enemy.left - BALL_SIZE)

    if ball_x + BALL_SIZE < 0:
        enemy_score += 1
        reset_ball(1)
    elif ball_x > WIDTH:
        player_score += 1
        reset_ball(-1)

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, enemy)
    pygame.draw.ellipse(screen, WHITE, ball_rect)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    score_text = font.render(f"{player_score}   {enemy_score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    pygame.display.flip()

pygame.quit()
sys.exit()