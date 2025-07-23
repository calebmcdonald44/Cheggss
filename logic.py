# CHEGGSS V1.0

# At some point need a day to try and clean up comments
# Any way to avoid cls.currGame all the time?
# classmethod vs staticmethod
# figure out user_move vs user_input (okay to make prop name variable name?)
# also, user_input should not be prop/variable names in functions that will be used for engine moves
# probably shortend start_square and end_square to st_sq and end_sq

# !
# need to figure out how to set everything (en_passant, half_moves, etc.) at the end of make_move()
# also update logic in line 404 and 416
# !

class Piece():
    # might not need these
    empty_square = '-'

    black_king = 'k'
    black_queen = 'q'
    black_rook = 'r'
    black_bishop = 'b'
    black_knight = 'n'
    black_pawn = 'p'

    white_king = 'K'
    white_queen = 'Q'
    white_rook = 'R'
    white_bishop = 'B'
    white_knight = 'N'
    white_pawn = 'P'
    
    @classmethod
    def color(cls, piece):
        if piece.islower():
            return 'b'
        if piece.isupper():
            return 'w'
        return '-'

class Board():
    # empty_board = [[], [], [], [], [], [], [], []]
    STARTING_BOARD_STATE = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ]
    # starting_game_state = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    # # Will this cause game state to reset everytime Board is instantiated?
    # # Maybe these should be kept in class Game() or something
    # board_state = starting_board_state
    # game_state = starting_game_state

    game_state = {
        "board_state": [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', 'n', '-', '-', '-'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
        ],
        "to_move": "b",
        "castling_rights": {
            "white": {
                "king_side": True,
                "queen_side": True,
            },
            "black": {
                "king_side": True,
                "queen_side": True,
            }
        },
        "en_passant_target_square": None,
        "halfmove_clock": 0,
        "fullmove_number": 1,
    }


    unicode_dict = {
        'k': '♔',
        'q': '♕',
        'r': '♖',
        'b': '♗',
        'n': '♘',
        'p': '♙',
        'K': '♚',
        'Q': '♛',
        'R': '♜',
        'B': '♝',
        'N': '♞',
        'P': '♟',
        '-': '-'
    }

    # @classmethod
    # def build_position_from_fen(cls, fen_string):
    #     current_position = []
    #     current_rank = []
    #     rank_count = 1
    #     for chr in fen_string:
    #         if rank_count > 8:
    #             return current_position
    #             # More to do
    #         elif chr.isalpha():
    #             current_rank.append(chr)
    #         # (Possibly) don't need to loop for this
    #         elif chr.isnumeric():
    #             for i in range(int(chr)):
    #                 current_rank.append('-')
    #         elif chr == '/':
    #             current_position.append(current_rank)
    #             current_rank = []
    #             rank_count += 1
    #         elif chr == ' ':
    #             if rank_count == 8:
    #                 current_position.append(current_rank)
    #                 current_rank = []
    #                 rank_count += 1
    #                 continue
    #             # More to do
    
    @classmethod
    def render_board(cls, board):
        print("\n")
        board_with_unicode_symbols = [[cls.unicode_dict[cell] for cell in row] for row in board]
        files = 'a b c d e f g h'
        for i, row in enumerate(board_with_unicode_symbols):
            rank = str(8 - i) + ' '
            print(f"{rank} {' '.join(row)}")
        print(f"\n   {files}\n")

