import arcade, math


class CustomList(list):
    def __setitem__(self, index, item):
        super().__setitem__(int(index), int(item))
    #def __getattribute__(self, __name):
    #    if type(__name) == float:
    #        __name = int(__name)
    #    return super().__getattribute__(__name)
    def __getitem__(self, __name):
        return super().__getitem__(int(__name))
    #def __setattr__(self, __name: str, __value) -> None:
    #    return super().__setattr__(int(__name), int(__value))

class LivingMap(object):
    def __init__(self, x_length:int, y_length:int,  size:int, *args, tilesize:int=50):
        self.x_length = x_length
        self.size = size
        self.tilesize = tilesize

        self.graph = CustomList()#[[0 for tile in range(y_length)] for tiles in range(x_length)]
        for tiles in range(x_length):
            self.graph.append(CustomList())
            for tile in range(y_length):
                self.graph[tiles].append(0)
        count = 1
        for barrierlist in args:
            for barrier in barrierlist:
                x = int(barrier.center_x/tilesize)
                y = int(barrier.center_y/tilesize)
                self.graph[x][y] = count
            count += 1



    def change(self, x:int, y:int, barrier:bool):
        x = int(x/50)
        y = int(y/50)

        if barrier:
            self.graph[x][y] = 1
        else:
            self.graph[x][y] = 0
    def __getitem__(self, i):
        return self.graph[i]
    def __setitem__(self, x, y, val):
        self.graph[x][y] = val
    def __len__(self):
        return self.x_length


def heuristic(start:tuple, goal:tuple):
        """

        Args:
            start:
            goal:

        Returns:

        """
        # Use Chebyshev distance heuristic if we can move one square either
        # adjacent or diagonal
        d = 1
        d2 = 1
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return d * (dx + dy) + (d2 - 2 * d) * min(dx, dy)

def move_cost(a:int, b:int):

    if a[0] == b[0] or a[1] == b[1]:
        return 1*5
    else:
        return 1.42*5
def get_dist(pos, pos2):
    return math.sqrt((pos[0]-pos2[0])**2+(pos[1]- pos2[1])**2)


def AStarSearch(Map:LivingMap, start:tuple, end:tuple, allow_diagonal_movement:bool=True, movelist=[], min_dist=0):
    tilesize = Map.tilesize
    start = (int(start[0]/tilesize), int(start[1]/tilesize))
    end = (int(end[0]/tilesize), int(end[1]/tilesize))

    G = {}  # Actual movement cost to each position from the start position
    F = {}  # Estimated movement cost of start to end going via this position

    graph = Map.graph
    max_iterations = len(graph[0]) * len(graph)

    # Initialize starting values
    G[start] = 0
    F[start] = heuristic(start, end)

    closed_vertices = set()
    open_vertices = set([start])
    came_from = {}

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    count = 0
    while len(open_vertices) > 0:
        count += 1
        if count > max_iterations:
            break

        # Get the vertex in the open list with the lowest F score
        current = None
        current_fscore = None
        for pos in open_vertices:
            if current is None or F[pos] < current_fscore:
                current_fscore = F[pos]
                current = pos

        # Check if we have reached the goal
        dist = get_dist(current, end)*50
        if dist <= min_dist:
            # Retrace our route backward
            path = [[current[0]*tilesize, current[1]*tilesize]]
            while current in came_from:
                current = came_from[current]
                path.append([current[0]*tilesize, current[1]*tilesize])
            path.reverse()

            return path  # Done!

        # Mark the current vertex as closed
        open_vertices.remove(current)
        closed_vertices.add(current)

        neighbours = []
        for new_position in adjacent_squares: # Adjacent squares
            neighbours.append((current[0] + new_position[0], current[1] + new_position[1]))

        # Update scores for vertices near the current position
        for neighbour in neighbours:
            if neighbour in closed_vertices:
                continue  # We have already processed this node exhaustively
            elif neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= 100 or neighbour[1] >= 100:
                continue

            if not graph[neighbour[0]][neighbour[1]] in movelist:
                continue


            candidate_g = G[current] + move_cost(current, neighbour)

            if not neighbour in open_vertices:
                open_vertices.add(neighbour)  # Discovered a new vertex
            elif candidate_g >= G[neighbour]:
                continue  # This G score is worse than previously found

            # Adopt this G score
            came_from[neighbour] = current
            G[neighbour] = candidate_g
            h = heuristic(neighbour, end)
            F[neighbour] = G[neighbour] + h

    # Out-of-bounds
    return []



def SearchTilesAround(Map:LivingMap, start:tuple, allow_diagonal_movement:bool=True, movelist=[]):
    tilesize = Map.tilesize
    start = (int(start[0]/tilesize), int(start[1]/tilesize))

    graph = Map.graph

    closed_vertices = set()
    open_vertices = set([start])

    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    count = 0
    while len(open_vertices) > 0:
        count += 1
        if count > 100:
            break

        #get first element in the set
        for current in open_vertices:
            break
        open_vertices.remove(current)
        closed_vertices.add(current)

        neighbours = []
        for new_position in adjacent_squares: # Adjacent squares
            neighbours.append((current[0] + new_position[0], current[1] + new_position[1]))

        # Update scores for vertices near the current position
        for neighbour in neighbours:
            if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= 100 or neighbour[1] >= 100:
                continue

            if not graph[neighbour[0]][neighbour[1]] in movelist:
                continue
            if neighbour in closed_vertices:
                continue

            if not neighbour in open_vertices:
                open_vertices.add(neighbour)  


    # Out-of-bounds
    return count
