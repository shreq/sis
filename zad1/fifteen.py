from copy import deepcopy


class Fifteen:

    tiles = []
    undo_move = ''
    next_states = []
    h_score = 0  # calculated using heuristic
    g_score = 0  # equal to depth
    f_score = 0  # sum of h_score and g_score
    previous_moves = []

    def __init__(self, fin, parent=None):
        if parent is None:
            fi = open(fin, 'r', encoding='utf-8')
            self.tiles = [list(map(int, line.split())) for line in fi]
            fi.close()
        elif parent is not None:
            self.tiles = deepcopy(parent.tiles)
            self.undo_move = deepcopy(parent.undo_move)
            self.h_score = deepcopy(parent.h_score)
            self.g_score = deepcopy(parent.g_score)
            self.f_score = deepcopy(parent.f_score)
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
            child = Fifteen(None, self)
            child.swap('u')
            child.g_score = len(child.previous_moves)
            self.next_states.append(child)
        if y + 1 <= len(self.tiles) - 1 and self.undo_move != 'd':
            child = Fifteen(None, self)
            child.swap('d')
            child.g_score = len(child.previous_moves)
            self.next_states.append(child)
        if x - 1 >= 0 and self.undo_move != 'l':
            child = Fifteen(None, self)
            child.swap('l')
            child.g_score = len(child.previous_moves)
            self.next_states.append(child)
        if x + 1 <= len(self.tiles[y]) - 1 and self.undo_move != 'r':
            child = Fifteen(None, self)
            child.swap('r')
            child.g_score = len(child.previous_moves)
            self.next_states.append(child)

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

    def astar(self):

        queue = [self]

        while len(queue) > 0:
            current_state = queue.pop(0)

            if current_state.hamming() == 0:
                print(current_state.tiles)
                return
            current_state.generate_next_states()
            for state in current_state.next_states:
                state.h_score = state.hamming()
                state.f_score = state.h_score + state.g_score
                queue.append(state)
                queue.sort(key=lambda x: x.f_score, reverse=False)

        print(-1)
        return
