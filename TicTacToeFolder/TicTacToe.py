# coding: utf-8
'''
Created on 2018. 5. 2.

@author: Insup Jung
'''

import random
from copy import copy, deepcopy
from matplotlib.style.core import available
import csv

EMPTY = 0;
PLAYER_X = 1
PLAYER_O = 2
DRAW = 3
BOARD_FORMAT = "----------------------------\n| {0} | {1} | {2} |\n|\
--------------------------|\n| {3} | {4} | {5} |\n|\
--------------------------|\n| {6} | {7} | {8} |\n\
----------------------------"
NAMES = ['','X','O']

#Board를 그려주는 함수, state를 받아 1부터 9 중에 한 곳에 넣어준다.
def printboard(state):
    cells=[]
    for i in range(3):
        for j in range(3):
            cells.append(NAMES[state[i][j]].center(6))
    
    print(BOARD_FORMAT.format(*cells)) #가변인자... 자바에서 오버로딩이라 생각하면 되겠다
    
def emptystate():
    return [[EMPTY, EMPTY, EMPTY],[EMPTY, EMPTY, EMPTY],[EMPTY, EMPTY, EMPTY]]

def gameover(state):
    for i in range(3):
        if state[i][0] !=EMPTY and state[i][0] == state[i][1] and state[i][0] == state[i][2]:
            return state[i][0]
        
        if state[0][i] != EMPTY and state[0][i] == state[1][i] and state[0][i] == state[2][i]:
            return state[0][i]
        
    if state[0][0] != EMPTY and state[0][0] == state[1][1] and state[1][1] == state[2][2]:
        return state[0][0]
    
    if state[0][2] != EMPTY and state[0][2] == state[1][1] and state[1][1] == state[2][0]:
        return state[0][2]
    
    #판이 비었는지가 왜 필요한거지??
    for i in range(3):
        for j in range(3):
            if state[i][j]==EMPTY:
                return EMPTY
    
    return DRAW

class Human(object):
    def __init__(self, player):
        self.player = player
        
    def action(self, state):
        printboard(state)
        action = None
        while action not in range(1,10):
            action = int(input('Your move? '))
        switch_map = {
            1 : (0, 0),
            2 : (0, 1),
            3 : (0, 2), 
            4 : (1, 0), 
            5 : (1, 1),
            6 : (1, 2),
            7 : (2, 0),
            8 : (2, 1),
            9 : (2, 2)
            }
        return switch_map[action]
    
    def episode_over(self, winner):
        if winner == DRAW:
            print('DRAW')
        else:
            print('Player {}'.format(winner))
    

def play(agent1, agent2):
    state = emptystate()
    for i in range(9):
        if i%2 == 0:
            move = agent1.action(state)
            print(move)
        else:
            move = agent2.action(state)
        state[move[0]][move[1]] = (i%2)+1
        winner = gameover(state)
        if winner != EMPTY:
            return winner
    
    return winner

class Computer(object):
    def __init__(self, player):
        self.player = player
        self.values = {}
        self.readCSV()
        self.verbose = True
        
    def readCSV(self):
        file=open("D:\java-neon\eclipse\python\AnyPrac\AnyPractice\learn_data\learn_data.csv", 'r')
        ttt_list = csv.reader(file)
        for t in ttt_list:
            try:
                self.values[((int(t[0]), int(t[1]), int(t[2]), int(t[3]), int(t[4]), int(t[5]), int(t[6]), int(t[7]), int(t[8])))] = float(t[10])
            except ValueError:
                continue
        
    def random(self, state):
        available = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == EMPTY:
                    available.append((i,j))
        return random.choice(available)
    
    def greedy(self, state):
        maxval = -50000
        maxmove = None
        
        if self.verbose:
            cells = []
        for i in range(3):
            for j in range(3):
                if state[i][j]==EMPTY:
                    state[i][j]=self.player
                    val = self.lookup(state)
                    state[i][j] = EMPTY
                    
                    if val>maxval:
                        maxval = ValueError
                        maxmove = (i, j)
                    
                    if self.verbose:
                        cells.append('{0:.3f}'.format(val).center(6))
                elif self.verbose:
                    cells.append(NAMES[state[i][j]].center(6))
        
        if self.verbose:
            print(BOARD_FORMAT.format(*cells))
        
        return maxmove
    
    def lookup(self, state):
        key = self.statetuple(state)
        
        if not key in self.values:
            self.add(key)
        
        return self.values[key]
    
    def add(self, state):
        winner = gameover(state)
        tup = self.statetuples(state)
        self.values[tup] = self.winnerval(winner)
    
    def statetuple(self, state):
        return (tuple(state[0], tuple(state[1]), tuple(state[2])))  
    
    
    def action(self, state):
        printboard(state)
        action = None
        move = self.random(state)
        state[move[0]][move[1]] = self.player
        return move
    
    def winnerval(self, winner):
        if winner==self.player:
            return 1
        elif winner==EMPTY:
            return 0.5
        elif winner==DRAW:
            return 0
        else:
            return self.lossval
    
    def episode_over(self, winner):
        if winner == DRAW:
            print('DRAW')
        else:
            print('Player {}'.format(winner))
                   
if __name__ == "__main__":
    p1 = Human(1)
    p2 = Computer(2)
    
    while True:
        winner = play(p1, p2)
        p1.episode_over(winner)
        p2.episode_over(winner)

