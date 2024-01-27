
from const import*
from square import Square
from piece import *
from move import Move
class Board:
    def __init__(self):
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(COLS)]

        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        self.last_move = None
    
         
    def move(self, piece,move):
        initial = move.initial
        final = move.final

        # move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # move
        piece.moved = True

        # clear valid move
        piece.clear_moves()

        # update last move
        self.last_move = move


    
    def valid_move(self, piece,move):
        return move in piece.moves

    def calc_moves(self, piece, row ,col):
        '''
        Calculate all possible moves for a given piece
        '''
        # method for piece move
        def pawn_moves():
            # step
            steps = 1 if piece.moved  else 2
            # vertical
            start = row + piece.dir
            end = row + piece.dir * (1+ steps)
            for posssible_move_row in range(start, end, piece.dir):
                if Square.in_range(posssible_move_row):
                    if self.squares[posssible_move_row][col].is_empty():
                     
                        initial = Square(row, col)
                        final = Square(posssible_move_row, col)
                        move = Move(initial, final)
                        piece.add_move(move)
                    else:
                        break
                else:
                    break
            # diagonal
            posssible_move_row = row + piece.dir
            posssible_move_col = [col - 1, col + 1]
            for posssible_move_col in posssible_move_col:
                if Square.in_range(posssible_move_row, posssible_move_col):
                    if self.squares[posssible_move_row][posssible_move_col].has_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(posssible_move_row, posssible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)


        def knight_moves():
            possible_moves = [
                (row - 2, col - 1), (row - 2, col + 1),
                (row - 1, col - 2), (row - 1, col + 2),
                (row + 1, col - 2), (row + 1, col + 2),
                (row + 2, col - 1), (row + 2, col + 1)
            ]
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        # create square of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create new move
                        move = Move(initial, final)
                        # append new valid move
                        piece.add_move(move)
        
        def straight_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # create square of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create new move
                        move = Move(initial, final)
                        # has friendly == break loop
                        if self.squares[possible_move_row][possible_move_col].has_friendly(piece.color):
                            break
                    
                        # empty == coninue loop
                        if self.squares[possible_move_row][possible_move_col].is_empty:
                            # append new valid move
                            piece.add_move(move)


                        #has enemy == break after move
                        if self.squares[possible_move_row][possible_move_col].has_rival(piece.color):
                            piece.add_move(move)
                            break

                    else:
                        break
                        
                    # incrementing incrs
                    possible_move_row, possible_move_col = possible_move_row + row_incr, possible_move_col + col_incr
        
        def king_moves():
            adjs = [
                 (row-1, col+0), # up
                (row-1, col+1), # up-right
                (row+0, col+1), # right
                (row+1, col+1), # down-right
                (row+1, col+0), # down
                (row+1, col-1), # down-left
                (row+0, col-1), # left
                (row-1, col-1), # up-left
            ]
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        # create square of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create new move
                        move = Move(initial, final)
                        # append new valid move
                        piece.add_move(move)
                        
        #castling moves
        
        #queen side
        
        # king side
        
        if isinstance(piece, Pawn):pawn_moves()
        elif isinstance(piece, Knight):knight_moves()
        elif isinstance(piece, Bishop):straight_moves([
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ])
        elif isinstance(piece, Rook):straight_moves([
            (-1, 0), (0, 1), (1, 0), (0, -1)
        ])
        elif isinstance(piece, Queen):straight_moves([
            (-1, -1), (-1, 1), (1, -1), (1, 1),
            (-1, 0), (0, 1), (1, 0), (0, -1)
        ])
        elif isinstance(piece, King):king_moves()
        


    def _create(self):
       
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        
       
        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))

        #test piece
        # self.squares[5][0] = Square(5, 0, Pawn(color))
        # self.squares[4][4] = Square(4, 4, Knight(color))
        # self.squares[4][4] = Square(4, 4, Rook(color))
        # self.squares[4][4] = Square(4, 4, Bihop(color))
        # self.squares[4][4] = Square(4, 4, Queen(color))
        # self.squares[4][4] = Square(4, 4, King(color))
        
