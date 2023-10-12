  # CONWAY'S GAME OF LIFE

## Video Demo:  <https://www.youtube.com/watch?v=UrAH45YTkQU>

## Description:
This Python program simulates Conway's Game of Life, a cellular automaton devised by mathematician John Conway. The game consists of a grid of cells that evolve over time based on simple rules.

## Features:

### Simulation:
Runs multiple simulations of the game on a customizable grid size. The core functionality is implemented in the 'conway' module, where the game field evolves based on predefined rules.


#### Termination Conditions:
The program stops each simulation if the game:
 - **Dies**: all cells are of value 0.
 - **Stagnates**: the field does not chenge from one generation to the next one.
 - **Loops**: the field cycles from varius stages until achieving a previous state.

 Simulation will run until achieving one of these conditions. If the field does not get to any of these end conditions before the predefined longest generation allowed, it will consider that the game is still **Evolving**, and it will quote the Jeff Goldblum character from the original Jurassic Park movie:
 > Life, uh, finds a way.

#### Visualizations:
- **Terminal Display**:
Results of each simulation are displayed on the terminal, with options for verbose and interactive modes.

- **Graphic mode**:
The program allows to create a GIF file illustrating the evolution of the game gor each run.
However, this files will not open automatically, as the program is conceived primarily for running multiple simulations and then saving the data and get some statistical or graphical representation of them. So, it will be very time-consuming to display the GIF file for all of the simulations.


#### Modes:
- **Verbose:** Displays the initial state of the field for each run or for each generation.
- **Interactive:** Prompts user confirmation before running each simulation, or for advancing a generation during any simulation.
- **Graphic:** Generates GIF files illustrating the evolution of the game for each run.
- **Recording:** Saves data for each generation in a CSV file.

### Plotting:
 Reads the CSV file that stores data for all previous simulations, allowing to create graphs showing:
- **1. Evolution of total population:** Asks the user for a size of field and creates a scattering graph showing all possible results for the population value for each generation and run. It also plots lines for the shortest run, i.e, the one that stops on a lower generation; and for the longest. Lastly, it displays the mean value of the population for each generation.
- **2. Comparison of population:** Asks the user for different sizes of fields (up to 4), and creates a graph very similar to the first case, but normalizing both X and Y axis, using a fraction of the longest run for each sixe for the X's, and the % of the fields that are alive for the Y's.
- **3. Length of runs by size:** Asks the user for field sizes (between 1 and 4), and creates a type histogram graph for the length of each run, i.e. the end generation for every simulation recorded for that given field. It also shows on the graph, textually, the values for mean, median and modes of the length of the runs.
- **4. End results by size:** Asks the user for field sized (up to 8), and creates a histogram showing how frequent each of the end conditions is achieved, and allowing to compare between sizes.

## Usage

1. **Run Simulation with default values:**

    Size: 25

    Longest generation allowed: 250

    Total number of simulations: 25

    Displays results on terminal, does not record data
    ```
    python project.py
    ```
    - **Customize size value:**

    -n N: will change field size to NxN,

    for [2 <= N <= 480]

    (for example, -n 47 will run simulations of size 47x47)
    ```
    python project.py -n N
    ```
    - **Customize maximum allowed generation value:**

    -t T: will change generation limit to T,

    for [1 <= T <= 10,000]
    ```
    python project.py -t T
    ```
    - **Customize number of simulations:**

    -s S: will change total number of runs to S,

    for [1 <= S <= 1,000]
    ```
    python project.py -t T
    ```


2. **Verbose Mode:**

    -v: Shows initial state for each run.

    -vv: Shows all stages of every simulation.

    ```
    python project.py -v
    python project.py -vv
3. **Interactive Mode:**

    -i: Asks the user for confirmation before running each simulation.

    -ii: Asks the user for confirmation before advancing a generation..

    ```
    python project.py -i
    python project.py -ii
    ```
4. **Graphic Mode:**

    -g: It will save GIFs showing the evolution of the field for each simulation.

    GIF's are saved on the folder *</cgl_images/>*. The program will erase all GIF's for the same field size on the folder whenever prompted again.
    ```
    python project.py -g
    ```

5. **Recording Mode:**

    -r: It will save data for field size, runs, generations, total population, % of population and end result for each stage of the simulations. It also creates a timestamp for each line of the CSV file.

    CSV file is saved on the folder *</cgl_logs/>*.
    ```
    python project.py -r
    ```


6. **Plotting Mode:**


    -p: does not run simulation mode, instead the program will read the CSV file: *</cgl_logs/cgl_log.csv>* and then prompt the user for type of graph desired, and which field size or sizes for the data to plot.

    ```
    python project.py -p
    ```

## Testng

Ensure the correctness of the code by running unit tests:


    pytest test_project.py


## Dependencies

- Python 3.x
- Required packages:
    - Numpy
    - matplotlib
    - csv
    - datetime
    - math
    - pandas
    - sys
    - PIL
    - argparse
    - os
- Font file <arial.ttf> must be saved on root folder

## Contributors

- Javier Ramalleira: <https://github.com/ramafoz>