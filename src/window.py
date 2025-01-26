from tkinter import Tk, BOTH, Canvas


class Window:

    def __init__(self, width, height, bg="white"):
        self.width = width
        self.height = height
        self.bg = bg
        self.root = Tk()
        self.root.title = "maze-solver"
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(self.root, bg=self.bg, height=self.height, width=self.width)
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
    def __init__(self, has_left_wall, has_right_wall, has_top_wall, has_bottom_wall, x1, y1, x2, y2, win):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self.p1 = Point(x1, y1)
        self.p2 = Point(x2, y2)
        self.win = win

    def draw(self):
        if self.has_left_wall:
            Line(self.p1, Point(self.p1.x, self.p2.y)).draw(self.win.canvas, "black")

        if self.has_right_wall:
            Line(self.p2, Point(self.p2.x, self.p1.y)).draw(self.win.canvas, "black")

        if self.has_top_wall:
            Line(self.p1, Point(self.p2.x, self.p1.y)).draw(self.win.canvas, "black")

        if self.has_bottom_wall:
            Line(self.p2, Point(self.p1.x, self.p2.y)).draw(self.win.canvas, "black")

    def draw_move(self, to_cell, undo=False):
        color = "gray" if undo else "red"

        center1 = Point((self.p2.x + self.p1.x)/2, (self.p2.y + self.p1.y)/2)
        center2 = Point((to_cell.p2.x + to_cell.p1.x)/2, (to_cell.p2.y + to_cell.p1.y)/2)
        print(center1, center2)
        line = Line(center1, center2)
        line.draw(self.win.canvas, color)