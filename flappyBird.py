import pygame
import sys
import random

# ---------- Config (tweak these to change difficulty) ----------
WIDTH, HEIGHT = 400, 600
GROUND_H = 100

# Game feel (pixels/second, seconds)
PIPE_SPEED = 100        # lower = easier
PIPE_GAP   = 220        # bigger = easier
SPAWN_EVERY = 1.6       # seconds between pipe spawns
GRAVITY    = 1200       # px/s^2
JUMP_VEL   = -300       # px/s

# Colors
SKY = (135, 206, 250)
PIPE = (46, 204, 113)
GROUND = (210, 105, 30)
BIRD = (255, 221, 0)
BIRD_BEAK = (255, 140, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Bird:
    def __init__(self):
        self.x = 60
        self.y = HEIGHT // 2
        self.r = 16
        self.vy = 0.0

    def flap(self):
        self.vy = JUMP_VEL

    def update(self, dt):
        self.vy += GRAVITY * dt
        self.y  += self.vy * dt
        # Clamp at top
        if self.y < self.r:
            self.y = self.r
            self.vy = 0

    def rect(self):
        return pygame.Rect(self.x - self.r, int(self.y - self.r), self.r * 2, self.r * 2)

    def draw(self, surf):
        pygame.draw.circle(surf, BIRD, (self.x, int(self.y)), self.r)
        # Eye
        pygame.draw.circle(surf, WHITE, (self.x + 6, int(self.y) - 5), 4)
        pygame.draw.circle(surf, BLACK, (self.x + 6, int(self.y) - 5), 2)
        # Beak
        pygame.draw.polygon(
            surf,
            BIRD_BEAK,
            [(self.x + self.r, int(self.y)),
             (self.x + self.r + 10, int(self.y) - 5),
             (self.x + self.r + 10, int(self.y) + 5)]
        )


class PipePair:
    WIDTH = 70

    def __init__(self, x):
        self.x = x
        max_top = HEIGHT - GROUND_H - PIPE_GAP - 100
        self.top_h = random.randint(80, max(80, max_top))
        self.passed = False

    def update(self, dt):
        self.x -= PIPE_SPEED * dt

    def offscreen(self):
        return self.x + self.WIDTH < 0

    def collide(self, bird_rect):
        top_rect = pygame.Rect(self.x, 0, self.WIDTH, self.top_h)
        bot_rect = pygame.Rect(self.x, self.top_h + PIPE_GAP, self.WIDTH, HEIGHT - (self.top_h + PIPE_GAP))
        return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bot_rect)

    def draw(self, surf):
        # Top
        pygame.draw.rect(surf, PIPE, (self.x, 0, self.WIDTH, self.top_h))
        # Bottom
        pygame.draw.rect(surf, PIPE, (self.x, self.top_h + PIPE_GAP, self.WIDTH, HEIGHT - (self.top_h + PIPE_GAP)))


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird - Smooth Easy Mode")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.Font(None, 56)
        self.font = pygame.font.Font(None, 36)
        self.reset()
        self.state = "menu"   # "menu" -> "play" -> "over"

    def reset(self):
        self.bird = Bird()
        self.pipes = []
        self.spawn_timer = 0.0
        self.score = 0

    def spawn_pipe(self):
        x = WIDTH + 10
        self.pipes.append(PipePair(x))

    def handle_input(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()

            if self.state == "menu":
                if e.type == pygame.KEYDOWN and e.key in (pygame.K_SPACE, pygame.K_UP):
                    self.state = "play"
                    self.reset()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self.state = "play"
                    self.reset()

            elif self.state == "play":
                if (e.type == pygame.KEYDOWN and e.key in (pygame.K_SPACE, pygame.K_UP)) or e.type == pygame.MOUSEBUTTONDOWN:
                    self.bird.flap()

            elif self.state == "over":
                if e.type == pygame.KEYDOWN and e.key in (pygame.K_SPACE, pygame.K_UP):
                    self.state = "menu"
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self.state = "menu"

    def update(self, dt):
        if self.state != "play":
            return

        self.bird.update(dt)

        # Spawn pipes
        self.spawn_timer += dt
        if self.spawn_timer >= SPAWN_EVERY:
            self.spawn_timer -= SPAWN_EVERY
            self.spawn_pipe()

        # Move pipes & score
        for p in list(self.pipes):
            p.update(dt)
            if not p.passed and p.x + p.WIDTH < self.bird.x:
                p.passed = True
                self.score += 1
            if p.offscreen():
                self.pipes.remove(p)

        # Collisions
        if self.bird.y + self.bird.r > HEIGHT - GROUND_H:
            self.state = "over"
        else:
            brect = self.bird.rect()
            for p in self.pipes:
                if p.collide(brect):
                    self.state = "over"
                    break

    def draw_background(self):
        self.screen.fill(SKY)
        # simple "clouds"
        t = pygame.time.get_ticks() / 1000.0
        for i, y in enumerate((90, 140, 190)):
            x = (WIDTH - (t * (20 + i * 10)) % (WIDTH + 60)) - 60
            pygame.draw.ellipse(self.screen, (255, 255, 255), (x, y, 80, 30))
            pygame.draw.ellipse(self.screen, (255, 255, 255), (x + 25, y - 10, 60, 35))

    def draw_ground(self):
        pygame.draw.rect(self.screen, GROUND, (0, HEIGHT - GROUND_H, WIDTH, GROUND_H))

    def draw_score(self):
        txt = self.font_big.render(str(self.score), True, BLACK)
        self.screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 30))

    def draw_menu(self):
        title = self.font_big.render("Flappy Bird", True, BLACK)
        sub = self.font.render("Press SPACE or Click to start", True, BLACK)
        help1 = self.font.render("Tap SPACE / Click to flap", True, BLACK)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 170))
        self.screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 230))
        self.screen.blit(help1, (WIDTH // 2 - help1.get_width() // 2, 270))

    def draw_over(self):
        over = self.font_big.render("Game Over", True, BLACK)
        sc = self.font.render(f"Score: {self.score}", True, BLACK)
        sub = self.font.render("Press SPACE or Click", True, BLACK)
        self.screen.blit(over, (WIDTH // 2 - over.get_width() // 2, 170))
        self.screen.blit(sc, (WIDTH // 2 - sc.get_width() // 2, 230))
        self.screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, 270))

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000.0  # seconds
            self.handle_input()
            self.update(dt)

            # Draw
            self.draw_background()
            for p in self.pipes:
                p.draw(self.screen)
            self.bird.draw(self.screen)
            self.draw_ground()

            if self.state == "play":
                self.draw_score()
            elif self.state == "menu":
                self.draw_menu()
            elif self.state == "over":
                self.draw_over()

            pygame.display.flip()


if __name__ == "__main__":
    Game().run()
