"""
管道鸟 (Flappy Bird) - Python + Pygame
点击空格让小鸟飞翔，穿越管道获取分数。
"""
import pygame
import random
import sys

# Constants
W, H = 400, 600
FPS = 60
GRAVITY = 0.45
FLAP_VEL = -7.5
PIPE_WIDTH = 52
PIPE_GAP = 140
PIPE_SPEED = 2.2
PIPE_SPAWN_FRAMES = 90
BIRD_X = 80
BIRD_SIZE = 18
GROUND_H = 40

# Colors
SKY_TOP = (78, 192, 232)
SKY_BOT = (200, 232, 192)
PIPE_BODY = (74, 140, 63)
PIPE_LIP = (92, 168, 74)
PIPE_LIP_DARK = (61, 114, 53)
GROUND_COLOR = (212, 168, 96)
GROUND_LINE = (122, 92, 48)
BIRD_COLOR = (245, 212, 66)
BIRD_BELLY = (250, 232, 155)
BIRD_WING = (224, 184, 48)
BEAK_COLOR = (240, 128, 48)
GAME_OVER_COLOR = (255, 96, 96)


class Bird:
    def __init__(self):
        self.y = H / 2
        self.vel = 0

    def flap(self):
        self.vel = FLAP_VEL

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel

    @property
    def rect(self):
        return pygame.Rect(BIRD_X - BIRD_SIZE, self.y - BIRD_SIZE,
                           BIRD_SIZE * 2, BIRD_SIZE * 2)

    def draw(self, surface):
        x, y = int(BIRD_X), int(self.y)
        angle = max(min(self.vel * 0.08, 0.8), -0.5)

        # Simple bird drawing without rotation for clarity
        # Body
        pygame.draw.circle(surface, BIRD_COLOR, (x, y), BIRD_SIZE)
        # Belly
        pygame.draw.circle(surface, BIRD_BELLY, (x - 3, y + 4), int(BIRD_SIZE * 0.6))
        # Eye
        pygame.draw.circle(surface, (255, 255, 255), (x + 8, y - 4), 6)
        pygame.draw.circle(surface, (0, 0, 0), (x + 10, y - 4), 3)
        # Beak
        pts = [(x + 16, y), (x + 24, y + 2), (x + 16, y + 6)]
        pygame.draw.polygon(surface, BEAK_COLOR, pts)
        # Wing
        wing_rect = pygame.Rect(x - 10, y - 2, 14, 8)
        pygame.draw.ellipse(surface, BIRD_WING, wing_rect)


