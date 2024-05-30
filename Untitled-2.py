import pygame
import sys

# 初始化Pygame
pygame.init()

# 定义常量
WIDTH, HEIGHT = 800, 800
LINE_WIDTH = 2
BOARD_ROWS, BOARD_COLS = 8, 8
SQUARE_SIZE = WIDTH // BOARD_COLS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# 设置窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reversi")

# 初始化棋盘
board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
board[3][3] = board[4][4] = 'W'
board[3][4] = board[4][3] = 'B'
turn = 'B'  # 黑子先行

# 方向向量
directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

# 绘制棋盘
def draw_board():
    screen.fill(GREEN)
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, BLACK, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (row * SQUARE_SIZE, 0), (row * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# 绘制棋子
def draw_piece(row, col, color):
    pygame.draw.circle(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

# 检查是否可以下子
def is_valid_move(board, row, col, player):
    if board[row][col] != '':
        return False
    opponent = 'B' if player == 'W' else 'W'
    for direction in directions:
        r, c = row + direction[0], col + direction[1]
        if r in range(BOARD_ROWS) and c in range(BOARD_COLS) and board[r][c] == opponent:
            while r in range(BOARD_ROWS) and c in range(BOARD_COLS):
                r += direction[0]
                c += direction[1]
                if r in range(BOARD_ROWS) and c in range(BOARD_COLS) and board[r][c] == player:
                    return True
                if r not in range(BOARD_ROWS) or c not in range(BOARD_COLS) or board[r][c] == '':
                    break
    return False

# 翻转棋子
def flip_pieces(board, row, col, player):
    opponent = 'B' if player == 'W' else 'W'
    pieces_to_flip = []
    for direction in directions:
        r, c = row + direction[0], col + direction[1]
        pieces_in_this_direction = []
        while r in range(BOARD_ROWS) and c in range(BOARD_COLS) and board[r][c] == opponent:
            pieces_in_this_direction.append((r, c))
            r += direction[0]
            c += direction[1]
        if r in range(BOARD_ROWS) and c in range(BOARD_COLS) and board[r][c] == player:
            pieces_to_flip.extend(pieces_in_this_direction)
    for r, c in pieces_to_flip:
        board[r][c] = player

# 检查是否还有有效的移动
def has_valid_move(board, player):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if is_valid_move(board, row, col, player):
                return True
    return False

# 计算棋子数量
def count_pieces(board):
    black_count = sum(row.count('B') for row in board)
    white_count = sum(row.count('W') for row in board)
    return black_count, white_count

# 主游戏循环
def main():
    global turn
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE
                if is_valid_move(board, row, col, turn):
                    board[row][col] = turn
                    flip_pieces(board, row, col, turn)
                    turn = 'W' if turn == 'B' else 'B'
                    if not has_valid_move(board, turn):
                        turn = 'W' if turn == 'B' else 'B'
                        if not has_valid_move(board, turn):
                            running = False

        draw_board()
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 'B':
                    draw_piece(row, col, BLACK)
                elif board[row][col] == 'W':
                    draw_piece(row, col, WHITE)

        pygame.display.flip()

    black_count, white_count = count_pieces(board)
    print(f"Game over! Black: {black_count}, White: {white_count}")

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
