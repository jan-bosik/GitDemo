# -*- coding: utf-8 -*-
from typing import List, Dict, Optional
import termcolor
from dataclasses import dataclass, field
from sys import exit


@dataclass
class Player:
    color: str

    def is_player_id (self, colour : str):
        if colour == self.color:
            return True
        else:
            return False

@dataclass
class Row:
    dimension: int
    # [1, None, 2]    1 pre hraca no.1, 2 pre hraca no.2, None, ak je policko nezabrate
    columns: List[Optional[int]] = field(default_factory=list)

    def __post_init__(self):
        for _ in range(self.dimension):
            self.columns.append(None)

    def print_row(self, player_list: List[Player]):    # !! on musi poznat vsetkych playerov, nie len jedneho  !!

        for column in self.columns:

            if column is None:                                                        # ak je policko volne5
                print(" |", end="")                                                   # vypis " |"
            else:                                                                     # ak je policko zabrate
                player = player_list[column]                                     # najdi v zozname hracov hraca pomocou indexu

                # ak to nie je posledny stlpec
                termcolor.cprint('*', player.color, end="")
                if (self.columns.index(column) + 1) != len(self.columns):
                    #termcolor.cprint('*|', player.color, end="")        # vypis symbol farbou hraca
                    print ("|", end ="")
               # else:
               #     termcolor.cprint('*', player.color, end="")
        print()


@dataclass
class Table:
    dimension: int
    rows: List[Row] = field(default_factory=list)  # [["this, "is", "row", "one"],["this, "is", "row", "two"], ["this, "is", "row", "three"]])

    # This will get called right after __init__()
    def __post_init__(self):
        if self.dimension < 4:
            raise ValueError("Table dimension must be 4 or more.")

        for _ in range(self.dimension):
            new_row = Row(self.dimension)
            self.rows.append(new_row)

    def print_table(self, player_list: List[Player]):
        for row_number, row in enumerate(self.rows):                    # pre prvky listu rows, teda jednotlive riadky; riadok == list stlpcov
            row.print_row(player_list)                      # vypis riadok
            if (row_number+1) != self.dimension:      # a ak to nie je posledny riadok,
                print("-" * (row.dimension * 2 + 1))            # vypis aj oddelovaciu ciaru {'-' * pocet stlpcov}

    def write(self, player, row: int, column: int, game: 'Game'):
        tile = game.players.get(player)              # zo dictionary hracov players najdi hodnotu pre zvoleneho hraca
        self.rows[row][column] = tile           # najdi specifikovany riadok a stlpec a oznac ho hodnotou hraca

    def vertical(self, player_turn: int): # treba mu passnut nie playera, ale rovno cislo hraca, ktory je na tahu. Namiesto blinu na riadku 79 sa len porovnaju inty

        r_index = 0
        while r_index < len(self.rows):
            c_index = 0
            while c_index < len(self.rows[c_index].columns) - 1:  # sem som pridal -1, lebo inak sem skakala 5 a hadzalo error
                count = 0
                for i in range(4):
                    if player_turn == self.rows[r_index + i].columns[c_index]:  # ked sa r_index dostane na max, teda 4, tak uz k nemu nemozno pridavat i, inak hodi index out of range error
                        count += 1
                        i += 1
                    else:
                        break
                if count == 4:
                    print(f"vertical: Game over at [{r_index},{c_index}]")
                    return

                c_index += 1
            r_index += 1


    def r_diagonal(self, player_turn: int):
        r_index = 0
        while r_index < len(self.rows):  # pridal som -1,. aby nedoslo na scenar, kde rindex bude 4 a rindex + i bude 5 == index out of range. UZ som to dal prec.
            c_index = 0
            while c_index < len(self.rows[c_index].columns) - 1:  # sem som pridal -1, lebo inak sem skakala 5 a hadzalo error
                count = 0
                for i in range(4):
                    if player_turn == self.rows[r_index + i].columns[c_index + i]:  # ked sa r_index dostane na max, teda 4, tak uz k nemu nemozno pridavat i, inak hodi index out of range error
                        count += 1
                        i += 1
                    else:
                        break
                if count == 4:
                    print(f"r_diagonal: Game over at [{r_index},{c_index}]")
                    return

                c_index += 1
            r_index += 1


    def l_diagonal(self, player_turn: int):

        r_index = 0
        while r_index < len(self.rows):
            c_index = len(self.rows[r_index].columns) - 1
            while c_index >= 0:
                count = 0
                for i in range(4):
                    if player_turn == self.rows[r_index + i].columns[c_index - i]:
                        count += 1
                        i += 1
                    else:
                        break
                if count == 4:
                    print(f"l_diagonal: Game over at [{r_index},{c_index}]")
                    return

                c_index -= 1
            r_index += 1


    def horizontal(self, player_turn: int):

        r_index = 0
        while r_index < len(self.rows):
            c_index = 0
            while c_index < len(self.rows[c_index].columns) -1:  # sem som pridal -1, lebo inak sem skakala 5 a hadzalo error
                count = 0
                for i in range(4):
                    if player_turn == self.rows[r_index].columns[c_index + i]:
                        count += 1
                        i += 1
                    else:
                        break
                if count == 4:
                    print(f"horizontal: Game over at [{r_index},{c_index}]")
                    return

                c_index += 1
            r_index += 1


