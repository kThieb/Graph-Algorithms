def DFS(start_nodes, end_nodes, pointers, starting_node):
    """
    Performs a Depth First Search
    The parameters are : a forward star representation of a graph and a starting node
    """

    # Initialize parameters
    stack = [starting_node]  # We use a stack to compute the order of traversal of the node

    result = []

    visited = [False for k in range(len(pointers) - 1)]  # We need to keep track of the visited nodes
    visited[starting_node - 1] = True

    # While the stack is not empty, we traverse the graph
    while len(stack) != 0:
        # We pop the next Node
        current = stack.pop()
        result.append(current)

        # We fetch the next nodes in the graph thanks to the pointers and end_nodes lists
        arc_number = pointers[current - 1]
        next_arc_number = pointers[current]
        # We try to add every node connected to the current one
        for i in range(arc_number, next_arc_number):
            # We only add non visited nodes
            if not visited[end_nodes[i - 1] - 1]:
                stack.append(end_nodes[i - 1])
                visited[end_nodes[i - 1] - 1] = True

    return result


def BFS(start_nodes, end_nodes, pointers, starting_node):
    """
    Performs a Breadth First Search
    The parameters are : a forward star representation of a graph and a starting node
    """

    q = [starting_node]
    result = []
    visited = [False for k in range(len(pointers) - 1)]
    visited[starting_node - 1] = True
    while len(q) != 0:
        current = q.pop(0)
        result += [current]
        arc_number = pointers[current - 1]
        next_arc_number = pointers[current]
        for i in range(arc_number, next_arc_number):
            if not visited[end_nodes[i - 1] - 1]:
                q.append(end_nodes[i - 1])
                visited[end_nodes[i - 1] - 1] = True

    return result


# data from a graph (the topological ordering one)
starting_nodes = [1, 1, 2, 4, 4, 5, 5, 5, 6, 6, 7, 7, 8]
ending_nodes = [3, 8, 1, 3, 8, 2, 6, 4, 1, 2, 4, 5, 3]
pointer_list = [1, 3, 4, 4, 6, 9, 11, 13, 14]

print("1st DFS = ", DFS(starting_nodes, ending_nodes, pointer_list, 7))
print("1st BFS = ", BFS(starting_nodes, ending_nodes, pointer_list, 7))

# another dataset
starting_node2 = [1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 6]
ending_node2 = [2, 3, 4, 5, 1, 4, 6, 5, 1, 2, 3]
pointer_list2 = [1, 3, 5, 8, 10, 11, 12]

print("2nd DFS = ", DFS(starting_node2, ending_node2, pointer_list2, 1))
print("2nd BFS = ", BFS(starting_node2, ending_node2, pointer_list2, 1))

# These are the result after executing the code
# 1st DFS =  [7, 5, 6, 1, 8, 3, 2, 4]
# 1st BFS =  [7, 4, 5, 3, 8, 2, 6, 1]
# 2nd DFS =  [1, 3, 6, 4, 5, 2]
# 2nd BFS =  [1, 2, 3, 4, 5, 6]