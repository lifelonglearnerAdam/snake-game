"""
贪吃蛇游戏 - Python + Pygame
使用方向键控制蛇的移动，吃到食物得分，撞墙或撞到自己则游戏结束。
"""

import pygame
import random
from enum import Enum
from collections import deque

# ============================================================
# 常量配置
# ============================================================
CELL_SIZE = 20          # 每个格子的像素大小
GRID_WIDTH = 30         # 网格宽度（格子数）
GRID_HEIGHT = 20        # 网格高度（格子数）
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10                # 帧率（控制蛇的速度）
BOOST_FPS = int(FPS * 1.5)  # 按住空格加速时的帧率

# 颜色
COLOR_BG = (20, 20, 30)
COLOR_GRID = (35, 35, 50)
COLOR_SNAKE_HEAD = (80, 200, 80)
COLOR_SNAKE_BODY = (60, 160, 60)
COLOR_FOOD = (220, 60, 60)
COLOR_SCORE = (180, 180, 180)
COLOR_GAME_OVER = (255, 80, 80)
COLOR_RESTART = (150, 150, 150)
COLOR_OBSTACLE = (80, 80, 100)
COLOR_OBSTACLE_BORDER = (120, 120, 140)
COLOR_BOOST = (255, 200, 50)


# ============================================================
# 地图定义
# ============================================================
def _make_classic_map():
    """经典模式 — 空旷无阻碍"""
    return set()


def _make_maze_map():
    """迷宫模式 — 墙体迷宫"""
    obstacles = set()
    # 横墙
    for x in range(4, 26):
        if x not in (14, 15):       # 留两个缺口
            obstacles.add((x, 5))
    for x in range(4, 26):
        if x not in (14, 15):
            obstacles.add((x, 14))
    # 竖墙
    for y in range(2, 18):
        if y not in (9, 10):
            obstacles.add((9, y))
    for y in range(2, 18):
        if y not in (9, 10):
            obstacles.add((21, y))
    return obstacles


def _make_pillars_map():
    """四柱模式 — 四角的方块"""
    obstacles = set()
    pillars = [
        (4, 2), (22, 2),   # 上方两柱
        (4, 14), (22, 14),  # 下方两柱
    ]
    for px, py in pillars:
        for dx in range(3):
            for dy in range(3):
                obstacles.add((px + dx, py + dy))
    return obstacles


def _make_corridor_map():
    """回廊模式 — 环形走廊"""
    obstacles = set()
    # 外圈围墙
    for x in range(GRID_WIDTH):
        obstacles.add((x, 1))
        obstacles.add((x, GRID_HEIGHT - 2))
    for y in range(2, GRID_HEIGHT - 2):
        obstacles.add((2, y))
        obstacles.add((GRID_WIDTH - 3, y))
    # 内圈围墙
    for x in range(6, GRID_WIDTH - 6):
        obstacles.add((x, 5))
        obstacles.add((x, GRID_HEIGHT - 6))
    for y in range(6, GRID_HEIGHT - 6):
        obstacles.add((6, y))
        obstacles.add((GRID_WIDTH - 7, y))
    # 开一些口
    gaps = [
        (0, 1), (14, 1), (29, 1),
        (0, 18), (14, 18), (29, 18),
        (2, 3), (2, 9), (2, 16),
        (27, 3), (27, 9), (27, 16),
        (9, 5), (20, 5), (9, 14), (20, 14),
    ]
    for gx, gy in gaps:
        obstacles.discard((gx, gy))
    return obstacles


