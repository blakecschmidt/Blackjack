import random

class Card:

    def __init__(self, rank, suit):
        if rank.isalpha() and rank != "A":
            self.value = 10
        elif rank == "A":
            self.value = 11
        else:
            self.value = int(rank)
        self.rank = rank
        self.suit = suit
        self.name = rank + suit

    def __str__(self):
        return (self.name)

class Deck:


    def __init__(self):
        suit = ["C", "D", "H", "S"]
        rank = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        self.cardList = []
        for i in suit:
            for j in rank:
                self.cardList.append(Card(j, i))

    def __str__(self):
        st = ""
        count = 0
        for card in self.cardList:
            if card.rank == "10":
                st += " "
                st += str(card)
            else:
                st += "  "
                st += str(card)
            count += 1
            if count % 13 == 0:
                st += "\n"
        return st

    def shuffle(self):
        random.shuffle(self.cardList)

    def dealOne(self, player):
        player.hand.append(self.cardList[0])
        player.handTotal += self.cardList[0].value
        self.cardList.remove(self.cardList[0])

class Player:

    def __init__(self):
        self.hand = []
        self.handTotal = 0

    def __str__(self):
        st = ""
        for card in self.hand:
            st += str(card)
            st += "  "
        return st

bust = False

def playerTurn(cardDeck, player):
    x = 1
    hasA11 = 0

    if player.hand[0].rank == "A" and player.hand[1].rank == "A":
        hasA11 = 1
        print("You have two aces. Assuming 11 points for one ace and 1 point for the other.")
        player.handTotal = 12
    elif player.hand[0].rank == "A" or player.hand[1].rank == "A":
        hasA11 = 1
        print("Assuming 11 points for an ace you were dealt for now.")

    print("You hold", player, "for a total of", player.handTotal)
    x = int(input("1 (hit) or 2 (stay)? "))

    while x == 1:
        cardDeck.dealOne(player)
        print("\nCard dealt:", player.hand[-1])

        if player.hand[-1].rank == "A":
            hasA11 += 1
        if player.handTotal > 21 and hasA11 > 0:
            print("Over 21. Switching an ace from 11 points to 1.")
            hasA11 -= 1
            player.handTotal -= 10
        elif player.handTotal > 21:
            print("New total:", player.handTotal)
            print("Player busts! You lose.")
            global bust
            bust = True
            return
        elif player.handTotal == 21:
            print("21!")
            return

        print("New total:", player.handTotal, "\n")
        print("You hold", player, "for a total of", player.handTotal)
        x = int(input("1 (hit) or 2 (stay)? "))

    if x == 2:
        print("Staying with", player.handTotal)

def dealerTurn(cardDeck, player, dealer):
    hasA11 = 0

    print("\nYou hold", player, "for a total of", player.handTotal)
    print("Dealer holds", dealer, "for a total of", dealer.handTotal)

    if dealer.hand[0].rank == "A" and dealer.hand[1].rank == "A":
        hasA11 = 1
        print("\nDealer has two aces. Assuming 11 points for one ace and 1 point for the other.")
        dealer.handTotal = 12
    elif dealer.hand[0].rank == "A" or dealer.hand[1].rank == "A":
        hasA11 = 1
        print("\nAssuming 11 points for an ace the dealer was dealt for now.")

    while True:
        if dealer.handTotal < player.handTotal:
            cardDeck.dealOne(dealer)
            print("\nDealer hits:", dealer.hand[-1])
            print("New total:", dealer.handTotal)
        elif dealer.handTotal >= player.handTotal and dealer.handTotal <= 21:
            print("Dealer has " + str(dealer.handTotal) + ". Dealer wins.")
            return

        if dealer.hand[-1].rank == "A":
            hasA11 += 1
        if dealer.handTotal > 21 and hasA11 > 0:
            print("\nOver 21. Switching an ace from 11 points to 1.")
            hasA11 -= 1
            dealer.handTotal -= 10
            print("New total:", dealer.handTotal)
        elif dealer.handTotal > 21:
            print("\nDealer has " + str(dealer.handTotal) + ". Dealer busts! You win.")
            return


def main():

    cardDeck = Deck()
    print("Initial Deck:")
    print(cardDeck)

    cardDeck.shuffle()
    print("Shuffled Deck:")
    print(cardDeck)

    player = Player()
    dealer = Player()

    cardDeck.dealOne(player)
    cardDeck.dealOne(dealer)
    cardDeck.dealOne(player)
    cardDeck.dealOne(dealer)

    print("Deck after dealing two cards each:")
    print(cardDeck)

    print("\nDealer shows", dealer.hand[0], "faceup.")
    print("You show", player.hand[0], "and", player.hand[1], "faceup.\n")
    print("You go first.\n")

    playerTurn(cardDeck, player)

    if bust == False:
        print("\nDealer's turn")
        dealerTurn(cardDeck, player, dealer)

    print("\nGame over.")
    print("Final hands:")
    print("\tDealer:", dealer)
    print("\tPlayer:", player)


main()