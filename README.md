# Games 🎮

A collection of small games built with Python.

Currently includes:

## 1. Wordly ✍️

A **Wordle-style game** implemented in Python with a Tkinter GUI.

> * Customizable number of letters and guesses
> * Interactive grid-based interface
> * Color-coded feedback:
>   * 🟩 Green for correct letter + position
>   * 🟨 Yellow for correct letter in wrong position
>   * ⬛ Gray for incorrect letter
> * Optionally allow a custom secret word (for testing)
> * "Reveal Secret" button (ends the game immediately)
> * Restart option after win/lose

## 2. Number Guessing Game 🔢

A simple number guessing game where the player tries to guess a randomly generated number within a certain range.

> * Computer guesses a number you are thinking of, or you guess a number the computer has chosen
> * Customizable range of numbers
> * Feedback on whether the number is higher or lower than guess, or correct
> * Counts the number of attempts taken, and computer tells optimal number of attempts based on binary search

## Clone this repository to get started

```bash
git clone https://github.com/DevadattaP/Games.git
```

### Requirements

* Python 3.8+
* Tkinter (comes pre-installed with most Python distributions)
* Install dependencies:

```bash
pip install -r requirements.txt
```

> [!NOTE]
> If you are on linux and don't have Tkinter, you can install it via your package manager. For example, on Debian/Ubuntu:
>
> ```bash
> sudo apt-get install python3-tk
> ```

### Run the game (Example for Wordly)

```bash
python wordly.py
```

---

> [!TIP]TODO
> Add instructions on how to play each game, and any additional features or settings available.

## Screenshots

1. Wordly game:

![game window](screenshots/wordly.png) |
2. Number Guessing Game:

| Computer guesses user's number                         | User guesses computer's number                          |
|--------------------------------------------------------|---------------------------------------------------------|
|![computer guesses user](screenshots/number_guess1.png) | ![user guesses computer](screenshots/number_guess2.png) |

## Future Plans

This repository will grow into a **mini-game collection**, where each game lives in its own file/module. Planned games may include:

* Finding birthday
* Finding erased number
* Hangman
* word guessing (type words, and you will know how near/far you are)
* Sudoku (both solver and generator)
* tic-tac-toe
* n-queens puzzle
* zip (like on LinkedIn)
* patches (like on LinkedIn)
* More puzzle/logic games

## Keep playing & Stay tuned 🚀

Feel free to contribute by adding new games, improving existing ones, or suggesting features!
