import copy
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

        # promotion
        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)

        # king side castling
        if isinstance(piece, King) :
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.right_rook if diff > 0 else piece.left_rook
                self.move(rook,rook.moves[-1])
        # move
        piece.moved = True

        # clear valid move
        piece.clear_moves()

        # update last move
        self.last_move = move


    
    def valid_move(self, piece,move):
        return move in piece.moves
    
    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)
    
    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)
        
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_rival(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        
        return False


    def calc_moves(self, piece, row ,col, bool = True):
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
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].is_empty():
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                       # create a new move
                        move = Move(initial, final)
                        
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)
                    # blocked
                    else:
                        break
                else:
                    break
            # diagonal
            possible_move_row = row + piece.dir
            possible_move_col = [col - 1, col + 1]
            for possible_move_col in possible_move_col:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival(piece.color):
                        initial = Square(row, col)
                        final_piece =self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col,final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
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
                        final_piece =self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col,final_piece)
                        # create new move
                        move = Move(initial, final)

                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else: break
                        else:
                            # append new move
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
                        final_piece =self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create new move
                        move = Move(initial, final)
                         # empty = continue looping
                        if self.squares[possible_move_row][possible_move_col].is_empty():
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)

                        # has enemy piece = add move + break
                        elif self.squares[possible_move_row][possible_move_col].has_rival(piece.color):
                            # check potencial checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)
                            else:
                                # append new move
                                piece.add_move(move)
                            break

                        # has team piece = break
                        elif self.squares[possible_move_row][possible_move_col].has_friendly(piece.color):
                            break

                    # not in range
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
            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        # create square of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create new move
                        move = Move(initial, final)
                         # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else: break
                        else:
                            # append new move
                            piece.add_move(move)
                        
            #castling moves
            if not piece.moved:  
                #queen side
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if not self.squares[row][c].is_empty():
                                break
                            if c == 3:
                                # add left rook to king
                                piece.left_rook = left_rook

                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)
                                

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)
                                 # check potencial checks
                                if bool:
                                    if not self.in_check(piece, moveK)and not self.in_check(left_rook, moveR):
                                        # append new move rook
                                        left_rook.add_move(moveR)
                                        # append new move king
                                        piece.add_move(moveK)
                                else:
                                    # append new move rook
                                    left_rook.add_move(moveR)
                                    # append new move King
                                    piece.add_move(moveK)
            
                # king side
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            if not self.squares[row][c].is_empty():
                                break
                            if c == 6:
                                # add right rook to king
                                piece.right_rook = right_rook

                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)
                               

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)
                                # check potencial checks
                                if bool:
                                    if not self.in_check(piece, moveK)and not self.in_check(right_rook, moveR):
                                        # append new move rook
                                        right_rook.add_move(moveR)
                                        # append new move king
                                        piece.add_move(moveK)
                                else:
                                    # append new move rook
                                    right_rook.add_move(moveR)
                                    # append new move King
                                    piece.add_move(moveK) 
                                
        
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
        
