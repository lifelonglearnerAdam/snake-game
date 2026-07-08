# 🎮 经典游戏合集

三个经典街机游戏，纯网页实现，手机电脑都能玩！

👉 **在线游玩**: [https://lifelonglearneradam.github.io/snake-game/](https://lifelonglearneradam.github.io/snake-game/)

---

## 🎯 游戏列表

### 🐍 贪吃蛇 · 八大地图版 — [snake.html](snake.html)

经典贪吃蛇，包含 8 张不同地图，支持方向键、WASD 操控，手机端有虚拟方向键。

**🖥️ 电脑操作**

| 按键 | 功能 |
|------|------|
| ↑ ↓ ← → / WASD | 控制方向 |
| 空格 | 按住加速 |
| P | 暂停/继续 |
| Tab | 切换地图 |
| R | 重新开始 |

**📱 手机操作**：屏幕下方有虚拟方向键 + 加速键 + 换地图/重来按钮

**🗺️ 八大地图**

| # | 地图 | 描述 |
|---|------|------|
| 1 | 🟢 经典模式 | 空旷场地，无障碍物，适合新手练习 |
| 2 | 🏗️ 迷宫模式 | 十字迷宫布局，通道狭窄，考验走位 |
| 3 | 🟫 四柱模式 | 四角各有 3×3 柱子障碍 |
| 4 | 🔄 回廊模式 | 环形走廊结构，内外两圈围墙 |
| 5 | ✚ 十字封锁 | 中央十字墙分割为四象限，仅留小口 |
| 6 | 🏁 棋盘模式 | 棋盘状 2×2 方块阵列，蛇形走位 |
| 7 | 🚇 隧道模式 | 上下障碍墙 + 左右边界，仅中间隧道可通 |
| 8 | 💎 散点模式 | 随机散布的单独石块，密度适中 |

---

### 🐤 管道鸟 · Flappy Bird — [flappy.html](flappy.html)

Flappy Bird 经典复刻，点击或空格让小鸟飞翔，穿越管道获取分数。

| 电脑 | 手机 |
|------|------|
| 空格 / ↑ / 鼠标点击 → 飞行 | 点击屏幕任意位置 → 飞行 |

---

### 🦖 小恐龙 · Dino Runner — [dino.html](dino.html)

Chrome Dino 跑酷，跳跃躲避仙人掌和飞鸟，速度越来越快。

| 电脑 | 手机 |
|------|------|
| 空格 / ↑ / 点击 → 跳跃 | 点击 → 跳跃 |
| ↓ → 蹲下 | 长按 → 蹲下 |

---

## 🐍 Python 桌面版

也提供了 Python + Pygame 桌面版：

```bash
pip install pygame
python snake_game.py    # 贪吃蛇
python flappy_bird.py   # 管道鸟
python dino_game.py     # 小恐龙
```

## 📁 项目结构

```
├── index.html        # 🎮 游戏大厅（入口）
├── snake.html        # 🐍 贪吃蛇 · 八大地图版
├── flappy.html       # 🐤 管道鸟
├── dino.html         # 🦖 小恐龙
├── snake_game.py     # 贪吃蛇 Python 版
├── flappy_bird.py    # 管道鸟 Python 版
├── dino_game.py      # 小恐龙 Python 版
└── README.md
```

---

🔗 **GitHub**: [github.com/lifelonglearnerAdam/snake-game](https://github.com/lifelonglearnerAdam/snake-game)
