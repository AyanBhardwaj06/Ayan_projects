

import random

def generate_colored_grid(dimension, red, green, blue, diagonal_colors, adjacent_tiles):
    def fill_grid():
        total_cells = dimension * dimension
        total_colors = red + green + blue

        if total_colors != total_cells:
            print("Error: Incorrect number of colors.")
            return None

        color_counts.update({'R': red, 'G': green, 'B': blue})
        main_diagonal = [(i, i) for i in range(dimension)]
        anti_diagonal = [(i, dimension - 1 - i) for i in range(dimension)]
        all_diagonal_positions = list(dict.fromkeys(main_diagonal + anti_diagonal))
        random.shuffle(all_diagonal_positions)

        for i, j in all_diagonal_positions:
            filled = False
            for priority_color in diagonal_colors:
                if color_counts[priority_color] > 0:
                    grid[i][j] = priority_color
                    color_counts[priority_color] -= 1
                    filled = True
                    break

            if not filled:
                available_colors = [c for c in 'RGB' if color_counts[c] > 0]
                random.shuffle(available_colors)
                for color in available_colors:
                    if color_counts[color] > 0:
                        grid[i][j] = color
                        color_counts[color] -= 1
                        break

    def violates_adjacency(row, col, tile):
        adjacent_positions = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        other_colors = {'R', 'G', 'B'} - set(adjacent_tiles)
        same_adjacent_count = 0

        for r, c in adjacent_positions:
            if 0 <= r < dimension and 0 <= c < dimension:
                if grid[r][c] == tile:
                    return True
                if grid[r][c] in other_colors:
                    same_adjacent_count += 1

        return same_adjacent_count >= 2

    def fill_with_adjacency():
        tile1, tile2 = sorted(adjacent_tiles, key=lambda x: color_counts[x])
        tile1_positions = []
        empty_positions = [(i, j) for i in range(dimension) for j in range(dimension) if grid[i][j] is None]
        random.shuffle(empty_positions)

        for i, j in empty_positions[:]:
            if color_counts[tile1] > 0 and not violates_adjacency(i, j, tile1):
                grid[i][j] = tile1
                color_counts[tile1] -= 1
                tile1_positions.append((i, j))
                empty_positions.remove((i, j))
                adjacent_positions = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                random.shuffle(adjacent_positions)

                for ai, aj in adjacent_positions:
                    if (0 <= ai < dimension and 0 <= aj < dimension and grid[ai][aj] is None and color_counts[tile2] > 0):
                        grid[ai][aj] = tile2
                        color_counts[tile2] -= 1
                        empty_positions.remove((ai, aj))

        for i, j in tile1_positions:
            diagonal_positions = [(i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1)]
            for di, dj in diagonal_positions:
                if (0 <= di < dimension and 0 <= dj < dimension and grid[di][dj] is None and color_counts[tile1] > 0):
                    grid[di][dj] = tile1
                    color_counts[tile1] -= 1
                    empty_positions.remove((di, dj))
                    if color_counts[tile1] == 0:
                        break
            if color_counts[tile1] == 0:
                break

        remaining_tiles = [tile for tile, count in color_counts.items() for _ in range(count)]
        random.shuffle(remaining_tiles)

        for i, j in empty_positions:
            if remaining_tiles:
                grid[i][j] = remaining_tiles.pop()

    grid = [[None] * dimension for _ in range(dimension)]
    color_counts = {}

    fill_grid()
    if None in [tile for row in grid for tile in row]:
        fill_with_adjacency()

    return grid

# Take input outside the function
dimension = int(input("Enter the dimension: "))
red = int(input("Enter the number of red tiles: "))
green = int(input("Enter the number of green tiles: "))
blue = int(input("Enter the number of blue tiles: "))
diagonal_colors = input("Enter the colors for the diagonal in order (R G B): ").strip().upper().split()
adjacent_tiles = input("Enter two tiles for adjacency constraint (e.g., R G): ").strip().upper().split()

# Run the function
grid = generate_colored_grid(dimension, red, green, blue, diagonal_colors, adjacent_tiles)
for row in grid:
    print(" ".join(row))