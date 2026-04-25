from flask import Flask, jsonify, render_template, request

from snake.gamecode_V3 import SnakeBackend
from tetris.gamecode_v1 import TetrisBackend

app = Flask(__name__)
snake_backend = SnakeBackend(width=16, height=12)
tetris_backend = TetrisBackend(width=10, height=20)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/snake')
def snake():
    state = snake_backend.state()
    return render_template('snake.html', board=state['board'], width=state['width'], height=state['height'])


@app.get('/api/snake/state')
def snake_state():
    return jsonify(snake_backend.state())


@app.post('/api/snake/direction')
def snake_direction():
    payload = request.get_json(silent=True) or {}
    direction = payload.get('direction', '')
    if direction not in {'up', 'down', 'left', 'right'}:
        return jsonify({'error': 'Invalid direction'}), 400
    snake_backend.set_direction(direction)
    return jsonify(snake_backend.state())


@app.post('/api/snake/tick')
def snake_tick():
    snake_backend.tick()
    return jsonify(snake_backend.state())


@app.post('/api/snake/reset')
def snake_reset():
    snake_backend.reset()
    return jsonify(snake_backend.state())

@app.route('/timer')
def timer():
    return render_template('timer.html')

@app.route('/tetris')
def tetris():
    state = tetris_backend.state()
    return render_template('tetris.html', board=state['board'], width=state['width'], height=state['height'])


@app.get('/api/tetris/state')
def tetris_state():
    return jsonify(tetris_backend.state())


@app.post('/api/tetris/direction')
def tetris_direction():
    payload = request.get_json(silent=True) or {}
    direction = payload.get('direction', '')
    allowed = {'left', 'right', 'soft_drop', 'hard_drop', 'rotate_cw', 'rotate_ccw', 'hold'}
    if direction not in allowed:
        return jsonify({'error': 'Invalid direction'}), 400
    tetris_backend.set_direction(direction)
    return jsonify(tetris_backend.state())


@app.post('/api/tetris/tick')
def tetris_tick():
    tetris_backend.tick()
    return jsonify(tetris_backend.state())


@app.post('/api/tetris/reset')
def tetris_reset():
    tetris_backend.reset()
    return jsonify(tetris_backend.state())

if __name__ == '__main__':
    app.run(debug=True)
