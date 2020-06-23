import csv
import copy

# This is the implementation of the successive shortest paths algorithm below the commented code
# Please Note that the implementation only works for a network with only one source node and one target node


# Change the link to the input below to the file that you want to test and
# run the codse. The result should appear in the console in a readable format
input = 'input.csv'

####################################################



def successsive_shortest_paths(link_to_csv):
    """
    The implementation of the successive shortest path algorithm for the minimum cost flow problem
    :param link_to_csv: The link to the csv file containing the data
    :return:
    """
    # Parse the input from the csv file into an input that is usable by the python algorithm
    inputs, flows = parse_input(link_to_csv)

    # Calculate the number of nodes
    arcs, number_of_nodes = get_number_of_nodes(inputs)

    # Make the flow array better and calculate the flow to attain denoted K
    K = 0
    for i in range(number_of_nodes):
        flows[i] = int(flows[i])
        K = max(K, flows[i])
    flows = flows[:number_of_nodes]

    # Get the source node and the target node
    source = -1
    target = -1
    for i, e in enumerate(flows):
        if e > 0:
            source = i + 1
        if e < 0:
            target = i + 1

    # Initialize the cost array to make it easier to access
    costs = [[0 for _ in range(number_of_nodes)] for _ in range(number_of_nodes)]
    for arc in arcs:
        start = arc[0]
        end = arc[1]
        costs[start - 1][end - 1] = arc[2]
        costs[end - 1][start - 1] = -arc[2]

    # Initialize the node potentials
    potentials = [0 for _ in range(number_of_nodes)]

    # Create the residual network
    res_arcs = copy.deepcopy(arcs)

    # Initialize the cost, the flow and the distances in the original network
    flow = 0
    cost = 0

    while flow < K:

        # Calculate the distances from the source node
        distances, predecessors = deque_implementation(res_arcs, number_of_nodes, source)
        if distances[target - 1] == float('inf'):
            break

        # Update Node Potentials
        potentials = update_node_potentials(distances, potentials)

        # Update reduced costs
        res_arcs = update_reduced_cost(costs, res_arcs, potentials)

        # Send flow along the shortest path
        max_flow, shortest_path, path_cost = get_maximum_possible_flow(arcs, res_arcs, predecessors, source)
        flow += max_flow
        cost += path_cost * max_flow

        # Update the residual network
        res_arcs = update_residual_network(res_arcs, shortest_path, max_flow)

    return res_arcs, cost


def update_node_potentials(distances, potentials):
    """
    Updates the node potentials
    :param distances: Distances calculated from the deque implementation shortest path algorithm
    :param potentials: The current Node Potentials
    :return: The updated Node potentials
    """
    for i in range(len(potentials)):
        potentials[i] -= distances[i]
    return potentials


def update_reduced_cost(costs, res_arcs, potentials):
    """
    Updates the reduced costs in the network
    :param costs:
    :param res_arcs:
    :param potentials:
    :return: The updated residual network
    """
    # Get the arcs to update
    for i, current_arc in enumerate(res_arcs):
        start = current_arc[0]
        end = current_arc[1]
        current_arc[2] = costs[start - 1][end - 1] - potentials[start - 1] + potentials[end - 1]
    return res_arcs


def get_maximum_possible_flow(arcs, res_arcs, predecessors, source):
    """
    Gets the maximum possible flow on the shortest path from start node to the target node
    :param res_arcs:
    :param predecessors:
    :param source:
    :return:
    """
    current = len(predecessors)
    shortest_path = []
    while current != source:
        shortest_path.append([predecessors[current - 1], current])
        current = predecessors[current - 1]
    shortest_path.reverse()

    # Get the maximum possible flow by iterating over the arcs of the residual network and the cost of this shortest path
    max_flow = float('inf')
    cost = 0
    for pair in shortest_path:
        arc = search_arc(res_arcs, pair)
        max_flow = min(max_flow, arc[3])
        cost += search_arc(arcs, pair)[2]

    return max_flow, shortest_path, cost


