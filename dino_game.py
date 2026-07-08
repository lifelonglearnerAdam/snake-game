"""
小恐龙跑酷 (Dino Runner) - Python + Pygame
躲避障碍物，跑得越远分数越高！
"""
import pygame
import random
import sys

# Constants
W, H = 700, 300
FPS = 60
GROUND_Y = 240
GRAVITY = 0.7
JUMP_VEL = -12

# Colors
BG = (247, 247, 247)
GROUND_LINE = (83, 83, 83)
DINO_COLOR = (83, 83, 83)
TEXT_COLOR = (83, 83, 83)
OVERLAY_COLOR = (255, 255, 255)


class Dino:
    def __init__(self):
        self.y = GROUND_Y
        self.vel = 0
        self.on_ground = True
        self.ducking = False

    def jump(self):
        if self.on_ground:
            self.vel = JUMP_VEL
            self.on_ground = False

    def duck(self, is_down):
        self.ducking = is_down and self.on_ground

    def update(self):
        if not self.on_ground:
            self.vel += GRAVITY
            self.y += self.vel
            if self.y >= GROUND_Y:
                self.y = GROUND_Y
                self.vel = 0
                self.on_ground = True

    @property
    def rect(self):
        if self.ducking and self.on_ground:
            return pygame.Rect(50, self.y - 30, 44, 30)
        return pygame.Rect(50, self.y - 44, 28, 44)

    def draw(self, surface, frame_count):
        x, y = 50, int(self.y)
        if self.ducking and self.on_ground:
            self._draw_duck(surface, x, y)
        else:
            self._draw_standing(surface, x, y, frame_count)

    def _draw_standing(self, surface, x, y, frame_count):
        top = y - 44
        # Body
        pygame.draw.rect(surface, DINO_COLOR, (x + 10, top + 8, 18, 24))
        # Head
        pygame.draw.rect(surface, DINO_COLOR, (x + 18, top, 16, 14))
        # Eye
        pygame.draw.rect(surface, (255, 255, 255), (x + 26, top + 4, 4, 4))
        pygame.draw.rect(surface, DINO_COLOR, (x + 28, top + 5, 2, 2))
        # Mouth
        pygame.draw.rect(surface, DINO_COLOR, (x + 30, top + 10, 8, 2))
        # Legs
        if self.on_ground:
            phase = (frame_count // 4) % 2
            pygame.draw.rect(surface, DINO_COLOR, (x + 10, top + 32, 6, 12))
            pygame.draw.rect(surface, DINO_COLOR, (x + 18, top + 32, 6, 8 if phase else 12))
            pygame.draw.rect(surface, DINO_COLOR, (x + 24, top + 32, 4, 12 if phase else 8))
        else:
            pygame.draw.rect(surface, DINO_COLOR, (x + 14, top + 32, 4, 8))
            pygame.draw.rect(surface, DINO_COLOR, (x + 20, top + 28, 4, 8))
        # Arm
        pygame.draw.rect(surface, DINO_COLOR, (x + 6, top + 14, 6, 3))
        # Tail
        pygame.draw.rect(surface, DINO_COLOR, (x, top + 12, 12, 4))
        pygame.draw.rect(surface, DINO_COLOR, (x - 2, top + 10, 4, 2))

    def _draw_duck(self, surface, x, y):
        top = y - 30
        pygame.draw.rect(surface, DINO_COLOR, (x, top, 44, 16))
        pygame.draw.rect(surface, (255, 255, 255), (x + 32, top + 4, 4, 4))
        pygame.draw.rect(surface, DINO_COLOR, (x + 34, top + 5, 2, 2))
        pygame.draw.rect(surface, DINO_COLOR, (x + 8, top + 16, 6, 10))
        pygame.draw.rect(surface, DINO_COLOR, (x + 30, top + 16, 6, 10))


class Obstacle:
    def __init__(self, x, speed):
        self.x = x
        r = random.random()
        if r < 0.65:
            # Cactus
            h = random.randint(25, 45)
            self.type = 'cactus'
            self.w = 16
            self.h = h
            self.y = GROUND_Y - h
            self.seed = random.randint(0, 2)
        else:
            # Bird
            self.type = 'bird'
            self.w = 30
            self.h = 20
            self.y = GROUND_Y - 35 - random.randint(0, 40)
            self.seed = 0

    def update(self, speed):
        self.x -= speed

    def offscreen(self):
        return self.x < -50

    @property
    def rect(self):
        if self.type == 'cactus':
            return pygame.Rect(self.x + 4, GROUND_Y - self.h, self.w - 8, self.h)
        return pygame.Rect(self.x + 4, self.y, self.w - 8, self.h - 4)

    def draw(self, surface, frame_count):
        if self.type == 'cactus':
            self._draw_cactus(surface)
        else:
            self._draw_bird(surface, frame_count)

    def _draw_cactus(self, surface):
        x, y = int(self.x), int(GROUND_Y - self.h)
        pygame.draw.rect(surface, DINO_COLOR, (x + 4, y + 4, 8, self.h - 4))
        if self.seed == 0:
            pygame.draw.rect(surface, DINO_COLOR, (x + 12, y + self.h * 0.3, 6, 4))
            pygame.draw.rect(surface, DINO_COLOR, (x + 14, y + self.h * 0.3 - 8, 4, 8))
        elif self.seed == 1:
            pygame.draw.rect(surface, DINO_COLOR, (x - 6, y + self.h * 0.5, 6, 4))
            pygame.draw.rect(surface, DINO_COLOR, (x - 6, y + self.h * 0.5 - 8, 4, 8))
        pygame.draw.rect(surface, DINO_COLOR, (x + 4, y, 8, 4))

    def _draw_bird(self, surface, frame_count):
        x, y = int(self.x), int(self.y)
        phase = (frame_count // 6) % 2
        pygame.draw.rect(surface, DINO_COLOR, (x, y + 6, 30, 8))
        pygame.draw.rect(surface, DINO_COLOR, (x + 24, y + 4, 8, 4))
        if phase == 0:
            pygame.draw.rect(surface, DINO_COLOR, (x + 10, y, 10, 8))
        else:
            pygame.draw.rect(surface, DINO_COLOR, (x + 10, y + 12, 10, 8))


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((W, H))
        pygame.display.set_caption("🦖 小恐龙跑酷 · Dino Runner")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.font_score = pygame.font.Font(None, 20)
        pygame.font.Font(None, 22)
        self.reset()

    def reset(self):
        self.dino = Dino()
        self.obstacles = []
        self.score = 0
        self.best = 0
        self.running = True
        self.started = False
        self.speed = 5
        self.frame = 0

    def update(self):
        if not self.running or not self.started:
            return
        self.frame += 1

        # Increase speed
        self.speed = min(14, 5 + (self.score // 300) * 0.8)

        self.dino.update()

        # Spawn obstacles
        spawn_gap = max(40, int(110 - self.score / 30))
        if self.frame % spawn_gap == 0:
            self.obstacles.append(Obstacle(W, self.speed))

        # Update obstacles
        for o in self.obstacles:
            o.update(self.speed)
        self.obstacles = [o for o in self.obstacles if not o.offscreen()]

        self.score += 1

        # Collision
        dino_rect = self.dino.rect
        for o in self.obstacles:
            if dino_rect.colliderect(o.rect):
                self.die()
                return

    def die(self):
        self.running = False
        if self.score > self.best:
            self.best = self.score

    def draw(self):
        self.screen.fill(BG)

        # Ground line
        pygame.draw.line(self.screen, GROUND_LINE, (0, GROUND_Y), (W, GROUND_Y))
        # Ground dots
        dot_offset = (self.frame * int(self.speed)) % 20
        for x in range(-dot_offset, W, 20):
            pygame.draw.rect(self.screen, (170, 170, 170), (x, GROUND_Y + 8, 3, 3))

        # Obstacles
        for o in self.obstacles:
            o.draw(self.screen, self.frame)

        # Dino
        self.dino.draw(self.screen, self.frame)

        # Score
        score_str = str(self.score // 10).zfill(5)
        score_surf = self.font_score.render(score_str, True, TEXT_COLOR)
        self.screen.blit(score_surf, (W - 80, 20))

        # Best
        best_str = f"HI {str(self.best // 10).zfill(5)}"
        best_surf = self.font_score.render(best_str, True, (170, 170, 170))
        self.screen.blit(best_surf, (W - 180, 20))

        # Start overlay
        if not self.started and self.running:
            overlay = pygame.Surface((W, H))
            overlay.set_alpha(130)
            overlay.fill(BG)
            self.screen.blit(overlay, (0, 0))
            txt = self.font.render("按空格键或 ↑ 开始游戏", True, TEXT_COLOR)
            self.screen.blit(txt, txt.get_rect(center=(W//2, H//2 - 10)))

        # Game over
        if not self.running:
            overlay = pygame.Surface((W, H))
            overlay.set_alpha(180)
            overlay.fill(BG)
            self.screen.blit(overlay, (0, 0))
            txt = self.font.render("游戏结束", True, TEXT_COLOR)
            self.screen.blit(txt, txt.get_rect(center=(W//2, H//2 - 30)))
            txt2 = pygame.font.Font(None, 18).render(
                f"得分: {self.score // 10}    最佳: {self.best // 10}", True, TEXT_COLOR
            )
            self.screen.blit(txt2, txt2.get_rect(center=(W//2, H//2 + 5)))
            txt3 = pygame.font.Font(None, 16).render(
                "按空格或 ↑ 重新开始", True, (150, 150, 150)
            )
            self.screen.blit(txt3, txt3.get_rect(center=(W//2, H//2 + 32)))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    if not self.running:
                        self.reset()
                    else:
                        if not self.started:
                            self.started = True
                        self.dino.jump()
                if event.key == pygame.K_DOWN:
                    self.dino.duck(True)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.dino.duck(False)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.running:
                    self.reset()
                else:
                    if not self.started:
                        self.started = True
                    self.dino.jump()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()
