"""
*******************************
*  James Andrew Ure 30653770  *
*Completed on 4th of June 2020*
*******************************
"""
import math


class Graph:
    class Node:
        class Edge:
            def __init__(self, target, weight):
                """
                Constructor for edges
                :Time complexity (worst case): O(1)
                :Auxiliary space (worst case): O(1)
                :param target: the node the edge is pointing to
                :param weight: the weight of the edge
                """
                self.target = target
                self.weight = weight

        # node
        def __init__(self, ID):
            """
            Constructor for nodes

            :Time complexity (worst case): O(1)
            :Auxiliary space (worst case): O(1)
            :param ID: The identifier of the node (must be unique)
            """
            self.edges = []
            self.ID = ID

        def add_edge(self, targetNode, weight):
            """
            Method to create a edge and add it to this node, which will point to another node to link them

            :Time complexity (worst case): O(1)
            :Auxiliary space (worst case): O(1)
            :param targetNode: The node the edge will point to
            :param weight: The weight of the edge
            """
            self.edges.append(self.Edge(targetNode, weight))

    def __init__(self, gfile):
        """
        Constructor for the graph

        :Time complexity (worst case): O(N^2) where N is the number of nodes
        :Auxiliary space (worst case): O(N^2) where N is the number of nodes
        :param gfile: The file containing the data of the graph to be inserted into this object
        """
        self.nodes = []
        self.nodecount = 0
        file = open(gfile, "r")

        self.nodecount = int(file.readline())
        for nodeID in range(self.nodecount):
            self.nodes.append(self.Node(nodeID))

        lines = file.readlines()
        for line in lines:
            data = line.strip()
            numbers = data.split()
            vertex1, vertex2, weight = int(numbers[0]), int(numbers[1]), int(numbers[2])

            self.nodes[vertex1].add_edge(self.nodes[vertex2], weight)
            self.nodes[vertex2].add_edge(self.nodes[vertex1], weight)

    def shallowest_spanning_tree(self):
        """
        Graph to calculate the optimal node in the graph which has the shortest maximum distance to any
        node across the graph (this does not take edge weights into account)

        :Time complexity (worst case): O(V^3) where V is the number of nodes in the graph
        --CHECK--:Auxiliary space (worst case): O(V) where V is the number of nodes in the graph
        :return: A tuple of the optimal node ID with the maximum distance to travel to any node in the graph
        """
        minDepth = math.inf
        minNode = None

        for rootnode in self.nodes:
            visitedcount = 1
            current = rootnode
            queue = [None] * self.nodecount
            queuestart = 0
            queueend = 0
            visited = [False] * self.nodecount
            distances = [0] * self.nodecount

            visited[rootnode.ID] = True

            # implementation of breadth first search
            while visitedcount < self.nodecount:
                for i in range(len(current.edges)):
                    neighbour = current.edges[i].target
                    if visited[neighbour.ID] is False:
                        visited[neighbour.ID] = True
                        distances[neighbour.ID] = distances[current.ID] + 1
                        visitedcount += 1
                        queue[queueend % self.nodecount] = neighbour
                        queueend += 1

                current = queue[queuestart % self.nodecount]
                queuestart += 1

            # gets longest path to a node
            # if this is more optimal than other root nodes, update
            if max(distances) < minDepth:
                minDepth = max(distances)
                minNode = rootnode.ID

        return minNode, minDepth

    def dijkstra(self, dist, visited, priorqueue, pred):
        """
        Dijkstra algorithm to find the shortest distance to every node in the graph from one or more nodes.

        :Time complexity (worst case): O(ELogV) where E is the number of edges in the graph and V is the number
        of nodes in the graph
        :Auxiliary space (worst case): O(V) where V is the number of nodes in the graph
        :param dist: The array containing known distances to nodes in the graph
        :param visited: The array containing the nodes which have been visited already
        :param priorqueue: The priorityqueue which will be used to use a greedy approach to traverse
        the graph (priorityqueue is implemented as a min heap in this approach)
        :param pred: The array containing the nodes that point to another for the optimal traversal
        :return: a tuple containing the dist array containing all distances to every node on the graph
        from the source and the pred array containing the nodes that point to another for the optimal
        traversal
        """

        # Keeps performing dijkstra until all nodes have been visited (queue will be empty)
        while not priorqueue.empty():
            currentnode = priorqueue.remove()
            visited[currentnode[1]] = True

            for edge in self.nodes[currentnode[1]].edges:
                if edge.weight + dist[currentnode[1]] < dist[edge.target.ID]:
                    dist[edge.target.ID] = edge.weight + dist[currentnode[1]]
                    pred[edge.target.ID] = currentnode[1]
                    priorqueue.add((edge.weight, edge.target.ID))
        return dist, pred

    def shortest_errand(self, start, destination, ice_locs, ice_cream_locs):
        """
        This method finds the shortest path to go from the source to an ice node to an ice cream node
        to the destination, and the nodes it must traverse through to reach this optimal solution.
        Edge weights are taken into account.

        :Time complexity (worst case): O(ELogV) where E is the number of edges in the graph and V is the number
        of nodes in the graph
        :Auxiliary space (worst case): O(V) where V is the number of nodes in the graph
        :param start: The node ID containing the source of where the traversal will begin
        :param destination: The node ID containing the final destination where the traversal will terminate once
        it has reached an ice_loc and ice_cream_loc prior
        :param ice_locs: An array of node IDs containing the nodes which are an ice location (first destination
        from the source)
        :param ice_cream_locs: An array of the node IDs containing the nodes which are an ice cream location
        (second destination from the source, after ice_locs)
        :return: A tuple of the total edge weights to reach the final destination node and an array of the
        node IDs which the graph must traverse across to reach the destination with the optimal solution.
        """
        # FIRST DIJKSTRA

        # Variable initialization to perform dijkstra
        minheap = MinHeap()
        dist = [math.inf] * self.nodecount
        dist[start] = 0
        minheap.add((0, start))
        visited = [False] * self.nodecount
        visited[start] = True
        pred = [0] * self.nodecount

        # Execute dijkstra with initialized variables as input
        distances, pred = self.dijkstra(dist, visited, minheap, pred)
        pred1 = pred

        # SECOND DIJKSTRA - Same thing applies here but we're adding distances
        # calculated from the previous dijkstra to the minheap to continue traversal
        pred = [0] * self.nodecount
        dist = [math.inf] * self.nodecount
        visited = [False] * self.nodecount

        for ice_loc in ice_locs:
            dist[ice_loc] = distances[ice_loc]
            minheap.add((dist[ice_loc], ice_loc))

        distances, pred = self.dijkstra(dist, visited, minheap, pred)
        pred2 = pred

        # THIRD AND FINAL DIJKSTRA - Again, same thing applies here however this will arrive at final
        # destination
        dist = [math.inf] * self.nodecount
        visited = [False] * self.nodecount
        pred = [0] * self.nodecount

        for ice_cream_loc in ice_cream_locs:
            dist[ice_cream_loc] = distances[ice_cream_loc]
            minheap.add((dist[ice_cream_loc], ice_cream_loc))

        distances, pred = self.dijkstra(dist, visited, minheap, pred)
        pred3 = pred

        # Getting the nodes that consist of optimal distance
        finalpred = [destination]

        level = 0
        currentnode = destination

        while level != 2 or currentnode != 0:
            if level == 0:
                if currentnode in ice_cream_locs:
                    level = 1
                else:
                    currentnode = pred3[currentnode]
                    finalpred.append(currentnode)

            elif level == 1:
                if currentnode in ice_locs:
                    level = 2
                else:
                    currentnode = pred2[currentnode]
                    finalpred.append(currentnode)

            else:
                currentnode = pred1[currentnode]
                finalpred.append(currentnode)

        finalpred.reverse()
        return dist[destination], finalpred


