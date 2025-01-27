from window import Window, Point, Line, Cell, Maze

def main():
    win = Window(1024, 900)
    maze = Maze(10, 10, 25, 25, 40, 40, win, seed=None, solve_algo="dfs", solve_speed=0.1)
    maze.solve()
    win.wait_for_close()

if __name__ == "__main__":
    main()