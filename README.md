# Python Advanced Pong Game

A two-player Pong game built with Python and the Turtle graphics library.

The game includes real-time paddle and ball movement, collision detection, score tracking, player statistics, and persistent game history.

## Features

- 🎮 Two-player gameplay
- 🏓 Paddle and ball collision detection
- 🏆 First player to 5 points wins
- 📊 Player statistics and win-rate tracking
- 💾 Persistent player statistics using JSON
- 📝 Game score history saved to a text file
- ⌨️ Keyboard controls
- 🖥️ Graphical interface using Python Turtle

## Controls

| Player | Move Up | Move Down |
|---|---|---|
| Player 1 | W | S |
| Player 2 | ↑ | ↓ |

## How It Works

1. Two players control their respective paddles.
2. The ball continuously moves across the game area.
3. The ball bounces from the top and bottom boundaries.
4. Paddle collisions reverse the ball's horizontal direction.
5. When the ball passes a paddle, the opponent receives a point.
6. The game ends when a player reaches 5 points.
7. Player statistics and game results are saved for future sessions.

## Technologies Used

- Python
- Turtle Graphics
- Object-Oriented Programming
- JSON
- File Handling
- Data Structures

## Project Structure

```text
Python-Advanced-Pong-Game/
│
└── pong_game.py
