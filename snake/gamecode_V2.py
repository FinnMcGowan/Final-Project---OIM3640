import random
import tkinter as tk


class Snake:
    def __init__(self, body, direction="right"):
        self.body = body
        self.direction = direction
        self.pending_growth = 0

    def head(self):
        return self.body[0]

    def set_dir(self, direction):
        opposites = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left",
        }
        if direction in opposites and direction != opposites[self.direction]:
            self.direction = direction

    def next_head(self):
        x, y = self.head()
        if self.direction == "up":
            return (x, y - 1)
        if self.direction == "down":
            return (x, y + 1)
        if self.direction == "left":
            return (x - 1, y)
        return (x + 1, y)

    def grow(self):
        self.pending_growth += 1

    def step(self):
        self.body.insert(0, self.next_head())
        if self.pending_growth > 0:
            self.pending_growth -= 1
        else:
            self.body.pop()


class Apple:
    def __init__(self):
        self.position = (0, 0)

    def respawn(self, width, height, snake_body):
        all_cells = [(x, y) for y in range(height) for x in range(width)]
        open_cells = [cell for cell in all_cells if cell not in snake_body]
        if not open_cells:
            self.position = None
            return
        self.position = random.choice(open_cells)


class Game:
    def __init__(self, width=20, height=12):
        self.width = width
        self.height = height
        self.game_over = False
        self.score = 0
        self.snake = None
        self.apple = Apple()
        self.reset()

    def reset(self):
        center_x = self.width // 2
        center_y = self.height // 2
        body = [
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y),
        ]
        self.snake = Snake(body=body, direction="right")
        self.apple.respawn(self.width, self.height, self.snake.body)
        self.score = 0
        self.game_over = False

    def in_bounds(self, pos):
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def collides_with_self(self, new_head, is_eating):
        if is_eating:
            body_to_check = self.snake.body
        else:
            body_to_check = self.snake.body[:-1]
        return new_head in body_to_check

    def step(self):
        if self.game_over:
            return

        new_head = self.snake.next_head()
        is_eating = self.apple.position is not None and new_head == self.apple.position

        if not self.in_bounds(new_head) or self.collides_with_self(new_head, is_eating):
            self.game_over = True
            return

        if is_eating:
            self.snake.grow()
            self.score += 1

        self.snake.step()

        if is_eating:
            self.apple.respawn(self.width, self.height, self.snake.body)
            if self.apple.position is None:
                self.game_over = True

class SnakeApp:
    def __init__(self, width=20, height=12, cell_size=28, tick_ms=120):
        self.game = Game(width=width, height=height)
        self.cell_size = cell_size
        self.tick_ms = tick_ms

        self.window = tk.Tk()
        self.window.title("Snake Game")
        self.window.resizable(False, False)

        board_px_width = self.game.width * self.cell_size
        board_px_height = self.game.height * self.cell_size

        self.score_label = tk.Label(
            self.window,
            text="Score: 0",
            font=("Segoe UI", 12, "bold"),
            pady=8,
        )
        self.score_label.pack()

        self.canvas = tk.Canvas(
            self.window,
            width=board_px_width,
            height=board_px_height,
            bg="#1f2937",
            highlightthickness=2,
            highlightbackground="#0f172a",
        )
        self.canvas.pack(padx=12, pady=(0, 12))

        self.message_label = tk.Label(
            self.window,
            text="Use Arrow Keys or WASD. Press R to restart.",
            font=("Segoe UI", 10),
            pady=2,
        )
        self.message_label.pack()

        self.window.bind("<KeyPress>", self.on_key_press)
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)

    def on_key_press(self, event):
        key = event.keysym.lower()
        direction_map = {
            "up": "up",
            "down": "down",
            "left": "left",
            "right": "right",
            "w": "up",
            "s": "down",
            "a": "left",
            "d": "right",
        }

        if key in direction_map:
            self.game.snake.set_dir(direction_map[key])
        elif key == "r":
            self.game.reset()
        elif key in ("q", "escape"):
            self.window.destroy()

    def draw_board(self):
        self.canvas.delete("all")

        for y in range(self.game.height):
            for x in range(self.game.width):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    outline="#111827",
                    fill="#111827",
                )

        if self.game.apple.position is not None:
            ax, ay = self.game.apple.position
            x1 = ax * self.cell_size + 5
            y1 = ay * self.cell_size + 5
            x2 = (ax + 1) * self.cell_size - 5
            y2 = (ay + 1) * self.cell_size - 5
            self.canvas.create_oval(x1, y1, x2, y2, fill="#ef4444", outline="")

        for idx, (x, y) in enumerate(self.game.snake.body):
            x1 = x * self.cell_size + 2
            y1 = y * self.cell_size + 2
            x2 = (x + 1) * self.cell_size - 2
            y2 = (y + 1) * self.cell_size - 2
            color = "#34d399" if idx == 0 else "#10b981"
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

        self.score_label.config(text=f"Score: {self.game.score}")

        if self.game.game_over:
            width = self.game.width * self.cell_size
            height = self.game.height * self.cell_size
            self.canvas.create_rectangle(
                0,
                height // 2 - 35,
                width,
                height // 2 + 35,
                fill="#000000",
                stipple="gray25",
                outline="",
            )
            self.canvas.create_text(
                width // 2,
                height // 2,
                text="Game Over - Press R to restart",
                fill="white",
                font=("Segoe UI", 14, "bold"),
            )

    def game_loop(self):
        if not self.game.game_over:
            self.game.step()
        self.draw_board()
        self.window.after(self.tick_ms, self.game_loop)

    def run(self):
        self.draw_board()
        self.game_loop()
        self.window.mainloop()


if __name__ == "__main__":
    SnakeApp().run()