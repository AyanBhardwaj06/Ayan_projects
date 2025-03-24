import random

def fill_grid(dimension, red, green, blue, diagonal_colors):
    total_cells = dimension * dimension
    total_colors = red + green + blue

    if total_colors != total_cells:
        print(f"Error: Incorrect number of colors. Need exactly {total_cells}, but have {total_colors}.")
        return
    
    grid = [[None] * dimension for _ in range(dimension)]
    color_counts = {'R': red, 'G': green, 'B': blue}

    # Get all diagonal positions (both main diagonal and anti-diagonal)
    main_diagonal = [(i, i) for i in range(dimension)]
    anti_diagonal = [(i, dimension - 1 - i) for i in range(dimension)]

    # Remove duplicates (center cell in odd-sized grids)
    all_diagonal_positions = []
    for pos in main_diagonal + anti_diagonal:
        if pos not in all_diagonal_positions:
            all_diagonal_positions.append(pos)
    
    random.shuffle(all_diagonal_positions)
    
    # First, try to fill all diagonal positions according to priority order
    for i, j in all_diagonal_positions:
        filled = False
        for priority_color in diagonal_colors:
            if color_counts[priority_color] > 0:
                grid[i][j] = priority_color
                color_counts[priority_color] -= 1
                filled = True
                break
    
    # Fill remaining empty positions
    empty_positions = [(i, j) for i in range(dimension) for j in range(dimension) if grid[i][j] is None]
    random.shuffle(empty_positions)
    
    for i, j in empty_positions:
        available_colors = [color for color in 'RGB' if color_counts[color] > 0]
        if available_colors:
            chosen_color = random.choice(available_colors)
            grid[i][j] = chosen_color
            color_counts[chosen_color] -= 1
    
    return grid

# Get user inputs
dimension = int(input("Enter the dimension: "))
red = int(input("Enter the number of red tiles: "))
green = int(input("Enter the number of green tiles: "))
blue = int(input("Enter the number of blue tiles: "))
diagonal_colors = input("Enter the colors for the diagonal in order (R/G/B, e.g., R G B): ").strip().upper().split()

grid = fill_grid(dimension, red, green, blue, diagonal_colors)

if grid:
    for row in grid:
        print(" ".join(row))
