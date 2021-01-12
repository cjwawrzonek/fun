from waypoint import Waypoint
from collections import deque
from heapq import *

vector = {
    0: (0, 1),
    1: (1, 0),
    2: (0, -1),
    3: (-1, 0),
}


class PathFinder(object):
    def is_valid(self, wp, grid):
        return 0 <= wp.x < grid.shape[0] and 0 <= wp.y < grid.shape[1] and not grid[wp.x, wp.y]

    def children(self, wp):
        children = []
        # Forward
        forward = vector[wp.orientation]
        new_wp = Waypoint(wp.x + forward[0], wp.y + forward[1], wp.orientation)
        children.append(new_wp)

        # Forward Right
        right = vector[(wp.orientation + 1) % 4]
        new_wp = Waypoint(
            wp.x + forward[0] + right[0], wp.y + forward[1] + right[1], (wp.orientation + 1) % 4)
        children.append(new_wp)

        # Forward Left
        left = vector[(wp.orientation - 1) % 4]
        new_wp = Waypoint(
            wp.x + forward[0] + left[0], wp.y + forward[1] + left[1], (wp.orientation - 1) % 4)
        children.append(new_wp)

        # Backwards
        left = vector[(wp.orientation - 1) % 4]
        new_wp = Waypoint(wp.x - forward[0], wp.y - forward[1], wp.orientation)
        children.append(new_wp)

        # Backwards Right
        new_wp = Waypoint(
            wp.x - forward[0] - left[0], wp.y - forward[1] - left[1], (wp.orientation - 1) % 4)
        children.append(new_wp)

        # Backwards Left
        new_wp = Waypoint(
            wp.x - forward[0] - right[0], wp.y - forward[1] - right[1], (wp.orientation + 1) % 4)
        children.append(new_wp)

        return children

    def get_path(self, grid, start_wp, end_wp):
        pq = [(0, start_wp, [start_wp])]
        visited = set()
        while pq:
            _, wp, path = heappop(pq)
            for child in self.children(wp):
                if child in visited or not self.is_valid(child, grid):
                    continue
                if child == end_wp:
                    return path + [child]
                visited.add(child)
                h = (abs(end_wp.x - wp.x) + abs(end_wp.y - wp.y)) + \
                    len(path)
                heappush(pq, (h, child, path + [child]))
