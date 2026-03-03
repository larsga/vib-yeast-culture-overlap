
# vib-yeast-culture-overlap

Code for computing and visualizing overlap between yeast cultures,
used for the paper _Distinctive domestication of farmhouse beer yeasts
preserved pre-industrial genetic and phenotypic diversity_, Peter
W. Bircham, Andrea Del Cortona, Lars M. Garshol, Mohammed T. Tawfeeq,
Beatriz Herrera-Malaver, Sofie Mannaerts, Jeroen Cortebeek, Robbe
Nolmans, Brigida Gallone, Jan Steensels, Kevin J. Verstrepen, Current
Biology. Currently in press.

Specifically, this is the code for Figure 2B.

It is also used for the following from the Supplemental Note: tables
1, 2, 3, and 4, and figures 6, 8, and 9.

Install everything in `requirements.txt` before starting.

# find-largest-overlaps.py

Run as `python find-largest-overlaps.py <groupsfile>`.

Outputs table 3 as well as a dot file. Running the dot file through
GraphViz will produce figure 2B (which is the same as figure 6).

Running it with a group file for a different cutoff will produce
figures 8 and 9 as well.

It also outputs the clusters found by Louvain community detection
(text in Supplemental Note, section 7.1).

# graph-statistics.py

Run as `python graph-statistics.py <graph-file>`.

For each groupsfile it outputs the figures used in table 2.

# find_overlap.py

Run as `python find_overlap.py <newick-file> <cutoff>`.

The cutoff used in the paper was 4.20005, except for figure 8 (5) and
figure 9 (7). Table 2 also used several cutoffs, as given in the
table.

Outputs a groupsfile, usable as input to other scripts.

# make-graph.py

Run as `python make-graph.py <groupsfile>`.

Outputs the graph file, used as input to other scripts.
