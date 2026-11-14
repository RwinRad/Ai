import pygame
import sys
import math

# الثوابت
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 4
CELL_SIZE = WIDTH // GRID_SIZE
LINE_WIDTH = 5
WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
BLUE = (41, 128, 185)
RED = (231, 76, 60)
GRAY = (189, 195, 199)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("4x4 L-Shaped Tic-Tac-Toe (AI vs Human)")
font = pygame.font.SysFont("arial", 40, bold=True)

# تولید تمام ۴۸ ترکیب ممکن شکل L (۴ خانه‌ای)
def generate_l_shapes():
    l_shapes = []
    # L‌های با ابعاد 3x2
    for r in range(GRID_SIZE - 2):
        for c in range(GRID_SIZE - 1):
            # 4 حالت مختلف L در مستطیل 3x2
            l_shapes.append([(r, c), (r+1, c), (r+2, c), (r+2, c+1)])
            l_shapes.append([(r, c), (r+1, c), (r+2, c), (r, c+1)])
            l_shapes.append([(r, c+1), (r+1, c+1), (r+2, c+1), (r+2, c)])
            l_shapes.append([(r, c+1), (r+1, c+1), (r+2, c+1), (r, c)])
            
    # L‌های با ابعاد 2x3
    for r in range(GRID_SIZE - 1):
        for c in range(GRID_SIZE - 2):
            l_shapes.append([(r, c), (r, c+1), (r, c+2), (r+1, c+2)])
            l_shapes.append([(r, c), (r, c+1), (r, c+2), (r+1, c)])
            l_shapes.append([(r+1, c), (r+1, c+1), (r+1, c+2), (r, c+2)])
            l_shapes.append([(r+1, c), (r+1, c+1), (r+1, c+2), (r, c)])
            
    return l_shapes

L_SHAPES = generate_l_shapes()

def check_winner(board):
    for shape in L_SHAPES:
        vals = [board[r][c] for r, c in shape]
        if vals[0] != " " and all(v == vals[0] for v in vals):
            return vals[0]
    return None

def is_full(board):
    return all(board[r][c] != " " for r in range(GRID_SIZE) for c in range(GRID_SIZE))

def evaluate(board):
    # تابع ارزیابی هوریستیک بر اساس Lهای بالقوه فعال
    score = 0
    for shape in L_SHAPES:
        vals = [board[r][c] for r, c in shape]
        if "O" in vals and "X" not in vals:
            score += vals.count("O") ** 2
        elif "X" in vals and "O" not in vals:
            score -= vals.count("X") ** 2
    return score

def minimax(board, depth, alpha, beta, is_maximizing):
    winner = check_winner(board)
    if winner == "O": return 1000 - depth, None
    if winner == "X": return -1000 + depth, None
    if is_full(board) or depth == 0:
        return evaluate(board), None

    best_move = None
    empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if board[r][c] == " "]

    if is_maximizing:
        max_eval = -math.inf
        for r, c in empty_cells:
            board[r][c] = "O"
            eval_score, _ = minimax(board, depth - 1, alpha, beta, False)
            board[r][c] = " "
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (r, c)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        for r, c in empty_cells:
            board[r][c] = "X"
            eval_score, _ = minimax(board, depth - 1, alpha, beta, True)
            board[r][c] = " "
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = (r, c)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def draw_board(screen, board):
    screen.fill(WHITE)
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, GRAY, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] != " ":
                color = RED if board[r][c] == "X" else BLUE
                text = font.render(board[r][c], True, color)
                rect = text.get_rect(center=(c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, rect)

def main():
    board = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    game_over = False
    turn = "X" # X = Human, O = AI

    while True:
        draw_board(screen, board)
        pygame.display.update()

        if turn == "O" and not game_over:
            _, move = minimax(board, depth=3, alpha=-math.inf, beta=math.inf, is_maximizing=True)
            if move:
                board[move[0]][move[1]] = "O"
                if check_winner(board) == "O":
                    print("AI wins!")
                    game_over = True
                elif is_full(board):
                    print("Draw!")
                    game_over = True
                turn = "X"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and turn == "X" and not game_over:
                x, y = event.pos
                row, col = y // CELL_SIZE, x // CELL_SIZE
                if board[row][col] == " ":
                    board[row][col] = "X"
                    if check_winner(board) == "X":
                        print("Human wins!")
                        game_over = True
                    elif is_full(board):
                        print("Draw!")
                        game_over = True
                    turn = "O"

if __name__ == "__main__":
    main()
