from turtle import Turtle, Screen
import time
from collections import namedtuple, deque
import json
import os
from datetime import datetime
GameConfig = namedtuple('GameConfig', [
    'screen_width', 'screen_height', 'bg_color',
    'paddle_speed', 'ball_speed', 'winning_score'
])
CONFIG = GameConfig(
    screen_width=800,
    screen_height=600,
    bg_color="black",
    paddle_speed=20,
    ball_speed=0.1,
    winning_score=5  # First to 5 wins
)
SCORES_FILE = "game_scores.txt"
STATS_FILE = "player_stats.json"
players = {
    "left": {
        "name": "Player 1",
        "score": 0,
        "total_wins": 0,
        "total_games": 0,
        "color": "cyan",
        "controls": {"up": "w", "down": "s"}
    },
    "right": {
        "name": "Player 2",
        "score": 0,
        "total_wins": 0,
        "total_games": 0,
        "color": "magenta",
        "controls": {"up": "Up", "down": "Down"}
    }
}
score_history = deque(maxlen=10)
def load_player_stats():
    """Load player statistics from JSON file"""
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, 'r') as file:
                stats = json.load(file)
                players["left"]["total_wins"] = stats.get("player1_wins", 0)
                players["left"]["total_games"] = stats.get("player1_games", 0)
                players["right"]["total_wins"] = stats.get("player2_wins", 0)
                players["right"]["total_games"] = stats.get("player2_games", 0)
                print("Loaded player statistics!")
                return stats
        except Exception as e:
            print(f" Error loading stats: {e}")
            return {}
    else:
        print("No previous stats found. Starting fresh!")
        return {}
