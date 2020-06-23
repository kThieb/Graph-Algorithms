def topological_ordering(start_node, end_node, pointers, indegree):
    """
    Returns a topological ordering of the graph represented using the forward star representation
    The parameters are : a forward star representation, and the indegrees of the node of the graph
    In this algorithm, we do not need to have the information about the start_nodes,
    but I decided to keep is as an argument because it is a part of the forward star representation
    """
    # Initialize the parameters
    order = [0 for i in range(8)]
    next_number = 0
    index = find_index(indegree, 0, range(1, 9))
    next_node = []
    next_node.append(index)

    # while loop to go through the graph
    while len(indegree) > 0 and len(next_node) > 0:
        index = next_node.pop()
        # next number increased by 1
        next_number += 1
        # We set the order of the node currently visited
        order[index - 1] = next_number

        # We do not need to delete the current node from the list for the algorithm to work,
        # so I commented the following line
        # del indegree[index]

        # We modify the list
        arc_number = pointers[index - 1]
        for i in range(arc_number, pointers[index]):
            n = end_node[i - 1]
            indegree[n] = indegree[n] - 1

            # This if statement is to compute the next node at the same time as going through the graph
            if indegree[n] == 0:
                next_node.append(n)

    # We return the topological order
    return order


def find_index(dictionary, number, possible_numbers):
    """
    Finds the first key of the value number in the dictionary, in a set of possible numbers
    If the key does not exists, returns -1
    """
    for i in possible_numbers:
        if i in dictionary and dictionary[i] == number:
            return i
    return -1


# data of the graph

starting_node = [1, 1, 2, 4, 4, 5, 5, 5, 6, 6, 7, 7, 8]
ending_node = [3, 8, 1, 3, 8, 2, 4, 6, 1, 2, 4, 5, 3]

pointer_list = [1, 3, 4, 4, 6, 9, 11, 13, 14]

indegree = {1: 2, 2: 2, 3: 3, 4: 2, 5: 1, 6: 1, 7: 0, 8: 2}

print("order = ", topological_ordering(starting_node, ending_node, pointer_list, indegree))

# The result after printing is : order = [5, 4, 8, 6, 2, 3, 1, 7]


