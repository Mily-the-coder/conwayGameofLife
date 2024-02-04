import grid
import time

empty_cell = '▢ '
full_cell = '▣ '

In_Console = True
debug = False

width = int(input("Width:  "))
height = int(input("Height: "))

cellGrid = grid.Grid(width, height, 0)


def show_cells():
    cellGrid.display_cells({0: empty_cell, 1: full_cell})


# console for setting where the live and dead cells are and the interval between generations
print("\nType 'help' for help.")
timer = None
while In_Console:
    console = input("> ").lower()
    cmd = console.split()

    if cmd[0] == 'set':

        cmd[1], cmd[2] = int(cmd[1]), int(cmd[2])

        if int(cmd[1]) > width or int(cmd[2]) > height:
            print('Failed to set cell: Out of range')
        else:
            if cellGrid.getCell((cmd[1], cmd[2])) == 0:
                value = 1
            else:
                value = 0
            cellGrid.setCell((cmd[1], cmd[2]), value)

            show_cells()

    elif cmd[0] == 'show':
        show_cells()

    elif cmd[0] == 'run':
        if len(cmd) == 1:
            timer = 0.5
        else:
            timer = float(cmd[1])
        In_Console = False

    elif cmd[0] == 'help':
        print("""-==|Commands|==-\n
    set  -Sets cell in grid to opposite of its value.\n
         -Syntax:  set [Tile X] [Tile Y]  ->  set 16 8\n
         \n
    show -Displays entire grid.\n
         -Syntax:  show\n
         \n
    run  -Runs program with optional time between generations (in seconds).\n
         -Syntax:  run [Time]  -> run 1.5   (if parameter time is empty default time is 0.5 seconds)\n
         """)

# main game loop
while not In_Console:
    frameGrid = grid.Grid(width, height, 0)
    frameGrid.grid = cellGrid.copy_grid()

    # main logic (rules)
    for cell in cellGrid.grid.keys():
        neighbor = cellGrid.getNeighbors(cell, False)
        live_neighbor_count = 0
        for j in neighbor.values():
            if j == 1:
                live_neighbor_count += 1
        if debug:
            print(live_neighbor_count)

        if cellGrid.getCell(cell) == 1:
            if live_neighbor_count < 2 or live_neighbor_count > 3:
                frameGrid.setCell(cell, 0)

            if live_neighbor_count == 2 or live_neighbor_count == 3:
                frameGrid.setCell(cell, 1)

        elif cellGrid.getCell(cell) == 0 and live_neighbor_count == 3:
            frameGrid.setCell(cell, 1)

    cellGrid.grid = frameGrid.copy_grid()

    show_cells()
    time.sleep(timer)
