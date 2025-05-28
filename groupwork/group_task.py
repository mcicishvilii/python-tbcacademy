import random
from collections import Counter

def create_deck():
    suits = ["S", "H", "D", "C"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    return [r + " of " + s for s in suits for r in ranks] * 4

rank_values = {
    "2": 2, "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10, "J": 11, "Q": 12, "K": 13, "A": 20
}

def deal_hand(deck, hand_size=5):
    return [deck.pop() for _ in range(hand_size)]

def max_same_suit_count(hand):
    suits = [card.split(" of ")[1] for card in hand]
    return max(Counter(suits).values())

def max_same_rank_count(hand):
    ranks = [card.split(" of ")[0] for card in hand]
    return max(Counter(ranks).values())

def calculate_score(hand):
    ranks = [card.split(" of ")[0] for card in hand]
    return sum(rank_values[rank] for rank in ranks)

def print_player_data(players):
    for p in players:
        print(f"{p['player']}: {p['hand']} | Score: {p['score']}")

def player_replacement(player_data, deck):
    print(f"\n{player_data['player']}, your hand is: {player_data['hand']}")
    while True:
        try:
            to_replace = int(input(f"{player_data['player']}, choose the card number to replace (1-5), or 0 to keep all: "))
            if to_replace == 0:
                print("No cards replaced.")
                return
            if 1 <= to_replace <= 5:
                old_card = player_data['hand'][to_replace - 1]
                new_card = deck.pop()
                player_data['hand'][to_replace - 1] = new_card
                print(f"Replaced {old_card} with {new_card}")
                return
            else:
                print("Invalid input. Please enter a number between 0 and 5.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def main():
    print("Welcome to the card game!")
    players_names = []
    for i in range(3):
        name = input(f"Please enter player {i+1} name: ")
        players_names.append(name)

    while len(players_names) > 1:
        deck = create_deck()
        random.shuffle(deck)
        players_data = []
        for player in players_names:
            hand = deal_hand(deck)
            score = calculate_score(hand)
            players_data.append({"player": player, "hand": hand, "score": score})

        print("\n--- New Round ---")
        print_player_data(players_data)
        highest_score = max(p["score"] for p in players_data)
        top_players = [p for p in players_data if p["score"] == highest_score]

        if len(top_players) > 1:
            for p in top_players:
                p["suit_count"] = max_same_suit_count(p["hand"])
            max_suit = max(p["suit_count"] for p in top_players)
            top_players = [p for p in top_players if p["suit_count"] == max_suit]

        if len(top_players) > 1:
            for p in top_players:
                p["rank_count"] = max_same_rank_count(p["hand"])
            max_rank = max(p["rank_count"] for p in top_players)
            top_players = [p for p in top_players if p["rank_count"] == max_rank]

        if len(top_players) > 1:
            print("\nTie persists after tie-breakers.")
            print("Players tied can choose to replace one card or keep their hand.")
            for player in top_players:
                player_replacement(player, deck)
                player["score"] = calculate_score(player["hand"])
            highest_score = max(p["score"] for p in players_data)
            top_players = [p for p in players_data if p["score"] == highest_score]

            if len(top_players) > 1:
                for p in top_players:
                    p["suit_count"] = max_same_suit_count(p["hand"])
                max_suit = max(p["suit_count"] for p in top_players)
                top_players = [p for p in top_players if p["suit_count"] == max_suit]

            if len(top_players) > 1:
                for p in top_players:
                    p["rank_count"] = max_same_rank_count(p["hand"])
                max_rank = max(p["rank_count"] for p in top_players)
                top_players = [p for p in top_players if p["rank_count"] == max_rank]

            if len(top_players) > 1:
                print("\nStill tied after replacement phase! No one is eliminated this round.")
            else:
                winner = top_players[0]
                print(f"\n🏆 {winner['player']} wins the round after replacement!")
        else:
            winner = top_players[0]
            print(f"\n🏆 {winner['player']} wins the round!")

        lowest_score = min(p["score"] for p in players_data)
        lowest_players = [p for p in players_data if p["score"] == lowest_score]

        if len(lowest_players) == len(players_data):
            print("\nAll players have the same score. No one eliminated.")
        elif len(lowest_players) > 1:
            print(f"\nTie for lowest score between {', '.join(p['player'] for p in lowest_players)}. No elimination.")
        else:
            eliminated_player = lowest_players[0]["player"]
            print(f"\n {eliminated_player} is eliminated from the game.")
            players_names.remove(eliminated_player)

        print(f"\nPlayers remaining: {', '.join(players_names)}")

    print(f"\n🎉 {players_names[0]} is the overall winner! Congratulations!")

if __name__ == "__main__":
    main()

