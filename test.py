import operator
import readGame
try:
    import Queue as Q
except ImportError:
    import queue as Q

def PQ ():
    q = Q.PriorityQueue()
    q.put((11,10))
    q.put((5,8))
    q.put((3,27))
    print(q.queue)
    while not q.empty():
        (p,item) = q.get()
        #print('%s-%s' % p, % item)
    print(q.queue)

def is_corner(pos):
    a, b = pos
    corner = [0, 1, 5, 6]
    if a in corner and b in corner:
        return True
    return False


def find_dir(dir):
    if dir == 'N':
        a, b = -2, 0
    elif dir == 'S':
        a, b = 2, 0
    elif dir == 'E':
        a, b = 0, 2
    elif dir == 'W':
        a, b = 0, -2
    return a, b


def is_newPos(oldPos, dir):
    # direction= [(-2,0),(2,0),(0,2),(0,-2)]
    # a,b=find_dir(dir)
    # d=a,b
    d = find_dir(dir)
    newPos = tuple(map(operator.add, oldPos, d))
    return newPos


def is_validMove(oldPos, dir):
    newPos = is_newPos(oldPos, dir)
    a, b = newPos
    p1 = readGame.readGameState("./game.txt")
    if p1[a][b] == 1:
        print("Valid Move")
    else:
        print("Invalid Move")


if __name__ == "__main__":
    print(is_corner((0, 1)))
    print(is_newPos((3, 2), 'N'))
    print(is_corner(is_newPos((3, 2), 'S')))
    is_validMove((3, 2), 'E')
    trace = []
    oldPos = 2, 3
    newPos = 2, 5
    x1, y1 = oldPos
    x2, y2 = newPos
    x3 = tuple(map(operator.sub, newPos, oldPos))
    print(x3)
    x4 = tuple(map(operator.div, x3, (2, 2)))
    print(x4)
    x = tuple(map(operator.add, oldPos, x4))
    print(x)
    trace.append(oldPos)
    trace.append(newPos)
    trace.append(x)
    print(trace)
    PQ()

# x3,y3=(((x2,y2)-(x1,y1))/2)+(x1,y1)
# print(x3,y3)

# --000--,--0X0--,00XXX00,000X000,000X000,--000--,--000-- plus 6
# --000--,--0X0--,000X000,0XXXXX0,000X000,--0X0--,--000-- cross 9
# --XXX--,--XXX--,00XXX00,00X0X00,0000000,--000--,--000-- fireplace 11
# --000--,--000--,0000000,000X000,0000000,--000--,--000-- goalstate 1
# --XXX--,--XXX--,XXXXXXX,XXX0XXX,XXXXXXX,--XXX--,--XXX-- full board 32
# --000--,--0X0--,00XXX00,0XXXXX0,00XXX00,--0X0--,--000-- 13 not a goal state
# --XXX--,--XX0--,XXX0X00,XXXXXX0,XXXXX00,--X00--,--000-- amit 21


# def DFS1(pegSolitaireObject, depth):
#    if depth == 0:
#        if isGoalState(pegSolitaireObject):
#             return pegSolitaireObject
#         else:
#             return None
#
#     FringeList = [(pegSolitaireObject,0)]
#     while len(FringeList) is not 0:
#         peg,lev=FringeList.pop(-1)
#         if isGoalState(peg):
#             return peg
#         else:
#             if lev is not depth:
#                 fringe = ExpandNode(peg)
#                 for successor in fringe:
#                     FringeList = FringeList+[(successor, lev+1)]
#     return None
