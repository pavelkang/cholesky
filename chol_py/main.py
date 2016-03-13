import sys
import cyamites as cy
from util import *
from reorderStrategy import *
from cholesky import cholesky_solve

def main():
    # Get the path for the mesh to load, either from the program argument if
    # one was given, or a dialog otherwise
    filename = readFileName()
    # Load a mesh
    mesh = cy.HalfEdgeMesh(cy.readMesh(filename))
    # Try different strategies on this mesh
    vs = list(mesh.verts)
    strats = [RandomStrat(mesh, vs), SortByXStrat(mesh, vs),
              MinDegreeStrat(mesh, vs), MaxDegreeStrat(mesh, vs),
              CuthillStrat(mesh, vs)]
    # print sparsities
    for strat in strats:
        color_print("------ "+strat.getName()+" ------", PRIMARY)
        m = strat.applyReorder()
        cholesky_solve(m, printSparsity = True)
    return 0

if __name__ == "__main__":
    main()
