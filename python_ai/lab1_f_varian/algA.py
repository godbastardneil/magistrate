from board import Board
import copy
import time

class AlgA:
    __turn = 0

    def __init__(self, turn):
        self.__turn = turn

    def __getScore(self, boa):
        return (len(boa.plStep()[self.__turn])-len(boa.plStep()[1-self.__turn]))

    def mathStep(self, boa, turn, steps, height):
        val = self.__getScore(boa)
        i = 0
        j = 0
        inline = 0

        if (height > 0 and not boa.checkEndGame() and not steps == []):
            max_st = -9223372036854775808
            
            tmp_cells = []
            for i in range(len(steps)):
                tmp_cells.append(Board(boa))

            for k in range(len(steps)):
                tmp_cells[k].stepWithOutChecks(steps[k][0], steps[k][1], turn, steps[k][2])
                st = self.mathStep(tmp_cells[k], 1-turn, tmp_cells[k].findStep(1-turn), height-1)[3]
                if (st > max_st):
                    max_st = st
                    i = steps[k][0]
                    j = steps[k][1]
                    inline = steps[k][2]
            val += max_st
        return [i, j, inline, val]