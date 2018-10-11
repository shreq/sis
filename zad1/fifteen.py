from copy import deepcopy


class Fifteen:
    def __init__(self, fin, fout, is_child, obj=None):
        self.is_child = is_child
        self.moves = []
        self.undo = ''
        if not is_child:
            self.fi = open(fin, 'r', encoding='utf-8')
            self.fo = open(fout, 'a', encoding='utf-8')
            self.tiles = [list(map(int, line.split())) for line in self.fi]
            self.fi.close()
            self.fo.truncate(0)
        elif obj is not None:
            self.tiles = deepcopy(obj.tiles)
        else:
            self.tiles = []

    def __del__(self):
        if not self.is_child:
            self.fo.close()

    def _copy_(self, tiles, moves, undo):
        self.tiles = tiles
        self.moves = moves
        self.undo = undo

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
            self.undo = 'd'
        elif d == 'd' and y + 1 <= len(self.tiles) - 1:
            self.tiles[y][x], self.tiles[y + 1][x] = self.tiles[y + 1][x], self.tiles[y][x]
            self.undo = 'u'
        elif d == 'l' and x - 1 >= 0:
            self.tiles[y][x], self.tiles[y][x - 1] = self.tiles[y][x - 1], self.tiles[y][x]
            self.undo = 'r'
        elif d == 'r' and x + 1 <= len(self.tiles[y]) - 1:
            self.tiles[y][x], self.tiles[y][x + 1] = self.tiles[y][x + 1], self.tiles[y][x]
            self.undo = 'l'
        else:
            raise NameError
        self.look_around()

    def look_around(self):
        self.moves = []
        x, y = self.find()
        if y - 1 >= 0 and self.undo != 'u':
            self.moves.append('u')
        if y + 1 <= len(self.tiles) - 1 and self.undo != 'd':
            self.moves.append('d')
        if x - 1 >= 0 and self.undo != 'l':
            self.moves.append('l')
        if x + 1 <= len(self.tiles[y]) - 1 and self.undo != 'r':
            self.moves.append('r')

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

    def best_move(self):
        best_move = ''
        smallest_error = 99
        self.look_around()

        children = []
        for i in range(len(self.moves)):
            children.append(Fifteen(self.fi, self.fo, True, self))

        for move, child in zip(self.moves, children):
            child.swap(move)
            ham = child.hamming()
            if ham < smallest_error:
                smallest_error = ham
                best_move = move

        return best_move

    def astar(self):
        loops = 0
        while self.hamming() > 0 and loops < 10000:
            closed = []
            open = []
            optimal_route = 0

            while len(open):
                best_move = self.best_move()

            # <-- NEW
            # OLD -->
            best = self.best_move()

            if best != '':
                self.swap(best)
            else:
                print('   l   i   p   a')

            print(loops)
            loops += 1
        return loops
