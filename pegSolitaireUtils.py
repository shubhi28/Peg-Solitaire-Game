import readGame
import operator


#######################################################
# These are some Helper functions which you have to use 
# and edit.
# Must try to find out usage of them, they can reduce
# your work by great deal.
#
# Functions to change:
# 1. is_wall(self, pos):
# 2. is_validMove(self, oldPos, direction):
# 3. getNextPosition(self, oldPos, direction):
# 4. getNextState(self, oldPos, direction):
#######################################################
class game:
    def __init__(self, filePath):
        self.gameState = readGame.readGameState(filePath)
        self.nodesExpanded = 0
        self.trace = []

    def find_middleDir(self, dir):
        ########################################
        # Method to find the coordinates of the#
        # peg removed                          #
        ########################################
        if dir == 'N':
            a, b = -1, 0
        elif dir == 'S':
            a, b = 1, 0
        elif dir == 'E':
            a, b = 0, 1
        elif dir == 'W':
            a, b = 0, -1
        return a, b

    def find_dir(self, dir):
        ########################################
        # Method to find the coordinates of the#
        # new peg position.                    #
        ########################################
        if dir == 'N':
            a, b = -2, 0
        elif dir == 'S':
            a, b = 2, 0
        elif dir == 'E':
            a, b = 0, 2
        elif dir == 'W':
            a, b = 0, -2
        return a, b

    def is_corner(self, pos):
        ########################################
        # You have to make changes from here
        # check for if the new positon is a corner or not
        # return true if the position is a corner
        corner = [0, 1, 5, 6]
        a, b = pos
        if a in corner and b in corner:
            return True
        return False

    def getMiddlePosition(self, oldPos, direction):
        ############################################
        # Calls 'find_middleDir' method to retrieve#
        # position of the peg removed              #
        ############################################
        dir = self.find_middleDir(direction)
        middlePos = tuple(map(operator.add, oldPos, dir))
        return middlePos

    def getNextPosition(self, oldPos, direction):
        #########################################
        # YOU HAVE TO MAKE CHANGES HERE
        # See DIRECTION dictionary in config.py and add
        # this to oldPos to get new position of the peg if moved
        # in given direction , you can remove next line
        dir = self.find_dir(direction)
        newPos = tuple(map(operator.add, oldPos, dir))
        return newPos

    def is_validMove(self, oldPos, direction):
        #########################################
        # DONT change Things in here
        # In this we have got the next peg position and
        # below lines check for if the new move is a corner
        newPos = self.getNextPosition(oldPos, direction)
        if self.is_corner(newPos):
            return False
        #########################################

        ########################################
        # YOU HAVE TO MAKE CHANGES BELOW THIS
        # check for cases like:
        # if new move is already occupied
        # or new move is outside peg Board
        # Remove next line according to your convenience
        a, b = newPos
        x, y = oldPos
        middlePos = self.getMiddlePosition(oldPos, direction)
        m, n = middlePos
        if a >= 7 or a < 0:
            return False
        if b >= 7 or b < 0:
            return False
        if x >= 7 or x < 0:
            return False
        if y >= 7 or y < 0:
            return False
        if self.gameState[x][y] == 1 and self.gameState[m][n] == 1 and self.gameState[a][b] == 0:
            return True

    def getNextState(self, oldPos, direction):
        ###############################################
        # DONT Change Things in here
        self.nodesExpanded += 1
        if not self.is_validMove(oldPos, direction):
            print "Error, You are not checking for valid move"
            exit(0)
        ###############################################

        ###############################################
        # YOU HAVE TO MAKE CHANGES BELOW THIS
        # Update the gameState after moving peg
        # eg: remove crossed over pegs by replacing it's
        # position in gameState by 0
        # and updating new peg position as 1
        newPos = self.getNextPosition(oldPos, direction)
        middlePos = self.getMiddlePosition(oldPos, direction)
        x1, y1 = oldPos
        x2, y2 = newPos
        x3, y3 = middlePos
        self.trace.append(oldPos)
        self.trace.append(newPos)
        self.gameState[x1][y1] = 0
        self.gameState[x2][y2] = 1
        self.gameState[x3][y3] = 0
        return self.gameState
