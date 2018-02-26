import random


class Card:
    """
    A class used to create object of single cards.
    """

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return '{} of {}'.format(self.rank, self.suit)


class Deck:
    """
    A class used to manipulate the Card class objects.
    """

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n ' + card.__str__()  # add each Card object's print string
        return 'The deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    """
    A class used to create the player's / dealer's actions in the game.
    """
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    """
    A class used to store the player's account balance.
    """
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    """
    The function is used to make bets by the player.
    :param chips: Balance of player's account.
    :return:
    """
    while True:

        try:
            chips.bet = int(input('How many chips would You like to bet? '))

        except ValueError:
            print('Sorry! Bet must to be integer!')

        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed: ", chips.total)

            else:
                break


def hit(deck, hand):
    """
    The function is used to take cards by the player / dealer.
    :param deck:
    :param hand:
    :return:
    """
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    """
    The function is used to take the card or to end its turn.
    :param deck: - Deck of available cards.
    :param hand: - Hand of player.
    :return:
    """
    global playing  # to control an upcoming while loop

    while True:

        x = input("Would you like to Hit or Stand? Enter 'h' or 's' ")

        if x[0].lower() == 'h':

            hit(deck, hand)  # hit() function defined above

        elif x[0].lower() == 's':

            print("Player stands. Dealer is playing.")
            playing = False

        else:

            print("Sorry, please try again.")
            continue

        break


def show_some(player, dealer):
    """
    Function is used to show hands of player and dealer.
    :param player: Hand of player.
    :param dealer: Hand of dealer.
    :return:
    """
    print("\nDealer's Hand:")
    print(" <Card Hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')


def show_all(player, dealer):
    """
    The function shows all player and dealer cards.
    :param player: Hand of player.
    :param dealer: Hand of dealer.
    :return:
    """
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("\nDealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("\nPlayer's Hand =", player.value)


def player_busts(chips):
    """
    The function updates the player's account after busting.
    :param chips: - Balance of player account.
    :return:
    """
    print('Player busts!')
    chips.lose_bet()


def player_wins(chips):
    """
    The function updates the player's account after winning.
    :param chips: - Balance of player account.
    :return:
    """
    print('Player wins!')
    chips.win_bet()


def dealer_busts(chips):
    """
    The function updates the player's account after dealer's busting.
    :param chips: - Balance of player account.
    :return:
    """
    print('Dealer busts!')
    chips.win_bet()


def dealer_wins(chips):
    """
    The function updates the player's account after dealer's winning.
    :param chips: - Balance of player account.
    :return:
    """
    print('Dealer wins!')
    chips.lose_bet()


def push():
    """
    The function shows a push message.
    """
    print("Dealer and Player tie! It's a push.")


# Initializing data to the card deck and setting the game to the player's turn.

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
playing = True

# The loop performs the Black Jack game according to simplified rules.

while True:

    print('Welcome to BlackJack! Get as close to 21 as you can without going over!')
    print('Dealer hits until she reaches 17. Aces count as 1 or 11.')

    game_deck = Deck()
    game_deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(game_deck.deal())
    player_hand.add_card(game_deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(game_deck.deal())
    dealer_hand.add_card(game_deck.deal())

    player_chips = Chips()

    take_bet(player_chips)

    show_some(player_hand, dealer_hand)

    while playing:

        hit_or_stand(game_deck, player_hand)

        show_some(player_hand, dealer_hand)

        if player_hand.value > 21:
            player_busts(player_chips)
            break

    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(game_deck, dealer_hand)

        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_chips)

        else:
            push()

    print("\nPlayer's winnings stand at", player_chips.total)

    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thanks for playing!")
        break
