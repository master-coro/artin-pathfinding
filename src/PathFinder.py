from Classes.World import World

from collections import OrderedDict
import time

# Depth-first search
# starting from tile number start, find a path to tile number target
# return (reached, path) where reached is true if such a path exists, false otherwise
# and path contains the path if it exists  

def dfs(World, start, target, display):

    # Check accessibility of the begining and end of path
    start_check = World.is_accessible(start, "Start")
    target_check = World.is_accessible(target, "Target")
    if (not(start_check) or not(target_check)):
        print("Start or Target are not accessible TILES.")
        return(False, [])

    # Depth First Search Algorithm
    reached = False
    stack = []
    visited = []
    visited.append(start)
    current_tile = start

    # First iteration for stack not to be empty at first
    iterations = 0
    children = World.successors(current_tile)
    for elem in children:
        if elem not in visited:
            stack.append(elem)

    while (stack and not(reached)):
        if (iterations != 0):
            children = World.successors(current_tile)
            for elem in children:
                if elem not in visited:
                    stack.append(elem)

        current_tile = stack.pop()
        visited.append(current_tile)

        if display:
            World.display_path(visited)

        iterations += 1
        if target in visited:
            reached = True
            break

    return (reached, visited)

def bfs(World, start, target, display):
    # Check accessibility of the begining and end of path
    start_check = World.is_accessible(start, "Start")
    target_check = World.is_accessible(target, "Target")
    if (not(start_check) or not(target_check)):
        print("Start or Target are not accessible TILES.")
        return(False, [])

    # Depth First Search Algorithm
    reached = False
    queue = []
    visited = []
    visited.append(start)
    current_tile = start

    # First iteration for queue not to be empty at first
    iterations = 0
    children = World.successors(current_tile)
    for elem in children:
        if elem not in visited:
            queue.append(elem)

    while (queue and not(reached)):
        if (iterations != 0):
            children = World.successors(current_tile)
            for elem in children:
                if elem not in visited:
                    queue.append(elem)

        current_tile = queue.pop(0)
        visited.append(current_tile)

        if display:
            World.display_path(visited)

        iterations += 1
        if target in visited:
            reached = True
            break

    return (reached, visited)

def dijkstra(World, start, target, display):
    available_tiles = World.list_available_tiles()
    predecessors = []
    queue = []
    cost = dict()
    for elem in available_tiles:
        cost[elem] = 99999
    cost[start] = 0
    reached = False
    queue.append(start)

    while queue and not(reached):
        # Extract smallest cost from queue    
        sorted_cost = OrderedDict(sorted(cost.items(), key = lambda x: x[1]))
        for tile in queue:
            if tile in sorted_cost.keys():
                current_tile = tile
                queue.remove(tile)
        
        # Did we reach the end ?
        if current_tile == target:
            reached = True
            break
        else:
            children = World.successors(current_tile)
            for elem in children:
                if cost[elem] > cost[current_tile] + 1:
                    cost[elem] = cost[current_tile] + 1 
                    predecessors.append(current_tile)
                    queue.append(elem)

    if display:   
        World.display_path(predecessors)

    return(reached, predecessors)

def get_path(predecessor, start, target):
    path = [target]
    elem = target
    while predecessor[elem] is not start:
        elem = predecessor[elem]
        path.append(elem)
    return path


def heuristic(World, current, target):
    row_current = int(current / World.L)
    col_current = current % World.H
    row_target = int(target / World.L)
    col_target = target % World.H
    return(abs(row_current - row_target) + abs(col_current - col_target))

def a_star(World, start, target, display):
    available_tiles = World.list_available_tiles()

    reached = False
    open_list = [start]
    closed_list = []
    path = []

    predecessor = dict()
    f_score = dict()
    g_score = dict()
    h_score = dict()

    for elem in available_tiles:
        f_score[elem] = 0
        g_score[elem] = 0
        h_score[elem] = 0

    while (not(reached) and open_list):
        current_tile = open_list.pop()
        closed_list.append(current_tile)
        if target in closed_list:
            reached = True
            break
        children = World.successors(current_tile)
        for cell in children:
            if cell not in closed_list:
                if cell in open_list:
                    if g_score[cell] > g_score[current_tile] + 1:
                        g_score[cell] = g_score[current_tile] + 1
                        h_score[cell] = heuristic(World, current_tile, target)
                        predecessor[cell] = current_tile
                        f_score[cell] = g_score[cell] + h_score[cell]
                else:
                    g_score[cell] = g_score[current_tile] + 1
                    h_score[cell] = heuristic(World, current_tile, target)
                    predecessor[cell] = current_tile
                    f_score[cell] = g_score[cell] + h_score[cell]
                    open_list.append(cell)

    path = get_path(predecessor, start, target)

    return(reached, path)

def path_info(path_found, path, algorithm):
    if path_found:
        print("\nGoal reached.")
    else:
        print("No path found...")
    print("With " + algorithm + " length of the shortest path is " + str(len(path)) + "\n")

if __name__ == '__main__':
    # create a world
    w = World(20, 10, 0.2)
    display = False

    path_found, dijkstra = dijkstra(w, 21, 164, display)
    path_info(path_found, dijkstra, "DIJKSTRA")

    path_found, a_star = a_star(w, 21, 164, display)
    w.display_path(a_star)
    path_info(path_found, a_star, "A*")

    path_found, dfs = dfs(w, 21, 164, display)
    path_info(path_found, dfs, "DFS")

    path_found, bfs = bfs(w, 21, 164, display)
    path_info(path_found, bfs, "BFS")



    

