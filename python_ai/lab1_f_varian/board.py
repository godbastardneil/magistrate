import copy

class Board:
    __width = 8
    __height = 8

    __chip = ['#', '@', ' ']
    __empty = __width*__height
    __plStep = [[], []]
    __cells  = []

    def chip(self):    return self.__chip
    
    def empty(self):   return self.__empty
    def plStep(self):  return copy.deepcopy(self.__plStep)

    def width(self):   return self.__width
    def height(self):  return self.__height

    def cells(self):   return copy.deepcopy(self.__cells)

    def __init__(self, tmp=None):
        if tmp is None:
            self.__plStep = [[(int(self.__height/2), int(self.__width/2)), (int((self.__height/2)-1), int((self.__width/2)-1))],
                                 [(int(self.__height/2), int(self.__width/2-1)), (int((self.__height/2)-1), int((self.__width/2)))]]
            self.__empty -= 4

            for i in range(self.__height):
                self.__cells.append([self.__chip[2]]*self.__width)
            self.__cells[self.__plStep[0][0][0]][self.__plStep[0][0][1]] = self.__chip[0]
            self.__cells[self.__plStep[0][1][0]][self.__plStep[0][1][1]] = self.__chip[0]
            self.__cells[self.__plStep[1][0][0]][self.__plStep[1][0][1]] = self.__chip[1]
            self.__cells[self.__plStep[1][1][0]][self.__plStep[1][1][1]] = self.__chip[1]
        elif type(tmp) == list:
            self.__cells = copy.deepcopy(tmp)
            self.__width = len(tmp[0])
            self.__height = len(tmp)

            self.__plStep = []
            self.__empty = self.__width*self.__height

            for i in range(self.__height):
                for j in range(self.__width):
                    if (self.__checkBeasy(i, j)):
                        self.__empty -= 1
                        if (self.__cells[i][j] == self.__chip[0]):
                            self.__plStep[0].append((i,j))
                        else:
                            self.__plStep[1].append((i,j))
        else:
            self.__cells = copy.deepcopy(tmp.cells())
            self.__empty = tmp.empty()
            self.__plStep = copy.deepcopy(tmp.plStep())

            self.__width = tmp.width()
            self.__height = tmp.height()

    def checkEndGame(self):
        return (self.__empty == 0 or self.__plStep[0] == [] or self.__plStep[1] == [])
    def getWinner(self):
        if (self.__empty == len(self.__plStep[0])): return 'Ничья'
        if (len(self.__plStep[0]) > len(self.__plStep[1])):
            return self.__chip[0]
        else:
            return self.__chip[1]

    def __checkOutBoard(self, i, j):
        return (i>=self.__height or j>=self.__width or i<0 or j<0)
    def __checkBeasy(self, i, j):
        return (not self.__cells[i][j] == self.__chip[2])

    def __checkLine(self, i, j, turn):
        inLine = []
        tmpLine = []
        for _i in range(i-1, i+2):
            for _j in range(j-1, j+2):
                if ((not self.__checkOutBoard(_i, _j)) and (self.__checkBeasy(_i, _j))):
                    if (not (self.__cells[_i][_j] == self.__chip[turn])):
                        ti = _i-i
                        tj = _j-j
                        i_ = _i+ti
                        j_ = _j+tj
                        tmpLine = [[_i, _j]]
                        while (i_ < self.__height and j_ < self.__width and i_ >= 0 and j_ >= 0):
                            if ((self.__checkOutBoard(i_, j_)) or (not self.__checkBeasy(i_, j_))):
                                tmpLine = []
                                break
                            if (self.__cells[i_][j_] == self.__chip[turn]):
                                inLine += tmpLine
                                break
                            tmpLine.append((i_, j_))
                            i_ += ti
                            j_ += tj
        return inLine

    def checkStep(self, i, j, turn):
        inLine = []
        try:
            if (self.__checkOutBoard(i, j)):
                raise Exception("Невозможная поле")
            if (self.__checkBeasy(i, j)):
                raise Exception("Поле занята")
            inLine = self.__checkLine(i, j, turn)
            if (inLine == []):
               raise Exception("Необходим непрерывный ряд") 
        except Exception as e:
            print(e)
        return inLine
        
    def findStep(self, turn):
        tmp = 1-turn
        steps = []
        for i in range(len(self.__plStep[tmp])):
            for _i in range(self.__plStep[tmp][i][0]-1, self.__plStep[tmp][i][0]+2):
                for _j in range(self.__plStep[tmp][i][1]-1, self.__plStep[tmp][i][1]+2):
                    if (not self.__checkOutBoard(_i, _j) and not self.__checkBeasy(_i, _j)):
                        inLine = self.__checkLine(_i, _j, turn)
                        if (not inLine == []):
                            steps.append((_i, _j, inLine))
        return steps

    def stepWithOutChecks(self, i, j, turn, inLine):
        if (inLine != []):
            self.__cells[i][j] = self.__chip[turn]

            l = len(inLine)
            for _i in range(l):
                self.__cells[inLine[_i][0]][inLine[_i][1]] = self.__chip[turn]

                self.__plStep[1-turn].remove((inLine[_i][0], inLine[_i][1]))
                self.__plStep[turn].append((inLine[_i][0], inLine[_i][1]))
            self.__plStep[turn].append((i, j))
            self.__empty -= 1

            return True
        else: return False
    def stepWithChecks(self, i, j, turn):
        inLine = self.checkStep(i, j, turn)
        return self.stepWithOutChecks(i, j, turn, inLine)


    def __printNumLine(self):
        _str = ' '
        for j in range(self.__width):
            _str += f'|{str(j+1)}'
        _str += '|\n'
        return _str

    def __str__(self):
        _str = self.__printNumLine()
        for i in range(self.__height):
            _str += ("-"*18+'\n')
            _str += str(i+1)
            for j in range(self.__width):
                _str += f'|{self.__cells[i][j]}'
            _str += "|\n"
        _str += ("-"*18+'\n')
        _str += self.__printNumLine()
        return _str