def update_residual_network(res_arcs, shortest_path, flow):
    """
    Updates the residual network
    :param res_arcs:
    :param shortest_path:
    :param flow:
    :return:
    """
    for pair in shortest_path:
        current_arc = search_arc(res_arcs, pair)
        flow_left = current_arc[3] - flow
        current_arc[3] = flow_left
        reverse_arc = search_arc(res_arcs, [pair[1], pair[0]])
        if reverse_arc:
            reverse_arc[3] += flow
        else:
            start = current_arc[1]
            end = current_arc[0]
            cost = -current_arc[2]
            capacity = flow
            flow = flow
            res_arcs.append([start, end, cost, capacity])
        if flow_left <= 0:
            res_arcs.remove(current_arc)
    res_arcs.sort(key=lambda arc: arc[0])
    return res_arcs


def search_arc(res_arcs, pair):
    """
    Search for a specific arc in the network
    :param res_arcs:
    :param pair:
    :return:
    """
    for current_arc in res_arcs:
        if pair[0] == current_arc[0] and pair[1] == current_arc[1]:
            return current_arc
    return []


def deque_implementation(arcs, number_of_nodes, source):
    """
    The function that implements Dijkstra's algorithm.
    Please note that it only works if the input graph has its vertices numbered from 1 to n if the number of node is n.
    :param arcs: the residual network of which we want the shortest paths from source node
    :param number_of_nodes: the number of nodes in the network
    :param source: The source node of the network
    :return: the distance array and the array of the predecessors
    """

    # # Parse the input from the csv file into an input that is usable by the python algorithm
    # inputs = parse_input(link_to_csv)
    # print(inputs)

    # Initialize the parameters
    dist = [float('inf') for i in range(number_of_nodes)]
    dist[source - 1] = 0
    predecessor = [0 for i in range(number_of_nodes)]

    # We set the array to be full of -2 to signify that it is empty and that no node has been visited yet
    s = [-2 for i in range(number_of_nodes)]
    s[source - 1] = 'flag'

    # Initialize the deque
    queue = [source]
    while len(queue) > 0:
        current_node = queue.pop(0)
        s[current_node - 1] = -1

        for i in range(len(arcs)):
            if arcs[i][0] == current_node:
                # The next 3 lines are there to make the code easier to read: the next node is the index 1 of the
                # current arc and the cost is the index 2
                current_arc = arcs[i]
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
        flow = []
        for row in spamreader:
            cnt += 1
            if cnt > 1:
                current_row = row[0].split(',')
                for i in range(len(current_row) - 1):
                    current_row[i] = int(current_row[i])
                lst += [current_row[:4]]
                flow += [current_row[4]]
    return lst, flow


def get_number_of_nodes(arcs):
    """
    Gets the number of nodes and sorts the arcs in increasing order of start point
    :param arcs:
    :return:
    """
    arcs.sort(key=lambda arc: arc[0])

    # Create all the variables that we will need for the algorithm
    unmarked_nodes = set([])
    number_of_nodes = 0

    # Pre-processing: fill out the unmarked nodes and calculate the number
    # of nodes in the graph from the forward star representation
    for arc in arcs:
        if not (arc[0] in unmarked_nodes):
            unmarked_nodes.add(arc[0])
            number_of_nodes += 1
        if not (arc[1] in unmarked_nodes):
            unmarked_nodes.add(arc[1])
            number_of_nodes += 1

    return arcs, number_of_nodes


def print_prettier_output(result):
    """
    This function is here to make the results easier to read
    :param result:
    :return:
    """
    print()
    print("The forward star representation of the residual network is:")
    print()
    print("|  Start Node  |", "  End Node   |", "Reduced Cost |", "  Capacity   |")
    print("_____________________________________________________________")
    for i, arc in enumerate(result[0]):
        print("|      ", arc[0], "     |      ", arc[1], "     |      ", arc[2],"     |      ", arc[3], "     |")

    print("_____________________________________________________________")
    print()
    print()
    print("The minimum cost is:", result[1])



result = successsive_shortest_paths("input.csv")
print_prettier_output(result)