COLUMNS: int = 8
ROWS: int = 8

PIECE_K_W = 10
PIECE_Q_W = 11
PIECE_R_W = 12
PIECE_N_W = 13
PIECE_B_W = 14
PIECE_P_W = 15
PIECE_K_B = 20
PIECE_Q_B = 21
PIECE_R_B = 22
PIECE_N_B = 23
PIECE_B_B = 24
PIECE_P_B = 25
PIECE_NONE = 0


initial_white_row = [PIECE_R_W, PIECE_N_W, PIECE_B_W, PIECE_Q_W, PIECE_K_W,
                     PIECE_B_W, PIECE_N_W, PIECE_R_W]

initial_white_row_2 = [PIECE_R_W, PIECE_N_W, PIECE_B_W, PIECE_K_W, PIECE_Q_W,
                       PIECE_B_W, PIECE_N_W, PIECE_R_W]

initial_black_row = [PIECE_R_B, PIECE_N_B, PIECE_B_B, PIECE_Q_B, PIECE_K_B,
                     PIECE_B_B, PIECE_N_B, PIECE_R_B]

initial_black_row_2 = [PIECE_R_B, PIECE_N_B, PIECE_B_B, PIECE_K_B, PIECE_Q_B,
                       PIECE_B_B, PIECE_N_B, PIECE_R_B]

GAME_IN_PROGRESS = 0
GAME_WIN_WHITE = 1
GAME_WIN_BLACK = 2