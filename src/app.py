import argparse

from window import Window, Maze

WINDOW_HEIGHT = 1800
WINDOW_WIDTH = 900


def main():
    args = parse_args()
    print(args)
    win = Window(WINDOW_HEIGHT, WINDOW_WIDTH)
    maze = Maze(args.rows, args.cols, win=win, seed=None, solve_speed=0.05)
    maze.solve(solve_algo=args.solve_algo)
    win.wait_for_close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rows",
        type=int,
        default=10,
        help="Number of rows in the maze",
    )
    parser.add_argument(
        "--cols",
        type=int,
        default=10,
        help="Number of cols in the maze",
    )
    parser.add_argument(
        "--solve_algo",
        choices=["dfs", "bfs"],
        default="dfs",
        help="Solve algorithm",
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
