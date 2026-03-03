
import marshal, sys

def process_all_reachable(start, seen):
    for c2 in find_neighbours(start):
        if c2 in seen:
            continue

        seen.add(c2)
        process_all_reachable(c2, seen)

def find_components(cultures):
    components = 0
    seen = set()
    for c1 in cultures:
        if c1 in seen:
            continue

        components += 1
        seen.add(c1)
        process_all_reachable(c1, seen)
    return components

def distance(c1, c2, pre_distance = 0, seen = None):
    seen = (seen or []).copy()
    distances = []
    for c1n in find_neighbours(c1):
        if c2 == c1n:
            return pre_distance + 1

        if c1n in seen:
            continue

        seen.append(c1n)
        dist = distance(c1n, c2, pre_distance + 1, seen)
        if dist:
            distances.append(dist)

    if distances:
        return min(distances)
    return None

def distance(c1, c2):
    'Dijkstras algorithm'
    distances = {c1 : 0}
    unvisited = set(cultures)

    current = c1
    while current and (c2 not in distances):
        distance = distances.get(current, 10000) + 1
        for c1n in find_neighbours(current):
            if c1n in unvisited:
                if distances.get(c1n, 10000) > distance:
                    # print('%s -> %s : %s' % (c1, c1n, distance))
                    distances[c1n] = distance

        unvisited.remove(current)

        smallest = 10000
        next = None
        for n in unvisited:
            if distances.get(n, 10000) < smallest:
                next = n
                smallest = distances.get(n, 10000)

        current = next
        # print('current:', next)

    # print(c2, distances[c2], distances)
    return distances.get(c2)

def find_distance(c1, c2, distance, min_distances, unvisited):
    distance += 1

    smallest = 100000
    next = None
    for n in unvisited:
        if min_distances.get(n, 1000000) < smallest:
            smallest = min_distances[n]
            next = n

    if n:
        find_distance(n, c2, distance, min_distances, unvisited)

def find_diameter(cultures):
    largest = 0
    for (ix, c1) in enumerate(cultures):
        for c2 in cultures[ix + 1 : ]:
            largest = max(distance(c1, c2) or 0, largest)
    return largest

def clique_number(cultures):
    largest = 0
    seen = set()
    for c1 in cultures:
        if c1 in seen:
            continue

        prev_seen = len(seen)
        seen.add(c1)
        process_all_reachable(c1, seen)
        largest = max(largest, len(seen) - prev_seen)

    return largest

(cultures, edges) = marshal.load(open(sys.argv[1], 'rb'))

neighbours = {}
for (c1, c2, weight) in edges:
    if c1 not in neighbours:
        neighbours[c1] = []
    if c2 not in neighbours:
        neighbours[c2] = []
    neighbours[c1].append(c2)
    neighbours[c2].append(c1)

def find_neighbours(node):
    return neighbours.get(node, [])

components = find_components(cultures)

print('Nodes:', len(cultures))
print('Edges:', len(edges))
print('Components:', components)
print('Circuit rank:', len(cultures) + len(edges) + components)
print('Diameter:', find_diameter(cultures))
print('Clique number:', clique_number(cultures))