# created by me for log N instead of N queue(very efficient, much awesome)
class MinHeap:
    def __init__(self):
        """
        Constructor for a min heap

        :Time complexity (worst case): O(1)
        :Auxiliary space (worst case): O(1)
        """
        # self.root = self.Node()
        self.array = [(-1, -1)]
        self.heapsize = 0

    def empty(self):
        """
        Checks if the min heap is empty

        :Time complexity (worst case): O(1)
        :Auxiliary space (worst case): O(1)
        :return: True if empty, false if not
        """
        if self.heapsize == 0:
            return True
        return False

    def get(self):
        """
        An accessor for the array of the min heap (mainly used for testing)

        :Time complexity (worst case): O(1)
        :Auxiliary space (worst case): O(1)
        :return: The array of the min heap
        """
        return self.array

    @staticmethod
    def parent(position):
        """
        A static method to calculate the index of the parent element from a child position

        :Time complexity (worst case): O(1)
        :Auxiliary space (worst case): O(1)
        :param position: The array index of the child
        :return: The index of the parent node
        """
        return position//2

    @staticmethod
    def right_child(position):
        """
        A static method to calculate the index of the right child from a parent node

        :Time complexity (worst case): O(1)
        :Auxiliary space (worst case): O(1)
        :param position: The array index of the parent
        :return: The array index of the right child
        """
        return (position * 2) + 1

    @staticmethod
    def left_child(position):
        """
        A static method to calculate the index of the left child from a parent node

        :Time complexity (worst case): O(1)
        :Auxiliary space (worst case): O(1)
        :param position: The array index of the parent
        :return: The array index of the left child
        """
        return position * 2

    def has_children(self, position):
        """
        Checks if a parent element has any children

        :Time complexity (worst case): O(1)
        :Auxiliary space (worst case): O(1)
        :param position: The index of the parent in the array
        :return: True if the parent has any children, False otherwise
        """
        if position * 2 > self.heapsize:
            return False
        return True

    def has_right(self, position):
        """
        Checks if a parent element has a right child

        :Time complexity (worst case): O(1)
        :Auxiliary space (worst case): O(1)
        :param position: The index of the parent in the array
        :return: True if the parent has a right child, False otherwise
        """
        if (position * 2) + 1 > self.heapsize:
            return False
        return True

    def swap(self, position1, position2):
        """
        Swaps two elements in the heap

        :Time complexity (worst case): O(1)
        :Auxiliary space (worst case): O(1)
        :param position1: The index of the first element to swap with the element at position2
        :param position2: The index of the second element to swap with the element at position1
        """
        self.array[position1], self.array[position2] = self.array[position2], self.array[position1]

    def heapify(self, position):
        """
        When an element is popped, the heap must be restructured to compensate for this
        data change. It will need to swap elements and traverse across these children until
        it reaches a leaf node.

        :Time complexity (worst case): O(LogN) where N is the number of elements in the heap
        :Auxiliary space (worst case): O(1)
        :param position: The index that contains the element to be swapped with its child
        """

        # Keep traversing till it's a leaf
        if self.has_children(position):

            # If it has a right child then it has a left child too
            if self.has_right(position):

                # Swap with the greater value child
                if self.array[position] > self.array[self.left_child(position)] or \
                        self.array[position] > self.array[self.right_child(position)]:

                    if self.array[self.left_child(position)] < self.array[self.right_child(position)]:
                        maxchildpos = self.left_child(position)
                    else:
                        maxchildpos = self.right_child(position)

                    self.swap(position, maxchildpos)
                    self.heapify(maxchildpos)

            # If it has a child but not a right child, it can only have a left child
            else:
                self.swap(position, self.left_child(position))
                self.heapify(self.left_child(position))

    def add(self, data):
        """
        Adds an element to the heap

        :Time complexity (worst case): O(LogN) where N is the number of elements in the heap
        :Auxiliary space (worst case): O(1) where N is the number of elements in the heap
        :param data: A tuple of a distance and a node ID
        """
        self.array.append(data)
        self.heapsize += 1
        current = self.heapsize

        while self.array[current] < self.array[self.parent(current)]:
            self.swap(current, self.parent(current))
            current = self.parent(current)

    def remove(self):
        """
        Pops the smallest value element from the heap

        :Time complexity (worst case): O(1)
        :Auxiliary space (worst case): O(1)
        :return: A tuple of a distance and node ID
        """
        removed = self.array[1]
        self.array[1] = self.array[self.heapsize]
        self.array.pop()
        self.heapsize -= 1
        self.heapify(1)
        return removed


if __name__ == "__main__":
    graph = Graph("shortesterrandfile")
    print(graph.shortest_errand(0, 8, [1], [0]))

    graph = Graph("gfile2")
    print(graph.shallowest_spanning_tree())
