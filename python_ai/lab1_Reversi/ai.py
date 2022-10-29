from rev_board import Board
import copy

class Ai:
    __turn:int = 0
    __height:int = 0
    __min: int = -1000
    __max: int =  1000

    def __init__(self, turn: Board.Value, height:int) -> None:
        self.__turn = turn
        self.__height = height
    
    def __getScore(self, board: Board, steps:int, op_steps:int, height:int) -> int:
        score = board.count()[self.__turn]-board.count()[1-self.__turn]
        
        level = self.__height-height
        if ((board.count()[board.Value.EMPTY] == 0) or (steps == 0 and op_steps == 0)):
            if score >= 0:
                return self.__max*level
            else:
                return self.__min*level
        return ((steps - op_steps)*3 + score)*level

    def mathStep(self, board: Board, turn:int, steps, height:int) -> list[int, int, dict[Board.Direction, int], int]:
        #score = self.__getScore(board, len(steps[self.__turn]), len(steps[1-self.__turn]), height)
        score = None
        _i = 0
        _j = 0
        line = {}

        if (height > 0 and (steps[self.__turn] != [] or steps[1-self.__turn] != [])):
            #max_st = -9223372036854775808

            if (steps[turn] == []): turn = 1-turn
            for (i, j, inLine) in steps[turn]:
                tmp_board = Board(board)
                tmp_board.stepWithOutChecks(i, j, turn, inLine)
                tmp_steps = [board.findSteps(board.Value.FPL), board.findSteps(board.Value.SPL)]

                st = self.mathStep(tmp_board, 1-turn, tmp_steps, height-1)[3]
                
                if (score is None) or (turn == self.__turn and st > score) or (turn != self.__turn and st < score):
                    score = st
                    _i = i
                    _j = j
                    line = inLine
                #if (st > max_st):
                #    max_st = st
                #    _i = i
                #    _j = j
                #    line = inLine
            #score += max_st
        else: score = self.__getScore(board, len(steps[self.__turn]), len(steps[1-self.__turn]), height)
        return (_i, _j, line, score)
    
    def step(self, board: Board) -> bool:
        try:
            step = self.mathStep(board, self.__turn, board.findSteps(self.__turn), self.__height)

            if (board.stepWithOutChecks(step[0], step[1], self.__turn, step[2])):
                return True
            else: raise Exception("")
        except Exception as e:
            print("Введите корректные координаты", e)
            return False

    def step(self, board: Board, steps) -> bool:
        try:
            step = self.mathStep(copy.deepcopy(board), self.__turn, steps, self.__height)

            if (board.stepWithOutChecks(step[0], step[1], self.__turn, step[2])):
                return True
            else: raise Exception("")
        except Exception as e:
            print("Введите корректные координаты", e)
            return False
