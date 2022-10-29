from rev_board import Board
from ai import Ai
from player import Player
import os

def statistic(board:Board):
    os.system('cls||clear')
    print(board)
    print(f'Фишка {board.CHIPS[board.Value.FPL]}', board.count()[board.Value.FPL])
    print(f'Фишка {board.CHIPS[board.Value.SPL]}', board.count()[board.Value.SPL])

# сделать поиск путей для завершения игры
def game(board:Board, play):
    turn = 0
    steps = [board.findSteps(board.Value.FPL), board.findSteps(board.Value.SPL)]
    statistic(board)
    while(True):
        statistic(board)
        try:
            while (not play[turn].step(board, steps)):
                statistic(board)
        except:
            print("Введите корректные координаты")
        
        if (board.count()[board.Value.EMPTY] == 0
            or board.count()[board.Value.FPL] == 0
            or board.count()[board.Value.SPL] == 0): break

        steps[0] = board.findSteps(board.Value.FPL)
        steps[1] = board.findSteps(board.Value.SPL)
        print(steps[0])
        print(steps[1])
        print(board.count())
        if (steps[1-turn] == []):
            if (steps[turn] == []):
                break
        else: turn = 1-turn

def PlVsAlg(board:Board):
    turn = 0
    alg = -1
    while (alg < 0 or alg > 1):
        alg = int(input(f"Введите порядок хода ИИ: "))-1

    aiplay:Ai   = Ai(alg)
    play:Player = Player(alg)
    steps = [board.findSteps(board.Value.FPL), board.findSteps(board.Value.FPL)]
    while(True):
        print(board)
        print(f'Фишка {board.CHIPS[board.Value.FPL]}', board.count()[board.Value.FPL])
        print(f'Фишка {board.CHIPS[board.Value.SPL]}', board.count()[board.Value.SPL])
        try:
            if (turn == alg):
                while (not play.step(board, steps[turn])):
                    continue
            else:
                while (not aiplay.step(board, steps[turn])):
                    continue
        except:
            print("Введите корректные координаты")
        
        if (board.count()[board.Value.EMPTY] == 0): break

        steps[turn] = board.findSteps(turn)
        steps[1-turn] = board.findSteps(1-turn)
        if (steps[1-turn] == []):
            if (steps[turn] == []):
                break
        else: turn = 1-turn
    print(board)

def AlgVsAlg(board:Board):
    play = [Ai(board.Value.FPL), Ai(board.Value.SPL)]
    turn = Board.Value.FPL
    steps = [board.findSteps(turn), board.findSteps(1-turn)]
    while(True):
        print(board)
        print(f'Фишка {board.CHIPS[board.Value.FPL]}', board.count()[board.Value.FPL])
        print(f'Фишка {board.CHIPS[board.Value.SPL]}', board.count()[board.Value.SPL])
        try:
            while (not play[turn].step(board, steps[turn])):
                continue
        except:
            print("Введите корректные координаты")
        
        if (board.count()[board.Value.EMPTY] == 0): break

        steps[turn] = board.findSteps(board.Value.FPL)
        steps[1-turn] = board.findSteps(board.Value.SPL)
        if (steps[1-turn] == []):
            if (steps[turn] == []):
                break
        else: turn = 1-turn
    print(board)

board:Board = Board()

print('----')
print(board)

alg_height = 4
menu = int(input(f"1. Игрок против игрока\n2. Игрок против компьютера\n3. Компьютер против компьютера (~)\n Введите: "))

if (menu == 1):
    game(board, [Player(Board.Value.FPL),Player(Board.Value.SPL)])
elif (menu == 2):
    alg = -1
    while (alg < 0 or alg > 1):
        alg = int(input(f"Введите порядок хода ИИ: "))-1
    if (alg == 0):
        game(board, [Ai(Board.Value.FPL, alg_height),Player(Board.Value.SPL)])
    else:
        game(board, [Player(Board.Value.FPL),Ai(Board.Value.SPL, alg_height)])
else:
    game(board, [Ai(Board.Value.FPL, alg_height),Ai(Board.Value.SPL, alg_height)])

print('Победитель: ', board.getWinner())