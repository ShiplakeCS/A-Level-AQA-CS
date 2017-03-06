"""
Python implementation of Dijkstra's shortest path algorithm.
AWD 2017

This implementation of Dijkstra's shortest path uses graphs represented as an adjacency matrix in accordance with
the AQA A Level Computer Science specification.
"""

# Adjacency matrix representation of the graph to perform the shortest path algorithm upon

graph = [[0,4,3,7,None,None,None],
         [4,0,None,1,None,5,None],
         [3,None,0,3,5,None,None],
         [7,1,3,0,2,2,7],
         [None,None,5,2,0,None,2],
         [None,5,None,2,None,0,5],
         [None,None,None,7,2,5,0]]


"""
# Another graph to test the algorithm with

graph = [[0,2,5,None,None,None,None],
         [2,0,4,None,None,7,None],
         [5,4,0,6,None,None,None],
         [None,None,6,0,3,4,None],
         [None,None,None,3,0,None,4],
         [None,7,None,4,None,0,2],
         [None,None,None,None,4,2,0]]
"""

# Create a list to store the distance from the start node for each vertex in the graph
distances_from_start = [None] * len(graph) # Used list multiplication to populate with the right number of 'None' values

# Create a list of visited vertexes so that we know which we can ignore when looking for shorter paths from the start
visited_vertexes = []


def print_adj_matrix():
    """ Prints the Adjacency Matrix representation of the global graph matrix in a nicely formatted way."""

    global graph

    print("\nAdjacency Matrix of Graph:\n")

    # Generate column headings
    headingString = "  "
    for colNum in range(len(graph)):
        headingString += "|{:^8}".format(chr(65 + colNum))
    print(headingString)
    print("-" * len(headingString))

    # Print each row
    for rowNum in range(len(graph)):
        rowString = "{0} ".format(chr(65 + rowNum))
        for colValue in graph[rowNum]:
            rowString += '|{:^8}'.format(str(colValue))
        print(rowString)

    print("-" * len(headingString))


def shortest_path():
    """
    Performs the shortest path algorithm and returns a list of vertexes in order with their distances from the start.
    """
    global graph, distances_from_start, visited_vertexes

    current_vertex = 0  # We start at the first vertex in the graph

    # Add [0, 0] to distances_from_start[] to represent that the distance from the start of the first vertex is 0, via
    # the first vertex
    distances_from_start[current_vertex] = [0, 0]  # [distance from start, via vertex]

    for rowNum in range(len(graph)):  # Iterate through each row in the matrix

        current_vertex = rowNum  # With each iteration, we are focused on a particular vertex

        # print("Current vertex: ", current_vertex)  # show which vertex we are currently investigating

        # Iterate through each column in the current row in the adjacency matrix
        for colNum in range(len(graph[current_vertex])):

            # If there is no distance for the current vertex in distances_from_start then copy it from the graph,
            # adding the distance it takes to get from the start to the current vertex
            if graph[current_vertex][colNum] is not None and distances_from_start[colNum] is None:
                distances_from_start[colNum] = [distances_from_start[current_vertex][0] + graph[current_vertex][colNum], current_vertex]

            # If there is a weight between the current vertex and node represented by the column that we are looking at,
            # test to see if its weight added to the distance of the current vertex is less than the distance from the
            # start that is presently recorded for that vertex in the distances_from_start array
            elif graph[current_vertex][colNum] is not None and (graph[current_vertex][colNum] + distances_from_start[current_vertex][0]) < distances_from_start[colNum][0]:
                distances_from_start[colNum] = [(graph[current_vertex][colNum] + distances_from_start[current_vertex][0]), current_vertex]

        # print("Distances from start: ", distances_from_start)  # show updated distances_from_start array

        # Add current_vertex to visited list so that its distance from the start is calculated again in future
        if current_vertex not in visited_vertexes:
            visited_vertexes.append(current_vertex)

        # print("Visited vertexes: ", visited_vertexes)

    # Print the shortest path in a friendly format
    print("Shortest path:")
    current_vertex = len(graph) - 1  # Start at the end, with the final vertex
    path_string = ""  # Start with a blank output string
    while current_vertex > 0:  # Keep looping until we have worked back to the start vertex
        # Use chr(65 + current_vertex) to represent the vertex as a letter from A, B, C, etc instead of 0, 1 2 -
        # recall that chr(65) = 'A'.
        #
        # Add the distance for the current vertex from the start in brackets after the letter of the vertex.
        path_string = "{0}({1}) ".format(chr(current_vertex + 65), distances_from_start[current_vertex][0]) + path_string

        # Update the current vertex to be the one that the current one goes via on its way back to the start
        current_vertex = distances_from_start[current_vertex][1]  # distances_from_start[vertex number, via vertex]

    # Add the start vertex to the output string as the while loop will stop before we add its details to the string
    path_string = "{0}({1}) ".format(chr(current_vertex + 65), distances_from_start[current_vertex][0]) + path_string

    print(path_string)



print_adj_matrix()
shortest_path()