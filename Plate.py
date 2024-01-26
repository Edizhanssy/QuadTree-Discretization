import matplotlib.pyplot as plt
from matplotlib import gridspec
from QuadtreewPIT import Point, Vertex, Rectangle, Quadtree
from circle import circle
from drawBoundary import drawBoundary

width, height = 30, 20
circle_radius = 10  # Define the radius of the circle
circle_center = Point(width/2, height/2)  # Center of the circle
depth = 0
SpaceTreeDepth = 10
# Initialize the circle domain
circle_domain = circle(circle_radius, circle_center)

points = circle_domain.generate_circle_points(circle_center, circle_radius)

Vertex1 = Vertex(Point(0, 0))
Vertex2 = Vertex(Point(width, 0))
Vertex3 = Vertex(Point(width, height))
Vertex4 = Vertex(Point(0, height))

# Initialize the Quadtree domain
domain = Rectangle(Vertex1, Vertex2, Vertex3, Vertex4)
qtree = Quadtree(domain, depth, SpaceTreeDepth)

for point in points:
    qtree.insert(point)

quadtrees = qtree.collect_quadtrees()

# Optional: Visualize the result
fig = plt.figure(figsize=(20, 12))
gs = gridspec.GridSpec(1, 1)
ax = fig.add_subplot(gs[0])
depth_colors = [
    '#00BFFF',  # Deep Sky Blue
    '#1E90FF',  # Dodger Blue
    '#6495ED',  # Cornflower Blue
    '#7B68EE',  # Medium Slate Blue
    '#8A2BE2',  # Blue Violet
    '#9932CC',  # Dark Orchid
    '#C71585',  # Medium Violet Red
    '#DB7093',  # Pale Violet Red
    '#F08080',  # Light Coral
    '#FF8C00',  # Dark Orange
    '#FF4500',  # Orange Red
    '#FF0000',  # Red
]

for quad in quadtrees:
    quad.drawBoundary(ax, depth_colors)
plt.show()
