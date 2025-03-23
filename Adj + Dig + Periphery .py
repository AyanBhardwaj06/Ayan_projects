import random

def generate_grid(dimension, red, green, blue, periphery_colors, diagonal_colors, adjacent_tiles):
    if dimension < 2:
        raise ValueError("Dimension must be at least 2")
    if any(c < 0 for c in (red, green, blue)):
        raise ValueError("Tile counts must be non-negative")
    
    def initialize_grid_and_counts():
        """Initialize an empty grid and color counts dictionary"""
        return [[None] * dimension for _ in range(dimension)], {'R': red, 'G': green, 'B': blue}

    def get_positions():
        """Get periphery and diagonal positions"""
        periphery = [(0, j) for j in range(dimension)] + \
                    [(i, dimension - 1) for i in range(1, dimension)] + \
                    [(dimension - 1, j) for j in range(dimension - 2, -1, -1)] + \
                    [(i, 0) for i in range(dimension - 2, 0, -1)]
        diagonal = list(dict.fromkeys([(i, i) for i in range(dimension)] +
                                      [(i, dimension - 1 - i) for i in range(dimension)]))
        return periphery, diagonal

    def fill_periphery(grid, periphery_positions, color_counts):
        """Fill periphery with available colors, prioritizing periphery_colors"""
        random.shuffle(periphery_positions)
        for i, j in periphery_positions:
            if grid[i][j] is None and periphery_colors and color_counts[periphery_colors[0]] > 0:
                grid[i][j] = periphery_colors[0]
                color_counts[periphery_colors[0]] -= 1

    def fill_diagonal(grid, diagonal_positions, color_counts):
        """Fill diagonal with available B tiles"""
        random.shuffle(diagonal_positions)
        for i, j in diagonal_positions:
            if grid[i][j] is None and diagonal_colors and color_counts[diagonal_colors[0]] > 0:
                grid[i][j] = diagonal_colors[0]
                color_counts[diagonal_colors[0]] -= 1

    def ensure_adjacency(grid, color_counts, tile1, tile2):
        """Ensure tile1 and tile2 are adjacent where possible"""
        empty_positions = [(i, j) for i in range(dimension) for j in range(dimension) if grid[i][j] is None]
        random.shuffle(empty_positions)
        pairs_needed = min(color_counts[tile1], color_counts[tile2])

        for _ in range(pairs_needed):
            for i, j in empty_positions[:]:
                if color_counts[tile1] > 0:
                    grid[i][j] = tile1
                    color_counts[tile1] -= 1
                    empty_positions.remove((i, j))
                    adjacent_positions = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                    random.shuffle(adjacent_positions)
                    for ai, aj in adjacent_positions:
                        if (0 <= ai < dimension and 0 <= aj < dimension and
                            grid[ai][aj] is None and color_counts[tile2] > 0):
                            grid[ai][aj] = tile2
                            color_counts[tile2] -= 1
                            empty_positions.remove((ai, aj))
                            break
                    break

    def fill_remaining(grid, color_counts):
        """Fill remaining positions with exact counts"""
        empty_positions = [(i, j) for i in range(dimension) for j in range(dimension) if grid[i][j] is None]
        remaining_tiles = [tile for tile, count in color_counts.items() for _ in range(count)]
        random.shuffle(remaining_tiles)
        
        valid_colors = ['R', 'G', 'B']
        while len(remaining_tiles) < len(empty_positions):
            remaining_tiles.append(random.choice(valid_colors))
        
        for (i, j), tile in zip(empty_positions, remaining_tiles[:len(empty_positions)]):
            grid[i][j] = tile

    # Validate constraints
    total_cells = dimension * dimension
    valid_colors = {'R', 'G', 'B'}
    if not all(c in valid_colors for c in periphery_colors + diagonal_colors + adjacent_tiles):
        raise ValueError("Invalid colors detected. Use only R, G, B.")
    if len(adjacent_tiles) != 2:
        raise ValueError("Exactly 2 adjacent tiles required.")
    if red + green + blue != total_cells:
        raise ValueError(f"Color counts ({red + green + blue}) don't match grid size ({total_cells}).")

    # Generate one grid with randomization for variety
    grid, color_counts = initialize_grid_and_counts()
    periphery_positions, diagonal_positions = get_positions()

    fill_periphery(grid, periphery_positions, color_counts)
    fill_diagonal(grid, diagonal_positions, color_counts)
    ensure_adjacency(grid, color_counts, adjacent_tiles[0], adjacent_tiles[1])
    fill_remaining(grid, color_counts)

    return grid  # Single return point for the grid

# Take input outside the function
dimension = int(input("Enter the dimension of the square grid: "))
red = int(input("Enter the number of red tiles: "))
green = int(input("Enter the number of green tiles: "))
blue = int(input("Enter the number of blue tiles: "))
periphery_colors = input("Enter periphery colors (e.g., R G B): ").strip().upper().split()
diagonal_colors = input("Enter diagonal colors (e.g., R G B): ").strip().upper().split()
adjacent_tiles = input("Enter two tiles for adjacency (e.g., R G): ").strip().upper().split()

# Generate and print one sample grid
grid = generate_grid(dimension, red, green, blue, periphery_colors, diagonal_colors, adjacent_tiles)
for row in grid:
    print(" ".join(row))
