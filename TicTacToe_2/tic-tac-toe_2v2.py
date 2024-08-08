import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import time
import webbrowser


data = pd.read_excel('TicTacToe.xls') # 1st column: football club; 2. country; 3. feature

# generation will have 3 clubs into the row, 2 countries&1 feature into the column (feature through other and posed in the middle)
class TicTacToeApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Tic Tac Toe')
        self.current_player = 'O'
        self.board = [['' for _ in range(4)] for _ in range(4)]  # Adjusted for additional non-playing grids
        self.buttons = [[None for _ in range(4)] for _ in range(4)]  # Adjusted for additional non-playing grids
        self.o_wins = 0
        self.x_wins = 0
        self.master.geometry('1600x1000')
        #self.master.set_full_screen()
        #self.master.bind("<Escape>", self.exit_full_screen)
        self.initialize_board_with_labels()
        self.initialize_approval_system()
        self.add_search_functionality()
        #self.setup_timer()


    def updates(self):
        random_values_col1 = data.iloc[:, 0].dropna().sample(3).tolist()
        random_values_col2 = data.iloc[:, 1].dropna().sample(2).tolist()
        random_values_col3 = data.iloc[:, 2].dropna().sample(1).tolist()
        return [random_values_col1, random_values_col2, random_values_col3]

    def initialize_board_with_labels(self):
        random_values_col1, random_values_col2, random_values_col3 = self.updates()
        if len(random_values_col1[0]) >= 17:
            middle_index = len(random_values_col1[0]) // 2
            random_values_col1[0] = random_values_col1[0][:middle_index] + '\n' + random_values_col1[0][middle_index:]
        if len(random_values_col1[1]) >= 17:
            middle_index = len(random_values_col1[1]) // 2
            random_values_col1[1] = random_values_col1[1][:middle_index] + '\n' + random_values_col1[1][middle_index:]
        if len(random_values_col1[2]) >= 17:
            middle_index = len(random_values_col1[2]) // 2
            random_values_col1[2] = random_values_col1[2][:middle_index] + '\n' + random_values_col1[2][middle_index:]
        if len(random_values_col2[0]) >= 17:
            middle_index = len(random_values_col2[0]) // 2
            random_values_col2[0] = random_values_col2[0][:middle_index] + '\n' + random_values_col2[0][middle_index:]
        if len(random_values_col2[1]) >= 17:
            middle_index = len(random_values_col2[1]) // 2
            random_values_col2[1] = random_values_col2[1][:middle_index] + '\n' + random_values_col2[1][middle_index:]
        if len(random_values_col3[0]) >= 17:
            middle_index = len(random_values_col3[0]) // 2
            random_values_col3[0] = random_values_col3[0][:middle_index] + '\n' + random_values_col3[0][middle_index:]
        self.board[0][0] = "Tic Tac Toe"
        self.board[0][1] = random_values_col1[0]
        self.board[0][2] = random_values_col1[1]
        self.board[0][3] = random_values_col1[2]
        self.board[1][0] = random_values_col2[0]
        self.board[2][0] = random_values_col3[0]
        self.board[3][0] = random_values_col2[1]

        for i in range(4):
            for j in range(4):
                if i == 0 and j == 0:
                    label = tk.Label(self.master, text=self.board[0][0], font=('Arial', 12), width=20, height=10)
                    label.grid(row=i, column=j)
                elif i == 0 and j == 1:
                    label = tk.Label(self.master, text=self.board[0][1], font=('Arial', 12), width=20, height=10)
                    label.grid(row=i, column=j)
                elif i == 0 and j == 2:
                    label = tk.Label(self.master, text=self.board[0][2], font=('Arial', 12), width=20, height=10)
                    label.grid(row=i, column=j)
                elif i == 0 and j == 3:
                    label = tk.Label(self.master, text=self.board[0][3], font=('Arial', 12), width=20, height=10)
                    label.grid(row=i, column=j)
                elif i == 1 and j == 0:
                    label = tk.Label(self.master, text=self.board[1][0], font=('Arial', 12), width=20, height=10)
                    label.grid(row=i, column=j)
                elif i == 2 and j == 0:
                    label = tk.Label(self.master, text=self.board[2][0], font=('Arial', 12), width=20, height=10)
                    label.grid(row=i, column=j)
                elif i == 3 and j == 0:
                    label = tk.Label(self.master, text=self.board[3][0], font=('Arial', 12), width=20, height=10)
                    label.grid(row=i, column=j)
                else:
                    self.buttons[i][j] = tk.Button(self.master, text='', font=('Arial', 12), width=20, height=10, command=lambda: self.propose_move(i, j))
                    self.buttons[i][j].grid(row=i, column=j)


    def toggle_mark(self, i, j):
        current_mark = self.buttons[i][j]['text']
        print(current_mark)
        if current_mark == 'O':
            self.buttons[i][j] = tk.Button(self.master, text='', font=('normal', 12), width=20, height=10, command=lambda: self.make_move(i, j))
            self.buttons[i][j].grid(row=i, column=j)
        elif current_mark == "X":
            self.buttons[i][j] = tk.Button(self.master, text='', font=('normal', 12), width=20, height=10, command=lambda: self.make_move(i, j))
            self.buttons[i][j].grid(row=i, column=j)

        elif current_mark != "X" or current_mark != "O":
            fix = str(input("X or O"))
            self.buttons[i][j] = tk.Button(self.master, text=fix, font=('normal', 12), width=20, height=10, command=lambda: self.make_move(i, j))
            self.buttons[i][j].grid(row=i, column=j)

    def make_move(self, i, j):
        if not self.board[i][j] and self.current_player:
            self.buttons[i][j]['text'] = self.current_player
            if self.check_winner(self.current_player):
                messagebox.showinfo("Game Over", f"'{self.current_player}' wins!")
                self.update_score(self.current_player)
                self.reset_board()
            elif self.is_board_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()
            self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        for i in range(1, 4):
            if self.board[i][1] == self.board[i][2] == self.board[i][3] != '':
                self.animate_winner([(i, 1), (i, 2), (i, 3)])
                return True
        for j in range(1, 4):
            if self.board[1][j] == self.board[2][j] == self.board[3][j] != '':
                self.animate_winner([(1, j), (2, j), (3, j)])
                return True
        if self.board[1][1] == self.board[2][2] == self.board[3][3] != '':
            self.animate_winner([(1, 1), (2, 2), (3, 3)])
            return True
        if self.board[1][3] == self.board[2][2] == self.board[3][1] != '':
            self.animate_winner([(1, 3), (2, 2), (3, 1)])
            return True
        return False


    def update_score(self, player):
        if player == 'X':
            self.x_wins += 1
        else:
            self.o_wins += 1
        self.master.title(f'Tic Tac Toe - роXана Wins: {self.x_wins}, чпO Wins: {self.o_wins}')

    def reset_board(self):
        for i in range(1, 4):
            for j in range(1, 4):
                self.buttons[i][j].config(text='')
        self.board = [['' for _ in range(4)] for _ in range(4)]
        self.current_player = 'X'
        self.initialize_board_with_labels()

    def is_board_full(self):
        if all(self.board[i][j] != '' for i in range(1, 4) for j in range(1, 4)):
            self.animate_draw()
            return True
        return False
    def initialize_approval_system(self):
        self.approve_label = tk.Label(self.master, text="Approve your move", font=('Arial', 14))
        self.approve_label.grid(row=5, column=3)

        self.accept_button = tk.Button(self.master, text="Accept", font=('Arial', 12), command=self.accept_move)
        self.accept_button.grid(row=5, column=4)

        self.decline_button = tk.Button(self.master, text="Decline", font=('Arial', 12), command=self.decline_move)
        self.decline_button.grid(row=5, column=5)

        self.accept_button.config(state='disabled')
        self.decline_button.config(state='disabled')

    def propose_move(self, i, j):
        if not self.board[i][j] and self.current_player:
            self.buttons[i][j]['text'] = self.current_player
            self.proposed_move = (i, j)
            self.accept_button.config(state='normal')
            self.decline_button.config(state='normal')

    def accept_move(self):
        i, j = self.proposed_move
        self.board[i][j] = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.accept_button.config(state='disabled')
        self.decline_button.config(state='disabled')
        if self.check_winner():
            messagebox.showinfo("Game Over", f"'{self.current_player}' wins!")
            self.reset_board()
        elif self.is_board_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.reset_board()

    def decline_move(self):
        i, j = self.proposed_move
        self.buttons[i][j]['text'] = ''
        self.buttons[i][j]['bg'] = 'SystemButtonFace'
        self.accept_button.config(state='disabled')
        self.decline_button.config(state='disabled')


    def animate_winner(self, winning_indices):
        for _ in range(5):
            for i, j in winning_indices:
                self.buttons[i][j]['bg'] = 'red' if self.current_player == 'X' else 'blue'
                self.master.update()
                time.sleep(0.05)  # pause for animation
                self.buttons[i][j]['bg'] = 'SystemButtonFace'
                self.master.update()
                time.sleep(0.05)

    def animate_draw(self):
        for _ in range(5):  # animation cycles
            for i in range(1, 4):
                for j in range(1, 4):
                    self.buttons[i][j]['bg'] = '#808080'  # grey
                    self.master.update()
                    time.sleep(0.05)
                    self.buttons[i][j]['bg'] = 'SystemButtonFace'
                    self.master.update()
                    time.sleep(0.05)

    def add_search_functionality(self):
        self.search_button = tk.Button(self.master, text="Search Footballer", command=self.search_footballer) # search based on name
        self.search_button.grid(row=5, column=1)

    def search_footballer(self):
        player_name = simpledialog.askstring("Input", "Enter the footballer's name:", parent=self.master) # 3/4 outputs
        if player_name:
            urls = [
                f"https://www.google.com/search?tbm=isch&q={player_name.replace(' ', '+')}"
                f"https://yandex.by/search/?text={player_name.replace(' ', '+')}",
                f"https://en.wikipedia.org/wiki/{player_name.replace(' ', '_')}",
                f"https://www.whoscored.com/Search/?t={player_name.replace(' ', '+')}"
            ]
            for url in urls:
                webbrowser.open(url, new=4)
