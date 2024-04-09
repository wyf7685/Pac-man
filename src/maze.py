import itertools
from collections import deque
from copy import deepcopy
from typing import List, Optional, Tuple

from src.const import Position, Region

WALL = 0
PASS = 1
PASSED = 2


class Pos(object):
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Pos({self.x},{self.y})"

    def __eq__(self, pos: "Pos") -> bool:
        return self.x == pos.x and self.y == pos.y

    def copy(self) -> "Pos":
        return Pos(self.x, self.y)

    def offset(self, offset: Tuple[int, int]) -> "Pos":
        ox, oy = offset
        return Pos(self.x + ox, self.y + oy)


type Maze = List[List[int]]
type MazePath = List[Pos]


def generate_maze(walls: List[Region]) -> Maze:
    maze = [[PASS for _ in range(21)] for _ in range(21)]

    for x1, y1, x2, y2 in walls:
        for i, j in itertools.product(
            range(min(x1, x2), max(x1, x2) + 1),
            range(min(y1, y2), max(y1, y2) + 1),
        ):
            maze[i][j] = WALL

    return maze


def get_path(maze: Maze, start_pos: Position, end_pos: Position):
    # sourcery skip: avoid-builtin-shadow
    # Deep copy the maze array to avoid subsequent impact
    maze = deepcopy(maze)
    # Convert the starting point/ending point to Pos for easier manipulation.
    start = Pos(*[i // 30 for i in start_pos])
    end = Pos(*[i // 30 for i in end_pos])

    que: deque[Pos] = deque()
    path: List[List[Optional[Pos]]] = [[None for _ in line] for line in maze]
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
            if next == end:
                path[next.x][next.y] = cur.copy()
                flag = True
                break
            elif maze[next.x][next.y] == PASS:
                que.append(next)
                path[next.x][next.y] = cur.copy()
                maze[next.x][next.y] = PASSED
        que.popleft()

    cur = next
    result = [cur]
    prev = path[cur.x][cur.y]
    while prev is not None:
        result.append(cur := prev)
        prev = path[cur.x][cur.y]

    return result[::-1]
