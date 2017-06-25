import random
import math
import progressbar
class SudokuGenerator(object):
    def __init__(self,dimention,difficulty):
        self.level = difficulty
        self.size = dimention
        
    def zerolistmaker(self,typ):
        if typ == 'dataframe':
            listofzeros = [[0 for j in range(self.size)] for i in range(self.size)]
        else:
            listofzeros = [[[] for j in range(self.size)] for i in range(self.size)]
        return listofzeros
    
    def search(self):
        unknown = []
        for i in range(self.size):
            for j in range(self.size):
                if self.dataframe[i][j] == 0:
                    unknown.append([i,j])
        return unknown
    
    def column(self,col):
        return [row[col] for row in self.dataframe]
    
    def find(self,coordinate):
        available = list(range(1,(self.size+1)))
        available = set(available) - set(self.trailframe[coordinate[0]][coordinate[1]])
        check = self.check(coordinate)
        available = list(available - check)
        if len(available) == 0:
            return 0
        else:
            return random.choice(available)

    def check(self,coordinate):
        rowcol = self.dataframe[coordinate[0]] + self.column(coordinate[1])
        cube_size = int(math.sqrt(self.size))
        cube = []
        cindex = [int(coordinate[0]/cube_size)*cube_size, int(coordinate[1]/cube_size)*cube_size]
        for row in range(cube_size):
            cube += self.dataframe[cindex[0]+row][cindex[1]:cindex[1]+cube_size]  
        return set(cube + rowcol)
    
    def generate(self):
        self.dataframe = self.zerolistmaker('dataframe')
        self.trailframe = self.zerolistmaker('trailframe')
        self.unknown = self.search()
        vol = len(self.unknown)
        index = 0
        bar = progressbar.ProgressBar(maxval=self.size*self.size, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Counter()])
        while(index < vol and index >=0):
            coordinate = self.unknown[index]
            self.dataframe[coordinate[0]][coordinate[1]] = 0
            r = self.find(coordinate)
            if r != 0:
                self.dataframe[coordinate[0]][coordinate[1]] = r
                self.trailframe[coordinate[0]][coordinate[1]].append(r)
                index += 1
            else:
                index -= 1
                self.dataframe[coordinate[0]][coordinate[1]] = 0 # !important
                self.trailframe[coordinate[0]][coordinate[1]] = []
            bar.update(index)
        bar.finish()
        self.sudoku = self.dataframe
        if self.level == 'easy':
            pazzle = random.sample(self.unknown,int(0.6*self.size*self.size))
        elif self.level == 'medium':
            pazzle = random.sample(self.unknown,int(0.7*self.size*self.size))
        elif self.level == 'hard':
            pazzle = random.sample(self.unknown,int(0.8*self.size*self.size))
        for cell in pazzle:
            self.sudoku[cell[0]][cell[1]] = 0
        return self.sudoku if index > 0 else "ERROR! No solution."
