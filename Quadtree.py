# Recursive partitioning Quadtree Implementation
# Quadtrees are used to store geometric data with partitioning

# while thinking about Quadtrees the constructive approach the certain things has to be considered:

#   1- Point (1-D)
#   2- Vertex (1-D)
#   3- Rectangle (2-D)

# ** Note: Which means that the points creates vertices, the vertices create rectangles,
#       the rectangles with certain paritioning process creates Quadtrees, and this goes !

# the procedure will be as follows:
# 1- Defining Point
# 2- Defining the vertices and Rectangle
# 3- Define the center of the corresponding rectangle
# 4- Recursive Partitioning Process

import numpy as np

# STEP 1 - Define Point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# STEP 2 - Define Vertex
class Vertex:
    def __init__(self, points):
        self.points = points

# STEP 3 - Define Rectangle
class Rectangle:
    def __init__(self, v1, v2, v3, v4):
        self.center = Point((v1.points.x + v3.points.x) / 2, (v1.points.y + v3.points.y) / 2)
        self.width = np.sqrt((v2.points.x - v1.points.x) ** 2 + (v2.points.y - v1.points.y) ** 2)
        self.height = np.sqrt((v4.points.x - v1.points.x) ** 2 + (v4.points.y - v1.points.y) ** 2)
        # Update boundaries
        x_coords = [v.points.x for v in [v1, v2, v3, v4]]
        y_coords = [v.points.y for v in [v1, v2, v3, v4]]
        self.west = min(x_coords)
        self.east = max(x_coords)
        self.south = max(y_coords)
        self.north = min(y_coords)

    def containsPoint(self, point):
        return self.west <= point.x < self.east and self.north <= point.y < self.south

    def Intersected(self, circle):
        # Find the closest x coordinate from circle's center to rectangle
        x_closest = max(self.west, min(circle.center.x, self.east))
        # Find the closest y coordinate from circle's center to rectangle
        y_closest = max(self.north, min(circle.center.y, self.south))

        # Calculate the distance from the closest point to the circle's center
        distance_x = x_closest - circle.center.x
        distance_y = y_closest - circle.center.y
        distance = np.sqrt(distance_x**2 + distance_y**2)

        # Check if the distance is less than or equal to the circle's radius
        return distance <= circle.radius

    def draw(self, ax, fill_color, c='k', lw=1, zorder=1, alpha=1, **kwargs):
        x1, y1 = self.west, self.north
        x2, y2 = self.east, self.south
        if fill_color:
            ax.fill([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], color=fill_color, alpha=alpha, zorder=zorder, **kwargs)
            ax.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], c=c, lw=lw, zorder=zorder, **kwargs)
        else:
            ax.plot([x1, x2, x2, x1, x1], [y1, y1, y2, y2, y1], c=c, lw=lw, zorder=zorder, **kwargs)


