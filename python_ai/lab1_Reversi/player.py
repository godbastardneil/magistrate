from rev_board import Board
import time

class Player:
    __turn:int = 0
    def __init__(self, turn:Board.Value) -> None:
        self.__turn = turn

    def step(self, board:Board) -> bool:
        try:
            i = int(input(f"Введите координату по горизонтали для фишки {board.CHIPS[self.__turn]}: "))-1
            j = int(input(f"Введите координату по ветрикали для фишки {board.CHIPS[self.__turn]}: "))-1

            if (board.stepWithChecks(i, j, self.__turn)):
                return True
            else: raise Exception("")
        except Exception as e:
            print("Введите корректные координаты", e)
            return False

    def step(self, board:Board, steps) -> bool:
        try:
            i = int(input(f"Введите координату по горизонтали для фишки {board.CHIPS[self.__turn]}: "))-1
            j = int(input(f"Введите координату по ветрикали для фишки {board.CHIPS[self.__turn]}: "))-1

            for (_i, _j, inLine) in steps[self.__turn]:
                if (_i == i and _j == j):
                    if (board.stepWithOutChecks(i, j, self.__turn, inLine)):
                        return True
            return False
        except Exception as e:
            print("Введите корректные координаты", e)
            return False
