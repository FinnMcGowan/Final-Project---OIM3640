Plan: Snake Board + Flask-Centered Design
Build Snake as a pure Python game engine first, then put Flask around it as a thin web layer. This keeps the board and game rules centralized so deployment does not change core behavior.

Steps

Define MVP rules and lock scope: board size, tick speed, controls, score, game-over behavior.
Design one authoritative game state model: width, height, snake body coordinates, current direction, food coordinate, score, status.
Implement deterministic board transition logic in the engine: validate direction, move head, detect collisions, grow on food, respawn food safely.
Keep architecture centralized in snake: all board/game logic lives there, Flask only calls engine methods and returns responses.
Design minimal Flask API contract: reset game, submit direction, fetch state snapshot; validate all input server-side.
Use one shared global game instance for MVP (your choice), and keep a clean seam to migrate to per-session games later.
Build browser render/input loop against API responses only (single source of truth remains server engine).
Add tests for board bounds, self-collision, growth, food spawning, invalid input, and repeated move stability before polishing UI.
Finalize deployment docs and project docs so the run path is clear and reproducible.
Relevant files

snake - central home for engine logic and Flask adapter code
README.md - setup, run instructions, architecture explanation
proposal.md - MVP/stretch goals and uncertainty notes
AI_USAGE.md - document AI-assisted design decisions
Verification

Unit tests pass for movement, growth, wall collision, self-collision, and food placement.
API checks confirm invalid directions are rejected and state remains consistent after many requests.
Manual browser run confirms controls, score updates, and game-over match expected engine behavior.
Fresh run from README instructions works on a clean environment.
Decisions

Included: single Snake loop with clean Flask wrapping and deployment readiness.
Excluded for now: multiplayer, audio, advanced animation, persistent leaderboard.
Chosen by you: shared single-game state for MVP.