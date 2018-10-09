class Fifteen:
    def __init__(self, fin, fout, is_child):
        self.is_child = is_child
        if not is_child:
            self.fi = open(fin, "r", encoding="utf-8")
            self.fo = open(fout, "a", encoding="utf-8")
            self.tiles = [list(map(int, line.split())) for line in self.fi]
            self.fi.close()
            self.fo.truncate(0)
        else:
            self.tiles = []
        self.neighbours = []
        self.moves = []
        self.undo = ""

    def __del__(self):
        if not self.is_child:
            self.fo.close()

    def _copy_(self, tiles, neighbours, moves, undo):
        self.tiles = tiles
        self.neighbours = neighbours
        self.moves = moves
        self.undo = undo

    def save2file(self):                        # write current state of tiles to file
        self.fo.write(self.tiles2str())

    def tiles2str(self):                        # saves state of tiles to string
        s = ''
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                s += str(self.tiles[y][x]) + ' '
            s += '\n'
        return s

    def find(self, tile):                       # find coordinates of specified tile
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if self.tiles[y][x] == tile:
                    return x, y
        raise NameError

    def swap(self, d, x, y):                    # moves tile with specified coordinates up/down/left/right
        if d == 'u' or d == 'U':
            if y-1 < 0:
                raise NameError
            self.tiles[y][x], self.tiles[y-1][x] = self.tiles[y-1][x], self.tiles[y][x]
            self.undo = 'd'
            if not self.is_child:
               self.fo.write('U')
        elif d == 'd' or d == 'D':
            if y+1 > len(self.tiles):
                raise NameError
            self.tiles[y][x], self.tiles[y+1][x] = self.tiles[y+1][x], self.tiles[y][x]
            self.undo = 'u'
            if not self.is_child:
                self.fo.write('D')
        elif d == 'l' or d == 'L':
            if x-1 < 0:
                raise NameError
            self.tiles[y][x], self.tiles[y][x-1] = self.tiles[y][x-1], self.tiles[y][x]
            self.undo = 'r'
            if not self.is_child:
                self.fo.write('L')
        elif d == 'r' or d == 'R':
            if x+1 > len(self.tiles[y]):
                raise NameError
            self.tiles[y][x], self.tiles[y][x+1] = self.tiles[y][x+1], self.tiles[y][x]
            self.undo = 'l'
            if not self.is_child:
                self.fo.write('R')
        else:
            raise NameError

    def move_zero(self, d):
        x, y = self.find(0)
        success = True
        try:
            self.swap(d, x, y)
        except NameError:
            success = False
        self.look_around()
        return success

    def look_around(self):                      # checks neighbourhood of blank tile and looks for possible moves
        self.neighbours = []
        self.moves = []
        x, y = self.find(0)
        if y-1 > 0:
            self.neighbours.append(self.tiles[y-1][x])
            if self.undo != 'u':
                self.moves.append('u')
        if y+1 < len(self.tiles):
            self.neighbours.append(self.tiles[y+1][x])
            if self.undo != 'd':
                self.moves.append('d')
        if x-1 > 0:
            self.neighbours.append(self.tiles[y][x-1])
            if self.undo != 'l':
                self.moves.append('l')
        if x+1 < len(self.tiles[y]):
            self.neighbours.append(self.tiles[y][x+1])
            if self.undo != 'r':
                self.moves.append('r')

    def hamming(self):                          # Hamming metric
        diff = 0
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if y == len(self.tiles)-1 and x == len(self.tiles[y])-1:
                    if self.tiles[y][x] != 0:
                        diff += 1
                elif self.tiles[y][x] != y * len(self.tiles) + x + 1:
                    diff += 1
        return diff

    def astar(self):
        loops = 0
        while self.hamming() > 0:
            self.look_around()
            # self.hamming()
            best_move = ""
            smallest_error = 99
            child = Fifteen(self.fi, self.fo, True)
            child._copy_(self.tiles, self.neighbours, self.moves, self.undo)

            for move in self.moves:
                child.move_zero(move)
                ham = child.hamming()
                if ham < smallest_error:
                    best_move = move
                    smallest_error = ham
                child.move_zero(child.undo)
            child.__del__()

            if best_move != "":
                self.move_zero(best_move)

            if loops % 10000 == 0:
                print(loops)
            loops += 1
        return loops
