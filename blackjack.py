import random

values = {r: i for i, r in enumerate('123456789', 1)}
for r in ["Ten", "Jack", "Queen", "King"]:
    values[r] = 10
values["Ace"] = 11

class Blackjack():
    def __init__(self):
        self.values = values
        self.original_deck = ["2", "3", "4", "5", "6", "7", "8", "9", "Ten", "Jack", "Queen", "King", "Ace"] * 4
        self.deck = self.original_deck.copy()
        self.player_hands = {"Player": [], "Dealer": []}
        self.wins = 0
        self.losses = 0
        self.ties = 0

    def evaluate_hand(self, hand):
        handval = 0
        for card in hand:
            handval += values[card]
            if handval > 21:
                break
        if "Ace" in hand and handval > 21:
            print("To prevent busting, an Ace is re-evaluated to have the value of 1.")
            hand[hand.index("Ace")] = "1"
            handval = self.evaluate_hand(hand)
        return handval
    
    def article(self, string):
        if string.startswith("A"):
            return f"an {string}"
        return f"a {string}"

    def deal_to(self, cards, player_name):
        player = self.player_hands[player_name]
        dealt = self.deck[:cards]
        self.deck = self.deck[cards:]
        for card in dealt:
            player.append(card)
        dealt = ', '.join(dealt)
        if cards > 1:
            if player_name == "Player":
                print(f"You are dealt {dealt}.")
            else:
               print(f"The dealer deals themselves {cards} cards and reveals {self.article(player[0])}.")
        elif player == "Player":
            print(f"You are dealt {self.article(dealt)}.")
        else:
            print(f"The dealer deals themselves {self.article(dealt)}.")

    def dealt(self, dealt):
        return print(f"You are dealt {'an ' + dealt if dealt.startswith('A') else 'a ' + dealt}.")

    def start_round(self):
        for player in self.player_hands.keys():
            self.player_hands[player] = []
        remaining = len(self.deck)
        if remaining < 20:
            print(f"The deck had {remaining} cards remaining and so has been shuffled.")
            self.deck = self.original_deck.copy()
        random.shuffle(self.deck)
        for player in self.player_hands.keys():
            self.deal_to(2, player)

    def turn(self):
        bust = False
        dealer_hand_val = self.evaluate_hand(self.player_hands["Dealer"])
        player_hand_val = self.evaluate_hand(self.player_hands["Player"])
        if player_hand_val == 21:
            print("Your hand is a natural blackjack!")
            if dealer_hand_val != 21:
                print(f"The dealer's hand value of {dealer_hand_val} is not a natural blackjack, so you win!")
                self.wins += 1
            else:
                print(f"The dealer's hand value of {dealer_hand_val} is also a natural blackjack, so you tie!")
                self.ties += 1
            return True
        while True:
            if player_hand_val <= 21:
                decision = input(f"Your hand of {', '.join(self.player_hands['Player'])} has a value of {player_hand_val}.\n [H]it or [S]tick? >")
                decision = decision.lower()
                if decision in ["h", "hit", "y"]:
                    self.deal_to(1, "Player")
                    player_hand_val = self.evaluate_hand(self.player_hands["Player"])
                    continue
            else:
                bust = True
            break
        if bust:
            print(f"You bust with a hand of {', '.join(self.player_hands['Player'])} valuing {player_hand_val}!")
            self.losses += 1
            return True
        if dealer_hand_val == 21:
            print(f"The dealer had a natural blackjack, so you lost!")
            self.losses += 1
            return True
        while (dealer_hand_val < player_hand_val) and (dealer_hand_val < 22):
            self.deal_to(1, "Dealer")
            dealer_hand_val = self.evaluate_hand(self.player_hands["Dealer"])
            print(f"The dealer has a hand of {', '.join(self.player_hands['Dealer'])} with a value of {dealer_hand_val}.")
        if dealer_hand_val > 21:
            print(f"The dealer's hand value of {dealer_hand_val} lost to your hand value of {player_hand_val}!")
            self.wins += 1
        elif dealer_hand_val > player_hand_val:
            print(f"The dealer's hand value of {dealer_hand_val} beat your hand value of {player_hand_val}!")
            self.losses += 1
        else:
            print(f"The dealer's hand value of {dealer_hand_val} drew with your hand value of {player_hand_val}!")
            self.ties += 1
        return True

    def play(self):
        while True:
            self.start_round()
            if self.turn():
                print(f"Your statistics for this session are {self.wins} wins, {self.losses} losses and {self.ties} ties!")
                decision = input("Play again? [Y]/[N] >")
                decision = decision.lower()
                if decision in ["y", "yes"]:
                    continue
                print("Thanks for playing!")
                break

blackjack = Blackjack()
blackjack.play()
