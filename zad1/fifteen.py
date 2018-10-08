class Fifteen:
    def __init__(self, fin, fout):
        self.fi = open(fin, "r", encoding="utf-8")
        self.fo = open(fout, "a", encoding="utf-8")
        self.fo.truncate(0)
        self.tiles = [list(map(int, line.split())) for line in self.fi]
        self.fi.close()
        self.neighbours = list

    def __del__(self):
        self.fo.close()

    def save2file(self):
        self.fo.write(self.tiles2str())

    def tiles2str(self):
        s = ''
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                s += str(self.tiles[y][x]) + ' '
            s += '\n'
        return s

    def find(self, tile):
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if self.tiles[y][x] == tile:
                    return x, y
        return -1, -1

    def swap(self, d, x, y):
        if d == 'u' or d == 'U':
            if y-1 < 0:
                raise NameError
            self.tiles[y][x], self.tiles[y-1][x] = self.tiles[y-1][x], self.tiles[y][x]
            self.fo.write('U')
        elif d == 'd' or d == 'D':
            if y+1 > len(self.tiles):
                raise NameError
            self.tiles[y][x], self.tiles[y+1][x] = self.tiles[y+1][x], self.tiles[y][x]
            self.fo.write('D')
        elif d == 'l' or d == 'L':
            if x-1 < 0:
                raise NameError
            self.tiles[y][x], self.tiles[y][x-1] = self.tiles[y][x-1], self.tiles[y][x]
            self.fo.write('L')
        elif d == 'r' or d == 'R':
            if x+1 > len(self.tiles[y]):
                raise NameError
            self.tiles[y][x], self.tiles[y][x+1] = self.tiles[y][x+1], self.tiles[y][x]
            self.fo.write('R')
        else:
            raise NameError
