# Keaton Ufheil
# created 7/31/19
import copy


class Board:
    """ An object which simulates a generic Game Of Life-esque board, in which
    an nxn grid contains cells which can be in an arbitrary number of states.
    A Board object also holds a grid of rules which govern state transitions
    between cells. The object also holds flags on how the simulation is to be
    run (dead-cell edges vs. cylindrical mapping), and buckets within which
    cells will be counted for each individual cell.Finally, the Board can
    advance its state according to these rules.
    """
    default_grid_size = 10
    # Note: due to list comprehension scoping rules the inner list comp.
    # range argument cannot be default_grid_size
    default_grid = [[0 for x in range(10)] for y in range(default_grid_size)]
    default_rule_set = [["'def'", 'surrounding[1] == 3'],
                         ['surrounding[1] < 2 or surrounding[1] > 3', "'def'"]]
    for row in default_rule_set:
        for transition in row:
            transition = compile(transition, '', 'eval')
    default_bucket = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0),
                      (-1, 1), (0, 1), (1, 1)]
    default_num_states = 2
    default_mode = 'NO-CHECK'

    def __init__(self, grid_size=default_grid_size, grid=default_grid,
                 rule_set=default_rule_set, bucket=default_bucket,
                 mode=default_mode, num_states=default_num_states):
        self.grid_size = grid_size
        self.grid = grid
        self.rule_set = rule_set
        self.bucket = bucket
        self.mode = mode
        self.num_states = num_states

    def fancy_print(self):
        """Print out the board's current state in a (somewhat) visually
        appealing manner in 2d space on the console
        """
        for row in self.grid:
            for entry in row:
                print(entry, end=' ')
            print()

    def set(self, x, y, state):
        """Sets the cell at [x][y] in the grid to state"""
        self.grid[x][y] = state

    def advance(self):
        """Advance the Board's grid according to its existing state and rules
        """
        future_grid = copy.deepcopy(self.grid)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                surrounding = [0 for state in range(self.num_states)]
                cur_cell_state = self.grid[i][j]
                for rel_pos in self.bucket:
                    if self.mode == 'NO-CHECK':
                        # NO-CHECK implies that would-be cells that lie outside
                        # of the grid are simply ignored
                        try:
                            nearby_x = i + rel_pos[0]
                            nearby_y = j + rel_pos[1]
                            nearby_cell = self.grid[nearby_x][nearby_y]
                            surrounding[nearby_cell] += 1
                        except IndexError:
                            pass
                    elif self.mode == 'WRAP':
                        # WRAP implies that if a check goes past its bounds,
                        # wrap to the other side of the grid and check there
                        wrapped_x = i + rel_pos[0] % self.grid_size
                        wrapped_y = j + rel_pos[1] % self.grid_size
                        nearby_cell = self.grid[wrapped_x][wrapped_y]
                        surrounding[nearby_cell] += 1

                # now the cells around our current cell have been accounted for
                possible_transitions = self.rule_set[cur_cell_state]
                for index in range(self.num_states):
                    # avoid checking for transition to the same state
                    # as that is already the default behaviour
                    if index != cur_cell_state:
                        if eval(possible_transitions[index]):
                            future_grid[i][j] = index
                            break

        self.grid = future_grid

b = Board()