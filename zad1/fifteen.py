class Fifteen:
    def __init__(self, fin, fout):
        self.fi = open(fin, "r", encoding="utf-8")
        self.fo = open(fout, "a", encoding="utf-8")
        self.fo.truncate(0)
        self.tiles = [list(map(int, line.split())) for line in self.fi]
        self.fi.close()

    def __del__(self):
        self.fo.close()

    def find0(self):
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                print(self.tiles[x][y])
