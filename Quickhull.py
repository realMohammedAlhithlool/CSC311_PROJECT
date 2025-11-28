import matplotlib.pyplot as plt

# -------------------------------------------------
#  QuickHull (Divide & Conquer Convex Hull)
# -------------------------------------------------

cloud = [(120.6, 873.2), (487.5, 965.4), (936.3, 286.7), (824.1, 755.5), (642.9, 213.8),
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
 (558.2, 286.4), (849.9, 216.7), (494.7, 824.1), (651.2, 415.3), (391.4, 341.5)]

# ------------------------------------------
# Helper Functions
# ------------------------------------------
 

def quickhull_divide_conquer_steps(points):
    """
This Algorithm finds the convex hull by picking extreme points, splitting the set, and recursively selecting the farthest points from each boundary segment until the outer boundary is formed.

Time complexity (worst case):
  -O(n^2) 
Space efficiency:
  -O(n) for storing points on the hull and the recursive stack.

    """
    fig, ax = plt.subplots(figsize=(10,10))
    xs, ys = zip(*points)
    ax.scatter(xs, ys, label="Points")
    ax.set_title("QuickHull Visualization steps")

    hull_points = []

    def point_line_distance(A, B, C):
        return abs((B[0]-A[0])*(A[1]-C[1]) - (A[0]-C[0])*(B[1]-A[1]))

    def is_left(A, B, C):
        return ((B[0]-A[0])*(C[1]-A[1]) - (B[1]-A[1])*(C[0]-A[0])) > 0

    def recursive_hull(points, A, B, depth=0):
        left_points = [p for p in points if is_left(A, B, p)]

        # Highlight current line
        ax.plot([A[0], B[0]], [A[1], B[1]], 'y--', alpha=0.5)
        plt.pause(1)

        if not left_points:
            hull_points.append(B)
            ax.plot([A[0], B[0]], [A[1], B[1]], 'r-', linewidth=2)
            plt.pause(1)
            return

        # Find farthest point
        Pmax = max(left_points, key=lambda p: point_line_distance(A, B, p))
        ax.scatter(*Pmax, color='red', s=80)  # highlight farthest point

        # Draw lines to Pmax
        ax.plot([A[0], Pmax[0]], [A[1], Pmax[1]], 'g--', linewidth=1)
        ax.plot([Pmax[0], B[0]], [Pmax[1], B[1]], 'g--', linewidth=1)
        plt.pause(1)

        # Recursive calls
        recursive_hull(left_points, A, Pmax, depth+1)
        recursive_hull(left_points, Pmax, B, depth+1)

    P1 = min(points)
    P2 = max(points)
    hull_points.append(P1)

    # Upper set
    recursive_hull(points, P1, P2)
    # Lower set
    recursive_hull(points, P2, P1)


    hx, hy = zip(*hull_points)
    ax.plot(hx, hy, 'b-', linewidth=2, label="Convex Hull")
    ax.legend()
    plt.show()

# Run the step-by-step visualization
quickhull_divide_conquer_steps(cloud)