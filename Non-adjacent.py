import random

def generate_colored_grid(n, m, red_count, green_count, blue_count):
    """Generates a valid n x m grid with no two adjacent tiles having the same color."""
    def is_valid(grid, row, col, color, n, m):
        """Checks if placing the given color at (row, col) is valid."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < n and 0 <= c < m and grid[r][c] == color:
                return False  # Adjacent tile has the same color
        return True

    def solve(grid, positions, color_counts, n, m):
        """Fills the grid ensuring no two adjacent tiles have the same color."""
        random.shuffle(positions)  # Shuffle positions for randomness
        
        for row, col in positions:
            available_colors = [color for color in ['R', 'G', 'B'] if color_counts[color] > 0 and is_valid(grid, row, col, color, n, m)]
            if available_colors:
                chosen_color = random.choice(available_colors)
                grid[row][col] = chosen_color
                color_counts[chosen_color] -= 1
        
    total_tiles = n * m
    if red_count + green_count + blue_count != total_tiles:
        print("Invalid input: Total number of tiles does not match grid size!")
        return None

    grid = [[None for _ in range(m)] for _ in range(n)]
    color_counts = {'R': red_count, 'G': green_count, 'B': blue_count}
    positions = [(i, j) for i in range(n) for j in range(m)]
    random.shuffle(positions)  # Shuffle positions for randomness
    solve(grid, positions, color_counts, n, m)
    
    # Collect remaining empty positions
    empty_positions = [(i, j) for i in range(n) for j in range(m) if grid[i][j] is None]
    random.shuffle(empty_positions)  # Shuffle for randomness
    
    # Fill remaining empty positions with available colors
    for row, col in empty_positions:
        available_colors = [color for color in ['R', 'G', 'B'] if color_counts[color] > 0]
        if available_colors:
            chosen_color = random.choice(available_colors)
            grid[row][col] = chosen_color
            color_counts[chosen_color] -= 1
    
    return grid

# User Input
n = int(input("Enter the number of rows: "))
m = int(input("Enter the number of columns: "))
red_count = int(input("Enter the number of Red tiles: "))
green_count = int(input("Enter the number of Green tiles: "))
blue_count = int(input("Enter the number of Blue tiles: "))

# Generate and print the grid
grid = generate_colored_grid(n, m, red_count, green_count, blue_count)

# Print the grid
if grid:
    for row in grid:
        print(" ".join(cell if cell is not None else '-' for cell in row))
