from colorama import init


def render_empty_board (width, height):
    board = [[EMPTY for _ in range(width)] for _ in range(height)]
    return board

def draw_board (board):
    for row in board:
        print(''.join(row))


class snake (object):
    def __init__(self):
        self.body = init.body
        self.direction = init.direction

    def head (self):
        return self.body[0]

    def step (self):
        head = self.body[0]
        if self.direction == 'up':
            new_head = (head[0], head[1] - 1)
        elif self.direction == 'down':
            new_head = (head[0], head[1] + 1)
        elif self.direction == 'left':
            new_head = (head[0] - 1, head[1])
        elif self.direction == 'right':
            new_head = (head[0] + 1, head[1])
        self.body.insert(0, new_head)
        self.body.pop()

    def grow (self, position):
        self.body.append(position)

    def set_dir (self, direction):
        self.direction = direction

class Apple (object):

class Game (object):
    def __init__ (self, width, height):
        self.width = width
        self.height = height
        self.board = render_empty_board(width, height)
        self.snake = snake()
        self.apple = Apple()


if __name__ == "__main__":
    Game()