class Pipe:
    def __init__(self, x):
        self.x = x
        min_y, max_y = 80, H - PIPE_GAP - 80
        self.top_h = random.randint(min_y, max_y)
        self.scored = False

    def update(self):
        self.x -= PIPE_SPEED

    def offscreen(self):
        return self.x < -PIPE_WIDTH

    @property
    def top_rect(self):
        return pygame.Rect(self.x, 0, PIPE_WIDTH, self.top_h)

    @property
    def bottom_rect(self):
        bot_y = self.top_h + PIPE_GAP
        return pygame.Rect(self.x, bot_y + 26, PIPE_WIDTH, H - bot_y - 26)

    @property
    def score_zone(self):
        return self.x + PIPE_WIDTH < BIRD_X

    def draw(self, surface):
        # Top pipe
        pygame.draw.rect(surface, PIPE_BODY, self.top_rect)
        lip_rect = pygame.Rect(self.x - 3, self.top_h - 26, PIPE_WIDTH + 6, 26)
        pygame.draw.rect(surface, PIPE_LIP, lip_rect)
        pygame.draw.rect(surface, PIPE_LIP_DARK, (self.x - 3, self.top_h - 26, PIPE_WIDTH + 6, 6))

        # Bottom pipe
        bot_y = self.top_h + PIPE_GAP
        lip_rect_bot = pygame.Rect(self.x - 3, bot_y, PIPE_WIDTH + 6, 26)
        pygame.draw.rect(surface, PIPE_LIP, lip_rect_bot)
        pygame.draw.rect(surface, PIPE_LIP_DARK, (self.x - 3, bot_y + 20, PIPE_WIDTH + 6, 6))
        pygame.draw.rect(surface, PIPE_BODY, self.bottom_rect)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((W, H))
        pygame.display.set_caption("🐤 管道鸟 · Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 22)
        self.reset()

    def reset(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.best = 0
        self.running = True
        self.started = False
        self.frame = 0

    def flap(self):
        if not self.running:
            self.reset()
            return
        if not self.started:
            self.started = True
            self.frame = PIPE_SPAWN_FRAMES - 15
        self.bird.flap()

    def update(self):
        if not self.started or not self.running:
            return
        self.frame += 1

        self.bird.update()

        # Spawn pipes
        if self.frame % PIPE_SPAWN_FRAMES == 0:
            self.pipes.append(Pipe(W))

        # Update pipes
        for p in self.pipes:
            p.update()
        self.pipes = [p for p in self.pipes if not p.offscreen()]

        # Score
        for p in self.pipes:
            if not p.scored and p.score_zone:
                p.scored = True
                self.score += 1

        # Collisions
        bird_rect = self.bird.rect
        # Ground / ceiling
        if self.bird.y + BIRD_SIZE > H - GROUND_H or self.bird.y - BIRD_SIZE < 0:
            self.die()
            return
        # Pipes
        for p in self.pipes:
            if bird_rect.colliderect(p.top_rect) or bird_rect.colliderect(p.bottom_rect):
                self.die()
                return

    def die(self):
        self.running = False
        if self.score > self.best:
            self.best = self.score

    def draw(self):
        # Sky gradient
        for i in range(H):
            t = i / H
            r = int(SKY_TOP[0] + (SKY_BOT[0] - SKY_TOP[0]) * t)
            g = int(SKY_TOP[1] + (SKY_BOT[1] - SKY_TOP[1]) * t)
            b = int(SKY_TOP[2] + (SKY_BOT[2] - SKY_TOP[2]) * t)
            pygame.draw.line(self.screen, (r, g, b), (0, i), (W, i))

        # Clouds
        for cx, cy, s in [(60, 80, 24), (200, 50, 18), (320, 100, 20)]:
            for dx, dy, r in [(0, 0, s), (25, -6, s-4), (20, 8, s-5), (-8, 4, s-4)]:
                pygame.draw.circle(self.screen, (255, 255, 255, 150), (cx+dx, cy+dy), r)

        # Pipes
        for p in self.pipes:
            p.draw(self.screen)

        # Ground
        pygame.draw.rect(self.screen, GROUND_COLOR, (0, H - GROUND_H, W, GROUND_H))
        pygame.draw.rect(self.screen, GROUND_LINE, (0, H - GROUND_H, W, 4))

        # Bird
        self.bird.draw(self.screen)

        # Score
        score_text = self.font.render(str(self.score), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(W // 2, 50))
        pygame.draw.rect(self.screen, (50, 50, 50, 150), score_rect.inflate(20, 10))
        self.screen.blit(score_text, score_rect)

        # Overlays
        if not self.started and self.running:
            overlay = pygame.Surface((W, H))
            overlay.set_alpha(100)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            txt = self.font.render("点击或按空格起飞", True, (255, 255, 255))
            self.screen.blit(txt, txt.get_rect(center=(W//2, H//2 - 20)))
            txt2 = self.font_small.render("躲开管道，飞得越远越好！", True, (220, 220, 220))
            self.screen.blit(txt2, txt2.get_rect(center=(W//2, H//2 + 20)))

        if not self.running:
            overlay = pygame.Surface((W, H))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            txt = self.font.render("游戏结束", True, GAME_OVER_COLOR)
            self.screen.blit(txt, txt.get_rect(center=(W//2, H//2 - 30)))
            txt2 = self.font_small.render(f"得分: {self.score}    最佳: {self.best}", True, (255, 255, 255))
            self.screen.blit(txt2, txt2.get_rect(center=(W//2, H//2 + 10)))
            txt3 = self.font_small.render("按空格或点击重新开始", True, (200, 200, 200))
            self.screen.blit(txt3, txt3.get_rect(center=(W//2, H//2 + 40)))

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        self.flap()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.flap()

            self.update()
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()
