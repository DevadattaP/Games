import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

WORD_LIST = [
    "APPLE", "GRAPE", "BERRY", "MANGO", "PEACH", "LEMON", "LIME", "PEAR",
    "PLUMB", "CHERRY", "ORANGE", "BANANA", "KIWI", "GUAVA", "MELON", "APRICOT",
    "DATES", "FIGS", "OLIVE", "PAPAYA", "LYCHE", "BASIL", "ROSE", "CLOVE"
]

COLOR_MAP = {
    'green': "#6aaa64",
    'yellow': "#c9b458",
    'gray': "#787c7e"
}

class WordlyGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wordly - Tkinter")
        self.resizable(False, False)
        self._build_start_screen()

    def _build_start_screen(self):
        for w in self.winfo_children():
            w.destroy()

        frame = ttk.Frame(self, padding=20)
        frame.grid()

        ttk.Label(frame, text="Wordly", font=("Helvetica", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=(0,10))

        ttk.Label(frame, text="Number of letters:").grid(row=1, column=0, sticky="e", pady=5)
        self.letters_var = tk.StringVar(value="5")
        ttk.Entry(frame, textvariable=self.letters_var, width=10).grid(row=1, column=1, sticky="w", pady=5)

        ttk.Label(frame, text="Number of guesses:").grid(row=2, column=0, sticky="e", pady=5)
        self.guesses_var = tk.StringVar(value="6")
        ttk.Entry(frame, textvariable=self.guesses_var, width=10).grid(row=2, column=1, sticky="w", pady=5)

        self.custom_word_var = tk.StringVar()
        ttk.Label(frame, text="(Optional) Secret word (for testing):").grid(row=3, column=0, sticky="e", pady=5)
        ttk.Entry(frame, textvariable=self.custom_word_var, width=15).grid(row=3, column=1, sticky="w", pady=5)
        ttk.Label(frame, text="(leave empty to pick randomly)").grid(row=4, column=0, columnspan=2)

        ttk.Button(frame, text="Next", command=self._on_start_next).grid(row=5, column=0, columnspan=2, pady=(10,0))

    def _on_start_next(self):
        try:
            n_letters = int(self.letters_var.get())
            n_guesses = int(self.guesses_var.get())
            if n_letters <= 0 or n_guesses <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid", "Please enter positive integers for letters and guesses.")
            return

        custom = self.custom_word_var.get().strip().upper()
        if custom and (len(custom) != n_letters or not custom.isalpha()):
            messagebox.showerror("Invalid secret word", "Custom secret word must be alphabetic and match length.")
            return

        self.n_letters = n_letters
        self.n_guesses = n_guesses
        self.secret_word = custom if custom else self._pick_secret(n_letters)
        print(f"[DEBUG] Secret: {self.secret_word}")
        self._build_game_screen()

    def _pick_secret(self, length):
        cand = [w.upper() for w in WORD_LIST if len(w) == length]
        if cand:
            return random.choice(cand)
        letters = list(string.ascii_uppercase)
        random.shuffle(letters)
        return "".join(letters[:length])

    def _build_game_screen(self):
        for w in self.winfo_children():
            w.destroy()

        top = ttk.Frame(self, padding=10)
        top.grid()

        ttk.Label(top, text=f"Wordly — {self.n_letters} letters, {self.n_guesses} guesses",
                  font=("Helvetica", 14, "bold")).grid(row=0, column=0, pady=(0,10))

        self.board_frame = ttk.Frame(top, padding=(5,5,5,10))
        self.board_frame.grid(row=1, column=0)

        # Data structures
        self.widgets = [[None for _ in range(self.n_letters)] for _ in range(self.n_guesses)]
        self.vars = [[None for _ in range(self.n_letters)] for _ in range(self.n_guesses)]
        self.guess_matrix = [['' for _ in range(self.n_letters)] for _ in range(self.n_guesses)]
        self.active_row = 0

        # Build all cells as Entry initially; disable non-active rows
        for r in range(self.n_guesses):
            for c in range(self.n_letters):
                sv = tk.StringVar()
                e = tk.Entry(self.board_frame,
                             width=2, justify="center",
                             textvariable=sv,
                             font=("Helvetica", 16, "bold"),
                             bg="white", disabledbackground="#f0f0f0")
                e.grid(row=r, column=c, padx=4, pady=4)
                # bind with captured r,c
                e.bind("<KeyRelease>", lambda ev, rr=r, cc=c: self._on_key_release(ev, rr, cc))
                e.bind("<Return>", lambda ev, rr=r: self._on_enter_pressed(ev, rr))
                self.widgets[r][c] = e
                self.vars[r][c] = sv

                # disable rows that are not the starting row
                if r != 0:
                    e.config(state='disabled')

        instr = ttk.Label(top, text="Type letters (A-Z). Use Backspace to edit. Press Enter when done with a row.")
        instr.grid(row=2, column=0, pady=(5,10))

        ctrl = ttk.Frame(top)
        ctrl.grid(row=3, column=0, pady=(5,0))
        ttk.Button(ctrl, text="Reveal Secret", command=self._reveal_secret).grid(row=0, column=0, padx=5)
        ttk.Button(ctrl, text="Restart", command=self._build_start_screen).grid(row=0, column=1, padx=5)

        # Focus first entry
        first = self.widgets[0][0]
        first.config(state='normal')
        first.focus_set()
        first.selection_range(0, tk.END)

    def _reveal_secret(self):
        messagebox.showinfo("Secret Word", f"The secret word was: {self.secret_word}")
        if messagebox.askyesno("Play again?", "Do you want to play again?"):
            self._build_start_screen()
        else:
            self.destroy()

    def _on_key_release(self, event, row, col):
        # Only accept input on the currently active row
        if row != self.active_row:
            return

        w = event.widget
        val = w.get().upper()

        # keep only last char and only A-Z
        if len(val) > 1:
            val = val[-1]
        if val and val not in string.ascii_uppercase:
            val = ''
        # update var (this will update the Entry's visible text)
        self.vars[row][col].set(val)

        # Move focus forward on valid letter
        if val:
            if col < self.n_letters - 1:
                nxt = self.widgets[row][col+1]
                # ensure it's an Entry (should be)
                if isinstance(nxt, tk.Entry):
                    nxt.focus_set()
                    nxt.selection_range(0, tk.END)
        # Backspace behaviour: go to previous if empty
        if event.keysym == "BackSpace":
            if not val and col > 0:
                prev = self.widgets[row][col-1]
                if isinstance(prev, tk.Entry):
                    prev.focus_set()
                    prev.selection_range(0, tk.END)

    def _on_enter_pressed(self, event, row):
        if row != self.active_row:
            return

        # Collect guess and verify full
        guess = "".join(self.vars[row][c].get().strip().upper() for c in range(self.n_letters))
        if len(guess) != self.n_letters or any(ch == "" for ch in guess):
            messagebox.showinfo("Incomplete", "Please fill all letters before pressing Enter.")
            return

        # Evaluate
        colors = self._evaluate_wordle_colors(guess, self.secret_word.upper())

        # Replace entries with colored labels and store guesses
        for c in range(self.n_letters):
            val = self.vars[row][c].get().upper()
            self.guess_matrix[row][c] = val

            # destroy entry widget
            w = self.widgets[row][c]
            if isinstance(w, tk.Entry):
                w.destroy()

            # create label tile with color
            bg = COLOR_MAP[colors[c]]
            lbl = tk.Label(self.board_frame, text=val,
                           width=2, height=1,
                           font=("Helvetica", 16, "bold"),
                           bg=bg, fg="white",
                           relief="raised", bd=2)
            lbl.grid(row=row, column=c, padx=4, pady=4)

            # store label in widgets matrix
            self.widgets[row][c] = lbl
            # keep var value in self.vars (optional)
            self.vars[row][c].set(val)

        # Check win
        if guess == self.secret_word.upper():
            messagebox.showinfo("You win!", f"Congratulations! You guessed: {self.secret_word}")
            if messagebox.askyesno("Play again?", "Play again?"):
                self._build_start_screen()
            else:
                self.destroy()
            return

        # Move to next row or lose
        self.active_row += 1
        if self.active_row >= self.n_guesses:
            messagebox.showinfo("Game Over", f"No guesses left. The word was: {self.secret_word}")
            if messagebox.askyesno("Play again?", "Play again?"):
                self._build_start_screen()
            else:
                self.destroy()
            return

        # Enable the next row's entry widgets and focus the first one
        for c in range(self.n_letters):
            w = self.widgets[self.active_row][c]
            # they should be Entry objects (we created them initially)
            if isinstance(w, tk.Entry):
                w.config(state='normal')
        first = self.widgets[self.active_row][0]
        if isinstance(first, tk.Entry):
            first.focus_set()
            first.selection_range(0, tk.END)

    def _evaluate_wordle_colors(self, guess, secret):
        # returns list of 'green'|'yellow'|'gray' for each position
        guess_chars = list(guess)
        secret_chars = list(secret)
        n = self.n_letters
        colors = ['gray'] * n

        # First pass greens
        for i in range(n):
            if guess_chars[i] == secret_chars[i]:
                colors[i] = 'green'
                guess_chars[i] = None
                secret_chars[i] = None

        # Count remaining in secret
        remaining = {}
        for ch in secret_chars:
            if ch is not None:
                remaining[ch] = remaining.get(ch, 0) + 1

        # Second pass yellows
        for i in range(n):
            if guess_chars[i] is not None:
                ch = guess_chars[i]
                if remaining.get(ch, 0) > 0:
                    colors[i] = 'yellow'
                    remaining[ch] -= 1
                else:
                    colors[i] = 'gray'
        return colors


if __name__ == "__main__":
    app = WordlyGame()
    app.mainloop()
