import copy
import itertools
import sys

class Point:
    def __init__(self, x, y, code):
        self.x = x
        self.y = y
        self.code = code
        self.used = 0

    def equal(self, P):
        if self.x == P.x and self.y == P.y :
            return True
        else:
            return False
    def view(self):
        return '('+str(self.x)+','+str(self.y)+')'

class Line:
    def __init__(self, P1, P2):
        self.P1 = P1
        self.P2 = P2
        self.points = [P1,P2]

    def slope(self):
        if (self.P1.x - self.P2.x) == 0:
            return float('inf')
        f = (self.P1.y - self.P2.y)/(self.P1.x - self.P2.x)
        return f

    def isPointInLine(self, P,slope = 'any'):
        L1 = Line(self.P1,P)
        L2 = Line(self.P2,P)
        if (slope == 'any'):
            return L1.slope() == L2.slope()
        else:
            return (L1.slope() == L2.slope() and (L1.slope == 0 or L1.slope == float('inf')))

    def checkPointsOnLine(self, S):
        for s in S:
            if (s.equal(self.P1)==False) and (s.equal(self.P2)==False):
                if (self.isPointInLine(s)):
                    self.points.append(s)

    def sortPoints(self):
        self.points.sort(key=lambda x: x.code, reverse=False)

    def equalOnPointSet(self, L):
        if (len(self.points)!=len(L.points)):
            return False
        self.sortPoints()
        L.sortPoints()
        for i in range(0,len(self.points)):
            if self.points[i].code != L.points[i].code:
                return False
        return True

    def view(self):
        back = ''
        for p in self.points:
            back = back +p.view()
        back = back + '\n'
        return back


def allLines(PS, par):
    AllLines = []
    for i in range(0,len(PS)-1):
        for j in range(i+1,len(PS)):
            L = Line(PS[i], PS[j])
            if par == 'YES':
                if (abs(L.slope()) == 0 or L.slope() == float('inf')):
                    AllLines.append(L)
            else:
                AllLines.append(L)
    return AllLines

def getUniqueLines(LINES):
    _LINES = [LINES[0]]
    c = 0
    for L in LINES:
        c = c + 1
        for _L in _LINES:
            if L.equalOnPointSet(_L) == False:
                _LINES.append(L)
                break
    return _LINES

def readPointsFile(filepath):
    PointsSet = []
    c = 1
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            lineElements = line.strip().split()
            P = Point(float(lineElements[0]), float(lineElements[1]), c)
            c = c + 1
            PointsSet.append(P)
            line = fp.readline()
    return PointsSet

def removeItem(l, item):
    new_l = []
    for k in l:
        if k.code != item.code:
            new_l.append(k)
    return new_l

def insertItem(l, item):
    c = 0
    for k in l:
        if k.code == item.code:
            break
        c = c + 1
    if c < len(l):
        l.append(item)

def getAllCombinations(a_list):
    all_combinations = []
    for r in range(len(a_list) + 1):
        combinations_object = itertools.combinations(a_list, r)
        combinations_list = list(combinations_object)
        all_combinations += combinations_list
    return all_combinations

def combinations(target,data):
    allCombinations = []
    for i in range(len(data)):
        new_target = copy.copy(target)
        new_data = copy.copy(data)
        new_target.append(data[i])
        new_data = data[i+1:]
        allCombinations.append(new_target)
        combinations(new_target,new_data)
    return allCombinations

def isPointInList(L, s):
    for l in L:
        if (l.code == s.code):
            return True
    return False

def getUniques(L):
    newL = []
    for l in L:
        if (isPointInList(newL,l)==False):
            newL.append(l)
    return len(newL)

def solve(filename, parallel, grd):
    Solution = []
    points = readPointsFile(filename)
    lines = allLines(points,parallel)
    if grd == 'YES':
        new_points = points.copy()
        new_lines = lines.copy()
        for currentLine in new_lines:
            currentLine.checkPointsOnLine(new_points)
        new_lines = getUniqueLines(new_lines)
        new_lines.sort(key=lambda x: len(x.points), reverse=True)
        while len(new_points) > 1:
            Solution.append(new_lines[0])
            for j in new_points:
                for r in new_lines[0].points:
                    if j.code == r.code:
                        if j in new_points:
                            new_points = removeItem(new_points, j)
                            #new_points.remove(j)
                            break
            new_lines = allLines(new_points,parallel)
            for currentLine in new_lines:
                currentLine.checkPointsOnLine(new_points)
            new_lines.sort(key=lambda x: len(x.points), reverse=True)
        if len(new_points) == 1:
            lastElement = Line(new_points[0], new_points[0])
            Solution.append(lastElement)
    else:
        new_points = points.copy()
        new_lines = lines.copy()
        for currentLine in new_lines:
            currentLine.checkPointsOnLine(new_points)
        new_lines = getUniqueLines(new_lines)
        initSet = []
        for i in range(0,len(new_lines)):
            initSet.append(i)
        allCombs = getAllCombinations(initSet)
        betterSolution = []
        betterSolutionLen = len(points)+1
        for i in range(0,len(allCombs)):
            case = allCombs[i]
            allCombinationPoints = []
            for c in case:
                for d in new_lines[c].points:
                    allCombinationPoints.append(d)
                    if getUniques(allCombinationPoints) == len(points):
                        if betterSolutionLen > len(allCombs[i]):
                            betterSolutionLen = len(allCombs[i])
                            betterSolution = allCombs[i]
        for i in betterSolution:
            Solution.append(new_lines[i])
    return Solution


def main(argv):
    file = '-'
    p = 'NO'
    a = 'NO'

    if len(sys.argv)==2:
        file = argv[1]
    elif len(sys.argv)==3:
        if sys.argv[1] =='-f':
            p = 'YES'
        if sys.argv[1] == '-g':
            a = 'YES'
        file = sys.argv[2]
    elif len(sys.argv)==4:
        p = 'NO'
        a = 'NO'
        if sys.argv[1]=='-f' and sys.argv[2]=='-g':
            p = 'YES'
            a = 'YES'
        file = sys.argv[3]


    Solution = solve(file,p,a)
    for sol in Solution:
        print()
        print(sol.view())

if __name__ == "__main__":
   main(sys.argv[1:])
