import random
import json
import os

WORDS = [
    "python", "terminal", "keyboard", "monitor", "browser",
    "function", "variable", "integer", "boolean", "library",
    "network", "program", "develop", "console", "package",
    "science", "captain", "lantern", "blanket", "crystal",
    "thunder", "kitchen", "dolphin", "journey", "penguin",
    "grammar", "comfort", "balance", "fashion", "gallery",
]

STATS_FILE = os.path.join(os.path.dirname(__file__), "stats.json")


def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE) as f:
            return json.load(f)
    return {"wins": 0, "losses": 0, "streak": 0, "best_streak": 0}


def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)


def scramble(word):
    letters = list(word)
    while True:
        random.shuffle(letters)
        scrambled = "".join(letters)
        if scrambled != word:
            return scrambled


def show_stats(stats):
    total = stats["wins"] + stats["losses"]
    win_pct = int(stats["wins"] / total * 100) if total else 0
    print(f"\n  Wins: {stats['wins']}  Losses: {stats['losses']}  "
          f"Win%: {win_pct}%  Streak: {stats['streak']}  Best: {stats['best_streak']}")


def play_round(stats):
    word = random.choice(WORDS)
    scrambled = scramble(word)
    max_guesses = 3

    print(f"\n{'='*40}")
    print(f"  Unscramble: {scrambled.upper()}")
    print(f"  ({len(word)} letters, {max_guesses} guesses)")
    print(f"{'='*40}")

    for attempt in range(1, max_guesses + 1):
        try:
            guess = input(f"  Guess {attempt}/{max_guesses}: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n  Bye!")
            return False

        if guess == word:
            print(f"  Correct! The word was '{word}'.")
            stats["wins"] += 1
            stats["streak"] += 1
            stats["best_streak"] = max(stats["streak"], stats["best_streak"])
            return True
        elif attempt < max_guesses:
            print(f"  Not quite, try again.")
        else:
            print(f"  Out of guesses! The word was '{word}'.")
            stats["losses"] += 1
            stats["streak"] = 0

    return True


def main():
    stats = load_stats()
    print("\nWord Scramble")
    print("Unscramble the word in 3 guesses. Type 'quit' to exit.\n")

    while True:
        keep_going = play_round(stats)
        save_stats(stats)
        show_stats(stats)

        if not keep_going:
            break

        try:
            again = input("\n  Play again? [Y/n]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n  Bye!")
            break

        if again in ("n", "no", "quit", "q"):
            print("  See you next time!")
            break


if __name__ == "__main__":
    main()
