import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from quadtree import Point, Rectangle, QuadTree

DPI = 72

width, height = 600, 400

N = 1000
xs = np.random.rand(N) * width
ys = np.random.rand(N) * height
points = [Point(xs[i], ys[i]) for i in range(N)]

domain = Rectangle(Point(width/2, height/2), width/2, height/2)
qtree = QuadTree(domain)

for point in points:
    qtree.insert(point)

print('Total points: ', len(qtree))

# draw rectangles
fig = plt.figure(figsize=(700/DPI, 500/DPI), dpi=DPI)
ax = plt.subplot()
ax.set_xlim(0, width)
ax.set_ylim(0, height)
qtree.draw(ax)

# draw points
ax.scatter([p.x for p in points], [p.y for p in points], s=4)
ax.set_xticks([])
ax.set_yticks([])

# generate the range
#center_x = np.random.rand() * width
#center_y = np.random.rand() * height
center_x = 300
center_y = 200

range_width = np.random.rand() * min(center_x, width - center_x)
range_height = np.random.rand() * min(center_y, height - center_y)

found_points = []
#range = Rectangle(Point(center_x, center_y), range_width, range_height)
#found_points = qtree.queryRange(range)
#radius = min(range_width, range_height)
radius = 150
range = Rectangle(Point(center_x, center_y), radius, radius)
found_points = qtree.queryRadius(range, Point(center_x, center_y))

print('points in range:', len(found_points))

ax.scatter([p.x for p in found_points], [p.y for p in found_points],
            facecolors='none', edgecolors='r', s=32)

range.draw(ax, c='r', lw=2)

ax.invert_yaxis()
plt.tight_layout()
plt.savefig('search-quadtree.png', DPI=72)
plt.show()
