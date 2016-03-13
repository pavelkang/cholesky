import numpy as np
import Queue as Q

def sort_by_second((v1, d1), (v2, d2)):
    if d1 > d2:
        return 1
    elif d1 == d2:
        return 0
    else:
        return -1

class ReorderStrategy(object):
    def __init__(self, mesh, vs):
        """
        mesh: the halfedge object of the 3D mesh
        vs: the vertices of the mesh in a list, this is also passed in so that
            all strategies can have a fixed ordering of vertices at the
            beginning as a reference
        """
        self.mesh = mesh
        self.vs = vs
        self.vd = {vs[i]: i for i in xrange(len(vs))}
        self.matrix = self.build_matrix()
        self.reorder_dict = self.reorder()

    def build_matrix(self):
        """
        Build the pattern graph matrix
        """
        verts, nv = self.vs, len(self.vs)
        m = [[0] * nv for i in xrange(nv)]
        for v in verts:
            m[self.vd[v]][self.vd[v]] = v.degree
            for u in v.adjacentVerts():
                m[self.vd[v]][self.vd[u]] = - 1.0
        return np.matrix(m)

    def getName(self):
        pass

    def reorder(self):
        return {i:i for i in xrange(self.matrix.shape[0])}

    def applyReorder(self):
        rows, cols = self.matrix.shape
        n = [[0]*cols for i in xrange(rows)]
        for i in xrange(rows):
            for j in xrange(cols):
                n[self.reorder_dict[i]][self.reorder_dict[j]] = self.matrix[(i, j)]
        return np.matrix(n)

class RandomStrat(ReorderStrategy):
    """
    Randomly order vertices
    """

    def getName(self):
        return "Strategy: Random"

    def reorder(self):
        reorder_list = np.random.permutation(self.vs)
        return {i : self.vd[reorder_list[i]] for i in xrange(len(self.vs))}

class SortByXStrat(ReorderStrategy):
    """
    Order vertices by their x coordinates
    """

    def getName(self):
        return "Strategy: Sort by X coordinates"

    def reorder(self):
        verts_and_xs = [(i, self.vs[i].pos[0]) for i in xrange(len(self.vs))]
        verts_and_xs.sort(sort_by_second)
        return {verts_and_xs[i][0] : i for i in xrange(len(verts_and_xs))}


class MinDegreeStrat(ReorderStrategy):
    """
    Order vertices by their degrees
    """
    def getName(self):
        return "Strategy: Minimum Degree"

    def reorder(self):
        verts_and_degs = [(i, self.vs[i].degree) for i in xrange(len(self.vs))]
        verts_and_degs.sort(sort_by_second)
        return {verts_and_degs[i][0] : i for i in xrange(len(verts_and_degs))}

class MaxDegreeStrat(ReorderStrategy):
    """
    Order vertices by their degrees
    """
    def getName(self):
        return "Strategy: Maximum Degree"

    def reorder(self):
        verts_and_degs = [(i, self.vs[i].degree) for i in xrange(len(self.vs))]
        verts_and_degs.sort(sort_by_second, reverse=True)
        return {verts_and_degs[i][0] : i for i in xrange(len(verts_and_degs))}

class CuthillStrat(ReorderStrategy):
    """
    The Cuthill-Mckee algorithm
    """
    def getName(self):
        return "Strategy: Cuthill"
    def reorder(self):
        """
        We start from a min-degree vertex, do BFS
        """
        verts_and_degs = [(i, self.vs[i].degree) for i in xrange(len(self.vs))]
        verts_and_degs.sort(sort_by_second)
        v = verts_and_degs[0][0]
        # initialize everything to map to -1
        R = {i: -1 for i in xrange(len(verts_and_degs))}
        curr = 0 # current mapped vertex to be assigned
        frontier = Q.Queue()
        frontier.put(v)
        while (frontier.empty() == False):
            u = frontier.get()
            if R[u] != -1:
                continue
            R[u] = curr
            curr += 1
            for un in self.vs[u].adjacentVerts():
                if R[self.vd[un]] == -1:
                    frontier.put(self.vd[un])
        return R
