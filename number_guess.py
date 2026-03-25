import tkinter as tk
from tkinter import ttk, messagebox
import random
import math


class NumberGuessGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Number Guessing Game")
        self.resizable(False, False)
        self._setup_styles()
        self._build_start_screen()
        
    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")  # better looking theme

        # Big primary button
        style.configure(
            "Big.TButton",
            font=("Helvetica", 12, "bold"),
            padding=10
        )

        # Small button
        style.configure(
            "Small.TButton",
            font=("Helvetica", 10),
            padding=5
        )

        # Guess buttons
        style.configure(
            "Guess.TButton",
            font=("Helvetica", 12, "bold"),
            padding=8,
            width=10
        )

    # ---------------- START SCREEN ----------------
    def _build_start_screen(self):
        for w in self.winfo_children():
            w.destroy()

        frame = ttk.Frame(self, padding=20)
        frame.grid()

        ttk.Label(frame, text="Number Guessing Game",
                  font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Mode selection
        self.mode_var = tk.StringVar(value="user")

        ttk.Radiobutton(frame, text="I guess the computer's number",
                        variable=self.mode_var, value="user").grid(row=1, column=0, columnspan=2, sticky="w")

        ttk.Radiobutton(frame, text="Computer guesses my number",
                        variable=self.mode_var, value="computer").grid(row=2, column=0, columnspan=2, sticky="w")

        # Range
        ttk.Label(frame, text="From:").grid(row=3, column=0, sticky="e", pady=5)
        self.from_var = tk.StringVar(value="1")
        ttk.Entry(frame, textvariable=self.from_var, width=10).grid(row=3, column=1, sticky="w")

        ttk.Label(frame, text="To:").grid(row=4, column=0, sticky="e", pady=5)
        self.to_var = tk.StringVar(value="100")
        ttk.Entry(frame, textvariable=self.to_var, width=10).grid(row=4, column=1, sticky="w")

        start_btn = ttk.Button(frame, text="Start Game", command=self._start_game, style="Big.TButton")
        start_btn.grid(row=5, column=0, columnspan=2, pady=10)

        self.bind("<Return>", lambda e: self._start_game())
        start_btn.focus_set()

    # ---------------- START GAME ----------------
    def _start_game(self):
        try:
            self.low = int(self.from_var.get())
            self.high = int(self.to_var.get())
            if self.low >= self.high:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Range", "Enter valid numbers (From < To).")
            return

        self.attempts = 0
        self.original_low = self.low
        self.original_high = self.high
        if self.mode_var.get() == "user":
            self.secret_number = random.randint(self.low, self.high)
            self._build_user_guess_screen()
        else:
            self._build_computer_guess_screen()
            self._computer_make_guess()

    # ---------------- USER GUESSES ----------------
    def _build_user_guess_screen(self):
        for w in self.winfo_children():
            w.destroy()

        frame = ttk.Frame(self, padding=20)
        frame.grid()

        ttk.Label(frame, text=f"Guess the number ({self.low} – {self.high})",
                  font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(frame, text="Enter your guess:").grid(row=1, column=0)

        self.guess_var = tk.StringVar()
        entry = ttk.Entry(frame, textvariable=self.guess_var, width=10)
        entry.grid(row=1, column=1)
        entry.focus_set()

        entry.bind("<Return>", lambda e: self._user_make_guess())

        ttk.Button(frame, text="Guess", command=self._user_make_guess, style="Big.TButton")\
            .grid(row=2, column=0, columnspan=2, pady=5)

        self.result_label = ttk.Label(frame, text="")
        self.result_label.grid(row=3, column=0, columnspan=2, pady=5)

        self.attempt_label = ttk.Label(frame, text="Attempts: 0")
        self.attempt_label.grid(row=4, column=0, columnspan=2)

        ttk.Button(frame, text="Restart", command=self._build_start_screen, style="Big.TButton")\
            .grid(row=5, column=0, columnspan=2, pady=10)

    def _user_make_guess(self):
        try:
            guess = int(self.guess_var.get())
        except ValueError:
            return

        self.attempts += 1
        self.attempt_label.config(text=f"Attempts: {self.attempts}")

        if guess < self.secret_number:  # computer's number is bigger than user's guess
            self.result_label.config(text="Bigger!")
        elif guess > self.secret_number:    # computer's number is smaller than user's guess
            self.result_label.config(text="Smaller!")
        else:
            messagebox.showinfo("Correct!", f"You guessed it in {self.attempts} attempts!")
            self._build_start_screen()

        self.guess_var.set("")

    # ---------------- COMPUTER GUESSES (BINARY SEARCH) ----------------
    def _build_computer_guess_screen(self):
        for w in self.winfo_children():
            w.destroy()

        frame = ttk.Frame(self, padding=20)
        frame.grid()

        ttk.Label(frame,
                  text=f"Think of a number between {self.low} and {self.high}",
                  font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=3, pady=10)

        self.guess_label = ttk.Label(frame, text="", font=("Helvetica", 12))
        self.guess_label.grid(row=1, column=0, columnspan=3, pady=10)

        ttk.Button(frame, text="< Smaller", command=self._smaller, style="Big.TButton")\
            .grid(row=2, column=0, padx=5)  # user's number is smaller than computer's guess

        ttk.Button(frame, text="= Correct", command=self._correct, style="Big.TButton")\
            .grid(row=2, column=1, padx=5)  # computer's guess is correct

        ttk.Button(frame, text="> Larger", command=self._larger, style="Big.TButton")\
            .grid(row=2, column=2, padx=5)  # user's number is larger than computer's guess

        self.attempt_label = ttk.Label(frame, text="Attempts: 0")
        self.attempt_label.grid(row=3, column=0, columnspan=3, pady=5)

        ttk.Button(frame, text="Restart", command=self._build_start_screen, style="Big.TButton")\
            .grid(row=4, column=0, columnspan=3, pady=10)

    def _computer_make_guess(self):
        if self.low > self.high:
            messagebox.showerror("Error", "Inconsistent answers!")
            self._build_start_screen()
            return

        self.current_guess = (self.low + self.high) // 2
        self.attempts += 1

        self.guess_label.config(text=f"My guess: {self.current_guess}")
        self.attempt_label.config(text=f"Attempts: {self.attempts}")

    def _smaller(self):
        self.high = self.current_guess - 1
        self._computer_make_guess()

    def _larger(self):
        self.low = self.current_guess + 1
        self._computer_make_guess()

    def _correct(self):
        optimal = math.ceil(math.log2(self.original_high - self.original_low + 1))
        messagebox.showinfo(
            "Found!",
            f"I guessed your number {self.current_guess} in {self.attempts} attempts!\n"
            f"Optimal binary search: {optimal} steps."
        )
        self._build_start_screen()


# ---------------- RUN ----------------
if __name__ == "__main__":
    app = NumberGuessGame()
    app.mainloop()
