"""Modules for efficient representation of the Minimum spanning tree problem.
"""
__author__ = 's131509'

import copy
import numpy
import unittest


class SquareMatrix:
    """Square matrix for storing numeric or boolean values. Backed by numpy array."""

    def __init__(self, size):
        """Creates a new square matrix.
        :param size: Size of the matrix to be created.
        """
        self.matrix = numpy.zeros(shape=(size, size))

    def get(self, row, col):
        """Retrieves an element from the matrix.

        :param row: row position.
        :param col: column position.
        :return: en element at specified position.
        """
        return self.matrix[row, col]

    def set(self, row, col, value):
        """Stores an element in the matrix.

        :param row: row position.
        :param col: col position.
        :param value: value to store. Must be numeric or boolean.
        """
        self.matrix[row, col] = value

    def size(self):
        """
        :return: size of the matrix.
        """
        return self.matrix.shape[0]

    def clone(self):
        """
        :return: clone of the matrix.
        """
        return copy.deepcopy(self)


class Edge:
    """A single edge in an undirected graph.
    """

    def __init__(self, vertex1, vertex2):
        """Creates a new edge. Order of the vertices doesn't matter.
        :param vertex1: number of the first vertex (0 - (length of graph - 1))
        :param vertex2: number of the second vertex1 (0 - (length of graph - 1))
        """
        if vertex1 > vertex2:
            vertex1, vertex2 = vertex2, vertex1
        self.vertex1 = vertex1
        self.vertex2 = vertex2

    def isBacktrackMarker(self):
        """Minimum spanning tree algorithm specific method.
        :return: True if the edge is an instance of the backtrack market.
        """
        return self.vertex1 == -1 and self.vertex2 == -1

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "({0}, {1})".format(self.vertex1, self.vertex2)

    def __eq__(self, other):
        sameOrder = self.vertex1 == other.vertex1 and self.vertex2 == other.vertex2
        crossedOrder = self.vertex1 == other.vertex2 and self.vertex2 == other.vertex1
        return sameOrder or crossedOrder

    def __lt__(self, other):
        return (10 * self.vertex1 + self.vertex2) < (10 * other.vertex1 + other.vertex2)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.vertex1) * hash(self.vertex2)


class SpanningTree:
    """Spanning tree of a graph. Optimized for memory efficiency, so it does not store the whole graph it belongs to.
     The intended usage is to exchange instance of this class between solvers working on a same undirected graph.
    """

    def __init__(self, graphSize):
        """Creates an empty spanning tree for a graph of given size.
        :param graphSize: size of the graph the spanning tree belongs to.
        """
        self.edges = []
        self.vertex_degrees = [0] * graphSize

    def edgeList(self):
        """
        :return: list of edges in the spanning tree.
        """
        return self.edges

    def vertexDegrees(self):
        return self.vertex_degrees

    def addEdge(self, edge):
        """Adds a new graph edge to the spanning tree. Does not check if the edge exists in the graph!
        If the edge is already present in the spanning tree, the tree won't be changed.
        Has complexity of O(n).
        :param edge: edge to add to the spanning tree.
        """
        if edge not in self.edges:
            self.vertex_degrees[edge.vertex1] += 1
            self.vertex_degrees[edge.vertex2] += 1
            self.edges.append(edge)

    def removeLastEdge(self):
        """Removes the last added edge. Can be called repeatedly until the spanning tree is empty.
        Call on an empty spanning tree has no effect.
        """
        if self.edges:
            removed = self.edges.pop()
            self.vertex_degrees[removed.vertex1] -= 1
            self.vertex_degrees[removed.vertex2] -= 1

    def edgeCount(self):
        """
        :return: number of edges in the spanning tree.
        """
        return len(self.edges)

    def maxDegree(self):
        """
        :return: maximum vertex degree of the spanning tree.
        """
        return max(self.vertex_degrees)

    def maxDegreeWith(self, edge):
        """
        Returns maximum vertex degree of a spanning tree consisting of this spanning tree with given edge added.
        Does not modify the spanning tree.
        :param edge: edge to add..
        :return: maximum degree of the hypothetical tree.
        """
        max = self.vertex_degrees[0]

        for i in range(len(self.vertex_degrees)):
            degree = self.vertex_degrees[i]
            if (edge.vertex1 == i) or (edge.vertex2 == i):
                degree += 1
            if degree > max:
                max = degree

        return max

    def __str__(self):
        result = ", ".join(str(edge) for edge in self.edges)
        return result