# STEP 4 - Defining Quadtree
class Quadtree:
    def __init__(self, boundary, depth, max_depth):
        self.boundary = boundary
        self.points = []
        self.divided = False
        self.depth = depth
        self.max_depth = max_depth

    def insert(self, point):
        # If the point is not in the range of the current quadtree, return False
        if not self.boundary.containsPoint(point):
            return False

        # If the current depth is less than the maximum depth, insert the point and subdivide if necessary
        if self.depth < self.max_depth:
            if not self.divided:
                self.divide()

            # Insert the point into the appropriate quadrant
            if self.nw.insert(point):
                return True
            elif self.ne.insert(point):
                return True
            elif self.sw.insert(point):
                return True
            elif self.se.insert(point):
                return True

        # If the current depth is the maximum depth, add the point to the current node
        else:
            self.points.append(point)
            return True

        return False

    def RecursivelyQuery(self, query_range):
        found_points = []

        # Check if the current node's boundary intersects with the query range
        if not self.boundary.intersects(query_range):
            return found_points

        # Add all points in the current node that are within the query range
        for point in self.points:
            if query_range.containsPoint(point):
                found_points.append(point)

        # If the current node is divided, recursively query each child
        if self.divided:
            found_points.extend(self.nw.RecursivelyQuery(query_range))
            found_points.extend(self.ne.RecursivelyQuery(query_range))
            found_points.extend(self.sw.RecursivelyQuery(query_range))
            found_points.extend(self.se.RecursivelyQuery(query_range))

        return found_points

    def divide(self):
        #print(f"Dividing at depth {self.depth}: {self.boundary}")
        if self.depth >= self.max_depth:
            return  # Stop further subdivision

        center_x = self.boundary.center.x
        center_y = self.boundary.center.y
        new_width = self.boundary.width / 2
        new_height = self.boundary.height / 2

        # NW Quadrant
        nw_v1 = Vertex(Point(center_x - new_width, center_y - new_height))
        nw_v2 = Vertex(Point(center_x, center_y - new_height))
        nw_v3 = Vertex(Point(center_x, center_y))
        nw_v4 = Vertex(Point(center_x - new_width, center_y))
        nw = Rectangle(nw_v1, nw_v2, nw_v3, nw_v4)
        self.nw = Quadtree(nw, depth=self.depth + 1, max_depth=self.max_depth)

        # NE Quadrant
        ne_v1 = Vertex(Point(center_x, center_y - new_height))
        ne_v2 = Vertex(Point(center_x + new_width, center_y - new_height))
        ne_v3 = Vertex(Point(center_x + new_width, center_y))
        ne_v4 = Vertex(Point(center_x, center_y))
        ne = Rectangle(ne_v1, ne_v2, ne_v3, ne_v4)
        self.ne = Quadtree(ne, depth=self.depth + 1, max_depth=self.max_depth)

        # SW Quadrant
        sw_v1 = Vertex(Point(center_x - new_width, center_y))
        sw_v2 = Vertex(Point(center_x, center_y))
        sw_v3 = Vertex(Point(center_x, center_y + new_height))
        sw_v4 = Vertex(Point(center_x - new_width, center_y + new_height))
        sw = Rectangle(sw_v1, sw_v2, sw_v3, sw_v4)
        self.sw = Quadtree(sw, depth=self.depth + 1, max_depth=self.max_depth)

        # SE Quadrant
        se_v1 = Vertex(Point(center_x, center_y))
        se_v2 = Vertex(Point(center_x + new_width, center_y))
        se_v3 = Vertex(Point(center_x + new_width, center_y + new_height))
        se_v4 = Vertex(Point(center_x, center_y + new_height))
        se = Rectangle(se_v1, se_v2, se_v3, se_v4)
        self.se = Quadtree(se, depth=self.depth + 1, max_depth=self.max_depth)

        self.divided = True

    def __len__(self):
        count = len(self.points)
        if self.divided:
            count += len(self.nw) + len(self.ne) + len(self.sw) + len(self.se)

        return count

    def draw(self, ax):
        self.boundary.draw(ax)
        if self.divided:
            self.nw.draw(ax)
            self.ne.draw(ax)
            self.sw.draw(ax)
            self.se.draw(ax)

    def drawBoundary(self, ax, depth_colors):
        color = depth_colors[min(self.depth-2, len(depth_colors) - 1)]
        # Use depth to scale alpha and zorder
        alpha = 0.3 + (self.depth / self.max_depth) * 0.7
        zorder = self.depth
        self.boundary.draw(ax, fill_color=color, zorder=zorder, alpha=alpha)

    def collect_quadtrees(self):
        quadtrees = [self]  # Start with the current Quadtree object
        if self.divided:
            quadtrees.extend(self.nw.collect_quadtrees())
            quadtrees.extend(self.ne.collect_quadtrees())
            quadtrees.extend(self.sw.collect_quadtrees())
            quadtrees.extend(self.se.collect_quadtrees())
        return quadtrees

