import os
import random
import sys
import time


EMPTY = " "
SNAKE_HEAD = "@"
SNAKE_BODY = "O"
APPLE = "*"


def render_empty_board(width, height):
    return [[EMPTY for _ in range(width)] for _ in range(height)]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


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
    def __init__(self, width=20, height=12, tick_seconds=0.12):
        self.width = width
        self.height = height
        self.tick_seconds = tick_seconds
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

    def render_board(self):
        board = render_empty_board(self.width, self.height)

        if self.apple.position is not None:
            ax, ay = self.apple.position
            board[ay][ax] = APPLE

        for idx, (x, y) in enumerate(self.snake.body):
            board[y][x] = SNAKE_HEAD if idx == 0 else SNAKE_BODY
        return board

    def draw(self):
        clear_screen()
        board = self.render_board()

        print("+" + "-" * self.width + "+")
        for row in board:
            print("|" + "".join(row) + "|")
        print("+" + "-" * self.width + "+")
        print(f"Score: {self.score}")
        if self.game_over:
            print("Game Over! Press R to restart or Q to quit.")

    def handle_input(self):
        if os.name == "nt":
            self._handle_input_windows()
        else:
            pass

    def _handle_input_windows(self):
        try:
            import msvcrt
        except ImportError:
            return

        while msvcrt.kbhit():
            key = msvcrt.getch()

            if key in (b"\xe0", b"\x00"):
                arrow = msvcrt.getch()
                mapping = {
                    b"H": "up",
                    b"P": "down",
                    b"K": "left",
                    b"M": "right",
                }
                if arrow in mapping:
                    self.snake.set_dir(mapping[arrow])
                continue

            lower = key.lower()
            if lower == b"w":
                self.snake.set_dir("up")
            elif lower == b"s":
                self.snake.set_dir("down")
            elif lower == b"a":
                self.snake.set_dir("left")
            elif lower == b"d":
                self.snake.set_dir("right")
            elif lower == b"q":
                print("Quitting game.")
                sys.exit(0)
            elif lower == b"r" and self.game_over:
                self.reset()

    def run(self):
        while True:
            self.draw()
            self.handle_input()
            if not self.game_over:
                self.step()
            time.sleep(self.tick_seconds)


if __name__ == "__main__":
    Game().run()