import random

def fill_grid_combined(dimension, red, green, blue, periphery_colors, diagonal_colors, constraint_priority):
    def initialize_grid():
        return [[None] * dimension for _ in range(dimension)]

    def get_positions():
        periphery = [(0, j) for j in range(dimension)] + \
                    [(i, dimension - 1) for i in range(1, dimension)] + \
                    [(dimension - 1, j) for j in range(dimension - 2, -1, -1)] + \
                    [(i, 0) for i in range(dimension - 2, 0, -1)]
        diagonal = list(set([(i, i) for i in range(dimension)] + [(i, dimension - 1 - i) for i in range(dimension)]))
        random.shuffle(periphery)
        random.shuffle(diagonal)
        return periphery, diagonal

    def assign_priority():
        return [(diagonal_positions, diagonal_colors), (periphery_positions, periphery_colors)] if constraint_priority == "diagonal" else [(periphery_positions, periphery_colors), (diagonal_positions, diagonal_colors)]

    def fill_positions(priority_order):
        for positions, color_priority in priority_order:
            if not color_priority:
                continue
            for i, j in positions:
                if grid[i][j] is not None:
                    continue
                assigned = False
                for color in color_priority:
                    if color_counts[color] > 0:
                        grid[i][j] = color
                        color_counts[color] -= 1
                        assigned = True
                        break
                if not assigned:
                    for color in 'RGB':
                        if color_counts[color] > 0:
                            grid[i][j] = color
                            color_counts[color] -= 1
                            break

    def fill_remaining():
        empty_positions = [(i, j) for i in range(dimension) for j in range(dimension) if grid[i][j] is None]
        random.shuffle(empty_positions)
        available_colors = ['R'] * color_counts['R'] + ['G'] * color_counts['G'] + ['B'] * color_counts['B']
        random.shuffle(available_colors)
        
        for (i, j), color in zip(empty_positions, available_colors):
            grid[i][j] = color

    if red + green + blue != dimension * dimension:
        raise ValueError(f"Error: The sum of tiles must equal {dimension * dimension} (dimension²). Please try again.")

    grid = initialize_grid()
    color_counts = {'R': red, 'G': green, 'B': blue}
    periphery_positions, diagonal_positions = get_positions()
    priority_order = assign_priority()
    fill_positions(priority_order)
    fill_remaining()
    return grid

# Taking input outside the function
dimension = int(input("Enter the dimension of the square grid: "))
red = int(input("Enter the number of red tiles: "))
green = int(input("Enter the number of green tiles: "))
blue = int(input("Enter the number of blue tiles: "))

# Default constraints applied
periphery_colors = list(dict.fromkeys(input("Enter periphery colors (R G B): ").strip().upper().split()))
diagonal_colors = list(dict.fromkeys(input("Enter diagonal colors (R G B): ").strip().upper().split()))
constraint_priority = input("Enter constraint priority (diagonal/periphery): ").strip().lower()

# Generating and printing the grid
grid = fill_grid_combined(dimension, red, green, blue, periphery_colors, diagonal_colors, constraint_priority)
for row in grid:
    print(" ".join(row))
