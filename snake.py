import tkinter as tk
import random
import time

CELL = 20
COLUMNS = 30
ROWS = 20
DELAY = 100

class SnakeGame:
    def __init__(self, master):
        self.master = master
        master.title('Snake - 貪食蛇')

        self.width = CELL * COLUMNS
        self.height = CELL * ROWS

        self.canvas = tk.Canvas(
            master,
            width=self.width,
            height=self.height,
            bg='black'
        )
        self.canvas.pack()

        master.bind('<Key>', self.on_key)

        self.reset()
        self.loop()

    def reset(self):
        self.direction = 'Right'
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
            return

        self.snake.append(new)

        if new == self.food:
            self.score += 1
            self.place_food()
        else:
            self.snake.pop(0)

        self.elapsed = int(time.time() - self.start_time)

    def draw(self):
        self.canvas.delete('all')

        # 🍎 蘋果
        self.draw_apple(*self.food)

        # 🐍 蛇
        for i, (x, y) in enumerate(self.snake):
            if i == len(self.snake) - 1:
                self.draw_snake_head(x, y)
            else:
                self.draw_snake_body(x, y)

        # 分數 + 時間
        self.canvas.create_text(
            10, 5,
            fill='white',
            anchor='nw',
            text=f"Score: {self.score}   Time: {self.elapsed}s"
        )

        if self.game_over:
            self.canvas.create_text(
                self.width // 2,
                self.height // 2,
                fill='white',
                text='GAME OVER\nR: Restart  Q: Quit',
                font=('Helvetica', 24),
                justify='center'
            )

    # ===== 繪圖 =====

    def draw_apple(self, x, y):
        cx = x * CELL + CELL // 2
        cy = y * CELL + CELL // 2

        # 蘋果本體
        self.canvas.create_oval(
            cx - 8, cy - 8,
            cx + 8, cy + 8,
            fill='red', outline=''
        )

        # 葉子
        self.canvas.create_oval(
            cx + 2, cy - 12,
            cx + 10, cy - 4,
            fill='green', outline=''
        )

    def draw_snake_body(self, x, y):
        x1 = x * CELL
        y1 = y * CELL
        x2 = x1 + CELL
        y2 = y1 + CELL
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill='#4CAF50', outline=''
        )

    def draw_snake_head(self, x, y):
        x1 = x * CELL
        y1 = y * CELL
        x2 = x1 + CELL
        y2 = y1 + CELL

        # 頭
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill='#2E7D32', outline=''
        )

        # 眼睛
        self.canvas.create_oval(
            x1 + 5, y1 + 5,
            x1 + 8, y1 + 8,
            fill='white', outline=''
        )
        self.canvas.create_oval(
            x1 + 12, y1 + 5,
            x1 + 15, y1 + 8,
            fill='white', outline=''
        )

    def loop(self):
        self.step()
        self.draw()
        if not self.game_over:
            self.master.after(DELAY, self.loop)

if __name__ == '__main__':
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()
