# CS 170 Project Spring 2021

Take a look at the project spec before you get started!

Requirements:

Python 3.6+

You'll only need to install networkx to work with the starter code. For installation instructions, follow: https://networkx.github.io/documentation/stable/install.html

If using pip to download, run `python3 -m pip install networkx`


Files:
- `parse.py`: functions to read/write inputs and outputs
- `solver.py`: where you should be writing your code to solve inputs
- `utils.py`: contains functions to compute cost and validate NetworkX graphs

When writing inputs/outputs:
- Make sure you use the functions `write_input_file` and `write_output_file` provided
- Run the functions `read_input_file` and `read_output_file` to validate your files before submitting!
  - These are the functions run by the autograder to validate submissions


Instructions:
1. Adust filepaths in the last if statement of `solver.py` according to which graphs you want to run: small, medium, or large. For example, if you want to run small graphs, you would change line the input of 217 to be `inputs/small/*`. On line, 222, modify the path to be `outputs/small/`
2. Run `python3 solver.py` to create 300 output files for the respective graph type
3. Repeat Steps 1 and 2 for both medium and large graphs.
4. Submit to CS170 Leaderboard.
5. Repeat Steps 1, 2, 3, and 4 for a week to continue generating the best outputs.
