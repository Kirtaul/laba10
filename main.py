import tkinter as tk
from tkinter import messagebox



class KrestikiNoliki:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")
        self.current_player = "X"  # X - игрок, O - бот
        self.board = [" " for _ in range(9)]

        # Настройка кнопок
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(root, text=" ", font=('Arial', 30), width=5, height=2,
                                   command=lambda row=i, col=j: self.on_click(row, col))
                button.grid(row=i, column=j, sticky="nsew")
                row.append(button)
            self.buttons.append(row)

        # Кнопка перезапуска
        self.restart_button = tk.Button(root, text="Новая игра", command=self.restart)
        self.restart_button.grid(row=3, column=0, columnspan=3, sticky="nsew")

        # Если бот ходит первым
        if self.current_player == "O":
            self.bot_move()

    def on_click(self, row, col):
        if self.board[row * 3 + col] == " " and self.current_player == "X":
            self.make_move(row, col, "X")

            if not self.check_game_over():
                self.current_player = "O"
                self.bot_move()

    def bot_move(self):
        if self.current_player == "O":
            # Находим лучший ход с помощью алгоритма Minimax
            best_score = -float('inf')
            best_move = None

            for i in range(9):
                if self.board[i] == " ":
                    self.board[i] = "O"
                    score = self.minimax(self.board, 0, False)
                    self.board[i] = " "

                    if score > best_score:
                        best_score = score
                        best_move = i

            if best_move is not None:
                row, col = best_move // 3, best_move % 3
                self.make_move(row, col, "O")
                self.current_player = "X"
                self.check_game_over()

    def minimax(self, board, depth, is_maximizing):
        # Проверка терминальных состояний
        winner = self.check_winner(board)
        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        elif " " not in board:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "O"
                    score = self.minimax(board, depth + 1, False)
                    board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = "X"
                    score = self.minimax(board, depth + 1, True)
                    board[i] = " "
                    best_score = min(score, best_score)
            return best_score

    def make_move(self, row, col, player):
        self.board[row * 3 + col] = player
        self.buttons[row][col].config(text=player, state="disabled")

    def check_winner(self, board=None):
        if board is None:
            board = self.board

        # Проверка строк
        for i in range(0, 9, 3):
            if board[i] == board[i + 1] == board[i + 2] != " ":
                return board[i]

        # Проверка столбцов
        for i in range(3):
            if board[i] == board[i + 3] == board[i + 6] != " ":
                return board[i]

        # Проверка диагоналей
        if board[0] == board[4] == board[8] != " ":
            return board[0]
        if board[2] == board[4] == board[6] != " ":
            return board[2]

        return None

    def check_game_over(self):
        winner = self.check_winner()
        if winner:
            message = f"Победили {winner}!"
            if winner == "X":
                messagebox.showinfo("Игра окончена", message)
            else:
                messagebox.showinfo("Игра окончена", "Бот победил!")
            self.disable_all_buttons()
            return True

        if " " not in self.board:
            messagebox.showinfo("Игра окончена", "Ничья!")
            self.disable_all_buttons()
            return True

        return False

    def disable_all_buttons(self):
        for row in self.buttons:
            for button in row:
                button.config(state="disabled")

    def restart(self):
        self.current_player = "X"
        self.board = [" " for _ in range(9)]

        for row in self.buttons:
            for button in row:
                button.config(text=" ", state="normal")

        # Если бот ходит первым
        if self.current_player == "O":
            self.bot_move()


if __name__ == "__main__":
    root = tk.Tk()
    game = KrestikiNoliki(root)
    root.mainloop()