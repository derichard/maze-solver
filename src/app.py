from window import Window, Point, Line, Cell, Maze

def main():
    win = Window(1024, 900)
    maze = Maze(10, 10, 15, 15, 40, 40, win, seed=3, solve_speed=0.1)
    maze.solve(solve_algo="bfs")
    win.wait_for_close()

if __name__ == "__main__":
    main()