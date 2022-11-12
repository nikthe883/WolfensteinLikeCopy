from collections import deque


class PathFindingBFS:
    """
    Class PathfindingBFS

    """
    def __init__(self, game):
        """
        Init method of the class.

        :param game: game instance
        :type game: object
        """

        self.game = game
        self.map = game.map.mini_map
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.graph = {}
        self.get_graph()

    def get_path(self, start, goal):
        """
        Function for getting the path

        :param start: Start positions
        :type start: int
        :param goal: End of the path
        :type goal: tuple
        :return: last position of the path
        :rtype: tuple
        """

        self.visited = self.bfs(start, goal, self.graph)
        path = [goal]
        step = self.visited.get(goal, start)

        while step and step != start:
            path.append(step)
            step = self.visited[step]
        return path[-1]

    def bfs(self, start, goal, graph):
        """
        Function for BFS algorithm

        More info in the docs under section Explanation

        :param start: Starting position
        :type start: int
        :param goal: Ending position
        :type goal: tuple
        :param graph: The graph dict
        :type graph: dict
        :return: visited dict
        :rtype: dict
        """

        queue = deque([start])
        visited = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break
            next_nodes = graph[cur_node]

            for next_node in next_nodes:
                if next_node not in visited and next_node not in self.game.object_handler.npc_positions:
                    queue.append(next_node)
                    visited[next_node] = cur_node
        return visited

    def get_next_nodes(self, x, y):
        """Function for defining the next positions

            :return: list of the next positions
            :rtype: list
        """

        return [(x + dx, y + dy) for dx, dy in self.ways if (x + dx, y + dy) not in self.game.map.world_map]

    def get_graph(self):
        """
        Function for creating the graph for the BFS.

        It is a dictionary and we are giving the position plus the next positions

        :return: None
        :rtype: None
        """

        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)

