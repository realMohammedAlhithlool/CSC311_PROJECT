import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import numpy as np
import itertools


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
x, y = zip(*cloud)
hull_segments = []

# Plot raw points
padding = 150
plt.xlim(min(x)-padding, max(x)+padding)
plt.ylim(min(y)-padding, max(y)+padding)
scatter = plt.scatter([i[0] for i in cloud], [i[1] for i in cloud])

# Helper functions
def draw_line(p1, p2, pause=0.001):
    plt.pause(pause)
    line = plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r-', marker='o')[0]
    plt.pause(0.001)
    plt.draw()
    return line

def hide_line(line, pause=0.001):
    plt.pause(pause)
    line.set_visible(False)
    plt.draw()

# --- FIX: ROBUST COLOR INITIALIZATION BLOCK ---

# 1.3 Get the total number of points (N)
N = len(cloud)

# 1.4 Get and store the original RGBA array for easy reverting
original_rgba = scatter.get_facecolors()

# Check if Matplotlib returned a single color (1, 4) and expand it to (N, 4)
# This fixes the bug where modifying index 0 changes all points.
if original_rgba.shape[0] == 1:
    # If Matplotlib returns a single color, use np.tile to repeat it for all N points
    ORIGINAL_COLORS = np.tile(original_rgba, (N, 1))
else:
    # Otherwise, use the colors as returned (should be N, 4)
    ORIGINAL_COLORS = original_rgba.copy()

# 1.5 Introduce a state variable to hold the CURRENT dynamic colors (The Fix)
CURRENT_COLORS = ORIGINAL_COLORS.copy()
# print(f"Initialized {N} points for coloring. Color array shape: {CURRENT_COLORS.shape}") # Debugging line

# --- END FIX ---


# --- 2. Color Changer Function ---
def change_point_color(index: int, pause=0.001, new_color: str = 'red', scatter_plot_object=scatter):
    plt.pause(pause)
    """
    Changes the face color of a single point in a Matplotlib scatter plot
    by modifying the external CURRENT_COLORS state array.

    Args:
        index (int): The zero-based index of the point to change.
        new_color (str): The color name (e.g., 'red', 'green', '#FF0000').
        scatter_plot_object (PathCollection): The object returned by plt.scatter().
    """
    global CURRENT_COLORS # Declare access to the global state variable

    # 2.1 Convert the new color name/hex string to a Matplotlib RGBA tuple
    try:
        rgba_color = mcolors.to_rgba(new_color)
    except ValueError:
        print(f"Error: Invalid color name/format '{new_color}'.")
        return

    # 2.2 Check if the index is valid
    # This check is now robust because CURRENT_COLORS has N rows.
    if index < 0 or index >= len(CURRENT_COLORS):
        print(f"Error: Index {index} is out of bounds (0 to {len(CURRENT_COLORS) - 1}).")
        return

    # 2.3 Update the global state array at the specified index
    CURRENT_COLORS[index] = rgba_color

    # 2.4 Apply the entire modified array back to the scatter plot
    scatter_plot_object.set_facecolors(CURRENT_COLORS)

    # 2.5 Refresh the figure to show the change
    plt.draw()
    #print(f"Color of point at index {index} successfully changed to {new_color}.")


# --- 3. The Revert Functions ---

def revert_point_color(index: int, pause=0.001, scatter_plot_object=scatter):
    plt.pause(pause)
    """
    Reverts the color of a single point to its initial color (stored in ORIGINAL_COLORS).

    Args:
        index (int): The zero-based index of the point to revert.
        scatter_plot_object (PathCollection): The object returned by plt.scatter().
    """
    global CURRENT_COLORS # Declare access to the global state variable

    # 3.1 Check if the index is valid
    if index < 0 or index >= len(CURRENT_COLORS):
        print(f"Error: Index {index} is out of bounds (0 to {len(CURRENT_COLORS) - 1}).")
        return

    # 3.2 Get the original RGBA color for this specific index
    original_rgba_color = ORIGINAL_COLORS[index]

    # 3.3 Update the global state array at the specified index
    CURRENT_COLORS[index] = original_rgba_color

    # 3.4 Apply the entire modified array back to the scatter plot
    scatter_plot_object.set_facecolors(CURRENT_COLORS)

    plt.draw()
    #print(f"Color of point at index {index} successfully reverted to original.")


def revert_colors(scatter_plot_object=scatter):
    """
    Reverts all point colors in the scatter plot to the original saved colors.

    Args:
        scatter_plot_object (PathCollection): The object returned by plt.scatter().
    """
    global CURRENT_COLORS
    # Use the globally stored ORIGINAL_COLORS array to reset the current state
    CURRENT_COLORS = ORIGINAL_COLORS.copy()
    scatter_plot_object.set_facecolors(CURRENT_COLORS)
    plt.draw()
    #print("All point colors reverted to original.")

#Math Sign function
def sign(n):
    return (n > 0) - (n < 0)

#Brute Force
def BF():
    """
    This Alogrithm tries every line segment possible within the entire point cloud, then point by point, checks if every point is on the same side of the segment, thus making it part of the hull, if a point is found to be on a different side than its predecessors then the segment is rejected.
    Abstract Data Types(ADTs):
        - Python's Iterator object in enumerate()
        - Itertools's combinations()
    Time complexity (worst case):
        - O(n) tests for O(n C 2) segments = O(n) tests for O(n^2) segments = O(n^3)
    Space efficiency:
        - O(1): `itertools.combinations` and `enumerate` are implemented in a generative way, so they don't store considerable auxiliary data
    """
    for i, (p1, p2) in enumerate(itertools.combinations(cloud, 2)):#for every line segment
        line = draw_line(p1, p2)
        is_hull = True
        side = None
        #print(i)

        last_index = -1
        for index, p in enumerate(cloud):
            if p is p1 or p is p2: continue#skip segment points
            last_index = index

            #calculate side of point to line
            direction = (p[0] - p1[0])*(p2[1]-p1[1]) - (p[1] - p1[1])*(p2[0]-p1[0])
            #converge to one of two sides or colinear
            direction = sign(direction)

            change_point_color(index, new_color= 'green' if direction==+1 else 'yellow')
            if direction != 0:#Not colinear
                if side is None:#if first point
                    side = direction
                elif side is not direction:#if different side than others before
                    is_hull = False
                    break#stop trying this line
        
        #for p in range(last_index+1): revert_point_color(p)#smooth recolouring
        revert_colors()

        if is_hull:
            hull_segments.append((p1, p2))
        else:
            hide_line(line)




#Quickhull

#Graham Scan




#TODO: Add running times
###
BF()
print(hull_segments)
#Segments: [((951.7, 848.9), (985.5, 485.6)), ((951.7, 848.9), (892.8, 982.4)), ((985.5, 485.6), (997.1, 342.4)), ((955.6, 145.3), (930.2, 111.9)), ((955.6, 145.3), (997.1, 342.4)), ((110.2, 553.3), (165.7, 111.2)), ((110.2, 553.3), (112.8, 933.8)), ((930.2, 111.9), (165.7, 111.2)), ((892.8, 982.4), (745.2, 995.4)), ((112.8, 933.8), (193.2, 968.3)), ((745.2, 995.4), (193.2, 968.3))]


plt.show()#run on plot window