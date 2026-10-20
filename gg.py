import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_W, PADDLE_H = 15, 100
BALL_SIZE = 15

player = pygame.Rect(30, HEIGHT // 2 - PADDLE_H // 2, PADDLE_W, PADDLE_H)
enemy = pygame.Rect(WIDTH - 30 - PADDLE_W, HEIGHT // 2 - PADDLE_H // 2, PADDLE_W, PADDLE_H)

ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_speed_x = 5
ball_speed_y = 5

player_score = 0
enemy_score = 0
font = pygame.font.SysFont("Arial", 40)

PADDLE_SPEED = 7
ENEMY_SPEED = 5


def reset_ball(direction):
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = 5 * direction
    ball_speed_y = 5 if ball_speed_y > 0 else -5


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player.top > 0:
        player.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player.bottom < HEIGHT:
        player.y += PADDLE_SPEED

    if enemy.centery < ball.centery and enemy.bottom < HEIGHT:
        enemy.y += ENEMY_SPEED
    if enemy.centery > ball.centery and enemy.top > 0:
        enemy.y -= ENEMY_SPEED

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    if ball.colliderect(player) and ball_speed_x < 0:
        ball_speed_x *= -1
        ball.left = player.right

    if ball.colliderect(enemy) and ball_speed_x > 0:
        ball_speed_x *= -1
        ball.right = enemy.left

    if ball.left <= 0:
        enemy_score += 1
        reset_ball(1)
    if ball.right >= WIDTH:
        player_score += 1
        reset_ball(-1)

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, enemy)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    score_text = font.render(f"{player_score}   {enemy_score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()