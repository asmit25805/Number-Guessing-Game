import random
import time
import json
import os

# --- Constants & Configuration ---
HIGH_SCORE_FILE = "high_scores.json"

def load_high_scores():
    """Load high scores from a JSON file."""
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_high_score(difficulty, score, name):
    """Save the new high score if it beats the previous one."""
    scores = load_high_scores()
    current_high = scores.get(difficulty, {}).get("score", 0)
    
    if score > current_high:
        scores[difficulty] = {"score": score, "name": name}
        with open(HIGH_SCORE_FILE, "w") as f:
            json.dump(scores, f)
        return True
    return False

def get_difficulty():
    """Level 2: Let the user choose difficulty and return settings."""
    print("\nSelect Difficulty:")
    print("1. Easy   (1-50,  10 attempts)")
    print("2. Medium (1-100, 7 attempts)")
    print("3. Hard   (1-500, 5 attempts)")
    
    while True:
        choice = input("Choice (1-3): ").strip()
        if choice == '1': return "Easy", 50, 10
        if choice == '2': return "Medium", 100, 7
        if choice == '3': return "Hard", 500, 5
        print("❌ Invalid choice. Please pick 1, 2, or 3.")

def calculate_score(attempts_left, total_attempts, elapsed_time, difficulty_multiplier):
    """Level 4: Advanced Scoring Logic."""
    # Base score is based on percentage of attempts remaining
    attempt_score = (attempts_left / total_attempts) * 1000
    # Time bonus: subtract 10 points for every second taken (min bonus 0)
    time_bonus = max(0, 500 - (elapsed_time * 5))
    
    final_score = int((attempt_score + time_bonus) * difficulty_multiplier)
    return max(0, final_score)

def play_game():
    """Main game logic loop."""
    print("\n" + "="*40)
    print("🎯 THE ULTIMATE NUMBER GUESSER 🎯")
    print("="*40)

    diff_name, max_num, max_attempts = get_difficulty()
    secret_number = random.randint(1, max_num)
    
    # Difficulty multipliers for scoring
    multipliers = {"Easy": 1, "Medium": 2, "Hard": 5}
    
    print(f"\nI'm thinking of a number between 1 and {max_num}.")
    print(f"You have {max_attempts} attempts. Good luck!")

    attempts = 0
    start_time = time.time() # Level 4: Timer start
    
    while attempts < max_attempts:
        try:
            guess = int(input(f"\n[{attempts + 1}/{max_attempts}] Enter your guess: "))
        except ValueError:
            print("❌ That's not a number! Try again.")
            continue

        attempts += 1
        diff = abs(guess - secret_number)

        # Level 1: Basic Feedback
        if guess == secret_number:
            end_time = time.time()
            elapsed = round(end_time - start_time, 2)
            
            print(f"\n✨ CONGRATULATIONS! ✨")
            print(f"You found it in {attempts} attempts and {elapsed} seconds.")
            
            # Level 4: Scoring
            score = calculate_score(max_attempts - attempts + 1, max_attempts, elapsed, multipliers[diff_name])
            print(f"🏆 Your Score: {score}")
            
            # Level 3: High Score Save
            if save_high_score(diff_name, score, "Player"):
                print("🎊 NEW PERSONAL BEST for this difficulty! 🎊")
            return

        # Level 4: "Very Close" Hint upgrade
        if diff <= 5:
            hint = "🔥 YOU ARE RED HOT! (Very Close)"
        elif guess < secret_number:
            hint = "📉 Too low!"
        else:
            hint = "📈 Too high!"
            
        print(hint)

    print(f"\n💀 GAME OVER! The number was {secret_number}.")

def main():
    while True:
        # Show high scores before starting
        scores = load_high_scores()
        if scores:
            print("\n--- Current High Scores ---")
            for diff, data in scores.items():
                print(f"{diff}: {data['score']} pts")

        play_game()
        
        # Level 2: Replay option
        again = input("\nPlay again? (y/n): ").lower().strip()
        if again != 'y':
            print("\nThanks for playing! 👋")
            break

if __name__ == "__main__":
    main()
