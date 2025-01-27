import time

from tkinter import Tk, BOTH, Canvas


class Window:

    def __init__(self, width, height, bg="white"):
        self.width = width
        self.height = height
        self.bg = bg
        self.root = Tk()
        self.root.title = "maze-solver"
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(
            self.root, bg=self.bg, height=self.height, width=self.width
        )
        self.canvas.pack(fill=BOTH, expand=1)
        self.is_running = False

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.is_running = True
        while self.is_running:
            self.redraw()

    def close(self):
        self.is_running = False

    def draw_linw(self, line, fill_color):
        line.draw(self.canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class Line:
    def __init__(self, p1, p2, width=2):
        self.p1 = p1
        self.p2 = p2
        self.width = width

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x,
            self.p1.y,
            self.p2.x,
            self.p2.y,
            fill=fill_color,
            width=self.width,
        )


class Cell:
    def __init__(
        self,
        x1,
        y1,
        x2,
        y2,
        win=None,
    ):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.p1 = Point(x1, y1)
        self.p2 = Point(x2, y2)
        self.win = win

    def draw(self):
        if self.has_left_wall:
            Line(self.p1, Point(self.p1.x, self.p2.y)).draw(self.win.canvas, "black")
        else:
            Line(self.p1, Point(self.p1.x, self.p2.y)).draw(self.win.canvas, self.win.bg)

        if self.has_right_wall:
            Line(self.p2, Point(self.p2.x, self.p1.y)).draw(self.win.canvas, "black")
        else:
            Line(self.p2, Point(self.p2.x, self.p1.y)).draw(self.win.canvas, self.win.bg)

        if self.has_top_wall:
            Line(self.p1, Point(self.p2.x, self.p1.y)).draw(self.win.canvas, "black")
        else:
            Line(self.p1, Point(self.p2.x, self.p1.y)).draw(self.win.canvas, self.win.bg)

        if self.has_bottom_wall:
            Line(self.p2, Point(self.p1.x, self.p2.y)).draw(self.win.canvas, "black")
        else:
            Line(self.p2, Point(self.p1.x, self.p2.y)).draw(self.win.canvas, self.win.bg)   

    def draw_move(self, to_cell, undo=False):
        color = "gray" if undo else "red"

        center1 = Point((self.p2.x + self.p1.x) / 2, (self.p2.y + self.p1.y) / 2)
        center2 = Point(
            (to_cell.p2.x + to_cell.p1.x) / 2, (to_cell.p2.y + to_cell.p1.y) / 2
        )
        print(center1, center2)
        line = Line(center1, center2)
        line.draw(self.win.canvas, color)

    def __repr__(self):
        return f"Cell({self.p1}, {self.p2})"


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.cells = []
        self.create_cells()
        self.break_entrance_and_exit()

    def create_cells(self):
        for i in range(self.num_cols):
            col = []
            for j in range(self.num_rows):
                cell = Cell(
                    self.x1 + i * self.cell_size_x,
                    self.y1 + j * self.cell_size_y,
                    self.x1 + (i + 1) * self.cell_size_x,
                    self.y1 + (j + 1) * self.cell_size_y,
                    self.win,
                )
                col.append(cell)
            self.cells.append(col)

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.draw_cell(i, j)

    def draw_cell(self, i, j):
        if self.win is None:
            return
        self.cells[i][j].draw()
        self.animate()

    def animate(self):
        self.win.redraw()
        time.sleep(0.05)

    def break_entrance_and_exit(self):
        self.cells[0][0].has_top_wall = False
        self.cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self.draw_cell(0, 0)
        self.draw_cell(self.num_cols - 1, self.num_rows - 1)
