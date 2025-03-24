import random

def generate_grid(row, col, red, green, blue, pattern_length, pattern):
    if row * col != red + green + blue:
        return "Error: The total number of colored cells does not match the grid size!", 0
    if pattern_length > col:
        return "\n❌ This configuration cannot be possible! The pattern length exceeds the number of columns.", 0
    if len(pattern) != pattern_length:
        return "\n❌ Invalid Pattern: The specified pattern length does not match the given pattern!", 0
    def max_patterns_count(color_counts, pattern):
        pattern_color_counts = {color: pattern.count(color) for color in set(pattern)}
        return min(
            (color_counts.get(color, 0) // count if count > 0 else float('inf'))
            for color, count in pattern_color_counts.items()
        )
    def fill_remaining(grid, color_counts):
        empty_positions = [(r, c) for r in range(row) for c in range(col) if grid[r][c] == ' ']
        random.shuffle(empty_positions)
        for r, c in empty_positions:
            available_colors = [color for color in color_counts if color_counts[color] > 0]
            if available_colors:
                chosen_color = random.choice(available_colors)
                grid[r][c] = chosen_color
                color_counts[chosen_color] -= 1
    def fill_with_patterns(grid, pattern, max_patterns_count):
        applied_patterns = 0
        row_positions = list(range(0, row))
        random.shuffle(row_positions)
        
        for r in row_positions:
            if applied_patterns >= max_patterns_count:
                break
            col_positions = list(range(0, col - pattern_length + 1))
            random.shuffle(col_positions)
            for start_col in col_positions:
                end_col = start_col + pattern_length
                if applied_patterns >= max_patterns_count:
                    break
                if all(grid[r][c] == ' ' for c in range(start_col, end_col)):
                    for i, color in enumerate(pattern):
                        grid[r][start_col + i] = color
                        color_counts[color] -= 1
                    applied_patterns += 1
        return applied_patterns
    grid = [[' ' for _ in range(col)] for _ in range(row)]
    color_counts = {'R': red, 'G': green, 'B': blue}

    if max_patterns_count(color_counts, pattern) == 0:
        return "\n❌ This configuration cannot be possible!", 0

    patterns_applied = fill_with_patterns(grid, pattern, max_patterns_count(color_counts, pattern))
    fill_remaining(grid, color_counts)

    print(f"\nTotal patterns applied: {patterns_applied}")

    return grid
row = int(input("Enter number of rows: "))
col = int(input("Enter number of columns: "))
red = int(input("Enter number of red cells: "))
green = int(input("Enter number of green cells: "))
blue = int(input("Enter number of blue cells: "))
pattern_length = int(input("Enter the number of tiles for the pattern: "))
pattern = input(f"Enter the pattern of {pattern_length} tiles (e.g., RRGB): ").strip().upper()
grid = generate_grid(row, col, red, green, blue, pattern_length, pattern)
print("\nGenerated Grid:")
for row in grid:
    print(" ".join(row))