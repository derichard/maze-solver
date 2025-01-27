import unittest


from window import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1.cells),
            num_cols,
        )
        self.assertEqual(
            len(m1.cells[0]),
            num_rows,
        )

    def test_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        entrance = (0, 0)
        exit = (num_cols - 1, num_rows - 1)
        m1 = Maze(num_rows, num_cols, entrance=entrance, exit=exit)
        m1.break_entrance_and_exit((0,0), exit)
        self.assertFalse(m1.cells[0][0].has_top_wall)
        self.assertFalse(m1.cells[num_cols - 1][num_rows - 1].has_bottom_wall)

    def test_break_walls_r(self):
        num_cols = 5
        num_rows = 5
        m1 = Maze(num_rows, num_cols, 10, 10, seed=0)
        print(m1.cells[2][3].get_walls())
        self.assertEqual(m1.cells[2][3].get_walls(), (False, False, True, True))

    def test_reset_cells_visited(self):
        num_cols = 5
        num_rows = 5
        m1 = Maze(num_rows, num_cols, 10, 10, seed=0)
        m1.cells[2][3].visited = True
        m1.reset_cells_visited()
        self.assertFalse(m1.cells[2][3].visited)
        self.assertFalse(any(c.visited for col in m1.cells for c in col))

if __name__ == "__main__":
    unittest.main()