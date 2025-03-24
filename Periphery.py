import sys
import random

def fill_grid(rows, cols, red, green, blue, periphery_colors):
    total_tiles = rows * cols
    
    if red + green + blue != total_tiles:
        print(f"Invalid input! The total number of tiles ({red + green + blue}) must be equal to {total_tiles}.")
        sys.exit(1)
    
    # Initialize the grid with None
    grid = [[None] * cols for _ in range(rows)]
    color_counts = {'R': red, 'G': green, 'B': blue}

    # Define periphery positions
    periphery_positions = [(0, j) for j in range(cols)] + [(rows - 1, j) for j in range(cols)] + \
                          [(i, 0) for i in range(1, rows - 1)] + [(i, cols - 1) for i in range(1, rows - 1)]

    # Shuffle periphery positions to make selection random
    random.shuffle(periphery_positions)

    # Assign periphery colors in the order given by the user
    for color in periphery_colors:
        for i, j in periphery_positions:
            if grid[i][j] is None and color_counts[color] > 0:
                grid[i][j] = color
                color_counts[color] -= 1

    # Fill remaining periphery positions with available colors
    for i, j in periphery_positions:
        if grid[i][j] is None:
            available_colors = [color for color in 'RGB' if color_counts[color] > 0]
            if available_colors:
                chosen_color = random.choice(available_colors)
                grid[i][j] = chosen_color
                color_counts[chosen_color] -= 1

    # Collect empty positions
    empty_positions = [(i, j) for i in range(rows) for j in range(cols) if grid[i][j] is None]
    random.shuffle(empty_positions)  # Shuffle the empty positions

    # Fill the shuffled empty positions with available colors
    for i, j in empty_positions:
        available_colors = [color for color in 'RGB' if color_counts[color] > 0]
        if available_colors:
            chosen_color = random.choice(available_colors)
            grid[i][j] = chosen_color
            color_counts[chosen_color] -= 1

    return grid

# Input handling
rows = int(input("Enter the number of rows: "))
cols = int(input("Enter the number of columns: "))
red = int(input("Enter the number of red tiles: "))
green = int(input("Enter the number of green tiles: "))
blue = int(input("Enter the number of blue tiles: "))
periphery_colors = input("Enter the colors for the periphery in order (R/G/B, e.g., R B G): ").strip().upper().split()

# Generate grid
grid = fill_grid(rows, cols, red, green, blue, periphery_colors)

# Print the grid
if grid:
    for row in grid:
        print(" ".join(cell if cell is not None else '-' for cell in row))
