import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 300
screen_height = 600
cell_size = 30

# Colors
colors = [
    (255, 0, 0),    # Red
    (255, 165, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (75, 0, 130),   # Purple
    (255, 105, 180) # Pink
]

# Tetromino shapes
shapes = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1], [1, 1]],  # O shape
    [[0, 1, 0], [1, 1, 1]],  # T shape
    [[1, 0, 0], [1, 1, 1]],  # L shape
    [[0, 0, 1], [1, 1, 1]],  # J shape
    [[1, 1, 0], [0, 1, 1]],  # S shape
    [[0, 1, 1], [1, 1, 0]]   # Z shape
]

# Game initialization settings
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Tetris')
font = pygame.font.Font(None, 36)

# Define the start screen button
button_rect = pygame.Rect(screen_width // 4, screen_height // 2 - 25, screen_width // 2, 50)

def draw_start_screen():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), button_rect)
    text = font.render('Start Game', True, (0, 0, 0))
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

def draw_game_over_screen():
    screen.fill((0, 0, 0))
    game_over_text = font.render('Game Over', True, (255, 255, 255))
    screen.blit(game_over_text, (screen_width // 4 - 30, screen_height // 3))
    restart_button_rect = pygame.Rect(screen_width // 4, screen_height // 2 - 25, screen_width // 2, 50)
    quit_button_rect = pygame.Rect(screen_width // 4, screen_height // 2 + 50, screen_width // 2, 50)
    pygame.draw.rect(screen, (0, 255, 0), restart_button_rect)
    pygame.draw.rect(screen, (255, 0, 0), quit_button_rect)
    restart_text = font.render('Try Again', True, (0, 0, 0))
    quit_text = font.render('Quit', True, (0, 0, 0))
    screen.blit(restart_text, (restart_button_rect.x + 10, restart_button_rect.y + 10))
    screen.blit(quit_text, (quit_button_rect.x + 60, quit_button_rect.y + 10))
    return restart_button_rect, quit_button_rect

def draw_grid():
    for x in range(0, screen_width, cell_size):
        for y in range(0, screen_height, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)

def get_random_tetromino():
    shape = random.choice(shapes)
    color = random.choice(colors)
    return shape, color

def draw_tetromino(tetromino, offset):
    shape, color = tetromino
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect((off_x + x) * cell_size, (off_y + y) * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)

def move_tetromino(tetromino_offset, direction):
    new_offset = tetromino_offset[:]
    if direction == 'left':
        new_offset[0] -= 1
    elif direction == 'right':
        new_offset[0] += 1
    return new_offset

def rotate_tetromino(tetromino, direction):
    shape, color = tetromino
    if direction == 'left':
        rotated_shape = [list(row) for row in zip(*shape[::-1])]
    elif direction == 'right':
        rotated_shape = [list(row)[::-1] for row in zip(*shape)]
    return rotated_shape, color

def is_valid_position(tetromino, offset, board):
    shape, _ = tetromino
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = offset[0] + x
                new_y = offset[1] + y
                if new_x < 0 or new_x >= 10 or new_y >= 20 or board[new_y][new_x]:
                    return False
    return True

def place_tetromino(board, tetromino, offset):
    shape, color = tetromino
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board[off_y + y][off_x + x] = color

def clear_rows(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    rows_cleared = len(board) - len(new_board)
    new_board = [[0] * 10 for _ in range(rows_cleared)] + new_board
    return new_board, rows_cleared

def check_game_over(board):
    return any(board[0])

def main():
    running = True
    game_started = False
    game_over = False
    current_tetromino = None
    tetromino_offset = [3, 0]
    last_fall_time = time.time()
    fall_speed = 2
    fast_fall = False
    board = [[0] * 10 for _ in range(20)]
    global screen

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not game_started and button_rect.collidepoint(event.pos):
                    game_started = True
                    game_over = False
                    current_tetromino = get_random_tetromino()
                    last_fall_time = time.time()
                    board = [[0] * 10 for _ in range(20)]
                    tetromino_offset = [3, 0]
                elif game_over:
                    restart_button_rect, quit_button_rect = draw_game_over_screen()
                    if restart_button_rect.collidepoint(event.pos):
                        game_started = True
                        game_over = False
                        current_tetromino = get_random_tetromino()
                        last_fall_time = time.time()
                        board = [[0] * 10 for _ in range(20)]
                        tetromino_offset = [3, 0]
                    elif quit_button_rect.collidepoint(event.pos):
                        game_started = False
                        game_over = False
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_LEFT:
                    new_offset = move_tetromino(tetromino_offset, 'left')
                    if is_valid_position(current_tetromino, new_offset, board):
                        tetromino_offset = new_offset
                elif event.key == pygame.K_RIGHT:
                    new_offset = move_tetromino(tetromino_offset, 'right')
                    if is_valid_position(current_tetromino, new_offset, board):
                        tetromino_offset = new_offset
                elif event.key == pygame.K_a:
                    rotated_tetromino = rotate_tetromino(current_tetromino, 'left')
                    if is_valid_position(rotated_tetromino, tetromino_offset, board):
                        current_tetromino = rotated_tetromino
                elif event.key == pygame.K_d:
                    rotated_tetromino = rotate_tetromino(current_tetromino, 'right')
                    if is_valid_position(rotated_tetromino, tetromino_offset, board):
                        current_tetromino = rotated_tetromino
                elif event.key == pygame.K_SPACE:
                    fast_fall = not fast_fall
                    fall_speed = 0.05 if fast_fall else 2

        if game_started and not game_over:
            screen.fill((0, 0, 0))
            draw_grid()
            elapsed_time = time.time() - last_fall_time
            if elapsed_time > fall_speed:
                tetromino_offset[1] += 1
                last_fall_time = time.time()
                if not is_valid_position(current_tetromino, tetromino_offset, board):
                    tetromino_offset[1] -= 1
                    place_tetromino(board, current_tetromino, tetromino_offset)
                    board, rows_cleared = clear_rows(board)
                    if check_game_over(board):
                        game_over = True
                    else:
                        current_tetromino = get_random_tetromino()
                        tetromino_offset = [3, 0]
                else:
                    if time.time() - last_fall_time > 120:
                        fall_speed = 0.5
                    elif time.time() - last_fall_time > 60:
                        fall_speed = 1
            draw_tetromino(current_tetromino, tetromino_offset)

            for y, row in enumerate(board):
                for x, cell in enumerate(row):
                    if cell:
                        rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, cell, rect)
                        pygame.draw.rect(screen, (255, 255, 255), rect, 1)
        elif game_over:
            restart_button_rect, quit_button_rect = draw_game_over_screen()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
