import random

def generate_grid(row, col, red, green, blue, periphery_order):
    """Generates a valid grid based on user input."""

    def is_valid(grid, x, y, color):
        """Check if placing color at (x, y) does not touch the same color."""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        return all(
            not (0 <= x + dx < len(grid) and 0 <= y + dy < len(grid[0]) and grid[x + dx][y + dy] == color)
            for dx, dy in directions
        )

    def fill_grid(grid, color_counts):
        """Fills the grid with colors based on given constraints."""
        positions = [(0, i) for i in range(col)] + [(row - 1, i) for i in range(col)] + \
                    [(i, 0) for i in range(1, row - 1)] + [(i, col - 1) for i in range(1, row - 1)]
        
        random.shuffle(positions)
        
        # Place colors in periphery first
        for color in periphery_order:
            for x, y in positions:
                if grid[x][y] == ' ' and color_counts[color] > 0:
                    grid[x][y] = color
                    color_counts[color] -= 1

        # Fill remaining positions
        empty_positions = [(i, j) for i in range(row) for j in range(col) if grid[i][j] == ' ']
        random.shuffle(empty_positions)
        
        for x, y in empty_positions:
            for color in random.sample(['R', 'G', 'B'], 3):
                if color_counts[color] > 0 and is_valid(grid, x, y, color):
                    grid[x][y] = color
                    color_counts[color] -= 1
                    break
        
        # Final pass to fill any remaining empty spaces
        empty_positions = [(i, j) for i in range(row) for j in range(col) if grid[i][j] == ' ']
        random.shuffle(empty_positions)
        
        for x, y in empty_positions:
            for color in random.sample(['R', 'G', 'B'], 3):
                if color_counts[color] > 0:
                    grid[x][y] = color
                    color_counts[color] -= 1
                    break

    if row * col != red + green + blue:
        print("Error: The total number of colored cells does not match the grid size!")
        return None

    grid = [[' ' for _ in range(col)] for _ in range(row)]
    color_counts = {'R': red, 'G': green, 'B': blue}
    
    fill_grid(grid, color_counts)

    return grid

# User Input
row = int(input("Enter number of rows: "))
col = int(input("Enter number of columns: "))
red = int(input("Enter number of red cells: "))
green = int(input("Enter number of green cells: "))
blue = int(input("Enter number of blue cells: "))
periphery_order = input("Enter the order of periphery colors (space-separated, e.g., G R B): ").split()
4
grid = generate_grid(row, col, red, green, blue, periphery_order)

# Print the grid if successfully generated
if grid:
    for r in grid:
        print(' '.join(r))
