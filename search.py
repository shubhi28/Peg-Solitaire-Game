import pegSolitaireUtils
import config
from copy import deepcopy
# Imported Queue to implement Priority Queue #
import Queue as Q

# Global variable to count number of nodes expanded #
numExpandNodes = 0

'''
############################################
# Method to check if GoalState is reached  #
############################################
'''
def isGoalState(pegSolitaireObject):
    Goal = [[-1, -1, 0, 0, 0, -1, -1], [-1, -1, 0, 0, 0, -1, -1], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0], [-1, -1, 0, 0, 0, -1, -1], [-1, -1, 0, 0, 0, -1, -1]]
    if pegSolitaireObject.gameState == Goal:
        return True
    else:
        return False

'''
########################################################
# Calculates heuristics as Manhattan Distance (dx+dy)  #
# for all pegs in a gameState from the centre of board #
########################################################
# Reference : https://www.cs.york.ac.uk/aig/projects/implied/docs/CPAIOR03.pdf #
'''
def manhattan_heuristic(pegSolitaireObject):
    manhattan_distance = 0
    # count=0
    for x in range(7):
        for y in range(7):
            if pegSolitaireObject.gameState[x][y] == 1:
                sum = abs(x - 3) + abs(y - 3)
                manhattan_distance += sum
    return (manhattan_distance)

'''
############################################################
# Calculates h(n) as sum of predefined Weighted_Cost       #
# Matrix for all pegs in a gameState. Each position of     #
# matrix are chosen based on how that position contributes #
# towards goal state. Higher value indicates larger        #
# distance from goal and vice-versa.                       #
############################################################
# Reference: https://www.jair.org/media/2096/live-2096-3136-jair.pdf #
'''
def weighted_heuristic(pegSolitaireObject):
    wsum = 0
    weighted_Cost = [[0, 0, 5, 0, 5, 0, 0], [0, 0, 0, 0, 0, 0, 0], [5, 0, 4, 0, 4, 0, 5], [0, 0, 0, 1, 0, 0, 0],
                     [5, 0, 4, 0, 4, 0, 5], [0, 0, 0, 0, 0, 0, 0], [0, 0, 5, 0, 5, 0, 0]]
    for x in range(7):
        for y in range(7):
            if pegSolitaireObject.gameState[x][y] == 1:
                wsum += weighted_Cost[x][y]
    return (wsum)

'''
################################################################
# This method is used for PRUNING of Game states in Iterative  #
# Deepening Search. We are eliminating the game states from    #
# being expanded if the pagoda value of child node is greater  #
# than parent node. The values of matrix satisfy the condition #
# that for any 3 adjacent board positions a,b,c: a+b>=c        #                                          #
################################################################
# Reference : https://ianm.host.cs.st-andrews.ac.uk/docs/CAORPreprint.pdf #
'''
def pagoda_heuristic(pegSolitaireObject):
    pagoda = 0
    pagodaMatrix = [[0, 0, 1, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0],
                    [1, 0, 1, 0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 1, 0, 1, 0]]
    for x in range(7):
        for y in range(7):
            if pegSolitaireObject.gameState[x][y] == 1:
                pagoda += pagodaMatrix[x][y]
    return (pagoda)

'''
#################################################################
# Method to expand a node if valid move is found in any of the  #
# 4 directions. For each valid move, a new reference of the     #
# object is created (via deepcopy) so as we dont lose the actual#
# game state of parent. It returns It returns the Fringe List   #
# containing child nodes.                                       #
#################################################################
'''
def ExpandNode(pegSolitaireObject):
    fringe = []
    for i in range(7):
        for j in range(7):
            if pegSolitaireObject.gameState[i][j] == 1:
                if pegSolitaireObject.is_validMove((i, j), 'N') == True:
                    p = deepcopy(pegSolitaireObject)
                    p.gameState = p.getNextState((i, j), 'N')
                    fringe.append(p)
                if pegSolitaireObject.is_validMove((i, j), 'S') == True:
                    p = deepcopy(pegSolitaireObject)
                    p.gameState = p.getNextState((i, j), 'S')
                    fringe.append(p)
                if pegSolitaireObject.is_validMove((i, j), 'E') == True:
                    p = deepcopy(pegSolitaireObject)
                    p.gameState = p.getNextState((i, j), 'E')
                    fringe.append(p)
                if pegSolitaireObject.is_validMove((i, j), 'W') == True:
                    p = deepcopy(pegSolitaireObject)
                    p.gameState = p.getNextState((i, j), 'W')
                    fringe.append(p)
    return fringe

'''
##############################################################
# Method to implement Depth Limited search used in Iterative #
# Deepening. It returns PegSolitaire Object if goal state    #
# is reached, otherwise it returns false.                    #
##############################################################
'''
def DLS_Itr_Deep(pegSolitaireObject, depth):
    global numExpandNodes
    visited = []
    FringeList = [(pegSolitaireObject, 0)]
    while len(FringeList) is not 0:
        peg, lev = FringeList.pop()
        if (peg.gameState, lev) not in visited:
            visited.append((peg.gameState, lev))
            if isGoalState(peg):
                return peg
            else:
                if lev is not depth:
                    fringe = ExpandNode(peg)
                    #Pagoda heuristic is implemented to prune the states.#
                    d = pagoda_heuristic(peg)
                    for i in fringe:
                        dchild = pagoda_heuristic(i)
                        # If pagoda value of child state is greater than #
                        # that of parent, that state is pruned.          #
                        if d < dchild:
                            visited.append((i.gameState, lev))
                    if fringe:
                        numExpandNodes += 1
                    for successor in fringe:
                        if (successor, lev) not in visited:
                            visited.append((successor.gameState, lev))
                            FringeList.append((successor, lev + 1))
    return None

