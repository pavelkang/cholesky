# Basic application to load a mesh from file and view it in window
# using openGL

# Python imports
import sys
from os.path import basename
import numpy as np
from math import sqrt
from util import *

# Cyamites imports
import cyamites as cy

EPSILON = 1e-5

reorder_dict = {0:2, 1:0, 2:1}
reorder_dict_inv = {v:k for k, v in reorder_dict.iteritems()}

def reorder_func(i):
    return reorder_dict[i]

def reorder_func_inv(i):
    return reorder_dict_inv[i]

def calc_sparsity(m):
    """
    return the percentage of nonzero numbers
    """
    rows, cols = m.shape
    nonzeros = 0
    for i in xrange(rows):
        for j in xrange(cols):
            if (m[(i, j)] != 0):
                nonzeros += 1
    return float(nonzeros) / (rows * cols)

def cholesky_solve(m, printSparsity):
    print "Start Cholesky Factorization..."
    cholesky(m)
    color_print("Sparsity is " + str((calc_sparsity(m))), WARNING)

def almost_zero(x):
    return abs(x) < EPSILON

def cholesky(m):
    rows, cols = m.shape
    if (rows == 1):
        if almost_zero(m[(0, 0)]):
            m[(0, 0)] = 0.0
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
    cholesky(sub) # inplace
    return m

def main():
    print "Hello Cholesky!"
    m = np.matrix([[4, 12, -16], [12, 37, -43], [-16, -43, 98]])
    print "matrix is \n", m
    mm = cholesky(m);
    print "factorization is \n", mm
    m = np.matrix([[4, 12, -16], [12, 37, -43], [-16, -43, 98]])
    # m_reordered = reorder(m, reorder_func)
    # m_reordered_fac = cholesky(m_reordered)
    # print "reordered cholesky is\n", m_reordered_fac
    # print "sparsity is %f, %f" %(calc_sparsity(mm), calc_sparsity(m_reordered_fac))

if __name__ == "__main__":
    main()
