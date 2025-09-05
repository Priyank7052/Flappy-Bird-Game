import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 250)
PIPE_GREEN = (0, 200, 0)
BIRD_YELLOW = (255, 230, 0)
GROUND_BROWN = (210, 105, 30)
ORANGE = (255, 140, 0)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird - Easy Mode")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Fonts
font = pygame.font.SysFont("Arial", 32, bold=True)


class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.radius = 18
        self.velocity = 0
        self.gravity = 0.35   # smoother fall
        self.jump_strength = -7  # smoother jump

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def jump(self):
        self.velocity = self.jump_strength

    def draw(self):
        # Bird body
        pygame.draw.circle(screen, BIRD_YELLOW, (self.x, int(self.y)), self.radius)
        # Eye
        pygame.draw.circle(screen, WHITE, (self.x + 8, int(self.y) - 5), 5)
        pygame.draw.circle(screen, BLACK, (self.x + 8, int(self.y) - 5), 2)
        # Beak
        pygame.draw.polygon(screen, ORANGE, [(self.x + self.radius, int(self.y)),
                                             (self.x + self.radius + 10, int(self.y) - 5),
                                             (self.x + self.radius + 10, int(self.y) + 5)])


class Pipe:
    def __init__(self, x):
        self.width = 70
        self.gap = 190  # wider gap = easier
        self.x = x
        self.height = random.randint(100, SCREEN_HEIGHT - self.gap - GROUND_HEIGHT)
        self.speed = 2  # slower pipes = easier

    def update(self):
        self.x -= self.speed

    def draw(self):
        # Top pipe
        pygame.draw.rect(screen, PIPE_GREEN, (self.x, 0, self.width, self.height))
        # Bottom pipe
        pygame.draw.rect(screen, PIPE_GREEN, (self.x, self.height + self.gap, self.width, SCREEN_HEIGHT))

    def collide(self, bird):
        if (bird.x + bird.radius > self.x and bird.x - bird.radius < self.x + self.width):
            if (bird.y - bird.radius < self.height) or (bird.y + bird.radius > self.height + self.gap):
                return True
        return False


def game_over_screen(score):
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER!", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = font.render("Press SPACE to Restart", True, WHITE)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 250))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 300))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


def main():
    bird = Bird()
    pipes = [Pipe(300)]
    score = 0

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(SKY_BLUE)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        # Update bird
        bird.update()

        # Update pipes
        for pipe in pipes:
            pipe.update()
            if pipe.x + pipe.width < 0:
                pipes.remove(pipe)
                pipes.append(Pipe(SCREEN_WIDTH))
                score += 1

        # Collision detection
        for pipe in pipes:
            if pipe.collide(bird):
                game_over_screen(score)
                main()
                return

        if bird.y + bird.radius > SCREEN_HEIGHT - GROUND_HEIGHT or bird.y - bird.radius < 0:
            game_over_screen(score)
            main()
            return

        # Draw objects
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        # Ground
        pygame.draw.rect(screen, GROUND_BROWN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

        # Score
        score_text = font.render(str(score), True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH // 2, 20))

        # Update display
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

