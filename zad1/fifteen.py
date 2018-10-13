from copy import deepcopy


class Fifteen:

    heur = ''
    tiles = []
    undo_move = ''
    h_score = 0  # calculated using heuristic
    depth = 0
    previous_moves = []

    def __init__(self, heur, fin, parent=None):
        if parent is None:
            self.heur = heur
            fi = open(fin, 'r', encoding='utf-8')
            self.tiles = [list(map(int, line.split())) for line in fi]
            fi.close()
        elif parent is not None:
            self.heur = deepcopy(parent.heur)
            self.tiles = deepcopy(parent.tiles)
            self.undo_move = deepcopy(parent.undo_move)
            self.depth = deepcopy(parent.depth) + 1
            self.previous_moves = deepcopy(parent.previous_moves)

    def find(self, tile=0):
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if self.tiles[y][x] == tile:
                    return x, y
        raise NameError

    def move_tile(self, direction):
        x, y = self.find()
        if direction == 'u':
            self.tiles[y][x], self.tiles[y - 1][x] = self.tiles[y - 1][x], self.tiles[y][x]
            self.previous_moves.append('u')
            self.undo_move = 'd'
        elif direction == 'd':
            self.tiles[y][x], self.tiles[y + 1][x] = self.tiles[y + 1][x], self.tiles[y][x]
            self.previous_moves.append('d')
            self.undo_move = 'u'
        elif direction == 'l':
            self.tiles[y][x], self.tiles[y][x - 1] = self.tiles[y][x - 1], self.tiles[y][x]
            self.previous_moves.append('l')
            self.undo_move = 'r'
        elif direction == 'r':
            self.tiles[y][x], self.tiles[y][x + 1] = self.tiles[y][x + 1], self.tiles[y][x]
            self.previous_moves.append('r')
            self.undo_move = 'l'
        else:
            raise NameError

    def generate_next_states(self):
        next_states = []
        x, y = self.find()
        if y != 0 and self.undo_move != 'u':
            child = Fifteen(None, None, self)
            child.move_tile('u')
            next_states.append(child)
        if y != len(self.tiles) - 1 and self.undo_move != 'd':
            child = Fifteen(None, None, self)
            child.move_tile('d')
            next_states.append(child)
        if x != 0 and self.undo_move != 'l':
            child = Fifteen(None, None, self)
            child.move_tile('l')
            next_states.append(child)
        if x != len(self.tiles[y]) - 1 and self.undo_move != 'r':
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
                    value = 0
                x_real, y_real = self.find(value)
                dx = abs(x - x_real)
                dy = abs(y - y_real)
                score += dx + dy
                value += 1
        return score

    def astar(self):

        queue = [self]
        closed_set = {}
        while len(queue) > 0:
            current_state = queue.pop(0)
            closed_set[repr(current_state.tiles)] = current_state
            if current_state.heuristic() == 0:
                print(current_state.tiles)
                print(current_state.previous_moves)
                print(len(current_state.previous_moves))
                return
            for state in current_state.generate_next_states():
                if repr(state.tiles) in closed_set:
                    continue
                state.h_score = state.heuristic()
                queue.append(state)
            queue.sort(key=lambda x: x.h_score, reverse=False)
        print(-1)
        return
