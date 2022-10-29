from enum import IntEnum
import copy

class Board:
    class Value(IntEnum):
        FPL = 0,
        SPL = 1,
        EMPTY = 2
    class Direction(IntEnum):
        LEFT = 0,
        RIGHT = 1,
        UP = 2,
        DOWN = 3,
        UP_LEFT = 4,
        UP_RIGHT = 5,
        DOWN_LEFT = 6,
        DOWN_RIGHT = 7
    __STEPS: dict[Direction, tuple[int, int]] = {
        Direction.LEFT: (0, -1),
        Direction.RIGHT: (0, 1),
        Direction.UP: (1, 0),
        Direction.DOWN: (-1, 0),
        Direction.UP_LEFT: (-1, -1),
        Direction.UP_RIGHT: (-1, 1),
        Direction.DOWN_LEFT: (1, -1),
        Direction.DOWN_RIGHT: (1, 1)
    }
    __SIZE = 8
    __cells = []

    CHIPS = {
        Value.FPL: "#",
        Value.SPL: "@",
        Value.EMPTY: " "
    }
    __count = {
        Value.FPL: 0,
        Value.SPL: 0,
        Value.EMPTY: __SIZE*__SIZE
    }
    def count(self): return self.__count
    def cells(self): return copy.deepcopy(self.__cells)
    def getWinner(self):
        if (self.__count[self.Value.FPL] > self.__count[self.Value.SPL]):
            return self.CHIPS[self.Value.FPL]
        elif (self.__count[self.Value.FPL] < self.__count[self.Value.SPL]):
            return self.CHIPS[self.Value.SPL]
        return 'НИЧЬЯ'

    def __init__(self, board=None) -> None:
        if (board is None):
            self.__cells = [self.Value.EMPTY] * self.__SIZE
            for i in range(self.__SIZE):
                self.__cells[i] = [self.Value.EMPTY] * self.__SIZE
            
            coord = int(self.__SIZE/2)
            self.__setValue(coord,   coord,   self.Value.FPL)
            self.__setValue(coord-1, coord-1, self.Value.FPL)
            self.__setValue(coord,   coord-1, self.Value.SPL)
            self.__setValue(coord-1, coord,   self.Value.SPL)
        else:
            self.__cells = copy.deepcopy(board.cells())
            self.__count = copy.deepcopy(board.count())
    
    def __setValue(self, i:int, j:int, chip:Value) -> None:
        if (self.__cells[i][j] != chip):
            if (self.__cells[i][j] == self.Value.EMPTY):
                self.__count[self.Value.EMPTY] -= 1
            else:
                self.__count[self.Value(1-chip)] -= 1
            self.__cells[i][j] = chip
            self.__count[chip] += 1

    def __checkOutBoard(self, i:int, j:int) -> bool:
        return (i>=self.__SIZE or j>=self.__SIZE or i<0 or j<0)
        
    def __checkEmpty(self, i:int, j:int) -> bool:
        return (self.__cells[i][j] == self.Value.EMPTY)

    def __checkLine(self, i:int, j:int, turn:Value) -> dict[Direction, int]:
        inLine: dict[self.Direction, int] = {}

        for direct in self.Direction:
            roll = 0
            _i, _j = self.__STEPS[direct]

            for k in range(1, self.__SIZE):
                i_ = i+k*_i
                j_ = j+k*_j
                if (self.__checkOutBoard(i_, j_) or self.__checkEmpty(i_, j_)):
                    roll = 0
                    break

                if (self.__cells[i_][j_] == turn): break
                roll += 1
            if (roll > 0 and roll < self.__SIZE-1): inLine[direct] = roll
        return inLine
    def __checkStep(self, i:int, j:int, turn:Value) -> dict[Direction, int]:
        inLine: dict[self.Direction, int] = {}
        try:
            if (self.__checkOutBoard(i, j)):
                raise Exception("Невозможная поле")
            if (not self.__checkEmpty(i, j)):
                raise Exception("Поле занята")
            
            inLine = self.__checkLine(i, j, turn)
            if (inLine == {}):
                raise Exception("Нет не прирывной линии")
        except Exception as e:
            #print(e)
            return inLine
        return inLine
            
    def stepWithOutChecks(self, i:int, j:int, turn:Value, inLine:dict[Direction, int]) -> bool:
        status = False
        if (not inLine == {}):
            self.__setValue(i, j, turn)

            for (direct, roll) in inLine.items():
                if roll > 0:
                    _i, _j = self.__STEPS[direct]
                    for k in range(1, roll+1):
                        i_ = i+k*_i
                        j_ = j+k*_j
                        self.__setValue(i_, j_, turn)
                    status = True

        return status
     
    def stepWithChecks(self, i:int, j:int, turn:Value) -> bool:
        inLine = self.__checkStep(i, j, turn)
        return self.stepWithOutChecks(i, j, turn, inLine)
 
    def findSteps(self, turn:Value) -> list[int, int, dict[Direction, int]]:
        steps = []
        if (self.__count[turn] != 0):
            for i in range(0, self.__SIZE):
                for j in range(0, self.__SIZE):
                    if (self.__checkEmpty(i, j)):
                        inLine = self.__checkStep(i, j, turn)
                        if inLine != {}:
                            steps.append((i, j, inLine))

        return steps

    def __printNumLine(self):
        _str = ' '
        for j in range(self.__SIZE):
            _str += f'|{str(j+1)}'
        _str += '|\n'
        return _str
    def __str__(self):
        _str = self.__printNumLine()
        for i in range(self.__SIZE):
            _str += ("-"*18+'\n') + str(i+1)
            for j in range(self.__SIZE):
                _str += f'|{self.CHIPS[self.__cells[i][j]]}'
            _str += "|\n"
        _str += ("-"*18+'\n') + self.__printNumLine()
        return _str
