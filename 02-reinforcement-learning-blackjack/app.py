import tkinter as tk
from tkinter import ttk
import numpy as np
from blackjack_mc import train_monte_carlo

class PolicyVisualizerApp:
    def __init__(self, root, Q):
        self.root = root
        self.Q = Q
        self.root.title("Blackjack Monte Carlo Optimal Policy Matrix")
        self.root.geometry("800x600")

        self.label = ttk.Label(root, text="Optimal Policy (Green = Stand [1], Red = Hit [0])", font=("Arial", 14, "bold"))
        self.label.pack(pady=10)

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.draw_policy_grid()

    def draw_policy_grid(self):
        player_sums = list(range(12, 26))
        dealer_cards = list(range(1, 11))

        rows = len(player_sums)
        cols = len(dealer_cards)

        cell_w = 700 // (cols + 1)
        cell_h = 500 // (rows + 1)

        # Draw Headers
        for j, d in enumerate(dealer_cards):
            x = (j + 1) * cell_w
            self.canvas.create_text(x + cell_w//2, cell_h//2, text=f"D:{d}", font=("Arial", 10, "bold"))

        for i, p in enumerate(player_sums):
            y = (i + 1) * cell_h
            self.canvas.create_text(cell_w//2, y + cell_h//2, text=f"P:{p}", font=("Arial", 10, "bold"))

            for j, d in enumerate(dealer_cards):
                x = (j + 1) * cell_w
                # Check action for state without usable ace
                state = (p, d, False)
                best_action = np.argmax(self.Q[state]) if state in self.Q else 0

                color = "#2ecc71" if best_action == 1 else "#e74c3c"
                action_text = "S" if best_action == 1 else "H"

                self.canvas.create_rectangle(x, y, x + cell_w, y + cell_h, fill=color, outline="white")
                self.canvas.create_text(x + cell_w//2, y + cell_h//2, text=action_text, fill="white", font=("Arial", 10, "bold"))

def main():
    print("Training RL agent for visualization...")
    Q = train_monte_carlo(episodes=150000)
    root = tk.Tk()
    app = PolicyVisualizerApp(root, Q)
    root.mainloop()

if __name__ == "__main__":
    main()
