#!/usr/bin/env python

"""Conway's Game of life, implemented in Python

author: Anthony Castiglia
email:  castiglia.anthony@gmail.com
"""

import os
import random
import sys
from argparse import ArgumentParser
from itertools import product
from time import sleep

NEIGHBOR_COORDINATES = [(-1, -1), (-1, 0), (-1, 1), (0, 1), 
                        (1, 1), (1, 0), (1, -1), (0, -1)]

class World(object):
    def __init__(self, w, h, state=None, cell_repr='+'):
        self.height = h
        self.width = w
        self.cells = [[False for j in range(w)] for i in range(h)]
        self.cell_repr = cell_repr
        
        if state is not None:
            for i, j in state:
                self.cells[i][j] = True

    def neighbors(self, i, j):
        for m, n in NEIGHBOR_COORDINATES:
            yield self.cells[(i+m) % self.height][(j+n) % self.width]


    def advance(self):
        next_cells = [[False for j in range(self.width)] 
                      for i in range(self.height)]

        for (i, j) in product(range(self.height), range(self.width)):
            n = sum(int(neighbor) for neighbor in self.neighbors(i, j))

            next_cells[i][j] = \
                (self.cells[i][j] and (n >= 2 and n <= 3)) or (n == 3)

        self.cells = next_cells

    def __str__(self):
        cell_strs = [[self.cell_repr if c else ' ' for c in row] 
                     for row in self.cells]
        return '\n'.join([' '.join(row) for row in cell_strs])

    def run(self):
        while(True):
           os.system('clear')
           print world
           world.advance()
           sleep(0.17)       
               
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-r', '--random', action='store_true', dest='rand', 
                        default=True, help='randomize the board\'s initial '
                        +'state')
    parser.add_argument('--height', action='store', type=int, dest='h',
                        default=24, help='height of the board')
    parser.add_argument('--width', action='store', type=int, dest='w',
                        default=80, help='width of the board')
    parser.add_argument('--density', action='store', type=float, dest='d',
                        default=0.5, help='specify the approximate initial '
                        +'density of live cells')
    parser.add_argument('--repr', action='store', type=str, dest='rep',
                        default='+', help='specify the character or string ' 
                        +'used to represent each cell')

    args = parser.parse_args()
    
    if args.rand:
        population = args.h * args.w * args.d
        initial_state = \
            zip([random.randint(0, args.h-1) for i in range(int(population))], 
                [random.randint(0, args.w-1) for i in range(int(population))])
    else:
        initial_state = [(2, 0), (2, 1), (2, 2), (1, 2), (0, 1)] 

    world = World(args.w, args.h, initial_state, args.rep)
    
    while(True):
        try:
            os.system('clear')
            print world
            sys.stdout.flush() # smoother animation
            world.advance()
            sleep(0.05)
        except KeyboardInterrupt:
            exit(0)
