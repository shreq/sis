from fifteen import Fifteen

f = Fifteen("start.txt", "outcome.txt", False)
f.save2file()
f.fo.write('\n')
'''
f.move_zero('d')
'''
f.undo = ''

f.fo.write('\n')
f.save2file()

f.astar()

f.fo.write('\n\n')
f.save2file()
