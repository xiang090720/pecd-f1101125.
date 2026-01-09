import tkinter as tk
import random
import time
import os

# ===== 基本設定 =====
CELL = 20
COLUMNS = 30
ROWS = 20
DELAY = 100
HIGHSCORE_FILE = "highscore.txt"

# ⚡ 皮卡丘主題色
BG_COLOR = "#FFF59D"
SNAKE_BODY_COLOR = "#FFD54F"
SNAKE_HEAD_COLOR = "#FBC02D"
TEXT_COLOR = "#5D4037"

class SnakeGame:
    def __init__(self, master):
        self.master = master
        master.title("⚡ Pikachu Snake")

        self.width = CELL * COLUMNS
        self.height = CELL * ROWS

        self.canvas = tk.Canvas(
            master,
            width=self.width,
            height=self.height,
            bg=BG_COLOR
        )
        self.canvas.pack()

        master.bind("<Key>", self.on_key)

        self.highscore = self.load_highscore()
        self.reset()
        self.loop()

    # ===== 高分處理 =====
    def load_highscore(self):
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, "r") as f:
                    return int(f.read())
            except:
                return 0
        return 0

    def save_highscore(self):
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(self.highscore))

    # ===== 遊戲初始化 =====
    def reset(self):
        self.direction = "Right"
        mx = COLUMNS // 2
        my = ROWS // 2

        self.snake = [(mx - 1, my), (mx, my), (mx + 1, my)]
        self.place_food()

        self.score = 0
        self.game_over = False
        self.start_time = time.time()
        self.elapsed = 0

    def place_food(self):
        empty = [
            (x, y)
            for x in range(COLUMNS)
            for y in range(ROWS)
            if (x, y) not in self.snake
        ]
        self.food = random.choice(empty)

    # ===== 操作 =====
    def on_key(self, event):
        key = event.keysym
        opposites = {'Up':'Down','Down':'Up','Left':'Right','Right':'Left'}

        if key in opposites and opposites[key] != self.direction:
            self.direction = key
        elif key in ('r','R') and self.game_over:
            self.reset()
            self.loop()
        elif key in ('q','Q'):
            self.master.quit()

    # ===== 遊戲邏輯 =====
    def step(self):
        if self.game_over:
            return

        x, y = self.snake[-1]
        dx, dy = {
            'Up': (0, -1),
            'Down': (0, 1),
            'Left': (-1, 0),
            'Right': (1, 0)
        }[self.direction]

        new = (x + dx, y + dy)

        if (
            not (0 <= new[0] < COLUMNS and 0 <= new[1] < ROWS)
            or new in self.snake
        ):
            self.game_over = True
            if self.score > self.highscore:
                self.highscore = self.score
                self.save_highscore()
            return

        self.snake.append(new)

        if new == self.food:
            self.score += 1
            self.place_food()
        else:
            self.snake.pop(0)

        self.elapsed = int(time.time() - self.start_time)

    # ===== 畫面 =====
    def draw(self):
        self.canvas.delete("all")

        # 🍎 蘋果（皮卡丘風）
        self.draw_apple(*self.food)

        # 🐍 蛇
        for i, (x, y) in enumerate(self.snake):
            if i == len(self.snake) - 1:
                self.draw_head(x, y)
            else:
                self.draw_body(x, y)

        # 📊 UI
        self.canvas.create_text(
            10, 5,
            anchor="nw",
            fill=TEXT_COLOR,
            font=("Arial", 12, "bold"),
            text=f"Score: {self.score}   High: {self.highscore}   Time: {self.elapsed}s"
        )

        if self.game_over:
            self.canvas.create_text(
                self.width // 2,
                self.height // 2,
                fill=TEXT_COLOR,
                font=("Helvetica", 24, "bold"),
                justify="center",
                text="GAME OVER ⚡\nR: Restart   Q: Quit"
            )

    # ===== 繪圖元件 =====
    def draw_body(self, x, y):
        self.canvas.create_rectangle(
            x*CELL, y*CELL,
            x*CELL+CELL, y*CELL+CELL,
            fill=SNAKE_BODY_COLOR, outline=""
        )

    def draw_head(self, x, y):
        x1 = x*CELL
        y1 = y*CELL
        x2 = x1+CELL
        y2 = y1+CELL

        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=SNAKE_HEAD_COLOR, outline=""
        )

        # 眼睛
        self.canvas.create_oval(x1+5, y1+6, x1+8, y1+9, fill="black")
        self.canvas.create_oval(x1+12, y1+6, x1+15, y1+9, fill="black")

    def draw_apple(self, x, y):
        cx = x * CELL + CELL // 2
        cy = y * CELL + CELL // 2

        # 蘋果本體
        self.canvas.create_oval(
            cx - 8, cy - 8,
            cx + 8, cy + 8,
            fill="red", outline=""
        )

        # 葉子
        self.canvas.create_oval(
            cx + 2, cy - 12,
            cx + 10, cy - 4,
            fill="green", outline=""
        )

        # ⚡ 能量符號
        self.canvas.create_polygon(
            cx - 2, cy - 4,
            cx + 2, cy - 1,
            cx - 1, cy - 1,
            cx + 3, cy + 5,
            cx - 3, cy + 1,
            cx + 1, cy + 1,
            fill="#FFEB3B",
            outline=""
        )

    def loop(self):
        self.step()
        self.draw()
        if not self.game_over:
            self.master.after(DELAY, self.loop)

if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()
