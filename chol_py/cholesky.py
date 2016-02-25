# Basic application to load a mesh from file and view it in window
# using openGL

# Python imports
import sys
from os.path import basename
import numpy as np
from math import sqrt

# Cyamites imports
import cyamites as cy

#         4
#         |
# 0 - 1 - 2 - 3
#         |
#         5
# pattern_graph =[[],
#                 [],
#                 [],
#                 [],
#                 [],
#                 []]

reorder_dict = {0:2, 1:0, 2:1}
reorder_dict_inv = {v:k for k, v in reorder_dict.iteritems()}

def reorder_func(i):
    return reorder_dict[i]

def reorder_func_inv(i):
    return reorder_dict_inv[i]

# m: a matrix-representation of the pattern grpah
# f: a reordering function
def reorder(m, f):
    rows, cols = m.shape
    n = [[0]*cols for i in xrange(rows)]
    for i in xrange(rows):
        for j in xrange(cols):
            n[f(i)][f(j)] = m[(i, j)]
    return np.matrix(n)


def cholesky(m):
    rows, cols = m.shape
    if (rows == 1):
        m[(0, 0)] = sqrt(m[(0, 0)])
        return m
    m[(0, 0)] = sqrt(m[(0, 0)])
    r = np.vectorize(lambda x: x/m[(0, 0)])(m[0, 1:])
    for i in xrange(1, rows):
        m[(0, i)] /= m[(0, 0)]
        m[(i, 0)] /= m[(0, 0)]
    to_subtract = r.T*r
    sub = m[1:rows, 1:cols]
    sub -= to_subtract
    m[np.ix_([1, rows-1], [1, cols-1])] = cholesky(sub)
    return m

def main():
    print "Hello Cholesky!"
    m = np.matrix([[4, 12, -16], [12, 37, -43], [-16, -43, 98]])
    print "matrix is \n", m
    mm = cholesky(m);
    print "factorization is \n", mm
    m = np.matrix([[4, 12, -16], [12, 37, -43], [-16, -43, 98]])
    m_reordered = reorder(m, reorder_func)
    m_reordered_fac = cholesky(m_reordered)
    print "reordered cholesky is\n", m_reordered_fac
    print "sparsity is %f, %f" %(calc_sparsity(mm), calc_sparsity(m_reordered_fac))

# return the percentage of nonzero numbers
def calc_sparsity(m):
    rows, cols = m.shape
    nonzeros = 0
    for i in xrange(rows):
        for j in xrange(cols):
            if (m[(i, j)] != 0):
                nonzeros += 1
    return float(nonzeros) / (rows * cols)

# def pickFace(vert):
#     print "register a function here"

# def main():

#     # Get the path for the mesh to load, either from the program argument if
#     # one was given, or a dialog otherwise
#     if(len(sys.argv) > 1):
#         filename = sys.argv[1]
#     else:
#         # TODO Implement a file dialog here
#         raise Exception("No file name specified")

#     # Read in the mesh
#     mesh = cy.HalfEdgeMesh(cy.readMesh(filename))
#     # Toss up a viewer window
#     winName = 'Cyamites meshview -- ' + basename(filename)
#     meshDisplay = cy.MeshDisplay(windowTitle=winName)
#     meshDisplay.setMesh(mesh)
#     meshDisplay.pickFaceCallback = pickFace
#     meshDisplay.setVectors("normal", vectorDefinedAt='face')
#     meshDisplay.startMainLoop()


if __name__ == "__main__": main()
