try:
    from pathfinding.core.grid import Grid
    from pathfinding.finder.a_star import AStarFinder
    library = True
except ImportError:
    library = False

import random
import settings


def drunken_walk():
    """"Very simple implementation of the random walk algorithm"""
    _ = False
    level_width = settings.LEVEL_SIZE
    level_height = settings.LEVEL_SIZE

    tiles_to_be_removed = level_height * level_width // 4

    drunk = {
        'remove_blocks': tiles_to_be_removed,
        'padding': 1,
        'x': int(level_width / 2),
        'y': int(level_height / 2)
    }

    start_coordinate = [drunk['x'], drunk['y']]

    level = [[1] * level_width for _ in range(level_height)]

    x = -1
    y = -1

    while drunk['remove_blocks'] >= 0:
        x = drunk['x']
        y = drunk['y']

        if level[y][x] == 1:
            level[y][x] = _
            drunk['remove_blocks'] -= 1

        roll = random.randint(1, 4)

        if roll == 1 and x > drunk['padding']:
            drunk['x'] -= 1
        if roll == 2 and x < level_width - 1 - drunk['padding']:
            drunk['x'] += 1
        if roll == 3 and y > drunk['padding']:
            drunk['y'] -= 1
        if roll == 4 and y < level_height - 1 - drunk['padding']:
            drunk['y'] += 1

    end_coordinate = [x, y]

    return [level, start_coordinate, end_coordinate]


def get_path(start, goal, random_map):
    """"A star algorithm from library"""
    grid = Grid(matrix=random_map, inverse=True)
    finder = AStarFinder()
    path, runs = finder.find_path(grid.node(start[0], start[1]), grid.node(goal[0], goal[1]), grid)
    return path


def evaluate_levels(levels):
    """"Function that evaluates the level created and returns the len of the path
    and the level. The path needs to be the longest gor the level to be selected as playable """
    evaluation_scores = []

    for generated_level, start_coordinate, end_coordinate in levels:
        shortest_solution = get_path(
            start_coordinate,
            end_coordinate,
            generated_level
        )

        evaluation_scores.append(
            [len(shortest_solution), generated_level]
        )

    return evaluation_scores


def generate_best_level(number_of_levels):
    """"Here we are choosing the best level with the longest path to play if there is the pathfinding
    library else we return the first generated level"""
    if library:
        levels = [drunken_walk() for _ in range(number_of_levels)]

        evaluation_scores = evaluate_levels(levels)

        evaluation_scores.sort()
        evaluation_scores.reverse()

        score, best_level = evaluation_scores.pop(0)

        return best_level
    else:
        return drunken_walk()[0]
