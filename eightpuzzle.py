import random
import copy
import math
from sre_parse import State

globalState = "b12 345 678"
initialState = ""
goalState = "b12 345 678"
moves = []
states = []
numMoves = 0
heurist = ""
isBeamSearch = False
limit = 0
maxN = -1
totalNodes = 0
randomizing = False
seed = 10
generating = False

def setState(state):
    global globalState
    globalState = state

def printState():
    print("")
    print(globalState[0:3])
    print(globalState[4:7])
    print(globalState[8:11])
    print("")

def printSpecState(state):
    print("")
    print(state[0:3])
    print(state[4:7])
    print(state[8:11])
    print("")

def getBlankPos():
    count = 0; 
    for letter in globalState:
        if letter == 'b':
            return count
        count += 1
    return 0

def move(direction):
    blankPos = getBlankPos(); 
    possMoves = getPossibleMoves()
    if possMoves.__contains__(direction):
        if direction == "down":
            swapIndices(blankPos, blankPos+4)
        if direction == "up":
            swapIndices(blankPos, blankPos-4)
        if direction == "left":
            swapIndices(blankPos, blankPos-1)
        if direction == "right":
            swapIndices(blankPos, blankPos+1)
        moves.append(direction)
        return True
    else:
        if randomizing == False:
            print("Invalid move " + direction)
        return False

def swapIndices(a, b):
    global globalState
    if a > len(globalState) or b > len(globalState):
        return
    tempStr = ""
    count = 0
    for i in globalState:
        if count == a:
            tempStr += globalState[b]
        elif count == b:
            tempStr += globalState[a]
        else:
            tempStr += i
        count += 1
    setState(tempStr)

def randomState(n):
    global initialState, globalState, randomizing, seed
    print("Randomizing State")
    print("")
    globalState, i = goalState, 0
    randomizing = True
    random.seed(seed)
    while i < n:
        direction = random.choice(["left","up","down","right"])
        while(isOppositeToLastMove(direction) == True):
            direction = random.choice(["left","up","down","right"])
        if move(direction) == True:
            i += 1
    initialState = globalState
    randomizing = False

def numMisplaced():
    trimmedState, count, numMisplaced = globalState.replace(" ",""), 0, 0
    for num in trimmedState.replace("b","9"):
        if int(num) != count:
            numMisplaced += 1
        count+=1
    return numMisplaced - 1  #subtract 1 because b will always be misplaced

def sumOfDistances():
    trimmedState = globalState.replace(" ","").replace("b","9")
    sum = 0
    i = 0
    for n in trimmedState:
        num = int(n)
        if num == 9:
            i += 1
            continue
        if num != i:
            # divide by 3 and mod by 3. For example. distance between 0th tile and 8 tile is 8 mod 3 = 2 + 8 / 3 = 2 = 4 moves.
            dist = (math.floor(abs(num - i) / 3)) + (abs(num - i) % 3)
            sum += dist
        else:
            dist = 0
        i += 1
    return sum

def solveAStar(heuristic):
    global moves, heurist
    moves = []
    heurist = heuristic
    print("Solving A Star with heuristic " + heurist)
    AStar()

def AStar():
    global moves, totalNodes, maxN
    failure = False
    states.append([-1, moves, globalState])
    while(isSolved() != True):
        if maxN != -1:
            if totalNodes > maxN:
                failure = True
                print("Error: Exceeded max number of nodes to be considered")
                break
        addStatesFromFirsts()
    if failure == False:
        puzzleSolved()


def addStatesFromFirsts():
    global moves, isBeamSearch
    if len(states) == 0:
        return
    depthOfFirst = states[0][0]
    while(states[0][0] == depthOfFirst):
        setState(states[0][2])
        moves = states[0][1]
        #finds the moves for the particular state we are searching
        possMoves = removeOpposite(getPossibleMoves())
        states.pop(0)
        for moveIn in possMoves:
            addStateWithMove(moveIn)
    states.sort(key=lambda x: x[0], reverse = False)
    if isBeamSearch == True:
        trimStates()
            
