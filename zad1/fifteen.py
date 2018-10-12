from copy import deepcopy


class Fifteen:

    heur = ''
    tiles = []
    undo_move = ''
    next_states = []
    h_score = 0  # calculated using heuristic
    depth = 0  # equal to depth
    f_score = 0  # sum of h_score and depth
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
            self.depth = deepcopy(parent.depth)
            self.previous_moves = deepcopy(parent.previous_moves)
        else:
            self.tiles = []

    def tiles2str(self):
        s = ''
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                s += str(self.tiles[y][x]) + ' '
            s += '\n'
        return s

    def save2file(self):
        self.fo.write(self.tiles2str())

    def find(self, tile=0):
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if self.tiles[y][x] == tile:
                    return x, y
        raise NameError

    def swap(self, d, x=-1, y=-1):
        if x == -1 or y == -1:
            x, y = self.find()
        if d == 'u' and y - 1 >= 0:
            self.tiles[y][x], self.tiles[y - 1][x] = self.tiles[y - 1][x], self.tiles[y][x]
            self.previous_moves.append('u')
            self.undo_move = 'd'
        elif d == 'd' and y + 1 <= len(self.tiles) - 1:
            self.tiles[y][x], self.tiles[y + 1][x] = self.tiles[y + 1][x], self.tiles[y][x]
            self.previous_moves.append('d')
            self.undo_move = 'u'
        elif d == 'l' and x - 1 >= 0:
            self.tiles[y][x], self.tiles[y][x - 1] = self.tiles[y][x - 1], self.tiles[y][x]
            self.previous_moves.append('l')
            self.undo_move = 'r'
        elif d == 'r' and x + 1 <= len(self.tiles[y]) - 1:
            self.tiles[y][x], self.tiles[y][x + 1] = self.tiles[y][x + 1], self.tiles[y][x]
            self.previous_moves.append('r')
            self.undo_move = 'l'
        else:
            raise NameError

    def generate_next_states(self):
        self.next_states = []
        x, y = self.find()
        if y - 1 >= 0 and self.undo_move != 'u':
            child = Fifteen(None, None, self)
            child.swap('u')
            child.depth = len(child.previous_moves)
            self.next_states.append(child)
        if y + 1 <= len(self.tiles) - 1 and self.undo_move != 'd':
            child = Fifteen(None, None, self)
            child.swap('d')
            child.depth = len(child.previous_moves)
            self.next_states.append(child)
        if x - 1 >= 0 and self.undo_move != 'l':
            child = Fifteen(None, None, self)
            child.swap('l')
            child.depth = len(child.previous_moves)
            self.next_states.append(child)
        if x + 1 <= len(self.tiles[y]) - 1 and self.undo_move != 'r':
            child = Fifteen(None, None, self)
            child.swap('r')
            child.depth = len(child.previous_moves)
            self.next_states.append(child)

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

    def is_contained(self, list, obj):
        for element in list:
            if element.tiles == obj.tiles:
                return True
            return False

    def astar(self):

        queue = [self]
        processed = []
        loops = 0
        while len(queue) > 0 and loops < 20000:
            loops += 1
            current_state = queue.pop(0)
            processed.append(current_state)
            if current_state.heuristic() == 0:
                print(current_state.tiles)
                return
            if current_state.depth < 200:
                current_state.generate_next_states()
                for state in current_state.next_states:
                    if self.is_contained(processed, state):
                        continue
                    state.h_score = state.heuristic()
                    state.f_score = state.h_score + state.depth
                    queue.append(state)
                queue.sort(key=lambda x: x.f_score, reverse=False)
        print(current_state.tiles)
        print(-1)
        return
