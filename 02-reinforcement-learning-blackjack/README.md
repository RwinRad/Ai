# 02. Blackjack Monte Carlo Control (Reinforcement Learning)

An implementation of **On-Policy First-Visit Monte Carlo Control** to solve a custom 25-point threshold Blackjack game. The AI agent learns the optimal policy directly from experience without prior knowledge of the environment's transition probabilities (Model-Free RL).

---

## 🎮 Game Rules & Logic (Custom Blackjack)

This variant modifies standard Blackjack rules to create a higher-dimensional state space and a more engaging learning problem:

* **Target Score**: Reach as close to **25** as possible without exceeding it (Bust).
* **Card Values**:
  * Cards 2 through 10: Face value.
  * Face cards (J, Q, K): Value of **10**.
  * Ace: Value of **1** or **11** (counted as 11 as long as total score $\le 25$, designated as a **Usable Ace**).
* **Action Space**:
  * **Hit (0)**: Draw another card.
  * **Stand (1)**: Stop drawing cards and pass the turn to the dealer.
* **Dealer Policy**:
  * Fixed policy: The dealer must hit until their score reaches at least **17**, at which point they must stand.
* **Reward Structure**:
  * **Win (+1.0)**: Player's score is higher than the dealer's, or the dealer busts.
  * **Loss (-1.0)**: Player busts (> 25) or the dealer's score is higher.
  * **Draw (0.0)**: Player and dealer scores are equal.

---

## 🧠 Reinforcement Learning Architecture

### 1. State Space
Each state $S_t$ is represented as a 3-tuple:
1. **Player's Current Sum**: Integer between 12 and 25.
2. **Dealer's Showing Card**: Integer between 1 and 10.
3. **Usable Ace**: Boolean (`True` or `False`).

### 2. Monte Carlo Control Algorithm
* **Model-Free Learning**: The agent learns action-value functions $Q(s, a)$ directly from simulated game episodes without environmental transition probabilities.
* **$\epsilon$-Greedy Policy**: Balances **Exploration** (random action with probability $\epsilon$) and **Exploitation** (best action according to $Q$-table with probability $1-\epsilon$).
* **Return Calculation**: At the end of each episode, total return $G_t$ is tracked, and $Q(s, a)$ values are updated using sample averages:
  $$Q(s, a) \leftarrow \frac{\sum G_t}{N(s, a)}$$

---

## 📊 Policy Visualizer (Tkinter GUI)

The `app.py` script trains the agent and displays the learned optimal policy matrix:
* **Green (S - Stand)**: Standing is the optimal decision.
* **Red (H - Hit)**: Drawing another card maximizes expected return.

---

## 🚀 Quick Start

```bash
# Install required packages
pip install -r requirements.txt

# Train the RL agent and display the optimal policy matrix
python app.py
