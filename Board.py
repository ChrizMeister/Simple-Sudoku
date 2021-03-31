# Code by Christopher Sommerville

import numpy as np
import random
import copy

# Class represting a Sudoku board
class Board:

    def __init__(self):
        self.reset()

    # Reset the entire board
    def reset(self):
        self.values = []
        self.solution = [[]]
        self.pencils = [[[0 for x in range(9)] for y in range(9)] for z in range(9)]

        for i in range(9):
            self.values.append([0 for x in range(9)])

        self.values = np.array(self.values)
        self.possible_values = [[[x + 1 for x in range(9)] for y in range(9)] for z in range(9)] # shape of (9, 9, 9)

    # TODO
    # Undo the last move made (a pencil or fill move) and return to the previous state
    # Requires keeping track of the previous state of self.values and self.pencils
    def undo(self):
        pass

    # Creates a solved Sudoku board by randomly generating values from the remaining possible values per individual square
    def create_solution(self):
        grids_filled = 0
        reset_count = 0
        while grids_filled < 9:
            while True:
                for i in range(9):
                    result = self.fill_subgrid(i)
                    # print(self.values[:9])

                    if result == -1:
                        # print("---Reset from beginning---")
                        grids_filled = 0
                        self.reset()
                        reset_count += 1
                        break
                    grids_filled += 1

                if grids_filled == 9:
                    pass
                    # print(f"Board solution after({reset_count} resets):")
                    # print(self.values)
                    self.solution = copy.deepcopy(self.values)
                    return reset_count
                break

            if reset_count > 250: # Should never be reached. Insurance to avoid infinite loop
                print("Could not generate solution")
                return reset_count


    # 0 = top left,    1 = top center,    2 = top right
    # 3 = middle left, 4 = middle center, 5 = middle right
    # 6 = bottom left, 7 = bottom center, 8 = bottom right
    # Fills a subgrid (9 squares) within the board
    # Returns 1 upon success
    # Returns 0 if the given grid_num is invalid (< 0 or > 8)
    # Returns -1 upon failure

    # Work on improving the algorithm to be more efficient
    def fill_subgrid(self, grid_num: int = -1):
        if grid_num < 0:
            print("Invalid grid number")
            return 0 
        cols = 3 * (grid_num % 3)
        rows = 3 * (grid_num // 3)

        save_state = copy.deepcopy(self.possible_values)
        count = 0
        while True:
            if count > 150:
                return -1 # Return failure if the subgrid cannot be filled
            try:
                count += 1
                for i in range(3): 
                    for j in range(3):
                        # if next line has only 3 choices, do not pick any of those choices on this line
                        if i < 2 and grid_num % 3 == 2:
                            curr_line_choices = self.possible_values[rows + i][cols + j]
                            next_line_choices = self.possible_values[rows + i + 1][cols + j]
                            
                            if len(next_line_choices) == 3:
                                for v in next_line_choices:
                                    if v in curr_line_choices:
                                        self.possible_values[rows + i][cols + j].remove(v)

                        must_picks = {}
                        must_pick_value = 0
                        found = False
                        for k in range(cols, cols + 3):
                            values = self.possible_values[rows + i][k]
                            if len(values) == 1:
                                found = True
                                must_picks[k] = values[0] # must_picks[index] = value

                        # remove values in must_picks from possible values in the remaining squares
                        for key in must_picks.keys():
                            for k in range(cols, cols + 3):
                                if k != key:
                                    if must_picks[key] in self.possible_values[rows + i][k]:
                                        self.possible_values[rows + i][k].remove(must_picks[key])

                        curr_value = np.random.choice(self.possible_values[rows + i][cols + j])
                        self.values[rows + i, cols + j] = curr_value
                        self.possible_values[rows + i][cols + j] = []

                        # remove from rest of row
                        for k in range(cols + j + 1, 9):
                            if curr_value in self.possible_values[rows + i][k]:
                                self.possible_values[rows + i][k].remove(curr_value)
                        
                        # remove from rest of column
                        for l in range(rows + i + 1, 9):
                            if curr_value in self.possible_values[l][cols + j]:
                                self.possible_values[l][cols + j].remove(curr_value)

                        # remove from rest of subgrid

                        for row in range(rows, rows + 3):
                            for col in range(cols, cols + 3):
                                if curr_value in self.possible_values[row][col]:
                                    self.possible_values[row][col].remove(curr_value)

                return 1 # Return 1 upon success
            except ValueError:
                # print("Reset")
                self.possible_values = copy.deepcopy(save_state)

    # Add more techniques for removing values
    def remove_values(self, difficulty = 'hard'):
        min_remove = 0
        max_remove = 0
        amount_to_remove = 0 # Total # of squares is 81
        # Hardest possible is remove 64 (leave 17 squares)
        if difficulty == 'medium':
            min_remove = 3
            max_remove = 6
            amount_to_remove = 40
        if difficulty == 'hard':
            min_remove = 4
            max_remove = 8
            amount_to_remove = 50
        
        # Randomly remove from each subgrid
        for i in range(9):
            cols = 3 * (i % 3)
            rows = 3 * (i // 3)
            indices = [x for x in range(9)]

            num_choices = random.randint(min_remove, max_remove)

            remove_indices = []
            for x in range(num_choices):
                val = random.choice(indices)
                while val in remove_indices:
                    val = random.choice(indices)
                remove_indices.append(val)

            index = 0
            for j in range(3):
                for k in range(3):
                    if index in remove_indices:
                        self.values[rows + j][cols + k] = 0
                    index += 1

    # Use backtracking to solve a board
    def solve(self):
        return
        # print(self.values)

    def pencil_value(self, value, row, col):
        if value not in self.pencils[row][col]:
            self.pencils[row][col].append(value)

    def remove_pencil(self, value, row, col):
        if value in self.pencils[row][col]:
            self.pencils[row][col].remove(value)

    # check if the given solution follows the Sudoku rules
    # Ensure that the puzzle is both UNIQUE and POSSIBLE
    def check_if_valid(self):
        pass

    def __str__(self):
        return str(self.values)