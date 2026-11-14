import random
import numpy as np
from collections import defaultdict

class BlackjackEnv:
    def __init__(self, target_score=25):
        self.target = target_score
        self.cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    def draw_card(self):
        return random.choice(self.cards)

    def get_hand_sum(self, hand):
        hand_sum = sum(hand)
        usable_ace = False
        if 1 in hand and hand_sum + 10 <= self.target:
            hand_sum += 10
            usable_ace = True
        return hand_sum, usable_ace

    def reset(self):
        player_hand = [self.draw_card(), self.draw_card()]
        dealer_hand = [self.draw_card(), self.draw_card()]
        p_sum, usable_ace = self.get_hand_sum(player_hand)
        return (p_sum, dealer_hand[0], usable_ace), player_hand, dealer_hand

    def step(self, player_hand, dealer_hand, action):
        # Action: 0 = Hit, 1 = Stand
        if action == 0:
            player_hand.append(self.draw_card())
            p_sum, usable_ace = self.get_hand_sum(player_hand)
            if p_sum > self.target:
                return (p_sum, dealer_hand[0], usable_ace), -1.0, True
            return (p_sum, dealer_hand[0], usable_ace), 0.0, False
        else:
            p_sum, _ = self.get_hand_sum(player_hand)
            d_sum, _ = self.get_hand_sum(dealer_hand)
            while d_sum < 17:
                dealer_hand.append(self.draw_card())
                d_sum, _ = self.get_hand_sum(dealer_hand)

            if d_sum > self.target or p_sum > d_sum:
                reward = 1.0
            elif p_sum < d_sum:
                reward = -1.0
            else:
                reward = 0.0
            return (p_sum, dealer_hand[0], False), reward, True

def train_monte_carlo(episodes=200000, epsilon=0.1, gamma=1.0):
    env = BlackjackEnv()
    Q = defaultdict(lambda: np.zeros(2))
    returns_sum = defaultdict(lambda: np.zeros(2))
    returns_count = defaultdict(lambda: np.zeros(2))

    for _ in range(episodes):
        state, player_hand, dealer_hand = env.reset()
        episode = []
        done = False

        while not done:
            if random.random() < epsilon:
                action = random.choice([0, 1])
            else:
                action = np.argmax(Q[state])

            next_state, reward, done = env.step(player_hand, dealer_hand, action)
            episode.append((state, action, reward))
            state = next_state

        visited_state_actions = set()
        G = 0
        for s, a, r in reversed(episode):
            G = gamma * G + r
            if (s, a) not in visited_state_actions:
                visited_state_actions.add((s, a))
                returns_sum[s][a] += G
                returns_count[s][a] += 1
                Q[s][a] = returns_sum[s][a] / returns_count[s][a]

    return Q

if __name__ == "__main__":
    print("Training Monte Carlo Agent...")
    Q_table = train_monte_carlo(episodes=100000)
    print(f"Training Complete! Unique states learned: {len(Q_table)}")
