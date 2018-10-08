class Fifteen:
    def __init__(self, fin, fout):
        self.fi = open(fin, "r", encoding="utf-8")
        self.fo = open(fout, "a", encoding="utf-8")
        self.tiles = [list(map(int, line.split())) for line in self.fi]
        self.fi.close()
        self.fo.truncate(0)
        self.neighbours = []
        self.moves = []
        self.undo = ""

    def __del__(self):
        self.fo.close()

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
            self.fo.write('U')
        elif d == 'd' or d == 'D':
            if y+1 > len(self.tiles):
                raise NameError
            self.tiles[y][x], self.tiles[y+1][x] = self.tiles[y+1][x], self.tiles[y][x]
            self.undo = 'u'
            self.fo.write('D')
        elif d == 'l' or d == 'L':
            if x-1 < 0:
                raise NameError
            self.tiles[y][x], self.tiles[y][x-1] = self.tiles[y][x-1], self.tiles[y][x]
            self.undo = 'r'
            self.fo.write('L')
        elif d == 'r' or d == 'R':
            if x+1 > len(self.tiles[y]):
                raise NameError
            self.tiles[y][x], self.tiles[y][x+1] = self.tiles[y][x+1], self.tiles[y][x]
            self.undo = 'l'
            self.fo.write('R')
        else:
            raise NameError

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
                if self.tiles[y][x] != y * len(self.tiles) + x + 1:
                    diff += 1
        return diff
