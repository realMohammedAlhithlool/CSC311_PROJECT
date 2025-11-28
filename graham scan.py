import matplotlib.pyplot as plt
import math
import time

# ---------------------------------------------------------
# 1. Helper Functions (Math & Logic)
# ---------------------------------------------------------

def polar_angle(p0, p1):
    """Calculates the polar angle of p1 with respect to p0."""
    y_span = p1[1] - p0[1]
    x_span = p1[0] - p0[0]
    return math.atan2(y_span, x_span)

def distance_sq(p0, p1):
    """Calculates the squared Euclidean distance between p0 and p1."""
    return (p1[0] - p0[0])**2 + (p1[1] - p0[1])**2

def cross_product(o, a, b):
    """
    Returns the cross product of vectors OA and OB.
    A positive value indicates a counter-clockwise turn (Left).
    A negative value indicates a clockwise turn (Right).
    Zero indicates collinear points.
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

# ---------------------------------------------------------
# 2. Visualization Function (Required by Project) [cite: 42]
# ---------------------------------------------------------

def update_plot(all_points, stack, current_point=None, title="Graham Scan"):
    plt.clf()  # Clear current figure
    
    # Unzip points for plotting
    xs, ys = zip(*all_points)
    plt.scatter(xs, ys, color='blue', s=10, label='Input Points')

    # Plot the hull in progress (Stack)
    if len(stack) > 1:
        hx, hy = zip(*stack)
        plt.plot(hx, hy, color='green', linewidth=2, marker='o', label='Current Hull')
        # Connect last point in stack back to current point being checked
        if current_point:
            plt.plot([stack[-1][0], current_point[0]], [stack[-1][1], current_point[1]], 
                     color='red', linestyle='--', label='Checking...')

    plt.title(title)
    plt.legend(loc='upper right')
    plt.draw()
    plt.pause(0.1)  # Pause to create animation effect

# ---------------------------------------------------------
# 3. Graham Scan Algorithm
# ---------------------------------------------------------

def graham_scan(points, visualize=True):
    n = len(points)
    if n < 3:
        return points

    # Step 1: Find the bottom-most point (and left-most if ties) 
    # We swap it to index 0
    min_idx = 0
    for i in range(1, n):
        if points[i][1] < points[min_idx][1] or \
           (points[i][1] == points[min_idx][1] and points[i][0] < points[min_idx][0]):
            min_idx = i
    
    points[0], points[min_idx] = points[min_idx], points[0]
    p0 = points[0]

    # Step 2: Sort remaining points by polar angle with respect to p0
    # If angles are same, keep the furthest point
    sorted_points = sorted(points[1:], key=lambda p: (polar_angle(p0, p), distance_sq(p0, p)))
    
    # Create the sorted array including p0
    points = [p0] + sorted_points

    # Step 3: Iterate through points and build the stack
    stack = [points[0], points[1], points[2]]

    if visualize:
        plt.ion()  # Turn on interactive mode for animation
        plt.figure(figsize=(10, 8))

    for i in range(3, n):
        # Top of stack is stack[-1], next-to-top is stack[-2]
        
        while len(stack) > 1 and cross_product(stack[-2], stack[-1], points[i]) <= 0:
            # If we turn right (or go straight), pop the stack (backtracking)
            popped = stack.pop()
            if visualize:
                update_plot(points, stack, points[i], title=f"Backtracking: Removing {popped}")
        
        stack.append(points[i])
        
        if visualize:
            update_plot(points, stack, points[i], title=f"Adding Point: {points[i]}")

    # Complete the loop visually
    if visualize:
        # Close the hull visually by connecting last to first
        update_plot(points, stack + [stack[0]], title="Final Convex Hull")
        plt.ioff() # Turn off interactive mode
        plt.show()

    return stack

# ---------------------------------------------------------
# 4. Data Loading (Parsing format from Screenshot)
# ---------------------------------------------------------

def load_data_from_string(data_string):
    """
    Parses the format: (x, y), (x, y), ...
    Removes parentheses and splits by comma.
    """
    # Clean up the string: remove parens and newlines
    cleaned = data_string.replace('(', '').replace(')', '').replace('\n', '')
    values = [float(x) for x in cleaned.split(',')]
    
    # Pair them up into tuples (x, y)
    points = []
    for i in range(0, len(values), 2):
        if i+1 < len(values):
            points.append((values[i], values[i+1]))
    return points

# ---------------------------------------------------------
# 5. Main Execution
# ---------------------------------------------------------

if __name__ == "__main__":
    # COPY THE CONTENT OF datapoints1.txt HERE
    # I have transcribed the first few lines from your image to demonstrate.
    # YOU MUST REPLACE THIS STRING WITH THE FULL CONTENT OF YOUR FILE.
    
    raw_data = """
    (120.6, 873.2), (487.5, 965.4), (936.3, 286.7), (824.1, 755.5), (642.9, 213.8),
    (951.7, 848.9), (211.2, 963.5), (563.7, 378.9), (295.4, 183.7), (704.8, 935.3),
    (345.9, 403.2), (951.8, 734.5), (839.6, 138.7), (447.3, 646.2), (732.1, 593.4),
    (117.9, 759.3), (839.2, 528.1), (321.3, 865.5), (769.6, 190.3), (123.5, 647.1),
    (671.9, 932.6), (214.8, 252.1), (358.6, 913.2), (985.5, 485.6), (154.7, 321.9),
    (684.1, 662.3), (419.8, 135.5), (955.6, 145.3), (818.7, 472.9), (284.4, 904.6),
    (798.4, 380.7), (110.2, 553.3), (250.9, 496.1), (352.3, 845.8), (646.7, 892.4),
    (930.2, 111.9), (476.2, 322.5), (599.8, 198.2), (145.4, 410.8), (927.3, 779.1),
    (892.8, 982.4), (153.2, 824.8), (615.9, 569.2), (518.4, 705.9), (376.3, 235.7),
    (165.7, 111.2), (442.8, 911.6), (997.1, 342.4), (288.2, 556.3), (710.9, 793.1),
    (607.6, 988.2), (752.4, 322.8), (873.2, 939.5), (661.7, 268.6), (923.8, 676.4),
    (865.7, 843.9), (139.9, 495.2), (563.5, 845.6), (770.2, 615.7), (183.4, 173.2),
    (944.5, 516.9), (723.1, 929.4), (168.2, 298.3), (831.4, 703.7), (513.6, 623.1),
    (900.8, 389.2), (606.9, 884.7), (754.2, 448.8), (372.6, 967.3), (679.8, 431.9),
    (327.1, 698.2), (196.3, 604.7), (571.1, 777.5), (840.2, 304.4), (112.8, 933.8),
    (257.9, 377.4), (693.4, 562.8), (472.3, 958.9), (312.7, 136.4), (920.3, 566.5),
    (649.9, 319.8), (380.1, 826.5), (918.7, 826.7), (222.8, 743.1), (789.9, 496.2),
    (476.1, 201.9), (930.7, 382.4), (342.7, 743.8), (745.2, 995.4), (193.2, 968.3),
    (587.3, 240.5), (287.1, 663.5), (903.8, 171.2), (174.8, 882.4), (669.1, 583.6),
    (558.2, 286.4), (849.9, 216.7), (494.7, 824.1), (651.2, 415.3), (391.4, 341.5)
    """ 
    # Note: Add the rest of the points from your datapoints1.txt file above
    
    try:
        points = load_data_from_string(raw_data)
        print(f"Loaded {len(points)} points.")
        
        hull = graham_scan(points, visualize=True)
        
        print("-" * 30)
        print("Convex Hull Points:")
        for p in hull:
            print(p)
            
    except Exception as e:
        print(f"Error parsing data: {e}")
