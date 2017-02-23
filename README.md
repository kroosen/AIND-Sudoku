# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: A naked twin is identified as 2 boxes within the same unit that have exactly 2 digits which are the same. 
    This means that without knowing which box should have which digit, we can conclude that all the other boxes within
    that unit don't contain these 2 digits.
    We perform constraint propagation by looping over all the units and removing the 2 digits from a naked twin from 
    the possible values of all the other boxes within that unit. By doing this, we reduce the search space and speed up the algorithm.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: This is done simply by defining the 2 main diagonals as units and adding these to the unitlist.
    By doing this, we apply the rules of Sudoku to the diagonals as well. More rules = more constraints and this leads to a smaller search space.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.