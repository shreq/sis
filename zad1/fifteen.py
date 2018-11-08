from copy import deepcopy
from collections import deque
import heapq


class Fifteen:
    heur = ''
    priority = ''
    tiles = []
    undo_move = ''  # used to avoid getting stuck in a back and forth loop
    h_score = None  # calculated using heuristic
    depth = 0       # amount of moves
    f_score = None  # h_score + depth
    previous_moves = []
    zero_x = 0
    zero_y = 0

    def __init__(self, fin, heur='hamm', parent=None):
        if parent is None:
            if heur == 'hamm' or heur == 'manh':                    # check if this parameter was used to pass heuristic or priority
                self.heur = heur
            else:
                self.priority = heur
            with open(fin, 'r', encoding='utf-8') as fi:
                next(fi)                                            # skip first line that contains size of puzzles as it is unnecessary
                self.tiles = [list(map(int, line.split())) for line in fi]
            self.zero_x, self.zero_y = self.find()
        elif parent is not None:                                    # if it's only a child just take parameters from parent
            self.heur = deepcopy(parent.heur)
            self.priority = deepcopy(parent.priority)
            self.tiles = deepcopy(parent.tiles)
            self.undo_move = deepcopy(parent.undo_move)
            self.depth = deepcopy(parent.depth) + 1
            self.previous_moves = deepcopy(parent.previous_moves)
            self.zero_x = deepcopy(parent.zero_x)
            self.zero_y = deepcopy(parent.zero_y)

    def __eq__(self, other):                    # functions needed for heapq
        return self.f_score == other.f_score

    def __ne__(self, other):
        return self.f_score != other.f_score

    def __lt__(self, other):
        return self.f_score < other.f_score

    def __gt__(self, other):
        return self.f_score > other.f_score

    def __le__(self, other):
        return self.f_score <= other.f_score

    def __ge__(self, other):
        return self.f_score >= other.f_score

    def __str__(self):
        return str(self.tiles)

    def __hash__(self):
        return hash(str(self))

    def tiles2str(self):
        s = ''
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                s += str(self.tiles[y][x]) + ' '
            s += '\n'
        return s

    def path2str(self):
        s = ''
        for step in self.previous_moves:
            s += str(step).upper()
        return s

    def find(self, tile=0):
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if self.tiles[y][x] == tile:
                    return x, y
        raise NameError

    def move_tile(self, direction):
        x, y = self.zero_x, self.zero_y
        if direction == 'u':
            self.tiles[y][x], self.tiles[y - 1][x] = self.tiles[y - 1][x], self.tiles[y][x]
            self.zero_y = self.zero_y - 1
            self.previous_moves.append('u')
            self.undo_move = 'd'
        elif direction == 'd':
            self.tiles[y][x], self.tiles[y + 1][x] = self.tiles[y + 1][x], self.tiles[y][x]
            self.zero_y = self.zero_y + 1
            self.previous_moves.append('d')
            self.undo_move = 'u'
        elif direction == 'l':
            self.tiles[y][x], self.tiles[y][x - 1] = self.tiles[y][x - 1], self.tiles[y][x]
            self.zero_x = self.zero_x - 1
            self.previous_moves.append('l')
            self.undo_move = 'r'
        elif direction == 'r':
            self.tiles[y][x], self.tiles[y][x + 1] = self.tiles[y][x + 1], self.tiles[y][x]
            self.zero_x = self.zero_x + 1
            self.previous_moves.append('r')
            self.undo_move = 'l'
        else:
            raise NameError

    def generate_next_states(self, priority=None):
        if priority is None:
            priority = 'UDLR'
        next_states = []
        x, y = self.zero_x, self.zero_y
        for direction in priority:
            direction = direction.upper()
            if direction == 'U' and y != 0 and self.undo_move != 'u':
                child = Fifteen(None, None, self)
                child.move_tile('u')
                next_states.append(child)
            elif direction == 'D' and y != len(self.tiles) - 1 and self.undo_move != 'd':
                child = Fifteen(None, None, self)
                child.move_tile('d')
                next_states.append(child)
            elif direction == 'L' and x != 0 and self.undo_move != 'l':
                child = Fifteen(None, None, self)
                child.move_tile('l')
                next_states.append(child)
            elif direction == 'R' and x != len(self.tiles[y]) - 1 and self.undo_move != 'r':
                child = Fifteen(None, None, self)
                child.move_tile('r')
                next_states.append(child)
        return next_states

    def heuristic(self):
        if self.heur == 'hamm':
            return self.hamming()
        return self.manhattan()

    def hamming(self):
        diff = 0
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if y == len(self.tiles) - 1 and x == len(self.tiles[y]) - 1:
                    if self.tiles[y][x] != 0:
                        diff += 1
                elif self.tiles[y][x] != y * len(self.tiles[y]) + x + 1:
                    diff += 1
        return diff

    def manhattan(self):
        score = 0
        tile = 1
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if tile == len(self.tiles) * len(self.tiles[y]):
                    continue
                x_real, y_real = self.find(tile)
                dx = abs(x - x_real)
                dy = abs(y - y_real)
                score += dx + dy
                tile += 1
        return score

    def astar(self):
        open_set = []
        closed_set = {}
        heapq.heappush(open_set, self)
        visited = 1
        processed = 0
        max_depth = 0

        while open_set:
            current_state = heapq.heappop(open_set)
            processed += 1
            if current_state.depth > max_depth:
                max_depth = current_state.depth
            closed_set[repr(current_state.tiles)] = current_state

            if current_state.heuristic() == 0:
                return len(current_state.previous_moves), visited, processed, max_depth, current_state.path2str(), current_state.tiles2str()

            for state in current_state.generate_next_states():
                if repr(state.tiles) in closed_set:
                    continue
                state.h_score = state.heuristic()
                state.f_score = state.h_score + state.depth
                heapq.heappush(open_set, state)
                visited += 1
        print(-1)
        return

    def bfs(self, priority):
        open_set = deque([self])
        visited = 1
        processed = 0
        max_depth = 0

        while open_set:
            current_state = open_set.popleft()
            processed += 1
            if current_state.depth > max_depth:
                max_depth = current_state.depth

            if current_state.hamming() == 0:
                return len(current_state.previous_moves), visited, processed, max_depth, current_state.path2str(), current_state.tiles2str()

            for state in current_state.generate_next_states(priority):
                open_set.append(state)
                visited += 1
        print(-1)
        return

    def dfs(self, priority):
        open_set = [self]  # stack
        visited = 1
        processed = 0
        max_depth = 0

        while open_set:
            current_state = open_set.pop()
            processed += 1
            if current_state.depth > max_depth:
                max_depth = current_state.depth

            if current_state.hamming() == 0:
                return len(current_state.previous_moves), visited, processed, max_depth, current_state.path2str(), current_state.tiles2str()

            if current_state.depth < 20:
                for state in current_state.generate_next_states(priority):
                    open_set.append(state)
                    visited += 1
        print(-1)
        return
