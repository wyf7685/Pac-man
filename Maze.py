import time
from copy import deepcopy
from collections import deque
from typing import List, Optional, Tuple

WALL = 0
PASS = 1
PASSED = 2


class Pos:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Pos({self.x},{self.y})"

    def copy(self) -> "Pos":
        return Pos(self.x, self.y)

    def offset(self, offset: Tuple[int, int]) -> "Pos":
        return Pos(self.x + offset[0], self.y + offset[1])


MazeType = List[List[int]]
PathType = List[Pos]


def generate_maze(walls: List[List[int]]) -> MazeType:
    large_maze = [[PASS for _ in range(101)] for _ in range(101)]

    # For each segment of the wall, convert it to large_maze with a ratio of pixels:coordinates = 6:1
    for pos in walls:
        x, y, dx, dy = [i // 6 for i in pos]
        for i in range(max(x - 2, 0), min(x + dx + 2, 101)):
            for j in range(max(y - 2, 0), min(y + dy + 2, 101)):
                large_maze[i][j] = WALL

    # Sampling from large_maze to maze
    maze = [[0 for _ in range(21)] for _ in range(21)]
    for i in range(20):
        for j in range(20):
            maze[i][j] = large_maze[i * 5 + 1][j * 5 + 1]

    return maze


def get_path(maze: MazeType, start_pos: Tuple[int, int], end_pos: Tuple[int, int]):
    # Deep copy the maze array to avoid subsequent impact
    maze = deepcopy(maze)
    # Convert the starting point/ending point to Pos for easier manipulation.
    start = Pos(*[i // 30 for i in start_pos])
    end = Pos(*[i // 30 for i in end_pos])

    # Create a queue to store coordinates (nodes) to be processed.
    que = deque()  # type: deque[Pos]
    # Create a two-dimensional array of the same size as the maze to store the previous step (predecessor node) for each coordinate.
    path = [[None for _ in line] for line in maze]  # type: List[List[Optional[Pos]]]
    # Coordinate offsets for each iteration.
    base_offset = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    # Flag indicating whether the destination has been found.
    flag = False

    # Handle the starting point.
    next = start.copy()
    que.append(next)
    maze[next.x][next.y] = PASSED

    while len(que) and not flag:
        # Current coordinate (node).
        cur = que[0]
        # Traverse in the four directions.
        for offset in base_offset:
            next = cur.offset(offset)
            # The next coordinate is passable.
            if maze[next.x][next.y] == PASS:
                # Enqueue and record the previous step (predecessor node).
                que.append(next)
                path[next.x][next.y] = cur.copy()
                # Arrive at the destination.
                if next.x == end.x and next.y == end.y:
                    flag = True
                    break
                #Mark as visited to avoid redundant visits.
                maze[next.x][next.y] = PASSED
            # Special case: Pac-Man's coordinates are on the wall (an unusual problem, but it does exist).
            elif maze[next.x][next.y] == WALL and next.x == end.x and next.y == end.y:
                path[next.x][next.y] = cur.copy()
                flag = True
                break
        # Pop the front of the queue, representing a processed coordinate (node).
        que.popleft()

    # Extract the final path from the path data structure.
    cur = next
    result = []  # type: List[Pos]
    result.insert(0, cur)
    prev = path[cur.x][cur.y]
    while prev is not None:
        cur = prev
        result.insert(0, cur)
        prev = path[cur.x][cur.y]

    return result
