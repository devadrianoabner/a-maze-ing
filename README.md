*This project has been created as part of the 42 curriculum by adrianda, lucferre.*

## Description

A-Maze-ing generates a maze from a configuration file, writes it to a file
in hexadecimal, and shows it in the terminal. The maze can be perfect (one
single path) or a playable board for a Pac-Man-like game (several routes,
no dead ends). A "42" pattern is drawn with fully closed cells.

## Instructions

Requirements: Python 3.10 or later.

    make install
    make run                      # uses config.txt
    make run CONFIG=other.txt
    make lint

Menu: new maze with a new seed, same seed again, show or hide the shortest
path, rotate the wall colours, quit.

## Config file

One `KEY=VALUE` per line. Lines starting with `#` are ignored.

| Key         | Description                         | Example           |
|-------------|-------------------------------------|-------------------|
| WIDTH       | Number of columns                   | WIDTH=20          |
| HEIGHT      | Number of rows                      | HEIGHT=15         |
| ENTRY       | Entry coordinates x,y               | ENTRY=0,0         |
| EXIT        | Exit coordinates x,y                | EXIT=19,14        |
| OUTPUT_FILE | Output filename                     | OUTPUT_FILE=maze.txt |
| PERFECT     | True or False                       | PERFECT=False     |
| SEED        | Optional integer, repeats the maze  | SEED=42           |

## Algorithm

Growing tree: a list of active cells, one is picked at random, opens a wall
to an unvisited neighbour, and that neighbour becomes active. A cell leaves
the list when it has no free neighbours. With PERFECT=False, every dead end
gets one more wall opened, skipping any opening that would create a 3x3
open area.

Why: it is simple, always gives a connected maze, is reproducible with a
seed, and the same loop covers both modes.

## Reusable code

The `mazegen` package (built as `mazegen-1.0.0-py3-none-any.whl`) holds
`MazeGenerator`, `Grid`, `solve` and the output writer. See
`mazegen/README.md`.

    pip install mazegen-1.0.0-py3-none-any.whl

## Team and project management

- Roles: 
- Planning and how it evolved: 
- What worked well / what to improve: 
- Tools: Python, flake8, mypy, pydocstyle, build, git.

## Resources

- Maze generation algorithms (Prim, Kruskal, growing tree, recursive backtracker) and BFS
- **AI usage:** 
Debugging, code review, and conceptualizing new features