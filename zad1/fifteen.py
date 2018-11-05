from copy import deepcopy
from collections import deque
import heapq

class Fifteen:
    heur = ''
    tiles = []
    undo_move = ''  # used to avoid getting stuck in a back and forth loop
    h_score = None  # calculated using heuristic
    depth = 0       # amount of moves
    f_score = None  # h_score + depth
    previous_moves = []
    zero_x = 0
    zero_y = 0

    def __init__(self, fin, heur = 'hamm', parent=None):
        if parent is None:
            self.heur = heur
            with open(fin, 'r', encoding='utf-8') as fi:
                self.tiles = [list(map(int, line.split())) for line in fi]
            self.zero_x, self.zero_y = self.find()
        elif parent is not None:
            self.heur = deepcopy(parent.heur)
            self.tiles = deepcopy(parent.tiles)
            self.undo_move = deepcopy(parent.undo_move)
            self.depth = deepcopy(parent.depth) + 1
            self.previous_moves = deepcopy(parent.previous_moves)
            self.zero_x = deepcopy(parent.zero_x)
            self.zero_y = deepcopy(parent.zero_y)

    def __eq__(self, other):
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
        return str(self.board)

    def __hash__(self):
        return hash(str(self))

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

    def generate_next_states(self, priority = ['u', 'd', 'l', 'r']):
        next_states = []
        x, y = self.zero_x, self.zero_y
        for direction in priority:
            if direction == 'u' and y != 0 and self.undo_move != 'u':
                child = Fifteen(None, None, self)
                child.move_tile('u')
                next_states.append(child)
            if direction == 'd' and y != len(self.tiles) - 1 and self.undo_move != 'd':
                child = Fifteen(None, None, self)
                child.move_tile('d')
                next_states.append(child)
            if direction == 'l' and x != 0 and self.undo_move != 'l':
                child = Fifteen(None, None, self)
                child.move_tile('l')
                next_states.append(child)
            if direction == 'r' and x != len(self.tiles[y]) - 1 and self.undo_move != 'r':
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
                elif self.tiles[y][x] != y * len(self.tiles) + x + 1:
                    diff += 1
        return diff

    def manhattan(self):
        score = 0
        value = 1

        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if value == 16:
                    continue
                x_real, y_real = self.find(value)
                dx = abs(x - x_real)
                dy = abs(y - y_real)
                score += dx + dy
                value += 1
        return score

    def astar(self):

        open_set = []
        closed_set = {}
        heapq.heappush(open_set, self)
        while len(open_set) > 0:

            current_state = heapq.heappop(open_set)
            closed_set[repr(current_state.tiles)] = current_state

            if current_state.heuristic() == 0:
                return current_state.tiles, current_state.previous_moves, len(current_state.previous_moves)
            if current_state.depth < 200:
                for state in current_state.generate_next_states():
                    if repr(state.tiles) in closed_set:
                        continue
                    state.h_score = state.heuristic()
                    state.f_score = state.h_score + state.depth
                    heapq.heappush(open_set, state)

        print(-1)
        return

    def bfs(self):

        order = ['u', 'r', 'd', 'l']
        dq = deque([self])

        while(len(dq) > 0):

            current_state = dq.popleft()

            if current_state.hamming() == 0:
                return current_state.tiles, current_state.previous_moves, len(current_state.previous_moves)

            for state in current_state.generate_next_states(order):
                dq.append(state)

        print(-1)
        return



