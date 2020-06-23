import csv


# input = "input_Dijkstra.csv"
input = "input.csv"


M = 10000
def preflow_push(link_to_csv):
    # helper functions for the algorithm
    def  find_overflow_vertex(excess, n):
        for i in range(1, n - 1):
            if excess[i] > 0:
                return i
        return -1

    # push operation
    def push(u, v):
        if not height[u] > height[v]:
            return False
        i = find_arc(forwardStar, u, v)
        if i < 0:
            i = find_arc(forwardStar, v, u)
        # print(i)
        # print(u)
        # print(v)
        # print()
        if i >= 0:
            send = min(excess[u], forwardStar[i][2] - F[u][v])
            if send == 0:
                return False
            F[u][v] += send
            F[v][u] -= send
            excess[u] -= send
            excess[v] += send
            return True
        return False

    # relabel operation
    def relabel(u):
        min_height = float('inf')
        for v in range(n):
            i = find_arc(forwardStar, u, v)
            if i >= 0:
                if forwardStar[i][2] - F[u][v] > 0:
                    min_height = min(min_height, height[v])
                    height[u] = min_height + 1

        return

    def sortKey(i):
        return height[i]

    forwardStar = parse_input(link_to_csv)
    unmarked_nodes = set([])
    n = 0
    # Pre-processing: fill out the unmarked nodes and calculate the number
    # of nodes in the graph from the forward star representation
    for arc in forwardStar:
        if not (arc[0] in unmarked_nodes):
            unmarked_nodes.add(arc[0])
            n += 1
        if not (arc[1] in unmarked_nodes):
            unmarked_nodes.add(arc[1])
            n += 1

    # Construct a "backward" star representation to perform a BFS later
    backwardStar = []
    for arc in forwardStar:
        backwardStar += [[arc[1], arc[0], 0]]

    F = [[0] * n for _ in range(n)]
    height = [0] * n
    excess = [0] * n

    # Pre-processing of the algorithm
    excess[0] = M

    height = BFS(backwardStar, n, height)
    height[0] = n

    for v in range(n):
        push(0, v)

    while find_overflow_vertex(excess, n) > 0:
        u = find_overflow_vertex(excess, n)

        pushed = False
        list_of_neighbors = [i for i in range(n)]
        list_of_neighbors.sort(key=sortKey)

        for v in list_of_neighbors:
            pushed = push(u, v)
            if pushed:
                break
        if not pushed:
            relabel(u)

    return excess[n - 1]



def find_min_height(height, u, forwardStar):
    index = -1
    min = float('inf')
    for i in range(len(height)):
        current = height[i]
        if current < min and find_arc(forwardStar, u, i) >= 0:
            min = current
            index = i
    return index


def find_arc(forwardStar, u, v):
    current_arc_index = -1
    for i in range(len(forwardStar)):
        arc = forwardStar[i]
        if arc[0] == u + 1 and arc[1] == v + 1:
            current_arc_index = i
            break
    return current_arc_index





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


def BFS(backwardStar, n, height):
    """
    Performs a Breadth First Search
    The parameters are : a forward star representation of a graph and a starting node
    """
    end_nodes = [backwardStar[i][1] for i in range(len(backwardStar))]
    q = [n - 1]
    result = []
    visited = [False for k in range(n)]
    visited[n - 1] = True
    current_height = 0
    while len(q) != 0:
        current = q.pop(0)
        current_height += 1
        result += [current + 1]
        for i in range(len(backwardStar)):
            if backwardStar[i][0] == current + 1:
                next = backwardStar[i][1]
                if not visited[next - 1]:
                    height[next - 1] = current_height
                    q.append(next - 1)
                    visited[next - 1] = True
    return height


# We store the result of the algorithm in the res variable
res = preflow_push(input)
print(res)