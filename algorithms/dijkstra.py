import csv

# Change the link to the input below to the file that you want to test and run the code. The result should appear in the console in a readable format
input = 'input.csv'

####################################################

def dijkstra(link_to_csv):
    """
    The function that implements Dijkstra's algorithm
    :param link_to_csv: the link to the csv file containing the input for the algorithm
    :return: the distance array and the array of the predecessors
    """
    # Parse the input from the csv file
    inputs = parse_input(link_to_csv)

    # Create all the variables that we will need for the algorithm
    visited = set([])
    unmarked_nodes = set([])
    number_of_nodes = 0

    # Preprocessing: fill out the unmarked nodes and calculate the number of nodes
    for arc in inputs:
        if not(arc[0] in unmarked_nodes):
            unmarked_nodes.add(arc[0])
            number_of_nodes += 1
        if not(arc[1] in unmarked_nodes):
            unmarked_nodes.add(arc[1])
            number_of_nodes += 1

    dist = [float('inf') for i in range(number_of_nodes)]
    dist[0] = 0
    predecessor = [0 for i in range(number_of_nodes)]

    # While we have some nodes to mark we do
    while (len(unmarked_nodes) > 0):

        # We find the node that is unmarked that has the minimum current distance
        current_node = find_minimum_distance(dist, unmarked_nodes)

        # We remove the node from the unmarked nodes
        if current_node == -1:
            current_node = unmarked_nodes.pop()
        else:
            unmarked_nodes.remove(current_node)

        # We add this node to visited
        visited.add(current_node)

        # We iterate the arcs in the input to find the arcs that start from the current node
        for i in range(len(inputs)):
            if inputs[i][0] == current_node:
                # The next 3 lines are there to make the code easier to read: the next node is the index 1 of the
                # current arc and the cost is the index 2
                current_arc = inputs[i]
                next_node = current_arc[1]
                cost = current_arc[2]
                # We calculate the current distance
                current_distance = dist[current_node - 1] + cost

                # We update the predecessors' list and the distance if the distance calculated with  is less
                # than the distance
                if current_distance < dist[next_node - 1]:
                    predecessor[next_node - 1] = current_node
                    dist[next_node - 1] = current_distance

    # The algorithm is finished so we return both the distance list and the predecessor list
    return dist, predecessor


def find_minimum_distance(dist, unmarked_nodes):
    """
    This function helps to find the node with the minimum current distance among the ones that have not been explored and removes this nodes from the unmarked_list
    :param dist: the list of distances
    :param unmarked_nodes: the set of unmarked nodes
    :return: the node with the minimum distance if there is one, -1 if there is none (that happens when all the node left to mark have a distance of +infinity
    """
    # Initialize parameters
    current_min = float('inf')
    current_ind = -1
    number_of_nodes = len(dist)

    # Iterate through all the nodes
    for i in range(number_of_nodes):
        # We only consider the node with the minimum distance
        if dist[i] < current_min and i + 1 in unmarked_nodes:
            current_min = dist[i]
            current_ind = i + 1
    return current_ind


def parse_input(input_to_parse):
    """
    :param input_to_parse: the string of the path of the file that contains the inputs
    :return: the list that represents the parsed input list
    """
    with open(input_to_parse, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        cnt = 0
        lst = []
        for row in spamreader:
            cnt += 1
            if cnt > 1:
                current_row = row[0].split(',')
                for i in range(len(current_row)):
                    current_row[i] = int(current_row[i])
                lst += [current_row]
    return lst


def print_prettier_output(result):
    """
    This function is only there to make the output of the algorithm more readable in the console
    :param result: The result from the deque implementation
    :return: nothing, but prints out the result in a prettier format that is more readable
    """

    # print the distances between the nodes
    print("The distances are :")
    print("Nodes:      ", end='')
    print(" | ", end='')
    for i in range(1, len(result[0]) + 1):
        print(i, end='')
        print(" | ", end='')
    print()

    print("Distances:  ", end='')
    for x in result[0]:
        if x >= 0:
            print(" | ", end='')
        else:
            print(" |", end='')
        print(x, end='')
    print(" |", end='')
    print()
    print()

    # print the predecessors of the nodes
    print("The predecessors of the nodes are:")
    print("Nodes:      ", end='')
    print(" | ", end='')
    for i in range(1, len(result[1]) + 1):
        print(i, end='')
        print(" | ", end='')
    print()

    print("Predecessors", end='')
    for x in result[1]:
        if x >= 0:
            print(" | ", end='')
        else:
            print(" |", end='')
        print(x, end='')
    print(" |", end='')
    print()
    return


res = dijkstra(input)

print_prettier_output(res)
