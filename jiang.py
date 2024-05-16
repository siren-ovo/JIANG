import pygame
import sys

# 初始化Pygame
pygame.init()

# 定义常量
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FONT_SIZE = 80

# 设置窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle and Cross")

# 设置字体
font = pygame.font.SysFont(None, FONT_SIZE)

# 初始化棋盘
board = [['' for _ in range(3)] for _ in range(3)]
turn = 'O'  # 圆圈先行

# 画出棋盘
def draw_board():
    screen.fill(BLACK)
    for i in range(1, 3):
        pygame.draw.line(screen, WHITE, (i * WIDTH / 3, 0), (i * WIDTH / 3, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, WHITE, (0, i * HEIGHT / 3), (WIDTH, i * HEIGHT / 3), LINE_WIDTH)

# 画出圆圈
def draw_circle(row, col):
    pygame.draw.circle(screen, BLUE, (int(col * WIDTH / 3 + WIDTH / 6), int(row * HEIGHT / 3 + HEIGHT / 6)), int(WIDTH / 6 - 10), LINE_WIDTH)

# 画出叉叉
def draw_cross(row, col):
    pygame.draw.line(screen, RED, (col * WIDTH / 3 + 10, row * HEIGHT / 3 + 10), ((col + 1) * WIDTH / 3 - 10, (row + 1) * HEIGHT / 3 - 10), LINE_WIDTH)
    pygame.draw.line(screen, RED, ((col + 1) * WIDTH / 3 - 10, row * HEIGHT / 3 + 10), (col * WIDTH / 3 + 10, (row + 1) * HEIGHT / 3 - 10), LINE_WIDTH)

# 检查胜利条件
def check_win(player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# 检查平局
def check_draw():
    return all(board[i][j] != '' for i in range(3) for j in range(3))

# 主游戏循环
def main():
    global turn

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row = y // (HEIGHT // 3)
                col = x // (WIDTH // 3)
                if board[row][col] == '':
                    if turn == 'O':
                        board[row][col] = 'O'
                        if check_win('O'):
                            print("Circle wins!")
                            pygame.quit()
                            sys.exit()
                        elif check_draw():
                            print("It's a draw!")
                            pygame.quit()
                            sys.exit()
                        turn = 'X'
                    else:
                        board[row][col] = 'X'
                        if check_win('X'):
                            print("Cross wins!")
                            pygame.quit()
                            sys.exit()
                        elif check_draw():
                            print("It's a draw!")
                            pygame.quit()
                            sys.exit()
                        turn = 'O'

        draw_board()

        # 画出棋盘上的圆圈和叉叉
        for row in range(3):
            for col in range(3):
                if board[row][col] == 'O':
                    draw_circle(row, col)
                elif board[row][col] == 'X':
                    draw_cross(row, col)

        pygame.display.flip()

if __name__ == "__main__":
    main()
