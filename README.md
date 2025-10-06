# Games 🎮

A collection of small games built with Python.

Currently includes:

## 1. Wordly ✍️

A **Wordle-style game** implemented in Python with a Tkinter GUI.

### Features

* Customizable number of letters and guesses
* Interactive grid-based interface
* Color-coded feedback:

  * 🟩 Green for correct letter + position
  * 🟨 Yellow for correct letter in wrong position
  * ⬛ Gray for incorrect letter
* Optionally allow a custom secret word (for testing)
* "Reveal Secret" button (ends the game immediately)
* Restart option after win/lose

### Requirements

* Python 3.8+
* Tkinter (comes pre-installed with most Python distributions)

### How to Run

```bash
git clone https://github.com/DevadattaP/Games.git
cd Games
python wordly.py
```

### Screenshots

*(optional – add screenshots here later)*

### TODO

* Replace static word list with words fetched from a **word generator / NLP library**
* Add more games to this repository (planning for yes-no questions game)

---

## Future Plans

This repository will grow into a **mini-game collection**, where each game lives in its own file/module. Planned games may include:

* Number guessing
* Hangman
* Puzzle/logic games

Stay tuned 🚀
