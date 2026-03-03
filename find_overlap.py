
import sys, re, marshal
from sprake import newick # https://github.com/larsga/sprake

# BEWARE!!
# This script has a bug. See email from Peter Bircham 2024-11-14.
# Nodes can end up being included in two groups. See check.py
# and doublecheck.py. Plus debug.pdf.
#
# Worked around problem by increasing cutoff to 4.200005.

#---------------------------------------------------------------------------
# DUPE FROM PCRLIB

REG_CULTURE = re.compile('(\\d+|A[ABCDEF])(P|R)\\d+')
def get_culture(strain_name):
    m = REG_CULTURE.match(strain_name)
    if m:
        return m.group(1)

#---------------------------------------------------------------------------

def find_subtree(node, subheight, cutoff):
    parent = node.get_parent()
    # nodeheight = max([ch.get_distance() for ch in parent.get_children()])
    nodeheight = node.get_distance()
    if nodeheight + subheight > cutoff:
        return node

    # print(node.get_label(), nodeheight, nodeheight + subheight)
    return find_subtree(parent, nodeheight + subheight, cutoff)

def find_neighbours(node, cutoff):
    top = find_subtree(node, 0, cutoff)
    neighbours = []
    find_leaves(top, 0, neighbours, cutoff)
    return neighbours

def find_leaves(node, predistance, neighbours, cutoff):
    if not node.get_children():
        neighbours.append(node)
        return

    for ch in node.get_children():
        # print(node, ch.get_label(), predistance + ch.get_distance())
        if predistance + ch.get_distance() <= cutoff:
            find_leaves(ch, predistance + ch.get_distance(), neighbours, cutoff)

def find_node(tree, label):
    for l in tree.get_leaves():
        if rewrite(l.get_label()) == label:
            return l

def shortfloat(num):
    return str(round(num * 100) / 100.0)

def load_tree(nwkfile):
    return newick.parse_string(open(nwkfile).read())

def build_groups(tree, cutoff):
    processed = set()
    groups = []

    for leaf in tree.get_leaves():
        l = rewrite(leaf.get_label())
        if l in processed:
            continue

        # print('\n---', l)
        neighbours = find_neighbours(leaf, cutoff)
        for subleaf in neighbours:
            # print(subleaf.get_label())
            processed.add(rewrite(subleaf.get_label()))

        group = [rewrite(sl.get_label()) for sl in neighbours]
        groups.append(group)

    return groups

def rewrite(s):
    if s.startswith('54b') or s.startswith('57b'):
        return s[ : 2] + s[3 : ]
    return s

# --- DUMP GROUPS

if __name__ == '__main__':
    tree = load_tree(sys.argv[1])
    cutoff = float(sys.argv[2])
    outfile = sys.argv[3]

    print('height:', tree.get_distance_height())
    groups = build_groups(tree, cutoff)

    print('GROUPS:', len(groups))
    print('STRAINS:', len(tree.get_leaves()))
    print('PERCENT:', len(groups) / len(tree.get_leaves()))

    with open(outfile, 'wb') as f:
        marshal.dump(groups, f)