MAPS = [
    {"name": "经典模式", "obstacles": _make_classic_map()},
    {"name": "迷宫模式", "obstacles": _make_maze_map()},
    {"name": "四柱模式", "obstacles": _make_pillars_map()},
    {"name": "回廊模式", "obstacles": _make_corridor_map()},
]


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Snake:
    """蛇的类，管理蛇的身体、移动和碰撞检测。"""

    def __init__(self):
        # 蛇身存储在双端队列中，头部在右侧
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        self.body = deque([
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y),
        ])
        self.direction = Direction.RIGHT
        self.growing = False

    @property
    def head(self):
        return self.body[0]

    def set_direction(self, new_dir: Direction):
        """更改方向，禁止直接反向（防止蛇穿自己）。"""
        # 不允许反向
        opposites = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        if new_dir != opposites[self.direction]:
            self.direction = new_dir

    def move(self) -> bool:
        """
        移动蛇一步。
        返回 True 表示移动成功，False 表示撞到自己。
        """
        dx, dy = self.direction.value
        new_head = (
            (self.head[0] + dx) % GRID_WIDTH,
            (self.head[1] + dy) % GRID_HEIGHT,
        )

        # 检查撞到自己（不含尾部，因为尾部即将移除，除非在生长中）
        body_to_check = list(self.body)
        if not self.growing:
            body_to_check = body_to_check[:-1]
        if new_head in body_to_check:
            return False

        self.body.appendleft(new_head)

        if self.growing:
            self.growing = False
        else:
            self.body.pop()

        return True

    def grow(self):
        """标记蛇下一次移动时生长一节。"""
        self.growing = True

    def draw(self, surface):
        """在给定的 pygame surface 上绘制蛇。"""
        for i, segment in enumerate(self.body):
            x = segment[0] * CELL_SIZE
            y = segment[1] * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (0, 0, 0, 40), rect, 1)  # 半透明边框

            # 给头部画上眼睛
            if i == 0:
                self._draw_eyes(surface, x, y)

    def _draw_eyes(self, surface, x, y):
        """给蛇头画上两只小眼睛。"""
        eye_size = 4
        eye_offset = 5
        eye_y = y + CELL_SIZE // 2 - eye_offset

        if self.direction == Direction.RIGHT:
            left_eye = (x + CELL_SIZE - 8, eye_y)
            right_eye = (x + CELL_SIZE - 8, y + eye_offset + 3)
        elif self.direction == Direction.LEFT:
            left_eye = (x + 8, eye_y)
            right_eye = (x + 8, y + eye_offset + 3)
        elif self.direction == Direction.UP:
            left_eye = (x + eye_offset, y + 8)
            right_eye = (x + CELL_SIZE - eye_offset - 3, y + 8)
        else:  # DOWN
            left_eye = (x + eye_offset, y + CELL_SIZE - 8)
            right_eye = (x + CELL_SIZE - eye_offset - 3, y + CELL_SIZE - 8)

        pygame.draw.circle(surface, (255, 255, 255), left_eye, eye_size)
        pygame.draw.circle(surface, (255, 255, 255), right_eye, eye_size)
        # 瞳孔
        pygame.draw.circle(surface, (0, 0, 0), left_eye, 2)
        pygame.draw.circle(surface, (0, 0, 0), right_eye, 2)