class TestSquareMatrix(unittest.TestCase):

    def setUp(self):
        self.matrix = SquareMatrix(5)

    def test_empty(self):
        for i in range(5):
            for j in range(5):
                element = self.matrix.get(i, j)
                self.assertTrue(element == 0)

    def test_set_get(self):
        self.matrix.set(3, 3, 1)
        elem = self.matrix.get(3, 3)
        self.assertTrue(elem == 1)

    def test_sizes(self):
        size = self.matrix.size()
        self.assertTrue(size == 5)

    def test_clone(self):
        self.matrix.set(2, 2, 1)
        clone = self.matrix.clone()
        self.matrix.set(3, 3, 1)
        clone.set(4, 4, 1)

        orig_before_cloning = self.matrix.get(2, 2)
        self.assertTrue(orig_before_cloning == 1)

        orig_after_cloning = self.matrix.get(3, 3)
        matching_clone_elem = clone.get(3, 3)
        self.assertTrue(orig_after_cloning == 1)
        self.assertTrue(matching_clone_elem == 0)

        modified_clone = clone.get(4, 4)
        matching_orig_elem = self.matrix.get(4, 4)
        self.assertTrue(modified_clone == 1)
        self.assertTrue(matching_orig_elem == 0)


class TestEdge(unittest.TestCase):

    def setUp(self):
        self.edge = Edge(1, 2)
        self.edge2 = Edge(2, 1)

    def test_str(self):
        edge_str = self.edge.__str__()
        self.assertEqual("(1, 2)", edge_str)

        edge_str_2 = self.edge2.__str__()
        self.assertEqual("(1, 2)", edge_str_2)

    def test_eq_ne(self):
        self.assertTrue(self.edge == self.edge2)
        self.assertFalse(self.edge != self.edge2)

        edge3 = Edge(1, 2)
        self.assertTrue(self.edge == edge3)
        self.assertFalse(self.edge != edge3)

        edge4 = Edge(1, 3)
        self.assertFalse(edge3 == edge4)
        self.assertTrue(edge3 != edge4)


class TestSpanningTree(unittest.TestCase):

    def setUp(self):
        self.spanning_tree = SpanningTree(7)

    def test_manipulateEdges(self):
        self.spanning_tree.addEdge(Edge(0, 1))
        self.assertEqual(1, self.spanning_tree.maxDegree())
        self.assertEqual(1, self.spanning_tree.edgeCount())

        self.spanning_tree.addEdge(Edge(1, 2))
        self.assertEqual(2, self.spanning_tree.maxDegree())
        self.assertEqual(2, self.spanning_tree.edgeCount())

        self.spanning_tree.removeLastEdge()
        self.assertEqual(1, self.spanning_tree.maxDegree())
        self.assertEqual(1, self.spanning_tree.edgeCount())

        self.spanning_tree.removeLastEdge()
        self.assertEqual(0, self.spanning_tree.maxDegree())
        self.assertEqual(0, self.spanning_tree.edgeCount())

    def test_maxDegree(self):
        self.spanning_tree.addEdge(Edge(0, 1))
        self.spanning_tree.addEdge(Edge(1, 2))
        self.spanning_tree.addEdge(Edge(1, 3))

        self.assertEqual(3, self.spanning_tree.maxDegree())

    def test_maxDegreeWith(self):
        self.spanning_tree.addEdge(Edge(0, 1))
        self.spanning_tree.addEdge(Edge(1, 2))

        degree = self.spanning_tree.maxDegreeWith(Edge(1, 3))
        self.assertEqual(3, degree)

    def test_str(self):
        self.spanning_tree.addEdge(Edge(0, 1))
        self.spanning_tree.addEdge(Edge(1, 2))
        self.spanning_tree.addEdge(Edge(1, 3))

        expected = "(0, 1), (1, 2), (1, 3)"
        actual = self.spanning_tree.__str__()
        self.assertEqual(expected, actual)

    def test_duplicate_edges(self):
        self.spanning_tree.addEdge(Edge(1, 2))
        self.assertEqual(1, self.spanning_tree.edgeCount())
        self.spanning_tree.addEdge(Edge(1, 2))
        self.assertEqual(1, self.spanning_tree.edgeCount())


if __name__ == '__main__':
        unittest.main()