# here's preprocessed for the future updates, if they are
    '''
    def setup_timer(self):
        self.timer_label = Label(self.master, text="00:00", font=('Arial', 20))
        self.timer_label.grid(row=0, column=1, sticky='nsew')
        self.timer_entry = Entry(self.master, font=('Arial', 20))
        self.timer_entry.grid(row=0, column=2)
        self.start_button = Button(self.master, text="Start", command=self.start_timer)
        self.start_button.grid(row=0, column=3)
        self.stop_button = Button(self.master, text="Stop", command=self.stop_timer)
        self.stop_button.grid(row=0, column=4)
        self.reset_button = Button(self.master, text="Reset", command=self.reset_timer)
        self.reset_button.grid(row=0, column=5)
        self.timer_thread = None
        self.timer_running = False

    def timer_func(self):
        total_seconds = int(self.timer_entry.get()) * 60
        while total_seconds > 0 and self.timer_running:
            mins, secs = divmod(total_seconds, 60)
            self.timer_label.config(text=f'{mins:02d}:{secs:02d}')
            time.sleep(1)
            total_seconds -= 1
        self.timer_label.config(text="Time's up!")
        self.timer_running = False

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.timer_thread = threading.Thread(target=self.timer_func)
            self.timer_thread.start()

    def stop_timer(self):
        self.timer_running = False

    def reset_timer(self):
        self.stop_timer()
        self.timer_label.config(text="00:00")
        self.timer_entry.delete(0, tk.END)

    '''

if __name__ == '__main__':
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
