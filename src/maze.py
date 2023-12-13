import itertools
from collections import deque
from copy import deepcopy
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


Maze = List[List[int]]
MazePath = List[Pos]


def generate_maze(walls: List[Tuple[int, int, int, int]]) -> Maze:
    large_maze = [[PASS for _ in range(101)] for _ in range(101)]

    # For each segment of the wall, convert it to large_maze with a ratio of pixels:coordinates = 6:1
    for pos in walls:
        x, y, w, h = [i // 6 for i in pos]
        for i, j in itertools.product(
            range(max(x - 2, 0), min(x + w + 2, 101)),
            range(max(y - 2, 0), min(y + h + 2, 101)),
        ):
            large_maze[i][j] = WALL

    # Sampling from large_maze to maze
    maze = [[0 for _ in range(21)] for _ in range(21)]
    for i, j in itertools.product(range(20), range(20)):
        maze[i][j] = large_maze[i * 5 + 1][j * 5 + 1]

    return maze


def get_path(maze: Maze, start_pos: Tuple[int, int], end_pos: Tuple[int, int]):
    # sourcery skip: avoid-builtin-shadow
    # Deep copy the maze array to avoid subsequent impact
    maze = deepcopy(maze)
    # Convert the starting point/ending point to Pos for easier manipulation.
    start = Pos(*[i // 30 for i in start_pos])
    end = Pos(*[i // 30 for i in end_pos])

    que = deque()  # type: deque[Pos]
    path = [[None for _ in line] for line in maze]  # type: List[List[Optional[Pos]]]
    # Coordinate offsets for each iteration.
    base_offset = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    flag = False

    next = start.copy()
    que.append(next)
    maze[next.x][next.y] = PASSED

    while len(que) and not flag:
        cur = que[0]
        for offset in base_offset:
            next = cur.offset(offset)
            if maze[next.x][next.y] == PASS:
                que.append(next)
                path[next.x][next.y] = cur.copy()
                if next.x == end.x and next.y == end.y:
                    flag = True
                    break
                maze[next.x][next.y] = PASSED
            elif maze[next.x][next.y] == WALL and next.x == end.x and next.y == end.y:
                path[next.x][next.y] = cur.copy()
                flag = True
                break
        que.popleft()

    cur = next
    result = []  # type: List[Pos]
    result.insert(0, cur)
    prev = path[cur.x][cur.y]
    while prev is not None:
        cur = prev
        result.insert(0, cur)
        prev = path[cur.x][cur.y]

    return result
