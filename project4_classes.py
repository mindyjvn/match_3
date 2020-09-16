#Mindy Jun
#ID: 25947137
FALLING = 0
FALLEN = 1
FROZEN = 2
MATCHED = 3

LEFT = -1
RIGHT = 1
DOWN = 0

class Faller:
    def __init__(self, jewels):
        self._active = False
        self._row = 0
        self._col = 0
        self.state = FALLING
        self._jewels = jewels
        self._match_pop = False

    def get_row(self):
        return self._row
    def get_col(self):
        return self._col
    def set_row(self, r):
        self._row = r
    def set_col(self, c):
        self._col = c
    def get_state(self):
        return self.state
    def set_state(self, s):
        self.state = s

    
class GameBoard:
    def __init__(self, rows, columns, field, jewels):
        self._rows = rows
        self._cols = columns
        self._field = field
        self._jewels = []
        for jewel in jewels:
            self._jewels.append('[' + jewel + ']')
        self._faller = Faller(jewels)
        self._match_made = False

    def get_field(self):
        return self._field

    #method from connectfour.py
    def lowest_empty_row(self, col):
        '''
        Determines the bottommost empty row within a given column, useful
        when dropping a piece; if the entire column in filled with pieces,
        this function returns -1
        '''
        for i in range(self._rows-1, -1, -1):
            if '   ' in self._field[i][col]:
                return i
        return -1

    def is_solid(self, row, col):
        '''Check if the cell is solid.'''
        empty_row = self.lowest_empty_row(col)
        #return True when the whole column is full
        if empty_row == -1:
            return True
        elif row > empty_row:
            return True
        return False

    def move(self, row, col, direction):
        '''Move the cell in the direction.'''
        temp = self._field[row][col]
        self._field[row][col] = '   '

        if direction == DOWN:
            row = row + 1
            self._field[row][col] = temp
        else:
            col = col + direction
            self._field[row][col] = temp
    
    def drop_frozen(self):
        '''Drops frozen cells to get rid of spaces underneath.'''
        for col in range(self._cols):
            for row in range(self._rows-1, -1, -1):
                cell = self._field[row][col]
                if not '   ' in cell:
                    i = 1
                    while not self.is_solid(row + i, col):
                        self.move(row+i-1, col, DOWN)
                        i += 1


    def make_faller(self, column, jewels):
        '''
        Construct a faller and resets all of its properties. This is in a separate method
        because it peeks the faller in row 0.
        '''
        if self._faller._active:
            return

        self._faller = Faller(jewels)
        self._jewels = jewels
        self._faller._active = True
        self._faller.set_row(0)
        self._faller.set_col(column-1)
        self._field[0][self._faller.get_col()] = self._jewels[0]
        self._faller.set_state(FALLING)
        
        self.update_faller_state()

    def rotate(self):
        '''Rotate so the last block becomes the first block.'''
        if not self._faller._active or self._faller.get_state() == FROZEN:
            return
        one = self._jewels[0]
        two = self._jewels[1]
        three = self._jewels[2]
        self._jewels = [two, three, one]

        row = self._faller.get_row()
        col = self._faller.get_col()
        if row >= 0:
            self._field[row][col] = self._jewels[0]
            if row-1 >= 0:
                self._field[row-1][col] = self._jewels[1]
                if row-2 >= 0:
                    self._field[row-2][col] = self._jewels[2]        

    def update_faller_state(self):
        '''Update the state of the faller.'''
        nxt_row = self._faller.get_row() + 1
        state = self._faller.get_state()
        if self.is_solid(nxt_row, self._faller.get_col()):
            self._faller.set_state(FALLEN)
            self.format()
            if state == FALLEN:
                self._faller.set_state(FROZEN)
                self.format()
        else:
            self._faller.set_state(FALLING)

    def tick(self):
        '''
        Ticks one time unit on the game. Fallers move down and matches occur.
        If this method returns true, the game ends.
        '''
        state = self._faller.get_state()
        if self._faller._active:
            if state == FALLEN:
                self.update_faller_state()
                if state == FALLEN:
                    above_board = False
                    if self._faller.get_row() - 2 < 0:
                        above_board = True
                    self._faller.set_state(FROZEN)
                    self._faller._active = False
                    self.match()
                    if self._match_made and above_board == True:
                        above_board = False
                        self._faller._match_pop = True
                    return above_board
            self.drop_faller()
            self.update_faller_state()
        self.match_vertical()
        self.match_horizontal()
        self.match_dia()
        if self._match_made:
            self.match()
            if self._faller._match_pop:
                self.match_drop_faller()
                self.match()
                self._faller._match_pop = False
        return False

    def drop_faller(self):
        '''Moves the faller down one space.'''
        row = self._faller.get_row()
        col = self._faller.get_col()
        if self.is_solid(row+1, col):
            self.update_faller_state()
            return

        self.move(row, col, DOWN)
        self._faller.set_state(FALLING)
        if row - 1 >= 0:
            self.move(row-1, col, DOWN)
            if row - 2 >= 0:
                self.move(row-2, col, DOWN)
            else:
                self._field[row-1][col] = self._jewels[2]
                self._faller.set_state(FALLING)
        else:
            self._field[row][col] = self._jewels[1]
            self._faller.set_state(FALLING)

        self._faller.set_row(row + 1)

    def match_drop_faller(self):
        '''Drops the rest of the faller after the first one or two jewels have been matched.'''
        row = self._faller.get_row()
        col = self._faller.get_col()
        if self.is_solid(row+1, col):
            self.update_faller_state()
            return

        empty_row = self.lowest_empty_row(col)
        if empty_row == 0:
            self._field[0][col] = self._jewels[1]
        elif empty_row > 0:
            self._field[1][col] = self._jewels[1]
            self._field[0][col] = self._jewels[2]
            self.drop_frozen()
            

    def move_faller(self, direction):
        '''Move the faller if possible.'''
        row = self._faller.get_row()
        col = self._faller.get_col()
        if not self._faller._active or (not direction == RIGHT and not direction == LEFT):
            return
        if (direction == LEFT and col == 0) or (direction == RIGHT and col == self._cols-1):
            return
        nxtCol = col + direction
        for i in range(3):
            if not self._field[row-i][nxtCol] == '   ':
                return

        for i in range(3):
            if row - i < 0:
                break
            self.move(row-i, col, direction)
        self._faller.set_col(nxtCol)
        self.update_faller_state()


    def match_vertical(self):
        '''Find all vertical matches and mark them with *.'''
        for row_index in range(self._rows - 2):
            for column_index in range(self._cols):
                cell = self._field[row_index][column_index]
                cell2 = self._field[row_index + 1][column_index]
                cell3 = self._field[row_index + 2][column_index]
                if (' ' in cell or '*' in cell) and not cell == '   ':
                    if (' ' in cell2 or '*' in cell2) and not cell2 == '   ':
                        if (' ' in cell3 or '*' in cell3) and not cell3 == '   ':
                            if cell[1] == cell2[1] == cell3[1]:
                                self._match_made = True
                                self._field[row_index][column_index] = '*' + cell[1] + '*'
                                self._field[row_index + 1][column_index] = '*' + cell2[1] + '*'
                                self._field[row_index + 2][column_index] = '*' + cell3[1] + '*'

    def match_horizontal(self):
        '''Find all horizontal matches and mark them with *.'''
        for column_index in range(self._cols - 2):
            for row_index in range(self._rows):
                cell = self._field[row_index][column_index]
                cell2 = self._field[row_index][column_index + 1]
                cell3 = self._field[row_index][column_index + 2]
                if (cell.startswith(' ') or cell.startswith('*')) and not cell == '   ':
                    if (cell2.startswith(' ') or cell2.startswith('*')) and not cell2 == '   ':
                        if (cell3.startswith(' ') or cell3.startswith('*')) and not cell3 == '   ':
                            if cell[1] == cell2[1] == cell3[1]:
                                self._match_made = True
                                self._field[row_index][column_index] = '*' + cell[1] + '*'
                                self._field[row_index][column_index + 1] = '*' + cell2[1] + '*'
                                self._field[row_index][column_index + 2] = '*' + cell3[1] + '*'

    def match_dia(self):
        '''Find all diagonal matches and mark them with *.'''
        #\ diagonals
        for row in range(3, self._rows + 1):
            for col in range(self._cols - 2):
                cell = self._field[row - 3][col]
                cell2 = self._field[row - 2][col + 1]
                cell3 = self._field[row - 1][col + 2]
                if (' ' in cell  or '*' in cell) and not cell == '   ':
                    if (' ' in cell2 or '*' in cell2) and not cell2 == '   ':
                        if (' ' in cell3  or '*' in cell3) and not cell3 == '   ':
                            if cell[1] == cell2[1] == cell3[1]:
                                self._match_made = True
                                self._field[row - 3][col] = '*' + cell[1] + '*'
                                self._field[row - 2][col + 1] = '*' + cell2[1] + '*'
                                self._field[row - 1][col + 2] = '*' + cell3[1] + '*'
        #/ diagonals
        for r in range(2, self._rows):
            for c in range(self._cols- 2 ):
                cell = self._field[r][c]
                cell2 = self._field[r - 1][c + 1]
                cell3 = self._field[r - 2][c + 2]
                if (' ' in cell or '*' in cell) and not cell == '   ':
                    if (' ' in cell2 or '*' in cell2) and not cell2 == '   ':
                        if (' ' in cell3 or '*' in cell3) and not cell3 == '   ':
                            if cell[1] == cell2[1] == cell3[1]:
                                self._match_made = True
                                self._field[r][c] = '*' + cell[1] + '*'
                                self._field[r - 1][c + 1] = '*' + cell2[1] + '*'
                                self._field[r - 2][c + 2] = '*' + cell3[1] + '*'


    def match(self):
        '''Destroys marked cells and moves them down. Checked again for matches.'''
        for row in range(self._rows):
            for col in range(self._cols):
                cell = self._field[row][col]
                if '*' in cell:
                    self._field[row][col] = '   '
        self.drop_frozen()
        self._match_made = False

        self.match_vertical()
        self.match_horizontal()
        self.match_dia()

    def format(self):
        ''' Correct the format of the faller depending on its state.'''
        state = self._faller.get_state()
        if state == FALLEN and '[' in self._jewels[0]:
            self._jewels[0] = '|' + self._jewels[0][1] + '|'
            self._jewels[1] = '|' + self._jewels[1][1] + '|'
            self._jewels[2] = '|' + self._jewels[2][1] + '|'
        elif state == FROZEN and '|' in self._jewels[0]:
            self._jewels[0] = ' ' + self._jewels[0][1] + ' '
            self._jewels[1] = ' ' + self._jewels[1][1] + ' '
            self._jewels[2] = ' ' + self._jewels[2][1] + ' '

        row = self._faller.get_row()
        col = self._faller.get_col()
        if row >= 0:
            self._field[row][col] = self._jewels[0]
            if row-1 >= 0:
                self._field[row-1][col] = self._jewels[1]
                if row-2 >= 0:
                    self._field[row-2][col] = self._jewels[2] 
            
