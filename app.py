from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/snake')
def snake():
    width, height = 16, 12
    snake_positions = {(5, 6), (6, 6), (7, 6), (8, 6)}
    apple_position = (10, 4)
    board = [
        [
            'snake' if (x, y) in snake_positions else 'apple' if (x, y) == apple_position else 'empty'
            for x in range(width)
        ]
        for y in range(height)
    ]
    return render_template('snake.html', board=board, width=width, height=height)

@app.route('/timer')
def timer():
    return render_template('timer.html')

@app.route('/tetris')
def tetris():
    return render_template('tetris.html')

if __name__ == '__main__':
    app.run(debug=True)