@dataclass
class Game:         # ak nebude existovat ziaden instance classu Game, tie  metody v nej budu na nic
    dimension: Optional[int] = None
    turn: int = 0
    players: List[Player] = field(default_factory=list)
    table: Table = None

    def check_for_player_symbol (self, symbol:str):
        for player in self.players:

            if player.id == symbol:
                print("This symbol has already been assigned to a different player.")
                return True

        else:
            return False


    def check_for_player_colour (self, colour:str):
        for player in self.players:

            if player.colour == colour:
                print("This colour has already been assigned to a different player.")
                return True

        else:
            return False

    def create_player(self):    # treba sem dodat nejake while, aby ked sa zada symbol/farba, ktora nie je volna sa to vratilo na zaciatok a poziadalo o zadanie znova

        player_id = input("Please, enter the symbol for this player (in unicode): ")    # poziadaj o symbol hraca
        if self.check_for_player_symbol(player_id) is False:                            # ak symbol nie je zabraty

            player_colour = input("Please, enter the colour for this player: ")             # poziadaj o farbu
            if self.check_for_player_colour(player_colour) is False:                        # ak farba nie je zabrata

                new_player = Player(player_id, player_colour)                           # vytvor noveho hraca s farbou a symbolom ake boli zadane
                return new_player                                                           # vrat noveho hraca

    def load_player(self, player: Player):
        self.players.append (player)

    def get_player(self, index):
        player_found = self.players.get(index)  # v dictionary hracov self.players najdi hodnotu podla indexu hraca
        return player_found

    def player_turn(self):
        player = self.players [self.turn]
        print ("It's {0} player's turn!".format (player.color))


    def end_turn(self):
        if self.turn != len(self.players) - 1:  # ak nie je self.turn na maximalnej hodnote / ak nie je na tahu posledny hrac
            self.turn += 1                      # zvys self.turn o 1
        else:                                   # inak
            self.turn = 0                       # nastav turn na 0 a chod od zaciatku

    def game_over(self, player: Player):
        print("{0} player is the winner! Well played!".format(player.color.title()))
        exit()

    # Asks for table dimension and creates it
    def initialize_table(self):
        self.dimension = int(input("Enter table dimension: "))
        self.table = Table(self.dimension)

    #
    def initialize_players(self):
        for player_index in range(2):
            player_color = input(f"Enter player's [{player_index}] color: ")
            new_player = Player(player_color)
            self.players.append(new_player)

    def show_table(self):
        self.table.print_table(self.players)

    def is_over(self) -> bool:
        if self.table.vertical(self.turn):
            return True
        if self.table.horizontal(self.turn):
            return True
        if self.table.r_diagonal(self.turn):
            return True
        if self.table.l_diagonal(self.turn):
            return True

        return False

    def get_player_input (self) -> tuple:
        player_row = int(input("Enter row, please: "))
        player_col = int(input("Enter column, please: "))

        return player_row, player_col

    def update_table (self, row: int, column: int):

        if self.table.rows[row].columns[column] is None:
            self.table.rows[row].columns[column] = self.turn # zapise sa cislo hraca, ktory je akurat na tahu

        else:
            print("This tile is already taken.")

    def is_free (self, row: int, col: int) -> bool:
        if self.table.rows[row].columns[col] is None:
            return True
        else:
            return False


game = Game() # Asks for table dimension and creates it
game.initialize_table()
game.initialize_players()
game.show_table()


while not game.is_over():
    game.player_turn()

    coordinates = game.get_player_input()
    while game.is_free(coordinates[0], coordinates[1]) is False:
        print("\nOops!It looks like that tile is already taken. Try again. \n")
        coordinates = game.get_player_input()

    game.update_table (coordinates[0], coordinates[1])
    game.show_table()
    game.end_turn()

