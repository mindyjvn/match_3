#Mindy Jun
#ID: 25947137

import project4_classes as methods
JEWELS = ['S', 'T', 'V', 'W', 'X', 'Y', 'Z']

class InvalidInputError(Exception):
    '''Error raised when input is invalid.'''
    pass


def print_field(field):
    '''Prints field onto the screen.'''
    for row in field:
        row[0] = '|' + row[0]
        row[-1] = row[-1] + '|'
        
    for r in field:
        for c in r:
            print(c, end = '')
        print()
    print(' ' + ('-' * len(field[0]) * 3) + ' ')
    remove_bounds(field)
    return field

def remove_bounds(field):
    '''Removes the boundaries to get pure entries.'''
    for row in field:
        row[0] = row[0][1:]
        row[-1] = row[-1][:-1]
    return field


def empty_field(rows, cols):
    '''
    Print an empty field with rows in field and returns a list of the rows.
    '''
    field = []

    for row in range(rows):
        field.append([])
        for col in range(cols):
            field[row].append('   ')
    return methods.GameBoard(rows, cols, field, [' ', ' ', ' '])


def content_field(rows, cols):
    '''
    Print the field and return a list of the rows.
    '''
    contents = []
    #fill the field with each row (includes spaces)
    while not len(contents) == rows:
        i = list(input().upper())
        if not len(i) == cols:
            raise InvalidInputError()
        else:
            for index in range(len(i)):
                i[index] = ' ' + i[index] + ' '
            contents.append(i)

    #make a list of the columns
    columns_list = []
    for c in range(cols):
        temp = []
        for r in range(rows):
            temp.append(contents[r][c])
        columns_list.append(temp)

    #remove spaces from the columns
    columns_list_modified = []
    for column in columns_list:
        temp = [i for i in column if not i == '   ']
        columns_list_modified.append(temp)

    #add spaces back to end of columns
    final_columns = []
    for col in columns_list_modified:
        if not len(col) == rows:
            diff = abs(len(col) - rows)
            for num in range(diff):
                col.insert(0, '   ')
            final_columns.append(col)
            
    #make field with columns
    field = []
    for ro in range(rows):
        temp = []
        for co in range(cols):
            temp.append(final_columns[co][ro])
        field.append(temp)

    game = methods.GameBoard(rows, cols, field, [' ', ' ', ' '])
    game.match_vertical()
    game.match_horizontal()
    game.match_dia()
    return game

def command(game):
    while True:
        print_field(game.get_field())
        cmd = input()
        if cmd == 'Q':
            return
        if cmd == '':
            if game.tick():
                print_field(game.get_field())
                print('GAME OVER')
                return
        elif cmd == 'R':
            game.rotate()
        elif cmd == '<':
            game.move_faller(methods.LEFT)
        elif cmd == '>':
            game.move_faller(methods.RIGHT)
        elif cmd.startswith('F'):
            temp = cmd.split()
            col_num = int(temp[1])
            if not temp[4] in JEWELS or not temp[3] in JEWELS or not temp[2] in JEWELS:
                    raise InvalidInputError()
            if game.lowest_empty_row(col_num-1) == -1:
                print_field(game.get_field())
                print('GAME OVER')
                return
            jewels = ['['+temp[4]+']', '['+temp[3]+']', '['+temp[2]+']']
            game.make_faller(col_num, jewels) 


if __name__ == '__main__':
    try:
        rows = int(input()) #no less than 4
        cols = int(input()) #no less than 3
    except:
        InvalidInputError()

    empty_or_content = input().upper()
    field = []
    jewels = [' ', ' ', ' ']
    
    if empty_or_content.upper() == 'EMPTY':
        x = empty_field(rows, cols)
    elif empty_or_content.upper() == 'CONTENTS':
        x = content_field(rows, cols)
    game = x
    command(game)
    
