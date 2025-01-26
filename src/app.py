from window import Window, Point, Line, Cell, Maze

def main():
    win = Window(800, 600)
    maze = Maze(50, 50, 10, 20, 25, 25, win)

    win.wait_for_close()

if __name__ == "__main__":
    main()