def trimStates():
    global limit
    if len(states) > limit:
        del states[limit-1:len(states)-1]

def isSolved():
    global states, moves
    if len(states) == 0:
        return False
    depthOfFirst = states[0][0]
    for s in states:
        if s[0] == depthOfFirst:
            if s[2] == goalState: #or s[0] == len(s[1]):
                setState(s[2])
                moves = s[1]
                return True
        else:
            break
    return False

def addStateWithMove(direction):
    global totalNodes
    if move(direction) == True:
        if stateAlreadyAdded() == False:
            tempMoves = copy.copy(moves)
            if heurist == "h1":
                states.append([numMisplaced() + len(tempMoves), tempMoves, globalState])
            elif heurist == "h2":
                states.append([sumOfDistances() + len(tempMoves), tempMoves, globalState])
            totalNodes += 1
            undoLastMove()

def stateAlreadyAdded():
    for state in states:
        if state[2] == globalState:
            return True
    return False

def undoLastMove():
    if len(moves) > 0:
        if moves[-1] == "left":
            move("right")
        elif moves[-1] == "right":
            move("left")
        elif moves[-1] == "up":
            move("down")
        elif moves[-1] == "down":
            move("up")
        #removes the two unnecessary moves from list of moves
        moves.pop()
        moves.pop()

def getPossibleMoves():
    possMoves = []
    blankPos = getBlankPos(); 
    if blankPos < 7:
        possMoves.append("down")
    if blankPos > 3:
        possMoves.append("up")
    if blankPos % 4 != 0:
        possMoves.append("left")
    if blankPos % 4 != 2:
        possMoves.append("right")
    return possMoves

def removeOpposite(moveArr):
    if moveArr == []:
        return []
    newMoves = []
    for move in moveArr:
        if not isOppositeToLastMove(move):
            newMoves.append(move)
    return newMoves

def isOppositeToLastMove(move):
    if len(moves) > 0:
        if (move == "right" and moves[-1] == "left") or (move == "left" and moves[-1] == "right"): return True
        elif (move == "up" and moves[-1] == "down") or (move == "down" and moves[-1] == "up"): return True
        else: return False
    return False

def solveBeam(k):  
    global isBeamSearch, limit
    isBeamSearch = True
    limit = k
    print("Solving the state with beam search ")
    solveAStar("h2")

def maxNodes(n):
    global maxN
    maxN = n

def puzzleSolved():
    if generating == True:
        return
    print("STARTING STATE: ")
    printSpecState(initialState)
    print("ENDING STATE: ")
    printSpecState(globalState)
    print("Number of Moves:" + str(len(moves)))
    print("Moves performed:")
    movelist = ""
    count = 0
    for move in moves:
        if count == 0:
            movelist = move
        else:
            movelist = movelist + ", " + move
        count += 1
    print(movelist)

def readAndExecute():
    with open('test.txt', 'r') as text:
        commands = text.readlines()
        for c in commands:
            func = c.replace("\n","").split(" ")
            executeFunc(func)
        text.close()

def executeFunc(func):
    if func[0].lower().__contains__("set"):
        if len(func) < 4:
            print("Incorrect syntax")
        else:
            str = func[1] + " " + func[2] + " " + func[3]
            setState(str)
    elif func[0].lower().__contains__("print"):
        printState()
        return
    elif func[0].lower().__contains__("restart"):
        reset()
        return
    elif func[0].lower().__contains__("generate"):
        generateExperiments()
        return
    if len(func) < 2:
            print("Incorrect syntax")
    if func[0].lower().__contains__("random"):
        randomState(int(func[1]))
    elif func[0] == "move":
        move(func[1])
    elif func[0].lower().__contains__("astar"):
        solveAStar(func[1])
    elif func[0].lower().__contains__("max"):
        maxNodes(int(func[1]))
    elif func[0].lower().__contains__("beam"):
        solveBeam(int(func[1]))
    
    
