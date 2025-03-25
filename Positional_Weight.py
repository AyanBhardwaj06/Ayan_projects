import itertools
import random

def generate_color_grid(rows, cols, red, green, blue, red_weights, green_weights, blue_weights, 
                        red_extra_weights, green_extra_weights, blue_extra_weights, adj_weights):
    # Validate grid dimensions
    if not (isinstance(rows, int) and isinstance(cols, int) and rows > 0 and cols > 0):
        raise ValueError("Rows and columns must be positive integers")
        
    # Validate cell counts
    if not (isinstance(red, int) and isinstance(green, int) and isinstance(blue, int)):
        raise ValueError("Cell counts must be integers")
    if red < 0 or green < 0 or blue < 0:
        raise ValueError("Cell counts cannot be negative")
    if red + green + blue != rows * cols:
        raise ValueError("Sum of cell counts must equal total grid size")
        
    # Validate weight lists
    for weights, name in [(red_weights, "Red"), (green_weights, "Green"), (blue_weights, "Blue")]:
        if not (isinstance(weights, list) and len(weights) == 4 and abs(sum(weights) - 10) < 1e-6):
            raise ValueError(f"{name} quadrant weights must be 4 numbers summing to 10")
            
    for weights, name in [(red_extra_weights, "Red"), (green_extra_weights, "Green"), (blue_extra_weights, "Blue")]:
        if not (isinstance(weights, list) and len(weights) == 5 and abs(sum(weights) - 10) < 1e-6):
            raise ValueError(f"{name} extra weights must be 5 numbers summing to 10")
            
    # Validate adjacency weights
    if not isinstance(adj_weights, dict) or not all(c in adj_weights for c in 'RGB'):
        raise ValueError("Adjacency weights must be a dictionary with R, G, B keys")
    weight_sum = adj_weights['R'].get('G', 0) + adj_weights['R'].get('B', 0) + adj_weights['G'].get('B', 0)
    if abs(weight_sum - 10) > 1e-6:
        raise ValueError("Adjacency weights must sum to 10")

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

    def fill_extra_cells(grid, color_counts, extra_weights, adj_weights, rows, cols, score):
        extra_positions = []
        extra_weight_map = {
            "+x": 0, "-x": 1, "+y": 2, "-y": 3, "O": 4
        }

        if rows % 2 == 1:
            extra_positions += [(rows // 2, c, "+x") for c in range(cols // 2 + 1, cols)]
            extra_positions += [(rows // 2, c, "-x") for c in range(0, cols // 2)]

        if cols % 2 == 1:
            extra_positions += [(r, cols // 2, "+y") for r in range(0, rows // 2)]
            extra_positions += [(r, cols // 2, "-y") for r in range(rows // 2 + 1, rows)]

        if rows % 2 == 1 and cols % 2 == 1:
            extra_positions.append((rows // 2, cols // 2, "O"))

        random.shuffle(extra_positions)

        for r, c, pos_type in extra_positions:
            neighbor_counts = count_neighbors(grid, r, c, rows, cols)
            weight_index = extra_weight_map[pos_type]

            scores = {
                color: extra_weights[color][weight_index] +
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

    best_grids = []
    quadrant_orders = list(itertools.permutations(['UL', 'UR', 'LR', 'LL']))[:24]

    for quadrant_order in quadrant_orders:
        grid = generate_empty_grid(rows, cols)
        color_counts = {'R': red, 'G': green, 'B': blue}
        color_weights = {'R': red_weights, 'G': green_weights, 'B': blue_weights}
        extra_weights = {'R': red_extra_weights, 'G': green_extra_weights, 'B': blue_extra_weights}
        score = [0]

        for quadrant in quadrant_order:
            fill_quadrant(grid, quadrant, color_counts, color_weights, adj_weights, rows, cols, score)

        fill_extra_cells(grid, color_counts, extra_weights, adj_weights, rows, cols, score)

        best_grids.append((score[0], grid))

    best_grids.sort(reverse=True, key=lambda x: x[0])
    return best_grids[0][1]  # Return the best grid

# Custom input collection
try:
    rows = int(input("Enter the number of rows: "))
    cols = int(input("Enter the number of columns: "))
    
    red = int(input("Enter the number of red cells: "))
    green = int(input("Enter the number of green cells: "))
    blue = int(input("Enter the number of blue cells: "))
    
    red_weights = list(map(float, input("Enter the quadrant weights for Red (UL UR LR LL): ").split()))
    green_weights = list(map(float, input("Enter the quadrant weights for Green (UL UR LR LL): ").split()))
    blue_weights = list(map(float, input("Enter the quadrant weights for Blue (UL UR LR LL): ").split()))
    
    red_extra_weights = list(map(float, input("Enter extra weights for Red (+x -x +y -y Origin): ").split()))
    green_extra_weights = list(map(float, input("Enter extra weights for Green (+x -x +y -y Origin): ").split()))
    blue_extra_weights = list(map(float, input("Enter extra weights for Blue (+x -x +y -y Origin): ").split()))
    
    adj_weights_input = list(map(float, input("Enter adjacency weights for Red-Green, Red-Blue, Green-Blue: ").split()))
    adj_weights = {
        'R': {'G': adj_weights_input[0], 'B': adj_weights_input[1]},
        'G': {'R': adj_weights_input[0], 'B': adj_weights_input[2]},
        'B': {'R': adj_weights_input[1], 'G': adj_weights_input[2]}
    }

    # Generate and print grid
    grid = generate_color_grid(rows, cols, red, green, blue, 
                              red_weights, green_weights, blue_weights,
                              red_extra_weights, green_extra_weights, blue_extra_weights, 
                              adj_weights)
    for row in grid:
        print(" ".join(row))

except ValueError as e:
    print(f"Error: {e}")
except IndexError:
    print("Error: Incorrect number of weights provided")
except Exception as e:
    print(f"Error: An unexpected error occurred - {e}")