
# This skips the 'P' strains

import marshal, sys

groupsfile = sys.argv[1]
groups = marshal.load(open(groupsfile, 'rb'))

ix = groupsfile.rfind('.')
stem = groupsfile[ : ix]

# ============================================================================
# time to report

def get_culture(strain):
    ix = strain.find('R')
    if ix == -1:
        ix = strain.find('P')
    assert ix != -1, 'Problem with strain %s' % strain

    return strain[ : ix]

def get_culture_overlaps(culture):
    strains = [cc for cc in culture_counts
               if culture in cc]
    totals = {}
    for cc in strains:
        for (c, count) in cc.items():
            if c == culture:
                continue

            totals[c] = totals.get(c, 0) + count

    return totals

def get_color(culture):
    import metadata
    return metadata.colors[metadata.culturemap[culture]]

# def get_color(culture):
#     return 'white'

# how many strains overlapping with different cultures in each
culture_counts = [] # parallel with 'groups' list, contains {c->count} dicts
cultures = set()
for group in groups:
    counts = {}
    for strain in group:
        if 'P' in strain:
            continue # skipping it

        c = get_culture(strain)
        counts[c] = counts.get(c, 0) + 1
        cultures.add(c)
    culture_counts.append(counts)

# --- OUTPUT DOT FILE

widths = set()

f = open(stem + '.dot', 'w')
f.write('''
graph {
''')

edges = set()
for culture in cultures:
    overlaps = get_culture_overlaps(culture)
    (fillc, textc) = get_color(culture)
    f.write('n%s [label = "%s"; fillcolor = "%s"; style=filled; fontcolor=%s; fontsize="40"; shape=circle; fixedsize=shape; width=1.1];\n' %
            (culture, culture, fillc, textc))
    for (c2, count) in overlaps.items():
        edge = (culture, c2)
        if (c2, culture) in edges:
            continue

        width = (count / 40.0) * 20
        widths.add(count)
        f.write('  n%s -- n%s [weight = %s; penwidth= %s];\n' % (culture, c2, count, width))
        edges.add(edge)

f.write('}\n')
f.close()

print(widths)

# --- DUMP GRAPH

def overlaps(c1, c2):
    overlaps = get_culture_overlaps(c1)
    return overlaps[c2]

import marshal

nodes = list(cultures)
edges = [(c1, c2, overlaps(c1, c2)) for (c1, c2) in edges]

with open(stem + '-graph.bin', 'wb') as f:
    marshal.dump((nodes, edges), f)

# --- DISPLAY OVERLAPS

# c1 = '5'
# c2 = '6'
# for group in groups:
#     gcultures = set([get_culture(s) for s in group])
#     # if len(gcultures) > 1:
#     #     print(gcultures)
#     if c1 in gcultures and c2 in gcultures:
#         print('-----')
#         for s in group:
#             print(s)
