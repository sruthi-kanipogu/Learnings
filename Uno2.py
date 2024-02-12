from __future__ import annotations
import random

class Card:

    def __init__(self, colour: str, name: str) -> None:
        self.colour = colour
        self.name = name

    def __repr__(self) -> str:
        return f'({self.colour}: {self.name})'
    
class Player:

    def __init__(self, name: str) -> None:
        self.name = name
        self.hand = []

    def add_card(self, card: Card) -> None:
        self.hand.append(card)

    def remove_card(self, card: Card) -> None:
        self.hand.remove(card)

    def __repr__(self) -> str:
        return f'{self.name}: {self.hand}'
    
class Uno:

    COLOURS = ["GREEN", "YELLOW", "RED", "BLUE"]
    NUMBERED_CARDS = ["0","1", "2", "3", "4", "5", "6", "7", "8", "9"]
    SPECIAL_CARDS = ["DRAW TWO", "REVERSE", "SKIP"]
    WILD_CARDS = ["WILD", "DRAW FOUR"]

    def __init__(self) -> None:
        self.deck = self._generate_deck()
        self.num_players = 0
        self.players = []
        self.discard_pile = []

    def _generate_deck(self) -> list[Card]:
        deck = []
        for clr in self.COLOURS:
            for value in self.NUMBERED_CARDS:
                if value == "0":
                    deck.append(Card(clr, value))
                    continue
                for _ in range(2):
                    deck.append(Card(clr, value))
            for value in self.SPECIAL_CARDS:
                for _ in range(2):
                    deck.append(Card(clr, value))
        for _ in range(4):
            for value in self.WILD_CARDS:
                deck.append(Card("WILD", value))
        return deck
    
    def shuffle_deck(self) -> None:
       random.shuffle(self.deck)

    def distribute_cards(self) -> None:
        self.shuffle_deck()
        for player in self.players:
            for _ in range(7):
                player.add_card(self.deck.pop())

    def add_player(self, name: str) -> None:
        self.players.append(Player(name))

    def initilizing_players(self) -> None:
        self.num_players = int(input("Enter number of players: "))
        for _ in range(self.num_players):
            self.add_player(input(f'Enter Player name: '))

    def update_open_card(self) -> None:
        self.open_card = self.discard_pile[len(self.discard_pile) - 1]

    def update_discard_pile(self) -> None:
        self.discard_pile.append(self.open_card)

    def next_index(self) -> int:
        return (self.index + 1) % self.num_players

    def initiate_open_card(self) -> bool:
        self.open_card =  self.deck.pop()
        self.compare_card = self.open_card
        while self.open_card.colour in  self.WILD or self.open_card.name in self.SPECIAL_CARDS:
            self.deck.insert(0, self.open_card)
            self.open_card =  self.deck.pop()
        self.update_discard_pile()

    def reverse(self) -> bool:
        if not self.check_possibility():
            return False
        print("\nThe direction is reversed")
        player = self.players[self.index]
        self.players = self.players[::-1]
        self.index = self.players.index(player)

    def skip(self) -> bool:
        if not self.check_possibility():
            return False
        print(f'\n{self.players[self.next_index()]}s turn is skipped')
        self.index = self.next_index() 
        return True

    def draw_two(self) -> bool:
        if not self.check_possibility():
            return False
        for _ in range(2):
            self.players[self.next_index()].add_card(self.deck.pop()) 
        print(f'\nTwo cards from deck have been added to \n{self.players[self.next_index()]} players hand')
        self.index = self.next_index() 
        return True
    
    def draw_four(self) -> bool:
        for _ in range(4):
            self.players[self.next_index()].add_card(self.deck.pop())
        self.play_wild_card()
        print(f'\nFour cards from deck have been added to \n{self.players[self.next_index()]} players hand')   
        self.index = self.next_index()  
        return True
    
    def play_wild_card(self) -> bool:
        if self.play_card.colour == self.WILD:
            self.open_card.name = ""
            self.open_card.colour = input(" \nChoose colour: YELLOW/GREEN/BLUE/RED: ").upper()
            print(f' \nColour changed to {self.open_card.colour}')
            return True
        return False
         
    DRAW_FOUR ="DRAW FOUR"
    DRAW_TWO = "DRAW TWO"
    SKIP = "SKIP"
    WILD = "WILD"
    REVERSE = "REVERSE"

    SKIPPERS = {DRAW_FOUR: draw_four, DRAW_TWO: draw_two, SKIP: skip, REVERSE : reverse}

    def is_special_card(self) -> bool:
        if self.play_card.name in self.SKIPPERS.keys():
            return self.SKIPPERS[self.play_card.name](self)
        return False
    
    def check_possibility(self) -> bool:
        return self.open_card.colour == self.play_card.colour or self.open_card.name == self.play_card.name
    
    def playing_card(self, player: Player) -> None:
        valid_card = False
        while not valid_card:
            ip = input("\nEnter the card number if you want to play or Enter 'DRAW' to draw a card: ")
            if ip.upper() == "DRAW":
                player.add_card(self.deck.pop())
                break
            elif not ip.isdigit():
                print("\nInvalid Input")
            elif int(ip) in range(0, len(player.hand) + 1):
                self.play_card = player.hand[int(ip) - 1]
                if self.is_special_card():
                    valid_card = True
                    player.remove_card(self.play_card)
                elif self.play_wild_card():
                    valid_card = True
                    player.remove_card(self.play_card)
                    self.update_discard_pile()
                elif self.check_possibility():
                    valid_card = True
                    player.remove_card(self.play_card)
                    self.open_card = self.play_card
                    self.update_discard_pile()
                else:
                    print("\nInvalid Card")
            else:
                print("\nInvalid Card")
        
    def game_starts(self):
        game_over = False
        self.index = 0
        while not game_over:
            player = self.players[self.index]
            print(f'\nOpen Card is: {self.open_card}')
            print(player)
            self.playing_card(player)
            self.index = self.next_index()
            if len(player.hand) == 0:
                print(f'\n{player.name} is the winner')
                game_over = True
                break

    def play(self) -> str:
        self.initilizing_players()
        self.distribute_cards()
        self.initiate_open_card()
        self.game_starts()

Uno().play()