from __future__ import annotations

import random
from dataclasses import dataclass


DEFAULT_WIDTH = 10
DEFAULT_HEIGHT = 20


PIECE_SHAPES = {
	# Coordinates are in a 4x4 local grid.
	"I": [
		{(0, 1), (1, 1), (2, 1), (3, 1)},
		{(2, 0), (2, 1), (2, 2), (2, 3)},
		{(0, 2), (1, 2), (2, 2), (3, 2)},
		{(1, 0), (1, 1), (1, 2), (1, 3)},
	],
	"O": [
		{(1, 0), (2, 0), (1, 1), (2, 1)},
		{(1, 0), (2, 0), (1, 1), (2, 1)},
		{(1, 0), (2, 0), (1, 1), (2, 1)},
		{(1, 0), (2, 0), (1, 1), (2, 1)},
	],
	"T": [
		{(1, 0), (0, 1), (1, 1), (2, 1)},
		{(1, 0), (1, 1), (2, 1), (1, 2)},
		{(0, 1), (1, 1), (2, 1), (1, 2)},
		{(1, 0), (0, 1), (1, 1), (1, 2)},
	],
	"S": [
		{(1, 0), (2, 0), (0, 1), (1, 1)},
		{(1, 0), (1, 1), (2, 1), (2, 2)},
		{(1, 1), (2, 1), (0, 2), (1, 2)},
		{(0, 0), (0, 1), (1, 1), (1, 2)},
	],
	"Z": [
		{(0, 0), (1, 0), (1, 1), (2, 1)},
		{(2, 0), (1, 1), (2, 1), (1, 2)},
		{(0, 1), (1, 1), (1, 2), (2, 2)},
		{(1, 0), (0, 1), (1, 1), (0, 2)},
	],
	"J": [
		{(0, 0), (0, 1), (1, 1), (2, 1)},
		{(1, 0), (2, 0), (1, 1), (1, 2)},
		{(0, 1), (1, 1), (2, 1), (2, 2)},
		{(1, 0), (1, 1), (0, 2), (1, 2)},
	],
	"L": [
		{(2, 0), (0, 1), (1, 1), (2, 1)},
		{(1, 0), (1, 1), (1, 2), (2, 2)},
		{(0, 1), (1, 1), (2, 1), (0, 2)},
		{(0, 0), (1, 0), (1, 1), (1, 2)},
	],
}

SCORE_BY_LINES = {
	0: 0,
	1: 100,
	2: 300,
	3: 500,
	4: 800,
}


@dataclass
class Piece:
	piece_type: str
	x: int
	y: int
	rotation: int = 0


