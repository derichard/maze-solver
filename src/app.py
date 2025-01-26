from window import Window, Point, Line, Cell

def main():
    win = Window(800, 600)
    p1 = Point(10, 10)
    p2 = Point(100, 200)
    line = Line(p1, p2)

    cell1 = Cell(True, True, False, True, 200, 200, 300, 300, win)
    cell1.draw()

    cell2 = Cell(True, True, False, True, 400, 400, 500, 500, win)
    cell2.draw()
    cell1.draw_move(cell2)

    win.draw_linw(line, "red")

    win.wait_for_close()

if __name__ == "__main__":
    main()