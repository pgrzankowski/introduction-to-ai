import numpy as np
import matplotlib.pyplot as plt
import random
import time


class Game():
    def __init__(self, algorithm='minimax'):
        self.algorithm = algorithm
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.times = []

    def show_board(self):
        for ix, row in enumerate(self.board):
            print('|'.join(row))
            print('-' * 5) if ix < 2 else None

    def chose_side(self):
        choice = ''
        while choice != 'x' and choice != 'o':
            choice = input("Choose your side (x/o): ")
            if choice == 'x':
                self.player = 'x'
                self.ai = 'o'
            elif choice == 'o':
                self.player = 'o'
                self.ai = 'x'
            else:
                print("Invalid choice")

    def moves_left(self):
        amount = 0
        for row in self.board:
            for cell in row:
                if cell == ' ':
                    amount += 1
        return amount

    def player_move(self):
        row, col = map(int, input("Your move: ").split())
        if self.board[row][col] == ' ':
            self.board[row][col] = self.player
        else:
            print("Invalid move")
            self.player_move()
        self.show_board()

    def ai_move(self):
        print("AI's move:", end=' ')
        if self.moves_left() == 9:
            best_start_moves = [(0, 0), (0, 2), (2, 0), (2, 2)]
            row, col = random.choice(best_start_moves)
        else:
            match self.algorithm:
                case 'minimax':
                    start_time = time.perf_counter()
                    row, col = self.minimax(self.board, True)['pos']
                    end_time = time.perf_counter()
                case 'alpha-beta':
                    start_time = time.perf_counter()
                    row, col = self.alpha_beta(self.board, -np.inf, np.inf, True)['pos']
                    end_time = time.perf_counter()
            duration = end_time - start_time
            self.times.append(duration)
            print(f"Time: {duration:.2f}s")
        self.board[row][col] = self.ai
        print(f"{row} {col}")
        self.show_board()

    def plot_times(self):
        x = range(1, len(self.times) + 1)
        plt.bar(x, self.times)
        plt.xlabel('State Number')
        plt.ylabel('Time (s)')
        plt.xticks(x)  # Set x-axis ticks to integers
        plt.yscale('log')  # Set y-axis to logarithmic scale
        match self.algorithm:
            case 'minimax':
                plt.title('Minimax')
            case 'alpha-beta':
                plt.title('Alpha-Beta')
        for i, time in enumerate(self.times):
            plt.text(x[i], time, str(round(time, 6)), ha='center', va='bottom')
        plt.show()

    def minimax(self, board, move_max):
        if self.check_winner(self.player):
            return {"pos": None, "score": -1 * (self.moves_left() + 1)}
        if self.check_winner(self.ai):
            return {"pos": None, "score": 1 * (self.moves_left() + 1)}
        if self.check_draw():
            return {"pos": None, "score": 0}
        
        if move_max:
            best = {"pos": None, "score": -np.inf}
            for row in range(3):
                for col in range(3):
                    if board[row][col] == ' ':
                        board[row][col] = self.ai
                        current = self.minimax(board, not move_max)
                        if current['score'] > best['score']:
                            best = {"pos": (row, col), "score": current["score"]}
                        board[row][col] = ' '
        
        else:
            best = {"pos": None, "score": np.inf}
            for row in range(3):
                for col in range(3):
                    if board[row][col] == ' ':
                        board[row][col] = self.player
                        current = self.minimax(board, not move_max)
                        if current['score'] < best['score']:
                            best = {"pos": (row, col), "score": current["score"]}
                        board[row][col] = ' '
        
        return best
    
    def alpha_beta(self, board, alpha, beta, move_max):
        if self.check_winner(self.player):
            return {"pos": None, "score": -1 * (self.moves_left() + 1)}
        if self.check_winner(self.ai):
            return {"pos": None, "score": 1 * (self.moves_left() + 1)}
        if self.check_draw():
            return {"pos": None, "score": 0}
        
        if move_max:
            best = {"pos": None, "score": -np.inf}
            for row in range(3):
                for col in range(3):
                    if board[row][col] == ' ':
                        board[row][col] = self.ai
                        current = self.alpha_beta(board, alpha, beta, not move_max)
                        if current['score'] > best['score']:
                            best = {"pos": (row, col), "score": current["score"]}
                        board[row][col] = ' '
                        alpha = max(best['score'], beta)
                        if beta <= alpha:
                            continue
        
        else:
            best = {"pos": None, "score": np.inf}
            for row in range(3):
                for col in range(3):
                    if board[row][col] == ' ':
                        board[row][col] = self.player
                        current = self.alpha_beta(board, alpha, beta, not move_max)
                        if current['score'] < best['score']:
                            best = {"pos": (row, col), "score": current["score"]}
                        board[row][col] = ' '
                        beta = min(best['score'], beta)
                        if beta <= alpha:
                            continue
        
        return best

    def check_winner(self, mark):
        # Check rows
        for row in self.board:
            if row.count(mark) == 3:
                return True
        # Check columns
        for col in range(3):
            if [self.board[row][col] for row in range(3)].count(mark) == 3:
                return True
        # Check diagonals
        if [self.board[i][i] for i in range(3)].count(mark) == 3:
            return True
        if [self.board[i][2 - i] for i in range(3)].count(mark) == 3:
            return True
        return False
    
    def check_draw(self):
        return all([cell != ' ' for row in self.board for cell in row])

    def start_game(self):
        while True:
            if self.player == 'x':
                self.player_move()
                if self.check_winner(self.player):
                    print("You win!")
                    break
                if self.check_draw():
                    print("It's a draw!")
                    break
                self.ai_move()
                if self.check_winner(self.ai):
                    print("You lose!")
                    break
            else:
                self.ai_move()
                if self.check_winner(self.ai):
                    print("You lose!")
                    break
                if self.check_draw():
                    print("It's a draw!")
                    break
                self.player_move()
                if self.check_winner(self.player):
                    print("You win!")
                    break

    def run(self):
        self.times = []
        self.chose_side()
        self.show_board()
        print("Rows and columns are indexed from 0 to 2. For example:")
        print("To select the middle left cell, type: 1 0")
        input("Press Enter to play...")
        self.start_game()