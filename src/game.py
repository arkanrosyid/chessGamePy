import pygame

from const import *
from board import Board
from dragger import Dragger
from config import Config
class Game:
    def __init__(self):
      self.next_player = 'white'
      self.board = Board()
      self.dragger = Dragger()
      self.hovered_sqr = None
      self.config = Config()
      self.idx = 0

    def show_bg(self, surface):
       theme = self.config.theme
       for row in range(ROWS):
           for col in range(COLS):
                # color
                color =  theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # rect
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                #check piece
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    # all pieces except dragged piece
                    if piece != self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)
    
    def show_moves(self, surface):
        if self.dragger.dragging:
            theme = self.config.theme
            piece = self.dragger.piece

            for move in piece.moves:
                # color
                color = theme.moves.light if (move.final.row +move.final.col) % 2 == 0 else theme.moves.dark
                # rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self,surface):
        theme = self.config.theme
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                row = pos.row
                col = pos.col
                # color
                color = theme.trace.light if (row + col) % 2 == 0 else theme.trace.dark
                # rect
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)
           
    def show_hover(self, surface):
        if self.hovered_sqr:
            # color
            color = '#b4b4b4'
            # rect
            rect = (self.hovered_sqr.col * SQSIZE, self.hovered_sqr.row * SQSIZE, SQSIZE, SQSIZE)
            # blit
            pygame.draw.rect(surface, color, rect, width=3)

    # other method
    def next_turn(self): 
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.config.themes)
        self.config.theme = self.config.themes[self.idx]

    def sound_effect(self,captured = False):
        if captured :
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    