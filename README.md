# Minesweeper with AI Assistant

This is a classic Minesweeper game with an AI assistant to help you dodge those mines! 

## Features

* Play the classic Minesweeper game.
* Get help from the AI assistant to make safe moves. 
* The AI assistant uses logical reasoning to infer the location of mines based on the information revealed.
* Click to reveal cells and right-click to mark suspected mines.

## AI Assistant
* The AI Assistant assists by making safe moves based on the current state of the Minesweeper board. It utilizes logical reasoning and inference to identify safe and mine cells. The AI adds knowledge about revealed cells and adjusts its strategy accordingly.

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/Shauryainks/Minesweeper-with-AI-Assistant.git
cd Minesweeper-with-AI-Assistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Requirements

* Python 3
* Pygame library (install using `pip install pygame`)

## How to Play

1. Download the repository and install the required library (`pip install pygame`).
2. Run the game using `python runner.py`.
3. Click a cell to reveal it, or right-click to mark it as a suspected mine.
4. Use the "AI Move" button to let the AI assistant make a safe move for you (be aware that the AI might not always have a safe move available).
5. The goal is to reveal all safe cells without hitting a mine.
6. You win if you successfully flag all the mines!

## Assets

The `assets` folder contains the images and fonts used in the game.

## Contribution

Feel free to explore the code and customize the game. If you encounter issues or have suggestions, create an issue or submit a pull request. Contributions are welcome!

