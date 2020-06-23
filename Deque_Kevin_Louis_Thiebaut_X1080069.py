import csv

# This is the Deque implementation of the shortest path algorithm below is the commented code

# Change the link to the input below to the file that you want to test and run the code. The result should appear in the console in a readable format
input = 'input.csv'

####################################################

def deque_implementation(link_to_csv):
    """
    The function that implements Dijkstra's algorithm.
    Please note that it only works if the input graph has its vertices numbered from 1 to n if the number of node is n.
    :param link_to_csv: the link to the csv file containing the input for the algorithm
    :return: the distance array and the array of the predecessors
    """

    # Parse the input from the csv file into an input that is usable by the python algorithm
    inputs = parse_input(link_to_csv)
    print(inputs)

    # Create all the variables that we will need for the algorithm
    unmarked_nodes = set([])
    number_of_nodes = 0

    # Pre-processing: fill out the unmarked nodes and calculate the number
    # of nodes in the graph from the forward star representation
    for arc in inputs:
        if not(arc[0] in unmarked_nodes):
            unmarked_nodes.add(arc[0])
            number_of_nodes += 1
        if not(arc[1] in unmarked_nodes):
            unmarked_nodes.add(arc[1])
            number_of_nodes += 1

    # Initialize the parameters
    dist = [float('inf') for i in range(number_of_nodes)]
    dist[0] = 0
    predecessor = [0 for i in range(number_of_nodes)]

    # We set the array to be full of -2 to signify that it is empty and that no node has been visited yet
    s = [-2 for i in range(number_of_nodes)]
    s[0] = 'flag'

    # Initialize the deque
    queue = [1]
    while len(queue) > 0:
        current_node = queue.pop(0)
        s[current_node - 1] = -1
        for i in range(len(inputs)):
            if inputs[i][0] == current_node:
                # The next 3 lines are there to make the code easier to read: the next node is the index 1 of the
                # current arc and the cost is the index 2
                current_arc = inputs[i]
                next_node = current_arc[1]
                cost = current_arc[2]

                # Update the queue according to the content of s at next node
                # (we get the next_node - 1 index because it is 0 indexed)
                if s[next_node - 1] != -1:
                    queue.append(next_node)
                elif cost < 0:
                    queue.insert(0, next_node)
                    s[next_node - 1] = find_flag(s);

                # We calculate the current distance
                current_distance = dist[current_node - 1] + cost

                # We update the predecessors' list and the distance if the distance calculated with  is less
                # than the distance
                if current_distance < dist[next_node - 1]:
                    predecessor[next_node - 1] = current_node
                    dist[next_node - 1] = current_distance

    # The algorithm is finished so we return both the distance list and the predecessor list
    return dist, predecessor


def find_flag(s):
    """
    :param s: The list s defined in the deque implementation
    :return: the index of the flag in the list
    """
    for i in range(len(s)):
        if s[i] == 'flag':
            return i
    return -1


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


# We store the result of the algorithm in the res variable
res = deque_implementation(input)

# We print out the result in the console in a pretty format
print_prettier_output(res)