def reset():
    global globalState, initialState, goalState, moves, states, numMoves, heurist, isBeamSearch, limit, maxN, totalNodes, randomizing
    globalState = "b12 345 678"
    initialState = ""
    goalState = "b12 345 678"
    moves = []
    states = []
    numMoves = 0
    heurist = ""
    isBeamSearch = False
    limit = 0
    totalNodes = 0
    randomizing = False

def generateExperiments():
    global seed, generating
    i, generating = 2, True
    h1totalNs, h1moveNum = [], 0
    h2totalNs, h2moveNum = [], 0
    beamtotalNs, beamMoveNum = [], 0
    h1moves = []
    h2moves = []
    beamMoves = []
    avgs = []
    avgMoves = []
    while (i < 25):
        k = 0
        h1totalNs, h1moveNum = [], 0
        h2totalNs, h2moveNum = [], 0
        beamtotalNs, beamMoveNum = [], 0
        h1moves = []
        h2moves = []
        beamMoves = []
        maxNodes(20000)
        random.seed(10)
        while(k < 100):
            seed = random.randrange(1,1000)
            reset()
            
            randomState(i)
            solveAStar("h1")
            h1nodes, h1moveNum = totalNodes, len(moves)

            reset()
            randomState(i)
            solveAStar("h2")
            h2nodes, h2moveNum = totalNodes, len(moves)

            reset()
            randomState(i)
            solveBeam(20)
            beamnodes, beamMoveNum = totalNodes, len(moves)

            h1totalNs.append(h1nodes)
            h1moves.append(h1moveNum)

            h2totalNs.append(h2nodes)
            h2moves.append(h2moveNum)

            beamtotalNs.append(beamnodes)
            beamMoves.append(beamMoveNum)
            k += 1
        avgs.append([math.floor(math.fsum(h1totalNs)/len(h1totalNs)), math.floor(math.fsum(h2totalNs)/len(h2totalNs)), math.floor(math.fsum(beamtotalNs)/len(beamtotalNs))])
        avgMoves.append([math.floor(math.fsum(h1moves)/len(h1moves)), math.floor(math.fsum(h2moves)/len(h2moves)), math.floor(math.fsum(beamMoves)/len(beamMoves))])
        i += 2
        
    maxNodes(8000)
    h1succ, h2succ, h3succ = [], [], []
    k = 0
    while(k < 100):
            seed = random.randrange(1,1000)
            reset()
            
            randomState(28)
            solveAStar("h1")
            if totalNodes < 7999:
                h1succ.append(1)
            else:
                h1succ.append(0)

            reset()
            randomState(28)
            solveAStar("h2")
            if totalNodes < 7999:
                h2succ.append(1)
            else:
                h2succ.append(0)

            reset()
            randomState(28)
            solveBeam(20)
            if totalNodes < 7999:
                h3succ.append(1)
            else:
                h3succ.append(0)
            k += 1

    print("Average Nodes generated for each search from d = 2 to d = 24 with 100 random samples each")
    print("\tH1 A* search\t H2 A* Search\t Local Beam Search k = 20")
    i = 2
    for l in avgs:
        print("d = " + str(i) + ": " + str(l[0]) + "\t\t  " + str(l[1]) + "\t\t" + str((l[2])))
        i += 2

    print("Average Solution Length for each search from d = 2 to d = 24 with 100 random samples each")
    print("\tH1 A* search\t H2 A* Search\t Local Beam Search k = 20")
    i = 2
    for p in avgMoves:
        print("d = " + str(i) + ": " + str(p[0]) + "\t\t  " + str(p[1]) + "\t\t" + str((p[2])))
        i += 2
    
    print("Success rate for each search for d = 28 with 100 random samples each")
    print("\tH1 A* search\t H2 A* Search\t Local Beam Search k = 20")
    i = 2
    print("d = 28: " + str(math.fsum(h1succ)/len(h1succ)) + "\t\t  " + str(math.fsum(h2succ)/len(h2succ)) + "\t\t" + str(math.fsum(h3succ)/len(h3succ)))
    i += 2
    
    generating = False

readAndExecute()