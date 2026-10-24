# mazegen

Maze generator with seed, '42' pattern and shortest path.

## Basic use

    from mazegen import MazeGenerator
    from mazegen.board import Grid, Point
    from mazegen.solver import solve

    grid = Grid(20, 15)
    MazeGenerator(grid, seed=42).generate()

## Custom parameters

    Grid(width, height)
    MazeGenerator(grid, seed=42, blocked=cells_to_keep_closed)

The same seed and the same parameters give the same maze.

## Access the maze and a solution

    grid.get_cell(Point(0, 0))   # int 0-15, bits N=1 E=2 S=4 W=8, 1 = wall
    solve(grid, Point(0, 0), Point(19, 14))   # e.g. "EESSE..."