import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 30
BALL_RADIUS = 30
DISTANCE_BETWEEN_BALLS = 100
TEXT_MARGIN = 50

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128), (0, 255, 255), (255, 192, 203), (0, 128, 0), (128, 128, 0)]
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лопни шарик!")
font = pygame.font.Font(None, 74)

def create_balls(num_balls):
    balls = []
    while len(balls) < num_balls:
        color = random.choice(colors)
        letter = random.choice(letters)
        if letter not in [b[3] for b in balls]:
            x = random.randint(BALL_RADIUS + 10, WIDTH - BALL_RADIUS - 10)
            y = random.randint(BALL_RADIUS + TEXT_MARGIN + 10, HEIGHT - BALL_RADIUS - 10)
            if (all((abs(x-bx) >= DISTANCE_BETWEEN_BALLS or abs(y - by) >= DISTANCE_BETWEEN_BALLS) for bx, by, _, _, _, _ in balls)):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 9)
                balls.append((x, y, color, letter, angle, speed))
    return balls

def move_balls(balls):
    for i in range(len(balls)):
        x, y, color, letter, angle, speed = balls[i]
        x += speed * math.cos(angle)
        y += speed * math.sin(angle)
        if x < BALL_RADIUS or x > WIDTH - BALL_RADIUS:
            angle = math.pi - angle
        if y < BALL_RADIUS + TEXT_MARGIN or y > HEIGHT - BALL_RADIUS:
            angle = -angle
        balls[i] = (x, y, color, letter, angle, speed)

def main():
    clock = pygame.time.Clock()
    running = True
    target_letter = random.choice(letters)
    balls = create_balls(len(letters))
    score = 0
    time_limit = 10
    start_time = pygame.time.get_ticks()

    while running:
        screen.fill((255,240,245))
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        remaining_time = max(0, time_limit - elapsed_time)

        target_text = font.render(f"Лопни: {target_letter}", True, (0, 0, 0))
        time_text = font.render(f"Время: {int(remaining_time)}", True, (0, 0, 0))
        score_text = font.render(f"Очки: {score}", True, (0, 0, 0))

        screen.blit(target_text, (WIDTH // 2 - target_text.get_width() // 2, 20))
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 100))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 180))

        move_balls(balls)

        for ball in balls:
            x, y, color, letter, angle, speed = ball
            pygame.draw.circle(screen, color, (int(x), int(y)), BALL_RADIUS)
            text_surface = font.render(letter, True, (255, 255, 255))
            screen.blit(text_surface, (x - text_surface.get_width() // 2, y - text_surface.get_height() // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for ball in balls[:]:
                    x, y, color, letter, _, _ = ball
                    if (x - BALL_RADIUS < mouse_x < x + BALL_RADIUS) and (y - BALL_RADIUS < mouse_y < y + BALL_RADIUS):
                        if letter == target_letter:
                            score += 15
                        else:
                            score -= 15
                        balls = create_balls(len(letters))
                        target_letter = random.choice(letters)
                        start_time = pygame.time.get_ticks()

        if remaining_time <= 0:
            score -= 20
            balls = create_balls(len(letters))
            target_letter = random.choice(letters)
            start_time = pygame.time.get_ticks()

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
