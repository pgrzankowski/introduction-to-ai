import numpy as np


class Game():
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

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

    def ai_move(self):
        row, col = self.minimax(self.board, True)['pos']
        self.board[row][col] = self.ai

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
                self.show_board()
                if self.check_winner(self.ai):
                    print("You lose!")
                    break
            else:
                self.ai_move()
                self.show_board()
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
        self.chose_side()
        self.show_board()
        print("Rows and columns are indexed from 0 to 2. For example:")
        print("To select the middle left cell, type: 1 0")
        input("Press Enter to play...")
        self.start_game()