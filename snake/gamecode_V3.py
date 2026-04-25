import random


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
    def __init__(self, width=16, height=12):
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


class SnakeBackend:
    def __init__(self, width=16, height=12):
        self.game = Game(width=width, height=height)

    def set_direction(self, direction):
        self.game.snake.set_dir(direction)

    def tick(self):
        self.game.step()

    def reset(self):
        self.game.reset()

    def state(self):
        snake_cells = set(self.game.snake.body)
        apple = self.game.apple.position
        board = [
            [
                "snake" if (x, y) in snake_cells else "apple" if apple == (x, y) else "empty"
                for x in range(self.game.width)
            ]
            for y in range(self.game.height)
        ]
        return {
            "width": self.game.width,
            "height": self.game.height,
            "board": board,
            "score": self.game.score,
            "game_over": self.game.game_over,
            "direction": self.game.snake.direction,
        }
