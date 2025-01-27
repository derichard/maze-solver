from window import Window, Point, Line, Cell, Maze

def main():
    win = Window(1024, 900)
    maze = Maze(10, 10, 20, 20, 40, 40, win, seed=0, solve_algo="bfs")
    maze.solve()
    win.wait_for_close()

if __name__ == "__main__":
    main()