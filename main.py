# Code by Christopher Sommerville

import tkinter as tk
import tkinter.font as font
from tkinter import *
import time

from Board import Board

def show_graphics(board):
    window = tk.Tk()
    window.title("Sudoku Board")

    # window.resizable(width=False, height=False)
    squares = [[]]
    number_buttons = []
    text_variables = [[]]

    selected_row = tk.StringVar()
    selected_row.set(-1)
    selected_col = tk.StringVar()
    selected_col.set(-1)

    bg_color = '#242424' # Background color
    tile_color = '#454545' # '#9c7b21' # Non-selected tile color
    selected_color = '#ffffff' # '#0d7cd1' # Selected tile color
    fill_color = '#17baff' # Text color of filled tile
    correct_color = '#1cff42' # Text color of user filled tile if correct
    incorrect_color = '#ed1c1c' # Text color of user filled tile if incorrect
    text_color = '#ffffff' # Text color of already solved tile
    selected_button_color = '#26bad4'
    button_color = '#757575' # '#5c7b21'

    def new(board: Board):
        board.reset()
        board.create_solution()
        board.remove_values()
        squares[int(selected_row.get())][int(selected_col.get())]['bg'] = tile_color
        selected_row.set(-1)
        selected_col.set(-1)
        for i in range(9):
            for j in range(9):
                squares[i][j]['fg'] = text_color
                if board.values[i][j] > 0:
                    text_variables[i][j].set(board.values[i][j])
                else:
                    text_variables[i][j].set(" ")


    new_btn = tk.Button(
        master=window,
        text='New Game',
        font=font.Font(family='Courier', size=16, weight='bold'),
        command= lambda board=board: new(board),
        bg='#ad9300',
        fg='#ffffff'
    )  

    new_btn.grid(row=0, column = 10, padx = (10, 0), pady = (5, 0))

    mode = tk.StringVar()
    mode.set('Pencil')

    def pencil_mode():
        mode.set('Pencil')
        pencil_btn['bg'] = selected_button_color
        fill_btn['bg'] = button_color

    def fill_mode():
        mode.set('Fill')
        fill_btn['bg'] = selected_button_color
        pencil_btn['bg'] = button_color

    pencil_btn = tk.Button(
        master=window,
        text='Pencil',
        font=font.Font(family='Courier', size=16, weight='bold'),
        command= pencil_mode,
        bg=button_color,
        fg='#ffffff'
    )

    pencil_btn.grid(row=1, column = 10, padx = (10, 0), pady = (5, 0))

    fill_btn = tk.Button(
        master=window,
        text='Fill',
        font=font.Font(family='Courier', size=16, weight='bold'),
        command= fill_mode,
        bg=button_color,
        fg='#ffffff'
    )

    fill_btn.grid(row=2, column = 10, padx = (10, 0), pady = (5, 0))

    def select_square(i, j, board):
        old_i = int(selected_row.get())
        old_j = int(selected_col.get())
        if old_i >= 0 and old_j >= 0: 
            if squares[old_i][old_j]['fg'] == '#000000':
                squares[old_i][old_j]['fg'] = '#ffffff'
            squares[old_i][old_j]['bg'] = tile_color
        if i == old_i and j == old_j:
            selected_row.set(-1)
            selected_col.set(-1)
        else:
            if board.values[i][j] < 1:
                selected_row.set(i)
                selected_col.set(j)
                # print(f"i, j: {i, j}" )
                if squares[i][j]['fg'] == '#ffffff':
                    squares[i][j]['fg'] = '#000000' #0ebff0
                squares[i][j]['bg'] = selected_color


    for i in range(9):
        for j in range(9):
            v = tk.StringVar()
            if board.values[i][j] > 0:
                v.set(board.values[i][j])
            else:
                v.set(" ")
            btn = tk.Button(
                master=window,
                textvariable= v,
                font=font.Font(family='Courier', size=18, weight='bold'),
                command= lambda i=i, j=j, board=board: select_square(i, j, board),
                bg=tile_color,
                fg='#ffffff'
            )

            padding_x = (0, 0)
            padding_y = (0, 0)
            if j == 0 or j == 3 or j == 6:
                padding_x = (10, 0)
            if i == 0 or i == 3 or i == 6:
                padding_y = (10, 0)

            btn.grid(row=i, column = j + 1, padx = padding_x, pady = padding_y)

            if len(squares) > i:
                squares[i].append(btn)
                text_variables[i].append(v)
            else:
                squares.append([btn])
                text_variables.append([v])

    def set_value(val, board):
        row = int(selected_row.get())
        col = int(selected_col.get())
        if row > -1 and col > -1:
            if board.values[row][col] <= 0:
                if val == 0:
                    text_variables[row][col].set(" ")
                else:
                    if mode.get() == 'Fill':
                        if board.solution[row][col] == val:
                            squares[row][col]['fg'] = correct_color
                            text_variables[row][col].set(val)
                            board.values[row][col] = val
                        else:
                            squares[row][col]['fg'] = incorrect_color
                            text_variables[row][col].set(board.solution[row][col])
                            board.values[row][col] = val
                    if mode.get() == 'Pencil':
                        board.pencils[row][col].append(val)
                        

    blank_btn = tk.Button(
        master=window,
        text= " ",
        font=font.Font(family='Courier', size=18, weight='bold'),
        command= lambda i=i: set_value(0, board),
        bg='#5c7b21',
        fg='#ffffff'
    )
    # blank_btn.grid(row=9, column = 0, padx = (10, 0), pady = (15, 0))

    for i in range(9):
        btn = tk.Button(
            master=window,
            text= str(i + 1),
            font=font.Font(family='Courier', size=18, weight='bold'),
            command= lambda i=i: set_value(i + 1, board),
            bg='#5c7b21',
            fg='#ffffff'
        )
        padding_x = (0, 0)
        if i == 0 or i == 3 or i == 6:
            padding_x = (10, 0)
        btn.grid(row=9, column = i + 1, padx = padding_x, pady = (15, 0))
        number_buttons.append(btn)

    window.geometry("515x525")
    window.configure(bg=bg_color)
    window.mainloop()

# Function to test the efficiency of creating 'num_solutions' boards
# Reports how many total resets were required for all of the boards 
# Reports how many resets were required on average for a single board
# Reports the total time to create all of the boards and the average time to create a single board
def test_board_resets(board: Board, num_solutions: int=50):
    print("Creating solutions...")

    total_resets: int = 0
    count: int = 0
    total_time: float = 0
    for i in range(num_solutions):
        start = time.time()
        resets = board.create_solution()
        end = time.time()
        total_time += (end - start)
        total_resets += resets
        board.reset()
        # print("resets:", resets)

    print("num solutions: ", num_solutions)
    print()

    print("total resets:  ", total_resets)
    print(f"average resets: {'{:.2f}'.format(total_resets / num_solutions)}")
    print()
    
    print(f"total time:     {'{:.4f}'.format(total_time)}")
    print(f"avg time:       {'{:.4f}'.format(total_time / num_solutions)}")

def main():
    b = Board()
    b.create_solution()
    difficulty = 'medium'
    b.remove_values(difficulty)
    # b.solve()
    # test_board_resets(b)
    show_graphics(b)


main()