class TetrisBackend:
	def __init__(self, width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT):
		self.width = width
		self.height = height
		self.board = self.create_empty_board(width, height)
		self.score = 0
		self.game_over = False
		self.held_piece_type: str | None = None
		self.hold_used_this_turn = False
		self.active_piece: Piece | None = None
		self.reset()

	def create_empty_board(self, width: int, height: int) -> list[list[str]]:
		return [["empty" for _ in range(width)] for _ in range(height)]

	def spawn_piece(self, piece_type: str | None = None) -> Piece:
		if piece_type is None:
			piece_type = random.choice(list(PIECE_SHAPES.keys()))
		piece = Piece(piece_type=piece_type, x=(self.width // 2) - 2, y=0, rotation=0)
		return piece

	def get_piece_cells(self, piece: Piece, rotation: int | None = None) -> list[tuple[int, int]]:
		rot = piece.rotation if rotation is None else rotation % 4
		return [(piece.x + dx, piece.y + dy) for (dx, dy) in PIECE_SHAPES[piece.piece_type][rot]]

	def is_valid_position(
		self,
		piece: Piece,
		dx: int = 0,
		dy: int = 0,
		rotation: int | None = None,
	) -> bool:
		test_rotation = piece.rotation if rotation is None else rotation % 4
		test_piece = Piece(piece.piece_type, piece.x + dx, piece.y + dy, test_rotation)
		for x, y in self.get_piece_cells(test_piece):
			if x < 0 or x >= self.width:
				return False
			if y < 0 or y >= self.height:
				return False
			if self.board[y][x] != "empty":
				return False
		return True

	def move_piece(self, dx: int, dy: int) -> bool:
		if self.active_piece is None:
			return False
		if self.is_valid_position(self.active_piece, dx=dx, dy=dy):
			self.active_piece.x += dx
			self.active_piece.y += dy
			return True
		return False

	def rotate_piece(self, clockwise: bool = True) -> bool:
		if self.active_piece is None:
			return False
		delta = 1 if clockwise else -1
		new_rotation = (self.active_piece.rotation + delta) % 4
		if self.is_valid_position(self.active_piece, rotation=new_rotation):
			self.active_piece.rotation = new_rotation
			return True
		return False

	def lock_piece(self) -> None:
		if self.active_piece is None:
			return
		for x, y in self.get_piece_cells(self.active_piece):
			if 0 <= x < self.width and 0 <= y < self.height:
				self.board[y][x] = f"block-{self.active_piece.piece_type}"

	def clear_full_lines(self) -> int:
		remaining_rows = [row for row in self.board if any(cell == "empty" for cell in row)]
		lines_cleared = self.height - len(remaining_rows)
		new_rows = [["empty" for _ in range(self.width)] for _ in range(lines_cleared)]
		self.board = new_rows + remaining_rows
		return lines_cleared

	def apply_line_clear_score(self, lines_cleared: int) -> None:
		self.score += SCORE_BY_LINES.get(lines_cleared, lines_cleared * 250)

	def render_board(self) -> list[list[str]]:
		rendered = [row[:] for row in self.board]
		if self.active_piece is not None:
			for x, y in self.get_piece_cells(self.active_piece):
				if 0 <= x < self.width and 0 <= y < self.height:
					rendered[y][x] = f"block-{self.active_piece.piece_type}"
		return rendered

	def tick(self) -> None:
		if self.game_over:
			return

		if self.active_piece is None:
			self.active_piece = self.spawn_piece()
			if not self.is_valid_position(self.active_piece):
				self.game_over = True
			return

		if self.move_piece(0, 1):
			return

		self.lock_piece()
		lines_cleared = self.clear_full_lines()
		self.apply_line_clear_score(lines_cleared)

		self.active_piece = self.spawn_piece()
		self.hold_used_this_turn = False
		if not self.is_valid_position(self.active_piece):
			self.game_over = True

	def hard_drop(self) -> None:
		if self.active_piece is None or self.game_over:
			return
		while self.move_piece(0, 1):
			pass
		self.tick()

	def hold_piece(self) -> None:
		if self.active_piece is None or self.game_over or self.hold_used_this_turn:
			return

		current_type = self.active_piece.piece_type
		if self.held_piece_type is None:
			self.held_piece_type = current_type
			self.active_piece = self.spawn_piece()
		else:
			swap_type = self.held_piece_type
			self.held_piece_type = current_type
			self.active_piece = self.spawn_piece(piece_type=swap_type)

		self.hold_used_this_turn = True
		if not self.is_valid_position(self.active_piece):
			self.game_over = True

	def set_direction(self, action: str) -> None:
		if self.game_over:
			return

		action = action.lower().strip()
		if action == "left":
			self.move_piece(-1, 0)
		elif action == "right":
			self.move_piece(1, 0)
		elif action == "soft_drop":
			moved = self.move_piece(0, 1)
			if not moved:
				self.tick()
		elif action == "hard_drop":
			self.hard_drop()
		elif action == "rotate_cw":
			self.rotate_piece(clockwise=True)
		elif action == "rotate_ccw":
			self.rotate_piece(clockwise=False)
		elif action == "hold":
			self.hold_piece()

	def state(self) -> dict:
		return {
			"board": self.render_board(),
			"width": self.width,
			"height": self.height,
			"score": self.score,
			"game_over": self.game_over,
			"held_piece": self.held_piece_type,
			"can_hold": (not self.game_over) and (not self.hold_used_this_turn),
		}

	def reset(self) -> None:
		self.board = self.create_empty_board(self.width, self.height)
		self.score = 0
		self.game_over = False
		self.held_piece_type = None
		self.hold_used_this_turn = False
		self.active_piece = self.spawn_piece()
		if not self.is_valid_position(self.active_piece):
			self.game_over = True
    
