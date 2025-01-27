import time
import random

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
        self.visited = False

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
        if self.win is None:
            return
        color = "gray" if undo else "red"

        center1 = Point((self.p2.x + self.p1.x) / 2, (self.p2.y + self.p1.y) / 2)
        center2 = Point(
            (to_cell.p2.x + to_cell.p1.x) / 2, (to_cell.p2.y + to_cell.p1.y) / 2
        )
        line = Line(center1, center2)
        line.draw(self.win.canvas, color)

    def __repr__(self):
        return f"Cell({self.p1}, {self.p2})"
    
    def get_walls(self):
        return (self.has_left_wall, self.has_right_wall, self.has_top_wall, self.has_bottom_wall)


class Maze:
    def __init__(
        self,
        num_rows=10,
        num_cols=10,
        cell_size_x=40,
        cell_size_y=40,
        win=None,
        animation_speed=0.01,
        solve_speed=0.5,
        seed=None,
        x=10,
        y=10,
        entrance=None,
        exit=None
    ):  
        self.x = x
        self.y = y
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.animation_speed = animation_speed
        self.solve_speed = solve_speed
        self.cells = []
        self.create_cells()
        if seed is not None:
            random.seed(seed)
        if entrance is None:
            self.entrance = (random.randint(0, num_cols - 1), 0)
        else:
            self.entrance = entrance
        if exit is None:
            self.exit = (random.randint(0, num_cols - 1), num_rows - 1)
        else:
            self.exit = exit
        self.break_entrance_and_exit(self.entrance, self.exit)

        self.break_walls_r(*self.entrance)
        self.reset_cells_visited()
        

    def create_cells(self):
        for i in range(self.num_cols):
            col = []
            for j in range(self.num_rows):
                cell = Cell(
                    self.x + i * self.cell_size_x,
                    self.y + j * self.cell_size_y,
                    self.x + (i + 1) * self.cell_size_x,
                    self.y + (j + 1) * self.cell_size_y,
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
        self.animate(self.animation_speed)

    def animate(self, speed=None):
        self.win.redraw()
        time.sleep(speed)

    def break_entrance_and_exit(self, entrance, exit):
        self.cells[entrance[0]][entrance[1]].has_top_wall = False
        self.cells[exit[0]][exit[1]].has_bottom_wall = False
        self.draw_cell(*entrance)
        self.draw_cell(*exit)
                       
    def break_walls_r(self, i, j):
        self.cells[i][j].visited = True

        while True:
            neighbors = []
            if i > 0 and not self.cells[i - 1][j].visited:
                neighbors.append((i - 1, j))
            if j > 0 and not self.cells[i][j - 1].visited:
                neighbors.append((i, j - 1))
            if i < self.num_cols - 1 and not self.cells[i + 1][j].visited:
                neighbors.append((i + 1, j))
            if j < self.num_rows - 1 and not self.cells[i][j + 1].visited:
                neighbors.append((i, j + 1))

            if not neighbors:
                self.draw_cell(i, j)
                return

            next_i, next_j = random.choice(neighbors)
            if next_i < i:
                self.cells[i][j].has_left_wall = False
                self.cells[next_i][next_j].has_right_wall = False   
            if next_i > i:
                self.cells[i][j].has_right_wall = False
                self.cells[next_i][next_j].has_left_wall = False
            if next_j < j:
                self.cells[i][j].has_top_wall = False
                self.cells[next_i][next_j].has_bottom_wall = False 
            if next_j > j:
                self.cells[i][j].has_bottom_wall = False
                self.cells[next_i][next_j].has_top_wall = False

            self.break_walls_r(next_i, next_j)

    def reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.cells[i][j].visited = False

    def solve(self, solve_algo="dfs"):
        if solve_algo == "dfs":
            return self.solve_dfs_r(*self.entrance)
        elif solve_algo == "bfs":
            return self.solve_bfs(*self.entrance)
        else:
            raise NotImplementedError("Only dfs and bfs are supported")
    
    def get_neighbors(self, i, j):
        neighbors = []
        if i > 0 and not self.cells[i - 1][j].visited and not self.cells[i][j].has_left_wall:
            neighbors.append((i - 1, j))
        if j > 0 and not self.cells[i][j - 1].visited and not self.cells[i][j].has_top_wall:
            neighbors.append((i, j - 1))
        if i < self.num_cols - 1 and not self.cells[i + 1][j].visited and not self.cells[i][j].has_right_wall:
            neighbors.append((i + 1, j))
        if j < self.num_rows - 1 and not self.cells[i][j + 1].visited and not self.cells[i][j].has_bottom_wall:
            neighbors.append((i, j + 1))

        return neighbors
    
    def solve_bfs(self, i, j):
        queue = [(i, j)]

        while queue:
            i, j = queue.pop(0)
            self.cells[i][j].visited = True
            neighbors = self.get_neighbors(i, j)
            for next_i, next_j in neighbors:
                self.cells[i][j].draw_move(self.cells[next_i][next_j])
                self.animate(self.solve_speed)
                if next_i == self.exit[0] and next_j == self.exit[1]:
                    return True
            queue.extend(neighbors)

        return False
    
    def solve_dfs_r(self, i, j):
        if i == self.exit[0] and j == self.exit[1]:
            return True
        
        self.cells[i][j].visited = True   
        neighbors = self.get_neighbors(i, j)

        while neighbors:
            next_i, next_j = neighbors.pop()
            self.cells[i][j].draw_move(self.cells[next_i][next_j])
            self.animate(self.solve_speed)
            if self.solve_dfs_r(next_i, next_j):
                return True
            else:
                self.cells[i][j].draw_move(self.cells[next_i][next_j], undo=True)
                self.animate(self.solve_speed)

        return False