'''
###############################################################
# Method to implement Iterative Deepening Search. It returns  #
# the trace and number of nodes expanded for PegSolitaire     #
# Object if goal state is reached, otherwise it returns false.#
###############################################################
'''
def ItrDeepSearch(pegSolitaireObject):
    #################################################
    # Must use functions:
    # getNextState(self,oldPos, direction)
    #
    # we are using this function to count,
    # number of nodes expanded, If you'll not
    # use this grading will automatically turned to 0
    #################################################
    #
    # using other utility functions from pegSolitaireUtility.py
    # is not necessary but they can reduce your work if you
    # use them.
    # In this function you'll start from initial gameState
    # and will keep searching and expanding tree until you
    # reach goal using Iterative Deepning Search.
    # you must save the trace of the execution in pegSolitaireObject.trace
    # SEE example in the PDF to see what to save
    #
    #################################################
    # result = None
    for depth in range(20, 31):
        result = DLS_Itr_Deep(pegSolitaireObject, depth)
        if result:
            pegSolitaireObject.nodesExpanded = numExpandNodes
            pegSolitaireObject.trace = deepcopy(result.trace)
            return True
    if not result:
        pegSolitaireObject.nodesExpanded = numExpandNodes
        pegSolitaireObject.trace="GOAL NOT FOUND"
    return False

'''
################################################################
# Method to implement A* Search Algorithm. In equation, f(n)=  #
# g(n)+h(n), g(n) is assumed to be zero as the cost for        #
# reaching each game state from parent is considered to be     #
# same.The heuristic h(n) used is Manhattan heuristics. It     #
# returns the trace and number of nodes expanded for           #
# PegSolitaire Object if goal state is reached, otherwise it   #
# returns false.                                               #
################################################################
'''
def aStarOne(pegSolitaireObject):
    #################################################
    # Must use functions:
    # getNextState(self,oldPos, direction)
    #
    # we are using this function to count,
    # number of nodes expanded, If you'll not
    # use this grading will automatically turned to 0
    #################################################
    #
    # using other utility functions from pegSolitaireUtility.py
    # is not necessary but they can reduce your work if you
    # use them.
    # In this function you'll start from initial gameState
    # and will keep searching and expanding tree until you
    # reach goal using A-Star searching with first Heuristic
    # you used.
    # you must save the trace of the execution in pegSolitaireObject.trace
    # SEE example in the PDF to see what to return
    #
    #################################################
    expandNodesAStarOne = 0
    # Child node is popped out on the basis of highest priority#
    # from the Priority Queue q.                              #
    q = Q.PriorityQueue()
    visited = []
    iPriority = manhattan_heuristic(pegSolitaireObject)
    q.put((iPriority, pegSolitaireObject))
    while not q.empty():
        (p, peg) = q.get()
        if peg.gameState not in visited:
            visited.append(peg.gameState)
            if isGoalState(peg):
                pegSolitaireObject.nodesExpanded = expandNodesAStarOne
                pegSolitaireObject.trace = deepcopy(peg.trace)
                return True
            else:
                Fringe = ExpandNode(peg)
                if Fringe:
                    expandNodesAStarOne += 1
                for successor in Fringe:
                    if successor.gameState not in visited:
                        d=manhattan_heuristic(successor)
                        q.put((d,successor))
    pegSolitaireObject.trace="GOAL NOT FOUND"
    pegSolitaireObject.nodesExpanded=expandNodesAStarOne
    return False

'''
################################################################
# Method to implement A* Search Algorithm. In equation, f(n)=  #
# g(n)+h(n), g(n) is assumed to be zero as the cost for        #
# reaching each game state from parent is considered to be     #
# same.The heuristic h(n) used is weighted matrix heuristics.  #
# This heuristic is more informed than manhattan heuristic.    #
# It returns the trace and number of nodes expanded for        #
# PegSolitaire Object if goal state is reached, otherwise it   #
# returns false.                                               #
################################################################
'''
def aStarTwo(pegSolitaireObject):
    #################################################
    # Must use functions:
    # getNextState(self,oldPos, direction)
    #
    # we are using this function to count,
    # number of nodes expanded, If you'll not
    # use this grading will automatically turned to 0
    #################################################
    #
    # using other utility functions from pegSolitaireUtility.py
    # is not necessary but they can reduce your work if you
    # use them.
    # In this function you'll start from initial gameState
    # and will keep searching and expanding tree until you
    # reach goal using A-Star searching with second Heuristic
    # you used.
    # you must save the trace of the execution in pegSolitaireObject.trace
    # SEE example in the PDF to see what to return
    #
    #################################################
    expandNodesAStarTwo = 0
    # Child node is popped out on the basis of highest priority#
    # from the Priority Queue q.                              #
    q = Q.PriorityQueue()
    visited = []
    iPriority = weighted_heuristic(pegSolitaireObject)
    q.put((iPriority, pegSolitaireObject))
    while not q.empty():
        (p, peg) = q.get()
        if peg.gameState not in visited:
            visited.append(peg.gameState)
            if isGoalState(peg):
                pegSolitaireObject.nodesExpanded = expandNodesAStarTwo
                pegSolitaireObject.trace = deepcopy(peg.trace)
                return True
            else:
                Fringe = ExpandNode(peg)
                if Fringe:
                    expandNodesAStarTwo += 1
                for successor in Fringe:
                    if successor.gameState not in visited:
                        d=weighted_heuristic(successor)
                        q.put((d,successor))
    pegSolitaireObject.trace="GOAL NOT FOUND"
    pegSolitaireObject.nodesExpanded=expandNodesAStarTwo
    return False