class Move():
    # Change end square to target square?
    # takes in square (i.e. "a1") and returns a single number that represents a square.
    # this makes things easier when checking if a move is legal.

    @classmethod
    def map_move_value(cls, user_input):
        start_square, end_square = user_input.split()
        start_square_mapped = 0
        end_square_mapped = 0

        file_map = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
            "g": 7,
            "h": 8,
        }

        for chr in start_square:
            if chr.isalpha():
                start_square_mapped += file_map[chr]
            elif chr.isnumeric():
                start_square_mapped += (int(chr) - 1) * 8

        for chr in end_square:
            if chr.isalpha():
                end_square_mapped += file_map[chr]
            elif chr.isnumeric():
                end_square_mapped += (int(chr) - 1) * 8
                
        return [start_square_mapped, end_square_mapped]
    
    @classmethod
    def map_move_coordinates(cls, user_input):
        start_square, end_square = user_input.split()
        start_square_mapped = 0
        end_square_mapped = 0

        file_map = {
            "a": "0",
            "b": "1",
            "c": "2",
            "d": "3",
            "e": "4",
            "f": "5",
            "g": "6",
            "h": "7",
        }

        rank_map = {
            "1": "7",
            "2": "6",
            "3": "5",
            "4": "4",
            "5": "3",
            "6": "2",
            "7": "1",
            "8": "0",
        }

        for chr in start_square:
            if chr.isalpha():
                start_square_mapped = file_map[chr]
            elif chr.isnumeric():
                start_square_mapped = rank_map[chr] + start_square_mapped

        for chr in end_square:
            if chr.isalpha():
                end_square_mapped = file_map[chr]
            elif chr.isnumeric():
                end_square_mapped = rank_map[chr] + end_square_mapped

        return [start_square_mapped, end_square_mapped]

    @classmethod
    def handle_user_move(cls, start_square, end_square):
        pass

    # first check if piece can move like that
    # then make move and check if king is in check
    # will probably need to pass in square values AND string coordinates
    @classmethod
    def is_legal_move(cls, user_input, game_state=None, proposed_board=None):
        # need to prevent same starting and ending square, and squares
        # that don't exist (a0, z6, etc)

        # VALUES
        # 8    57 58 59 60 61 62 63 64
        # 7    49 50 51 52 53 54 55 56
        # 6    41 42 43 44 45 46 47 48
        # 5    33 34 35 36 37 38 39 40
        # 4    25 26 27 28 29 30 31 32
        # 3    17 18 19 20 21 22 23 24
        # 2    9  10 11 12 13 14 15 16
        # 1    1  2  3  4  5  6  7  8

        #      a  b  c  d  e  f  g  h

        # COORDINATES
        # 8    00 01 02 03 04 05 06 07
        # 7    10 11 12 13 14 15 16 17
        # 6    20 21 22 23 24 25 26 27
        # 5    30 31 32 33 34 35 36 37
        # 4    40 41 42 43 44 45 46 47
        # 3    50 51 52 53 54 55 56 57
        # 2    60 61 62 63 64 65 66 67
        # 1    70 71 72 73 74 75 76 77

        #      a  b  c  d  e  f  g  h
        start_square, end_square = user_input.split()

        square_coordinates = cls.map_move_coordinates(user_input)
        start_square_coordinates = [square_coordinates[0][0], square_coordinates[0][1]]
        end_square_coordinates = [square_coordinates[1][0], square_coordinates[1][1]]
        start_square_rank = int(start_square_coordinates[0])
        start_square_file = int(start_square_coordinates[1])
        end_square_rank = int(end_square_coordinates[0])
        end_square_file = int(end_square_coordinates[1])

        square_values = cls.map_move_value(user_input)
        # start_square_value = square_values[0]
        # end_square_value = square_values[1]

        moving_piece = game_state["board_state"][start_square_rank][start_square_file]

        # making sure a move is actually made
        if start_square == end_square:
            return False
        
        # making sure the correct color is being moved
        if Piece.color(moving_piece) != game_state["to_move"]:
            return False
        # making sure target square is not occupied by friendly piece
        # if Piece.color(game_state["board_state"][end_square_rank][end_square_file]) == game_state["to_move"]:
        #     return False
        
        if moving_piece.upper() == "N":
            return cls.legal_knight_move(game_state, start_square_rank, start_square_file, end_square_rank, end_square_file)

        if moving_piece.upper() == "R":
            return cls.legal_rook_move(game_state, start_square_rank, start_square_file, end_square_rank, end_square_file)
        
        if moving_piece.upper() == "B":
            return cls.legal_bishop_move(game_state, start_square_rank, start_square_file, end_square_rank, end_square_file)
        
        if moving_piece.upper() == "Q":
            return (
                cls.legal_bishop_move(game_state, start_square_rank, start_square_file, end_square_rank, end_square_file) or 
                cls.legal_rook_move(game_state, start_square_rank, start_square_file, end_square_rank, end_square_file)
            )
        
        if moving_piece.upper() == "P":
            retVal, en_passant = cls.legal_pawn_move(game_state, start_square_rank, start_square_file, end_square_rank, end_square_file)
            if retVal:
                game_state["to_move"] = en_passant
            return retVal
        # Need to eventually have a "retVal" variable that these if statements
        # are setting, and get prompt_user_move to handle tuples with en passant
        # information

        # remove this?
        return True
    
    @classmethod
    def legal_rook_move(cls, game_state, start_square_rank, start_square_file, end_square_rank, end_square_file):
        # making sure move is orthagonal
        if (start_square_rank != end_square_rank) and (start_square_file != end_square_file):
            return False

        # horizontal move
        if (start_square_rank == end_square_rank):
            step = +1 if start_square_file < end_square_file else -1
            for file in range((start_square_file + step), (end_square_file + step), step):
                if Piece.color(game_state["board_state"][start_square_rank][file]) == '-':
                    continue # empty square
                elif Piece.color(game_state["board_state"][start_square_rank][file]) == game_state["to_move"]:
                    return False # friendly piece in the way
                else:
                    if file == end_square_file:
                        break
                    return False
            return True
        
        # vertical move
        else:
            step = 1 if start_square_rank < end_square_rank else -1
            for rank in range((start_square_rank + step), (end_square_rank + step), step):
                if Piece.color(game_state["board_state"][rank][start_square_file]) == '-':
                    continue # empty square
                elif Piece.color(game_state["board_state"][rank][start_square_file]) == game_state["to_move"]:
                    return False # friendly piece in the way
                else:
                    if rank == end_square_rank:
                        break # current square is end_square and occupied by opposing piece
                    return False
            return True
        
    @classmethod
    def legal_bishop_move(cls, game_state, start_square_rank, start_square_file, end_square_rank, end_square_file):
        # making sure move is diagonal
        if (abs(end_square_rank - start_square_rank) != abs(end_square_file - start_square_file)):
            return False

        rank_step = 1 if start_square_rank < end_square_rank else -1
        file_step = 1 if start_square_file < end_square_file else -1

        for rank, file in zip(
            range((start_square_rank + rank_step), (end_square_rank + rank_step), rank_step),
            range((start_square_file + file_step), (end_square_file + file_step), file_step)
        ):
            if Piece.color(game_state["board_state"][rank][file]) == '-':
                continue # empty square
            elif Piece.color(game_state["board_state"][rank][file]) == game_state["to_move"]:
                return False # friendly piece in the way
            else:
                if [rank, file] == [end_square_rank, end_square_file]:
                    break # current square is end_square and occupied by opposing piece
                return False 
        return True
    
    @classmethod
    def legal_knight_move(cls, game_state, start_square_rank, start_square_file, end_square_rank, end_square_file):
        rank_offset = start_square_rank - end_square_rank
        file_offset = start_square_file - end_square_file
        if abs(rank_offset) not in (1, 2):
            return False
        if abs(file_offset) not in (1, 2):
            return False
        if abs(file_offset) == abs(rank_offset):
            return False
        # if Piece.color(game_state["board_state"][end_square_rank][end_square_file]) == game_state["to_move"]:
        #     return False
        return True

    @classmethod
    def legal_pawn_move(cls, game_state, start_square_rank, start_square_file, end_square_rank, end_square_file):
        home_rank = 6
        # first_move = False
        legal_rank_increment = -1
        new_en_passant_square = '-'

        if game_state["to_move"] == 'b': # establishing starting rank for pawns
            home_rank = 1
            legal_rank_increment = 1
        if home_rank == start_square_rank: # establishing whether or not a pawn can move forward two spaces
            # first_move = True
            legal_rank_increment *= 2

        rank_offset = end_square_rank - start_square_rank
        file_offset = end_square_file - start_square_file
        two_square_move = False
        en_passant_capture = False

        if file_offset == 0: # forward moves
            if game_state["board_state"][end_square_rank][end_square_file] != '-':
                return False, new_en_passant_square
            if abs(rank_offset) > abs(legal_rank_increment):
                return False, new_en_passant_square
            if (home_rank == 6 and rank_offset > 0) or (home_rank == 1 and rank_offset < 0):
                return False, new_en_passant_square
            if rank_offset == 2 and game_state["board_state"][end_square_rank - 1][end_square_file] == '-': # this logic is wrong
                two_square_move == True 
            # PROMOTION LOGIC HERE

        else: # capturing moves
            legal_rank_increment = legal_rank_increment if abs(legal_rank_increment) == 1 else (legal_rank_increment / 2)
            if abs(file_offset) != 1 or rank_offset != legal_rank_increment:
                return False, new_en_passant_square
            if Piece.color(game_state["board_state"][end_square_rank][end_square_file]) == '-':
                if game_state["en_passant_target_square"] == str(end_square_rank) + str(end_square_file):
                    en_passant_capture = True
                else:
                    return False, new_en_passant_square

        if two_square_move == True:
            new_en_passant_square = str(end_square_rank) + str(end_square_file) # update this logic
        if en_passant_capture:
            game_state["board_state"][end_square_rank][end_square_file - legal_rank_increment] = '-' # removing captured piece in en passant

        return True, new_en_passant_square

    @classmethod
    def legal_king_move(cls, game_state, start_square_rank, start_square_file, end_square_rank, end_square_file):
        pass
    
    @classmethod
    def make_move(cls, move, current_game):
        moving_piece = current_game.game_state["board_state"][int(move[0][0])][int(move[0][1])]
        
        current_game.game_state["board_state"][int(move[1][0])][int(move[1][1])] = moving_piece
        current_game.game_state["board_state"][int(move[0][0])][int(move[0][1])] = Piece.empty_square

        cls.switch_color_to_move(current_game)
        # update game state (whose turn it is, halfmoves, clear en_passant squares, etc.)
        # keeping track of en passant will be tricky. if we clear en passant squares at end
        # of making move, it will clear a square that has just been created. If we want to 
        # set the en passant square outside of legal_pawn_move, it's parent function will have
        # to handle a return of both boolean and string.

    @classmethod
    def switch_color_to_move(cls, current_game):
        if current_game.game_state["to_move"] == 'w':
            current_game.game_state["to_move"] = 'b'
        else:
            current_game.game_state["to_move"] = 'w'

    # EngineMoves class that extends Moves class?
    # generate legal moves function 

