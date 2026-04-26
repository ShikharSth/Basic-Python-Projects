import pygame
import sys
from dataclasses import dataclass
from typing import List, Optional, Tuple


WIDTH = 650
HEIGHT = 650
ROWS = 8
COLS = 8
SQ = WIDTH // 8
FPS = 60

LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
YELLOW = (255, 255, 0)
GREEN = (60, 180, 75)
RED = (220, 50, 50)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28)


# LOAD IMAGES
IMAGES = {}

def load_images():
    pieces = [
        "wp","wr","wn","wb","wq","wk",
        "bp","br","bn","bb","bq","bk"
    ]
    for p in pieces:
        img = pygame.image.load("image/" + p + ".png").convert_alpha()
        IMAGES[p] = pygame.transform.scale(img, (SQ, SQ))


# MoVe
@dataclass
class Move:
    start: Tuple[int,int]
    end: Tuple[int,int]
    piece_moved: str
    piece_captured: str = "--"
    promotion: Optional[str] = None
    en_passant: bool = False
    castle: bool = False


# GAME STATE
class GameState:
    def __init__(self):
        self.board = [
            ["br","bn","bb","bq","bk","bb","bn","br"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wr","wn","wb","wq","wk","wb","wn","wr"]
        ]

        self.white_turn = True
        self.move_log = []

        self.white_king = (7,4)
        self.black_king = (0,4)

        self.en_passant = None

        self.wks = True
        self.wqs = True
        self.bks = True
        self.bqs = True

        self.checkmate = False
        self.stalemate = False

    # ------------------------------------------------------
    def make_move(self, move):
        sr,sc = move.start
        er,ec = move.end

        self.board[sr][sc] = "--"
        self.board[er][ec] = move.piece_moved

        if move.promotion:
            self.board[er][ec] = move.promotion

        if move.en_passant:
            if move.piece_moved[0] == "w":
                self.board[er+1][ec] = "--"
            else:
                self.board[er-1][ec] = "--"

        if move.piece_moved == "wk":
            self.white_king = (er,ec)
            self.wks = False
            self.wqs = False

        if move.piece_moved == "bk":
            self.black_king = (er,ec)
            self.bks = False
            self.bqs = False

        if move.piece_moved == "wr":
            if sr == 7 and sc == 0:
                self.wqs = False
            if sr == 7 and sc == 7:
                self.wks = False

        if move.piece_moved == "br":
            if sr == 0 and sc == 0:
                self.bqs = False
            if sr == 0 and sc == 7:
                self.bks = False

        # castle rook move
        if move.castle:
            if ec == 6:
                self.board[er][5] = self.board[er][7]
                self.board[er][7] = "--"
            else:
                self.board[er][3] = self.board[er][0]
                self.board[er][0] = "--"

        # en passant square
        self.en_passant = None
        if move.piece_moved[1] == "p" and abs(er-sr) == 2:
            self.en_passant = ((sr+er)//2, sc)

        self.move_log.append(move)
        self.white_turn = not self.white_turn

    # ------------------------------------------------------
    def undo(self):
        if len(self.move_log) == 0:
            return

        move = self.move_log.pop()
        sr,sc = move.start
        er,ec = move.end

        self.board[sr][sc] = move.piece_moved
        self.board[er][ec] = move.piece_captured

        if move.en_passant:
            self.board[er][ec] = "--"
            if move.piece_moved[0] == "w":
                self.board[er+1][ec] = "bp"
            else:
                self.board[er-1][ec] = "wp"

        if move.castle:
            if ec == 6:
                self.board[er][7] = self.board[er][5]
                self.board[er][5] = "--"
            else:
                self.board[er][0] = self.board[er][3]
                self.board[er][3] = "--"

        if move.piece_moved == "wk":
            self.white_king = (sr,sc)

        if move.piece_moved == "bk":
            self.black_king = (sr,sc)

        self.white_turn = not self.white_turn
        self.checkmate = False
        self.stalemate = False

    # ------------------------------------------------------
    def in_bounds(self,r,c):
        return 0 <= r < 8 and 0 <= c < 8

    # ------------------------------------------------------
    def in_check(self, white):
        if white:
            r,c = self.white_king
            return self.square_attacked(r,c,False)
        else:
            r,c = self.black_king
            return self.square_attacked(r,c,True)

    # ------------------------------------------------------
    def square_attacked(self,r,c,by_white):

        enemy = "w" if by_white else "b"

        # pawn
        d = -1 if by_white else 1
        for dc in [-1,1]:
            rr = r + d
            cc = c + dc
            if self.in_bounds(rr,cc):
                if self.board[rr][cc] == enemy+"p":
                    return True

        # knight
        knight = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
        for dr,dc in knight:
            rr=r+dr; cc=c+dc
            if self.in_bounds(rr,cc):
                if self.board[rr][cc] == enemy+"n":
                    return True

        # rook queen
        dirs=[(-1,0),(1,0),(0,-1),(0,1)]
        for dr,dc in dirs:
            rr=r+dr; cc=c+dc
            while self.in_bounds(rr,cc):
                p=self.board[rr][cc]
                if p!="--":
                    if p[0]==enemy and p[1] in ["r","q"]:
                        return True
                    break
                rr+=dr; cc+=dc

        # bishop queen
        dirs=[(-1,-1),(-1,1),(1,-1),(1,1)]
        for dr,dc in dirs:
            rr=r+dr; cc=c+dc
            while self.in_bounds(rr,cc):
                p=self.board[rr][cc]
                if p!="--":
                    if p[0]==enemy and p[1] in ["b","q"]:
                        return True
                    break
                rr+=dr; cc+=dc

        # king
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr==0 and dc==0:
                    continue
                rr=r+dr; cc=c+dc
                if self.in_bounds(rr,cc):
                    if self.board[rr][cc]==enemy+"k":
                        return True

        return False

    # ------------------------------------------------------
    def valid_moves(self):
        moves = self.all_moves()
        legal = []

        for m in moves:
            self.make_move(m)
            if not self.in_check(not self.white_turn):
                legal.append(m)
            self.undo()

        if len(legal)==0:
            if self.in_check(self.white_turn):
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        return legal

    # ------------------------------------------------------
    def all_moves(self):
        moves=[]

        for r in range(8):
            for c in range(8):
                p=self.board[r][c]
                if p=="--":
                    continue

                if self.white_turn and p[0]!="w":
                    continue
                if not self.white_turn and p[0]!="b":
                    continue

                t=p[1]

                if t=="p":
                    self.pawn_moves(r,c,moves)
                elif t=="r":
                    self.slide(r,c,moves,[(-1,0),(1,0),(0,-1),(0,1)])
                elif t=="b":
                    self.slide(r,c,moves,[(-1,-1),(-1,1),(1,-1),(1,1)])
                elif t=="q":
                    self.slide(r,c,moves,[(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)])
                elif t=="n":
                    self.knight_moves(r,c,moves)
                elif t=="k":
                    self.king_moves(r,c,moves)

        return moves

    # ------------------------------------------------------
    def pawn_moves(self,r,c,moves):
        p=self.board[r][c]
        white = p[0]=="w"
        d=-1 if white else 1
        start=6 if white else 1
        promo=0 if white else 7
        enemy="b" if white else "w"

        # forward
        if self.in_bounds(r+d,c) and self.board[r+d][c]=="--":
            piece = p[0]+"q" if r+d==promo else None
            moves.append(Move((r,c),(r+d,c),p,"--",piece))

            if r==start and self.board[r+2*d][c]=="--":
                moves.append(Move((r,c),(r+2*d,c),p))

        # capture
        for dc in [-1,1]:
            rr=r+d
            cc=c+dc
            if self.in_bounds(rr,cc):
                target=self.board[rr][cc]
                if target!="--" and target[0]==enemy:
                    piece = p[0]+"q" if rr==promo else None
                    moves.append(Move((r,c),(rr,cc),p,target,piece))

        # en passant
        for dc in [-1,1]:
            rr=r+d
            cc=c+dc
            if self.en_passant == (rr,cc):
                moves.append(Move((r,c),(rr,cc),p,enemy+"p",None,True))

    # ------------------------------------------------------
    def slide(self,r,c,moves,dirs):
        p=self.board[r][c]
        enemy="b" if p[0]=="w" else "w"

        for dr,dc in dirs:
            rr=r+dr
            cc=c+dc
            while self.in_bounds(rr,cc):
                t=self.board[rr][cc]
                if t=="--":
                    moves.append(Move((r,c),(rr,cc),p))
                else:
                    if t[0]==enemy:
                        moves.append(Move((r,c),(rr,cc),p,t))
                    break
                rr+=dr
                cc+=dc

    # ------------------------------------------------------
    def knight_moves(self,r,c,moves):
        p=self.board[r][c]
        enemy="b" if p[0]=="w" else "w"

        vals=[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
        for dr,dc in vals:
            rr=r+dr
            cc=c+dc
            if self.in_bounds(rr,cc):
                t=self.board[rr][cc]
                if t=="--" or t[0]==enemy:
                    moves.append(Move((r,c),(rr,cc),p,t))

    # ------------------------------------------------------
    def king_moves(self,r,c,moves):
        p=self.board[r][c]
        enemy="b" if p[0]=="w" else "w"

        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr==0 and dc==0:
                    continue
                rr=r+dr
                cc=c+dc
                if self.in_bounds(rr,cc):
                    t=self.board[rr][cc]
                    if t=="--" or t[0]==enemy:
                        moves.append(Move((r,c),(rr,cc),p,t))

        # castling
        if p=="wk":
            if self.wks and self.board[7][5]=="--" and self.board[7][6]=="--":
                if not self.square_attacked(7,4,False) and not self.square_attacked(7,5,False):
                    moves.append(Move((7,4),(7,6),p,"--",None,False,True))
            if self.wqs and self.board[7][1]=="--" and self.board[7][2]=="--" and self.board[7][3]=="--":
                if not self.square_attacked(7,4,False):
                    moves.append(Move((7,4),(7,2),p,"--",None,False,True))

        if p=="bk":
            if self.bks and self.board[0][5]=="--" and self.board[0][6]=="--":
                if not self.square_attacked(0,4,True):
                    moves.append(Move((0,4),(0,6),p,"--",None,False,True))
            if self.bqs and self.board[0][1]=="--" and self.board[0][2]=="--" and self.board[0][3]=="--":
                if not self.square_attacked(0,4,True):
                    moves.append(Move((0,4),(0,2),p,"--",None,False,True))


# DRAWING
def draw_board():
    for r in range(8):
        for c in range(8):
            color = LIGHT if (r+c)%2==0 else DARK
            pygame.draw.rect(screen,color,(c*SQ,r*SQ,SQ,SQ))

def draw_pieces(gs):
    for r in range(8):
        for c in range(8):
            p=gs.board[r][c]
            if p!="--":
                screen.blit(IMAGES[p],(c*SQ,r*SQ))

def draw_selected(selected,moves):
    if selected:
        r,c=selected
        pygame.draw.rect(screen,YELLOW,(c*SQ,r*SQ,SQ,SQ),4)
        for m in moves:
            if m.start==selected:
                rr,cc=m.end
                pygame.draw.circle(screen,GREEN,(cc*SQ+SQ//2,rr*SQ+SQ//2),10)

def draw_text(msg):
    t=font.render(msg,True,RED)
    screen.blit(t,(10,10))


# MAIN
def main():
    load_images()

    gs = GameState()
    moves = gs.valid_moves()
    selected = None

    run=True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    gs = GameState()
                    moves = gs.valid_moves()
                    selected=None

                if event.key == pygame.K_u:
                    gs.undo()
                    moves = gs.valid_moves()
                    selected=None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not gs.checkmate and not gs.stalemate:

                    x,y = pygame.mouse.get_pos()
                    r=y//SQ
                    c=x//SQ

                    if selected is None:
                        if gs.board[r][c]!="--":
                            if gs.white_turn and gs.board[r][c][0]=="w":
                                selected=(r,c)
                            elif not gs.white_turn and gs.board[r][c][0]=="b":
                                selected=(r,c)
                    else:
                        chosen=None
                        for m in moves:
                            if m.start==selected and m.end==(r,c):
                                chosen=m
                                break

                        if chosen:
                            gs.make_move(chosen)
                            moves = gs.valid_moves()
                            selected=None
                        else:
                            selected=None

        draw_board()
        draw_selected(selected,moves)
        draw_pieces(gs)

        if gs.checkmate:
            winner = "Black Wins" if gs.white_turn else "White Wins"
            draw_text("Checkmate - " + winner)

        elif gs.stalemate:
            draw_text("Stalemate")

        elif gs.in_check(gs.white_turn):
            draw_text("Check")

        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
