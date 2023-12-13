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
    maze = [[PASS for _ in range(21)] for _ in range(21)]
    for x1, y1, x2, y2 in walls:
        for i, j in itertools.product(
            range(min(x1, x2), max(x1, x2) + 1),
            range(min(y1, y2), max(y1, y2) + 1),
        ):
            maze[i][j] = WALL

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
