import random

def fill_grid(rows, cols, red, green, blue, periphery_colors):
    grid = [[None] * cols for _ in range(rows)]
    color_counts = {'R': red, 'G': green, 'B': blue}

    # Define periphery positions
    periphery_positions = [(0, j) for j in range(cols)] + [(rows - 1, j) for j in range(cols)] + \
                          [(i, 0) for i in range(1, rows - 1)] + [(i, cols - 1) for i in range(1, rows - 1)]
    
    # Shuffle periphery positions
    random.shuffle(periphery_positions)
    
    # Assign periphery colors
    index = 0
    for i, j in periphery_positions:
        if index < len(periphery_colors) and color_counts[periphery_colors[index]] > 0:
            grid[i][j] = periphery_colors[index]
            color_counts[periphery_colors[index]] -= 1
            index += 1
    
    # Collect all empty positions
    empty_positions = [(i, j) for i in range(rows) for j in range(cols) if grid[i][j] is None]
    random.shuffle(empty_positions)
    
    # Assign colors randomly to empty positions
    for i, j in empty_positions:
        available_colors = [color for color in 'RGB' if color_counts[color] > 0]
        if available_colors:
            chosen_color = random.choice(available_colors)
            grid[i][j] = chosen_color
            color_counts[chosen_color] -= 1
    
    return grid

# Example usage
rows = int(input("Enter the number of rows: "))
cols = int(input("Enter the number of columns: "))
red = int(input("Enter the number of red tiles: "))
green = int(input("Enter the number of green tiles: "))
blue = int(input("Enter the number of blue tiles: "))
periphery_colors = input("Enter the colors for the periphery in order (R/G/B, e.g., R B G): ").strip().upper().split()

grid = fill_grid(rows, cols, red, green, blue, periphery_colors)

# Display grid
print("\nGenerated Grid:")
for row in grid:
    print(" ".join(row))