def save_player_stats():
    """Save player statistics to JSON file"""
    stats = {
        "player1_wins": players["left"]["total_wins"],
        "player1_games": players["left"]["total_games"],
        "player2_wins": players["right"]["total_wins"],
        "player2_games": players["right"]["total_games"],
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        with open(STATS_FILE, 'w') as file:
            json.dump(stats, file, indent=4)
        print(" Player statistics saved!")
    except Exception as e:
        print(f" Error saving stats: {e}")
def save_game_score(winner_side, final_scores):
    """Append game result to scores text file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    winner_name = players[winner_side]["name"]
   
    score_line = (
        f"\n{'='*50}\n"
        f"Game Date: {timestamp}\n"
        f"Winner: {winner_name}\n"
        f"Final Score - {players['left']['name']}: {final_scores['left']} | "
        f"{players['right']['name']}: {final_scores['right']}\n"
        f"{'='*50}\n"
    )
 
    try:
        with open(SCORES_FILE, 'a') as file:
            file.write(score_line)
        print(" Game score saved to file!")
    except Exception as e:
        print(f" Error saving score: {e}")
def read_all_scores():
    """Read and display all saved scores from file"""
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, 'r') as file:
                content = file.read()
                if content.strip():
                    print("\n PREVIOUS GAME SCORES:")
                    print(content)
                else:
                    print(" No previous games recorded yet!")
        except Exception as e:
            print(f" Error reading scores: {e}")
    else:
        print(" No score history file found!")


def display_stats():
    """Display current player statistics"""
    print("\n" + "="*50)
    print(" PLAYER STATISTICS")
    print("="*50)
    for side, player in players.items():
        games = player['total_games']
        wins = player['total_wins']
        win_rate = (wins / games * 100) if games > 0 else 0
        print(f"{player['name']}:")
        print(f"  Total Games: {games}")
        print(f"  Total Wins: {wins}")
        print(f"  Win Rate: {win_rate:.1f}%")
    print("="*50 + "\n")
class Paddle(Turtle):
    """Represents a paddle that players control"""
   
    def __init__(self, position, color="white"):
        super().__init__()
        self.shape("square")
        self.color(color)
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()
        self.goto(position)
        self.speed = CONFIG.paddle_speed

    def go_up(self):
        """Move paddle up with boundary checking"""
        new_y = self.ycor() + self.speed
        if new_y < (CONFIG.screen_height / 2) - 40:
            self.goto(self.xcor(), new_y)

    def go_down(self):
        """Move paddle down with boundary checking"""
        new_y = self.ycor() - self.speed
        if new_y > -(CONFIG.screen_height / 2) + 40:
            self.goto(self.xcor(), new_y)
class Ball(Turtle):
    """Represents the ball that bounces around the screen"""
   
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.x_move = 10
        self.y_move = 10
        self.move_speed = CONFIG.ball_speed
        self.position_history = deque(maxlen=10)  # Track last 10 positions

    def move(self):
        """Move the ball and track position history"""
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)
       
        # Store position in history
        self.position_history.append((new_x, new_y))

    def bounce_y(self):
        """Bounce the ball vertically (off top/bottom walls)"""
        self.y_move *= -1

    def bounce_x(self):
        """Bounce the ball horizontally (off paddles) and increase speed"""
        self.x_move *= -1
        self.move_speed *= 0.9

    def reset_position(self):
        """Reset ball to center and restore initial speed"""
        self.goto(0, 0)
        self.move_speed = CONFIG.ball_speed
        self.position_history.clear()
        self.bounce_x()
class Scoreboard(Turtle):
    """Displays and manages the game score"""
   
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.scores = {"left": 0, "right": 0}  # Dictionary for scores
        self.game_over_flag = False
        self.update_scoreboard()

    def update_scoreboard(self):
        """Clear and redraw the scoreboard"""
        self.clear()
       
        # Draw center line
        self.goto(0, CONFIG.screen_height // 2)
        self.goto(0, -CONFIG.screen_height // 2)
        self.color("gray")
        for y in range(-CONFIG.screen_height // 2, CONFIG.screen_height // 2, 20):
            self.goto(0, y)
            self.pendown()
            self.goto(0, y + 10)
            self.penup()
       
        # Draw scores
        self.color("white")
        self.goto(-100, 200)
        self.write(self.scores["left"], align="center",
                  font=("Courier", 80, "normal"))
        self.goto(100, 200)
        self.write(self.scores["right"], align="center",
                  font=("Courier", 80, "normal"))
       
        # Draw player names
        self.goto(-100, 250)
        self.write(players["left"]["name"], align="center",
                  font=("Courier", 16, "normal"))
        self.goto(100, 250)
        self.write(players["right"]["name"], align="center",
                  font=("Courier", 16, "normal"))

    def add_point(self, side):
        """Add point to specified side ('left' or 'right')"""
        self.scores[side] += 1
        players[side]["score"] = self.scores[side]
        score_history.append((players[side]["name"], self.scores[side]))
        self.update_scoreboard()
       
        # Print current score to console
        print(f" {players[side]['name']} scored! "
              f"Score: {self.scores['left']} - {self.scores['right']}")
       
        # Check for winner
        if self.scores[side] >= CONFIG.winning_score:
            self.game_over(side)

    def game_over(self, winner_side):
        """Display game over message and save results"""
        self.game_over_flag = True
       
        # Update player statistics
        players[winner_side]["total_wins"] += 1
        players["left"]["total_games"] += 1
        players["right"]["total_games"] += 1
       
        # Display winner message
        self.goto(0, 0)
        self.color(players[winner_side]["color"])
        self.write(f" {players[winner_side]['name']} WINS! ",
                  align="center", font=("Courier", 36, "bold"))
       
        # Display final score
        self.goto(0, -50)
        self.color("white")
        self.write(f"Final Score: {self.scores['left']} - {self.scores['right']}",
                  align="center", font=("Courier", 20, "normal"))
       
        # Save game results to files
        save_game_score(winner_side, self.scores)
        save_player_stats()
       
        # Display score history
        self.goto(0, -100)
        self.write("Recent Scores: " + str(list(score_history)),
                  align="center", font=("Courier", 12, "normal"))
       
        print(f"\n GAME OVER! {players[winner_side]['name']} WINS! ")
        print(f"Final Score: {self.scores['left']} - {self.scores['right']}")
def setup_screen():
    """Initialize and configure the game screen"""
    screen = Screen()
    screen.setup(width=CONFIG.screen_width, height=CONFIG.screen_height)
    screen.bgcolor(CONFIG.bg_color)
    screen.title(" Advanced Pong Game - Score Tracking Edition")
    screen.tracer(0)
    return screen
def setup_controls(screen, paddles_dict):
    """Set up keyboard controls for both paddles"""
    screen.listen()
    for side, paddle in paddles_dict.items():
        controls = players[side]["controls"]
        screen.onkey(paddle.go_up, controls["up"])
        screen.onkey(paddle.go_down, controls["down"])
def check_wall_collision(ball):
    """Check if ball hits top or bottom wall"""
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()
def check_paddle_collision(ball, paddles_dict):
    """Check if ball collides with either paddle"""
    for side, paddle in paddles_dict.items():
        distance_threshold = 50
        if side == "right":
            if ball.distance(paddle) < distance_threshold and ball.xcor() > 320:
                ball.bounce_x()
                print(f" {players[side]['name']} hit the ball!")
        else:  # left
            if ball.distance(paddle) < distance_threshold and ball.xcor() < -320:
                ball.bounce_x()
                print(f" {players[side]['name']} hit the ball!")
def check_scoring(ball, scoreboard):
    """Check if a player scored and update scoreboard"""
    if ball.xcor() > 380:
        ball.reset_position()
        scoreboard.add_point("left")
        return True
   
    if ball.xcor() < -380:
        ball.reset_position()
        scoreboard.add_point("right")
        return True
   
    return False
def main():
    """Main function to run the Pong game"""
   
    print("\n" + "="*50)
    print(" WELCOME TO ADVANCED PONG GAME ")
    print("="*50)
    print(f"\nFirst to {CONFIG.winning_score} points wins!")
    print("\nControls:")
    print(f"  {players['left']['name']}: W (up) / S (down)")
    print(f"  {players['right']['name']}: ↑ (up) / ↓ (down)")
    print("\n" + "="*50 + "\n")
   
    # Load previous statistics
    load_player_stats()
    display_stats()
   
    # Optional: Display previous game scores
    read_all_scores()
   
    # Setup game
    screen = setup_screen()
   
    # Create paddles with colors from player dict
    paddles = {
        "left": Paddle((-350, 0), players["left"]["color"]),
        "right": Paddle((350, 0), players["right"]["color"])
    }
   
    ball = Ball()
    scoreboard = Scoreboard()
   
    setup_controls(screen, paddles)
   
    print("\n🎮 GAME STARTED! \n")
   
    # Game loop
    game_is_on = True
    while game_is_on:
        time.sleep(ball.move_speed)
        screen.update()
        ball.move()
       
        check_wall_collision(ball)
        check_paddle_collision(ball, paddles)
        check_scoring(ball, scoreboard)
       
        # Check if game is over
        if scoreboard.game_over_flag:
            game_is_on = False
   
    # Display final statistics
    print("\n")
    display_stats()
    print(" Thanks for playing! Click the window to exit.\n")
   
    screen.exitonclick()
if __name__ == "__main__":
    main()