class Food:
    """食物类，在随机空位生成。"""

    def __init__(self):
        self.position = (0, 0)
        self.pulse = 0  # 用于动画效果

    def spawn(self, occupied: set, obstacles: set):
        """在未被占用的位置随机生成食物（避开蛇身和障碍物）。"""
        all_positions = {
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
        }
        available = all_positions - occupied - obstacles
        if available:
            self.position = random.choice(list(available))
        else:
            self.position = None  # 胜利状态

    def draw(self, surface):
        """绘制食物，带呼吸动画。"""
        if self.position is None:
            return

        self.pulse = (self.pulse + 1) % 60
        scale = 1.0 + 0.15 * (1 if self.pulse < 30 else -1) * (self.pulse % 30) / 30

        cx = self.position[0] * CELL_SIZE + CELL_SIZE // 2
        cy = self.position[1] * CELL_SIZE + CELL_SIZE // 2
        r = int(CELL_SIZE // 2 * scale)

        pygame.draw.circle(surface, COLOR_FOOD, (cx, cy), r)
        # 高光
        highlight_r = max(2, r // 3)
        pygame.draw.circle(surface, (255, 180, 180), (cx - r // 3, cy - r // 3), highlight_r)


class Game:
    """游戏主控类，管理游戏循环和状态。"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🐍 贪吃蛇 · 多地图版")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 22)
        self.quit = False
        self.speed_boost = False
        self.current_map = 0
        self.obstacles = set()
        self.reset()

    def reset(self):
        """重置游戏状态。"""
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.running = True
        self.paused = False
        self.speed_boost = False
        self.obstacles = MAPS[self.current_map]["obstacles"]
        self._spawn_food()

    def _spawn_food(self):
        occupied = set(self.snake.body)
        self.food.spawn(occupied, self.obstacles)

    def handle_events(self):
        """处理所有输入事件。"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit = True

                elif self.running:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.snake.set_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.snake.set_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.snake.set_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.snake.set_direction(Direction.RIGHT)
                    elif event.key == pygame.K_SPACE:
                        self.speed_boost = True
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_TAB:
                        self.current_map = (self.current_map + 1) % len(MAPS)
                        self.reset()
                else:
                    if event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_TAB:
                        self.current_map = (self.current_map + 1) % len(MAPS)
                        self.reset()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.speed_boost = False

    def update(self):
        """更新游戏逻辑。"""
        if self.paused:
            return

        # 移动蛇
        if not self.snake.move():
            self.running = False  # 撞到自己
            return

        head = self.snake.head

        # 检查撞到障碍物
        if head in self.obstacles:
            self.running = False
            return

        # 检查吃到食物
        if head == self.food.position:
            self.snake.grow()
            self.score += 10
            self._spawn_food()

            # 食物吃完（胜利）
            if self.food.position is None:
                self.running = False

    def draw(self):
        """渲染整个画面。"""
        self.screen.fill(COLOR_BG)

        # 绘制网格线
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (0, y), (WINDOW_WIDTH, y))

        # 绘制障碍物
        for ox, oy in self.obstacles:
            rect = pygame.Rect(ox * CELL_SIZE, oy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, COLOR_OBSTACLE, rect)
            pygame.draw.rect(self.screen, COLOR_OBSTACLE_BORDER, rect, 1)

        # 绘制游戏对象
        self.food.draw(self.screen)
        self.snake.draw(self.screen)

        # 顶栏：分数 + 地图名
        map_info = MAPS[self.current_map]
        score_text = self.font.render(f"得分: {self.score}", True, COLOR_SCORE)
        self.screen.blit(score_text, (10, 8))

        map_text = self.font_small.render(f"地图: {map_info['name']}", True, COLOR_SCORE)
        map_rect = map_text.get_rect(midtop=(WINDOW_WIDTH // 2, 10))
        self.screen.blit(map_text, map_rect)

        # 加速提示
        if self.speed_boost:
            boost_text = self.font_small.render("⚡ 加速中", True, COLOR_BOOST)
            self.screen.blit(boost_text, (10, 36))

        # 底部操作提示
        hint_text = self.font_small.render(
            "方向键/WASD 移动 | 空格 加速 | P 暂停 | Tab 换地图",
            True, (100, 100, 110),
        )
        hint_rect = hint_text.get_rect(midbottom=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 6))
        self.screen.blit(hint_text, hint_rect)

        # 暂停提示
        if self.paused:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            pause_text = self.font.render("⏸ 已暂停", True, COLOR_SCORE)
            pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 10))
            self.screen.blit(pause_text, pause_rect)
            hint = self.font_small.render("按 P 继续", True, COLOR_RESTART)
            hint_rect = hint.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 25))
            self.screen.blit(hint, hint_rect)

        pygame.display.flip()

    def draw_game_over(self):
        """绘制游戏结束画面。"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(190)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        over_text = self.font.render("💀 游戏结束", True, COLOR_GAME_OVER)
        over_rect = over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        self.screen.blit(over_text, over_rect)

        map_info = MAPS[self.current_map]
        info_text = self.font_small.render(
            f"地图: {map_info['name']}　　最终得分: {self.score}",
            True, COLOR_SCORE,
        )
        info_rect = info_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(info_text, info_rect)

        restart_text = self.font_small.render(
            "按 R 重新开始 | Tab 换地图 | ESC 退出",
            True, COLOR_RESTART,
        )
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
        self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self):
        """主游戏循环。"""
        while not self.quit:
            self.handle_events()

            if not self.running:
                self.draw_game_over()
                self.clock.tick(FPS)
                continue

            self.update()

            if not self.running:
                continue

            self.draw()
            current_fps = BOOST_FPS if self.speed_boost else FPS
            self.clock.tick(current_fps)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
