# Code based on the following StackOverflow answer:
# https://stackoverflow.com/questions/56792519/crop-line-inside-range

EPSILON = 1e-6
INSIDE = 1
OUTSIDE = 0

def intersection(
        segment1_x1, 
        segment1_y1, 
        segment1_x2, 
        segment1_y2, 
        segment2_x1, 
        segment2_y1, 
        segment2_x2, 
        segment2_y2):
    
    """
    Calculate the intersection point of two line segments and return the result.
    """

    # Rewrite the line segments as parametric equations using t as parameter
    # point_on_segment  = point + t * vector
    # point_on_segment1 = p1 + t * v1

    p1_x = segment1_x1
    p1_y = segment1_y1
    v1_x = segment1_x2 - segment1_x1
    v1_y = segment1_y2 - segment1_y1

    p2_x = segment2_x1
    p2_y = segment2_y1
    v2_x = segment2_x2 - segment2_x1
    v2_y = segment2_y2 - segment2_y1

    # Check if the lines are parallel
    if v1_x * v2_y - v1_y * v2_x == 0:
        return None

    # Calculate the intersection point
    t1 = (v2_x * (p1_y - p2_y) - v2_y * (p1_x - p2_x)) / (v1_x * v2_y - v1_y * v2_x)
    t2 = (v1_x * (p1_y - p2_y) - v1_y * (p1_x - p2_x)) / (v1_x * v2_y - v1_y * v2_x)

    # Check if the intersection point is within the line segments
    if 0 <= t1 <= 1 and 0 <= t2 <= 1:
        x = p1_x + t1 * v1_x
        y = p1_y + t1 * v1_y
        return x, y
    
    # Return None if the intersection point is outside the line segments
    return None


def clip(line_p1, line_p2, box):
    
    # First, check if the line is completely outside the box
    out_left   = line_p1[0] < box[0] and line_p2[0] < box[0]
    out_right  = line_p1[0] > box[2] and line_p2[0] > box[2]
    out_top    = line_p1[1] < box[1] and line_p2[1] < box[1]
    out_bottom = line_p1[1] > box[3] and line_p2[1] > box[3]
    
    if out_left or out_right or out_top or out_bottom:
        return None, None
    
    # Second, check if the line is completely inside the box
    in_left   = line_p1[0] >= box[0] and line_p2[0] >= box[0]
    in_right  = line_p1[0] <= box[2] and line_p2[0] <= box[2]
    in_top    = line_p1[1] >= box[1] and line_p2[1] >= box[1]
    in_bottom = line_p1[1] <= box[3] and line_p2[1] <= box[3]

    if in_left and in_right and in_top and in_bottom:
        return line_p1, line_p2
    
    # Third, check if the line is partially inside the box
    intersection_points = []
    
    # Check the intersection with the left side of the box
    intersection_point = intersection(
        line_p1[0], line_p1[1], line_p2[0], line_p2[1], 
        box[0], box[1], box[0], box[3])
    
    if intersection_point is not None:
        intersection_points.append(intersection_point)

    # Check the intersection with the right side of the box
    intersection_point = intersection(
        line_p1[0], line_p1[1], line_p2[0], line_p2[1], 
        box[2], box[1], box[2], box[3])
    
    if intersection_point is not None:
        intersection_points.append(intersection_point)

    # Check the intersection with the top side of the box
    intersection_point = intersection(
        line_p1[0], line_p1[1], line_p2[0], line_p2[1], 
        box[0], box[1], box[2], box[1])
    
    if intersection_point is not None:
        intersection_points.append(intersection_point)

    # Check the intersection with the bottom side of the box
    intersection_point = intersection(
        line_p1[0], line_p1[1], line_p2[0], line_p2[1], 
        box[0], box[3], box[2], box[3])
    
    if intersection_point is not None:
        intersection_points.append(intersection_point)

    # Substitute the line points that fall outside the box
    # If two intersctions were found, both line points fall outside the box, substitute both
    if len(intersection_points) == 2:
        return intersection_points[0], intersection_points[1]
    
    # If only one falls outside the box, substitute that one
    if len(intersection_points) == 1:
        if line_p1[0] < box[0] or line_p1[0] > box[2] or line_p1[1] < box[1] or line_p1[1] > box[3]:
            return intersection_points[0], line_p2
        elif line_p2[0] < box[0] or line_p2[0] > box[2] or line_p2[1] < box[1] or line_p2[1] > box[3]:
            return line_p1, intersection_points[0]
    
    return None, None



#     """
#     Clips a line segment to a bounding box.

#     Args:
#         point_1 (list): Starting point [x, y].
#         point_2 (list): Ending point [x, y].
#         box (list): Bounding box [xmin, ymin, xmax, ymax].

#     Returns:
#         point_1 (list): Result starting point [x, y].
#         point_2 (list): Result ending point [x, y].
#     """
    
#     x1, y1 = point_1
#     x2, y2 = point_2
#     dx = x2 - x1
#     dy = y2 - y1

#     c = [0, 1]  # Clipping parameters
#     # if (
#     #     clipT(box[0] - x1, dx, c)
#     #     and clipT(x1 - box[2], -dx, c)
#     #     and clipT(box[1] - y1, dy, c)
#     #     and clipT(y1 - box[3], -dy, c)
#     # ):
#     tE, tL = c
#     if tL < 1:
#         point_2[0] = x1 + tL * dx
#         point_2[1] = y1 + tL * dy
#     if tE > 0:
#         point_1[0] += tE * dx
#         point_1[1] += tE * dy
    
#     return point_1, point_2

# Define input variables
x0, y0, x1, y1 = 0, 0, 640, 480
xa, ya, xb, yb = 20, -40, 680, 460

point_1 = [xa, ya]
point_2 = [xb, yb]
box = [x0, y0, x1, y1]

# Perform clipping
print("before ", point_1, point_2)
point_1, point_2 = clip(point_1, point_2, box)

# Extract results
print("after ", point_1, point_2)
