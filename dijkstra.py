# Copyright (c) 2017 Lim Ming Yean. Modified.

from math import inf
import time

def dijkstra(grid, src, dest):
    start_taking_nodes = time.time()
    Q = grid.get_nodes()
    end_taking_nodes = time.time()
    dist = {node : inf for node in Q}
    prev = {node : None for node in Q}
    visitable_nodes = []

    x = dest[0]
    y = dest[1]
    dist[src] = 0
    visitable_nodes.append(src)

    counter = 0
    while len(visitable_nodes) != 0:
        current_min = (0, 0)
        current_min_distance = inf
        for visitable_node in visitable_nodes:
            if dist[visitable_node] < current_min_distance:
                current_min_distance = dist[visitable_node]
                current_min = visitable_node

        visitable_nodes.remove(current_min)

        if current_min[0] == x:
            if current_min[1] == y:
                break

        counter += 1
        for v in grid.get_adjacent(current_min):
            alt = dist[current_min] + 1
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = current_min
                visitable_nodes.append(v)

    path = [dest]
    cur = dest

    while prev[cur]:
        path.append(prev[cur])
        cur = prev[cur]

    return list(reversed(path))
