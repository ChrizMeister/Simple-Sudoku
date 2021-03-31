# Simple-Sudoku
 A relatively simple Sudoku game written in Python (currently a WIP).

![The Sudoku Game](https://i.gyazo.com/125531b43c15601296996752f86c89d7.png)

## Functionality
Currently this project generates a valid Sudoku solution by randomly selecting values for each square from the remaining possible values in each square. The program then removes a certain amount of values from each subgrid (or box) to create a Sudoku puzzle. Finally the program shows the user a GUI using Tkinter where the user can interact with the board, being able to fill in values or generate a new board. Correct values are filled in as green on the board and incorrect values are filled in as red.

## Current project goals
- Develop functionality for the user to be able to pencil in values on the Sudoku board
- Develop an 'undo' button which will allow the user to undo their last move
- Develop a solving algorithm that can resolve a board after removing values and can determine the difficulty of a given board. Show a button on the GUI which allows the user to 'give up' on the current puzzle and show them the solution.
- Highlight the row, column, & box of the currently selected square to assist the user in deciding their next move
- Develop a system to give the user a hint on what their next move should be
- Investigate other Python libraries to use as a GUI for the application

## Libraries used
- Numpy
- Tkinter