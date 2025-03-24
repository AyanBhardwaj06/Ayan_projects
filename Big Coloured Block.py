def generate_grid(row, col, red, green, blue, block_color, block_size, block_count):
    grid = [[' ' for _ in range(col)] for _ in range(row)]
    color_counts = {'R': red, 'G': green, 'B': blue}
    max_possible_blocks = min(block_count, color_counts.get(block_color, 0) // (block_size ** 2))
    placed_blocks = 0
    available_rows = list(range(0, row - block_size+1))
    random.shuffle(available_rows)
    
    for row_index in available_rows:
        if placed_blocks >= max_possible_blocks:
            break
        available_cols = list(range(0, col - block_size+1))
        random.shuffle(available_cols)
        for col_index in available_cols:
            if placed_blocks >= max_possible_blocks:
                break
            if all(grid[r][c] == ' ' for r in range(row_index, row_index + block_size) for c in range(col_index, col_index + block_size)):
                for r in range(row_index, row_index + block_size):
                    for c in range(col_index, col_index + block_size):
                        grid[r][c] = block_color
                placed_blocks += 1
                color_counts[block_color] -= (block_size ** 2)
    
    if placed_blocks < block_count:
        print(f"Warning: Could only place {placed_blocks} out of {block_count} blocks.")

    empty_positions = [(r, c) for r in range(row) for c in range(col) if grid[r][c] == ' ']
    random.shuffle(empty_positions)

    for r, c in empty_positions:
        available_colors = [color for color in color_counts if color_counts[color] > 0]
        if available_colors:
            chosen_color = random.choice(available_colors)
            grid[r][c] = chosen_color
            color_counts[chosen_color] -= 1

    return grid



row = int(input("Enter number of rows: "))
col = int(input("Enter number of columns: "))
red = int(input("Enter number of red cells: "))
green = int(input("Enter number of green cells: "))
blue = int(input("Enter number of blue cells: "))
block_color = input("Enter block color (R/G/B): ").strip().upper()
block_size = int(input("Enter block size: "))
block_count = int(input("Enter number of blocks: "))
grid = generate_grid(row, col, red, green, blue, block_color, block_size, block_count)
print("\nGenerated Grid:")
for row in grid:
    print(" ".join(row))


