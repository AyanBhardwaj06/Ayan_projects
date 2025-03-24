import random

def fill_grid_combined(dimension, red, green, blue, periphery_colors=None, diagonal_colors=None):
    total_cells = dimension * dimension
    if red + green + blue != total_cells:
        print(f"Error: The sum of tiles must equal {total_cells} (dimension²). Please try again.")
        return None
    
    grid = [[None] * dimension for _ in range(dimension)]
    color_counts = {'R': red, 'G': green, 'B': blue}
    all_colors = ['R', 'G', 'B']

    periphery_positions = []
    for j in range(dimension):
        periphery_positions.append((0, j))
    for i in range(1, dimension):
        periphery_positions.append((i, dimension - 1))
    for j in range(dimension - 2, -1, -1):
        periphery_positions.append((dimension - 1, j))
    for i in range(dimension - 2, 0, -1):
        periphery_positions.append((i, 0))

    main_diagonal = [(i, i) for i in range(dimension)]
    anti_diagonal = [(i, dimension - 1 - i) for i in range(dimension)]
    all_diagonal_positions = main_diagonal + anti_diagonal

    diagonal_index = 0
    for pos in all_diagonal_positions:
        i, j = pos
        if grid[i][j] is not None:
            continue
        if diagonal_colors and diagonal_index < len(diagonal_colors) and color_counts[diagonal_colors[diagonal_index]] > 0:
            grid[i][j] = diagonal_colors[diagonal_index]
            color_counts[diagonal_colors[diagonal_index]] -= 1
        else:
            # Randomly select from available colors with remaining count
            available_colors = [color for color in all_colors if color_counts[color] > 0]
            if available_colors:
                chosen_color = random.choice(available_colors)
                grid[i][j] = chosen_color
                color_counts[chosen_color] -= 1
        diagonal_index = (diagonal_index + 1) % len(diagonal_colors) if diagonal_colors else 0

    periphery_index = 0
    for pos in periphery_positions:
        i, j = pos
        if grid[i][j] is not None:
            continue
        if periphery_colors and periphery_index < len(periphery_colors) and color_counts[periphery_colors[periphery_index]] > 0:
            grid[i][j] = periphery_colors[periphery_index]
            color_counts[periphery_colors[periphery_index]] -= 1
        else:
            # Randomly select from available colors with remaining count
            available_colors = [color for color in all_colors if color_counts[color] > 0]
            if available_colors:
                chosen_color = random.choice(available_colors)
                grid[i][j] = chosen_color
                color_counts[chosen_color] -= 1
        periphery_index = (periphery_index + 1) % len(periphery_colors) if periphery_colors else 0

    empty_positions = [(i, j) for i in range(dimension) for j in range(dimension) if grid[i][j] is None]
    random.shuffle(empty_positions)
    
    remaining_colors = []
    for color, count in color_counts.items():
        remaining_colors.extend([color] * count)
    random.shuffle(remaining_colors)
    
    for i, (x, y) in enumerate(empty_positions):
        grid[x][y] = remaining_colors[i]

    return grid


dimension = int(input("Enter the dimension of the square grid: "))
total_cells = dimension * dimension

red = int(input("Enter the number of red tiles: "))
green = int(input("Enter the number of green tiles: "))
blue = int(input("Enter the number of blue tiles: "))

periphery_colors = input("Enter the color pattern for the periphery in order (R/G/B, e.g., R G B): ").strip().upper().split()
diagonal_colors = input("Enter the color pattern for the diagonal in order (R/G/B, e.g., R G B): ").strip().upper().split()

grid = fill_grid_combined(dimension, red, green, blue, periphery_colors, diagonal_colors)

for row in grid:
    print(" ".join(row))
