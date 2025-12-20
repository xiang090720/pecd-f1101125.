import tkinter as tk
import random

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
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg='black')
        self.canvas.pack()
        self.score = 0
        self.reset()
        master.bind('<Key>', self.on_key)
        self.running = True
        self.after_id = None
        self.draw()
        self.loop()

    def reset(self):
        self.direction = 'Right'
        mid_x = COLUMNS // 2
        mid_y = ROWS // 2
        self.snake = [(mid_x-1, mid_y), (mid_x, mid_y), (mid_x+1, mid_y)]
        self.place_food()
        self.score = 0
        self.game_over = False

    def place_food(self):
        empty = [(x,y) for x in range(COLUMNS) for y in range(ROWS) if (x,y) not in self.snake]
        self.food = random.choice(empty) if empty else None

    def on_key(self, event):
        key = event.keysym
        if key in ('Up','Down','Left','Right'):
            opposites = {'Up':'Down','Down':'Up','Left':'Right','Right':'Left'}
            if opposites.get(key) != self.direction:
                self.direction = key
        elif key in ('r','R') and self.game_over:
            self.reset()
            self.running = True
            self.loop()
        elif key in ('q','Q'):
            self.master.quit()

    def step(self):
        if self.game_over:
            return
        head = self.snake[-1]
        x,y = head
        move = {'Up':(0,-1),'Down':(0,1),'Left':(-1,0),'Right':(1,0)}[self.direction]
        new = (x+move[0], y+move[1])
        if not (0 <= new[0] < COLUMNS and 0 <= new[1] < ROWS) or new in self.snake:
            self.game_over = True
            return
        self.snake.append(new)
        if self.food and new == self.food:
            self.score += 1
            self.place_food()
        else:
            self.snake.pop(0)

    def draw(self):
        self.canvas.delete('all')
        # draw food
        if self.food:
            x,y = self.food
            self._draw_cell(x,y, fill='red')
        # draw snake
        for i,(x,y) in enumerate(self.snake):
            color = 'green' if i < len(self.snake)-1 else 'lime'
            self._draw_cell(x,y, fill=color)
        # score
        self.canvas.create_text(60, 10, fill='white', text=f'Score: {self.score}', anchor='nw')
        if self.game_over:
            self.canvas.create_text(self.width//2, self.height//2, fill='white', text='Game Over\nPress R to restart', font=('Helvetica', 24), justify='center')

    def _draw_cell(self, x, y, fill='white'):
        x1 = x * CELL
        y1 = y * CELL
        x2 = x1 + CELL
        y2 = y1 + CELL
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline='')

    def loop(self):
        self.step()
        self.draw()
        if not self.game_over:
            self.after_id = self.master.after(DELAY, self.loop)
        else:
            self.running = False

if __name__ == '__main__':
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
