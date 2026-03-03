
# This skips the 'P' strains

import marshal, sys, pprint

groupsfile = sys.argv[1]
groups = marshal.load(open(groupsfile, 'rb'))

ix = groupsfile.rfind('.')
stem = groupsfile[ : ix]

def get_culture(strain):
    ix = strain.find('R')
    if ix == -1:
        ix = strain.find('P')
    assert ix != -1, 'Problem with strain %s' % strain

    return strain[ : ix]

def group_by_key(collection, keyfunc):
    by_key = {}
    for o in collection:
        key = keyfunc(o)
        if key not in by_key:
            by_key[key] = []

        by_key[key].append(o)

    return by_key

samples_by_culture = {}

all_cultures = set()
overlaps = {} # (c1, c2) -> [...]
for group in groups:
    group = filter(lambda s: 'P' not in s, group)
    by_culture = group_by_key(group, get_culture)
    for c in by_culture.keys():
        all_cultures.add(c)

        samples_by_culture[c] = samples_by_culture.get(c, 0) + len(by_culture[c])

    if len(by_culture) == 1:
        continue

    cultures = list(by_culture.keys())
    cultures.sort()

    for ix1 in range(len(cultures)):
        c1 = cultures[ix1]
        for ix2 in range(ix1 + 1, len(cultures)):
            c2 = cultures[ix2]

            key = (c1, c2)
            if key not in overlaps:
                overlaps[key] = []
            overlaps[key] += by_culture[c1]
            overlaps[key] += by_culture[c2]

c_pairs = list(overlaps.keys())
c_pairs.sort(key = lambda pair: len(overlaps[pair]))
c_pairs.reverse()

import tablelib

print('--- TABLE 3\n')

writer = tablelib.ConsoleWriter(sys.stdout)
writer.start_table()

writer.header_row('C1', 'C2', 'C1 strains', 'C2 strains', 'Overlap')

for (c1, c2) in c_pairs:
    strains = overlaps[(c1, c2)]

    total = samples_by_culture.get(c1) + samples_by_culture.get(c2)
    overlap = (len(strains) / total) * 100
    c1c = len([s for s in strains if get_culture(s) == c1])
    c2c = len([s for s in strains if get_culture(s) == c2])
    writer.row(c1, c2,
               '%s / %s' % (c1c, samples_by_culture.get(c1)),
               '%s / %s' % (c2c, samples_by_culture.get(c2)),
               overlap)

writer.end_table()

# --- OUTPUT DOT FILE

import random

def get_color(culture):
    import metadata
    return metadata.colors[metadata.culturemap[culture]]

f = open(stem + '.dot', 'w')
f.write('''
graph {
''')

all_cultures = list(all_cultures)
random.shuffle(all_cultures)
for culture in all_cultures:
    (fillc, textc) = get_color(culture)
    f.write('n%s [label = "%s"; fillcolor = "%s"; style=filled; fontcolor=%s; fontsize="40"; shape=circle; fixedsize=shape; width=1.1];\n' %
            (culture, culture, fillc, textc))

edges = list(overlaps.items())
random.shuffle(edges)
for ((c1, c2), strains) in edges:
    width = (len(strains) / 80.0) * 20
    f.write('  n%s -- n%s [weight = %s; penwidth= %s];\n' % (c1, c2, width, width))

f.write('}\n')
f.close()

# --- CONSTRUCT NETWORKX GRAPH

print('\n--- LOUVAIN COMMUNITIES\n')

import networkx as nx

G = nx.Graph()

G.add_nodes_from(all_cultures)

for ((c1, c2), strains) in edges:
    weight = len(strains) / 80.0
    G.add_edge(c1, c2, weight = weight)

from networkx.algorithms.community import louvain

partitions = list(louvain.louvain_partitions(G))
pprint.pprint(partitions)
