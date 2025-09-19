Pro AI Pathfinding Visualizer
A Python-based tool built with Pygame to visualize classic pathfinding algorithms like A*, Dijkstra's, and Breadth-First Search (BFS) on an interactive grid.

![GIF of the pathfinding visualizer in action]
(Note: You should record a short GIF of your program running and replace the line above. Tools like ScreenToGif or GIPHY Capture are great for this.)

🚀 Features
Multiple Algorithms: Visualize and compare A*, Dijkstra's, and Breadth-First Search.

Interactive Grid: Add walls, weights ('mud'), and set the start/end points with your mouse.

Maze Generation: Instantly create a random maze to challenge the algorithms.

Modern UI: A clean control panel to run algorithms, generate mazes, and clear the grid.

Performance Stats: See the final path length and the number of nodes visited after a search is complete.

🛠️ Installation & Setup
To get a local copy up and running, follow these simple steps.

Clone the repository:

Bash

git clone https://github.com/Daksh5151/your-repo-name.git
cd your-repo-name
(Remember to replace your-repo-name with the actual name of your repository.)

Install dependencies:
This project requires Pygame. You can install it using the provided requirements.txt file.

Bash

pip install -r requirements.txt
Run the visualizer:

Bash

python advanced_pathfinding_visualizer.py
🎮 How to Use
Use your mouse and keyboard to interact with the grid and the control panel.

Mouse Controls
Left Mouse Button:

First click: Place the Start Node.

Second click: Place the End Node.

Subsequent clicks: Draw Barriers/Walls.

Middle Mouse Button: Draw Weighted Nodes ('mud'), which are more "expensive" to travel through.

Right Mouse Button: Erase any node (start, end, barrier, or weight).

Keyboard & UI Controls
You can either press the corresponding keys or click the buttons on the UI panel.

Run A* Search: Press the 'A' key.

Run Dijkstra's Algorithm: Press the 'D' key.

Run Breadth-First Search (BFS): Press the 'B' key.

Generate Maze: Press the 'M' key to clear the grid and generate a new random maze.

Clear Grid: Press the 'C' key to reset the grid to a blank state.
