import itertools
import random

def generate_24_grids(rows, cols, red, green, blue, red_weights, green_weights, blue_weights,
                       red_extra_weights, green_extra_weights, blue_extra_weights, adj_weights):
    
    def validate_quadrant_weights(weights):
        if sum(weights) != 10:
            print(f"Error: The sum of quadrant weights must be equal to 10. Given: {sum(weights)}")
            exit()

    def generate_empty_grid(rows, cols):
        return [['-' for _ in range(cols)] for _ in range(rows)]

    def count_neighbors(grid, row, col, rows, cols):
        neighbors = {'R': 0, 'G': 0, 'B': 0}
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] in neighbors:
                neighbors[grid[nr][nc]] += 1
        return neighbors

    def fill_quadrant(grid, quadrant, color_counts, color_weights, adj_weights, rows, cols, score):
        quadrant_map = {
            'UL': (0, 0, rows // 2, cols // 2),
            'UR': (0, cols // 2, rows // 2, cols),
            'LL': (rows // 2, 0, rows, cols // 2),
            'LR': (rows // 2, cols // 2, rows, cols)
        }

        r_start, c_start, r_end, c_end = quadrant_map[quadrant]
        positions = [(r, c) for r in range(r_start, r_end) for c in range(c_start, c_end)]
        random.shuffle(positions)

        for r, c in positions:
            neighbor_counts = count_neighbors(grid, r, c, rows, cols)
            scores = {
                color: color_weights[color][list(quadrant_map.keys()).index(quadrant)] +
                       sum(neighbor_counts[n] * adj_weights[color].get(n, 0) for n in 'RGB')
                for color in 'RGB'
            }

            sorted_colors = sorted(scores.keys(), key=lambda c: scores[c], reverse=True)

            for best_color in sorted_colors:
                if color_counts[best_color] > 0:
                    grid[r][c] = best_color
                    color_counts[best_color] -= 1
                    score[0] += scores[best_color]
                    break
    
    if red + green + blue != rows * cols:
        print("Error: The sum of Red, Green, and Blue cells must equal the total grid size. Please re-enter.")  
        exit()
    
    validate_quadrant_weights(red_weights)
    validate_quadrant_weights(green_weights)
    validate_quadrant_weights(blue_weights)
    validate_quadrant_weights(red_extra_weights)
    validate_quadrant_weights(green_extra_weights)
    validate_quadrant_weights(blue_extra_weights)
    
    best_grid = None
    best_score = float('-inf')
    quadrant_orders = list(itertools.permutations(['UL', 'UR', 'LR', 'LL']))[:24]

    for quadrant_order in quadrant_orders:
        grid = generate_empty_grid(rows, cols)
        color_counts = {'R': red, 'G': green, 'B': blue}
        color_weights = {'R': red_weights, 'G': green_weights, 'B': blue_weights}
        score = [0]

        for quadrant in quadrant_order:
            fill_quadrant(grid, quadrant, color_counts, color_weights, adj_weights, rows, cols, score)

        if score[0] > best_score:
            best_score = score[0]
            best_grid = grid

    return best_grid

rows = int(input("Enter the number of rows: "))
cols = int(input("Enter the number of columns: "))
red = int(input("Enter the number of red cells: "))
green = int(input("Enter the number of green cells: "))
blue = int(input("Enter the number of blue cells: "))
red_weights = list(map(float, input("Enter the quadrant weights for Red (UL, UR, LR, LL) sum equal to 10: ").split()))
green_weights = list(map(float, input("Enter the quadrant weights for Green (UL, UR, LR, LL) sum equal to 10: ").split()))
blue_weights = list(map(float, input("Enter the quadrant weights for Blue (UL, UR, LR, LL) sum equal to 10: ").split()))
red_extra_weights = list(map(float, input("If the number of rows or cols are odd, enter extra weights for Red (+x, -x, +y, -y, Origin) sum equal to 10: ").split()))
green_extra_weights = list(map(float, input("If the number of rows or cols are odd, enter extra weights for Green (+x, -x, +y, -y, Origin) sum equal to 10: ").split()))
blue_extra_weights = list(map(float, input("If the number of rows or cols are odd, enter extra weights for Blue (+x, -x, +y, -y, Origin) sum equal to 10: ").split()))

adj_weights = {}
print("Enter adjacency weights sum equal to 10::")
adj_weights['R'] = {'G': float(input("R-G: ")), 'B': float(input("R-B: "))}
adj_weights['G'] = {'B': float(input("G-B: ")), 'R': adj_weights['R']['G']}
adj_weights['B'] = {'R': adj_weights['R']['B'], 'G': adj_weights['G2']['B']}

best_grid = generate_24_grids(rows, cols, red, green, blue, red_weights, green_weights, blue_weights, red_extra_weights, green_extra_weights, blue_extra_weights, adj_weights)
print("Best grid:")
for row in best_grid:
    print(" ".join(row))
