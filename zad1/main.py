from fifteen import Fifteen

f = Fifteen("start.txt", "outcome.txt", False)
f.save2file()
f.fo.write('\n')
'''
f.move_zero('u')
f.move_zero('l')
f.move_zero('u')
f.move_zero('l')
f.move_zero('d')
f.undo = ''
'''
f.fo.write('\n\n')
f.save2file()

f.astar()
