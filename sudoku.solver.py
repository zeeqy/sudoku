class SudokuSolver(object):

    def __init__(self,sdk):
        self.sudoku = sdk
        self.size = len(sdk)
        self.unknown = self.search()

    def search(self):
        unknown = []
        for i in range(self.size):
            for j in range(self.size):
                if self.sudoku[i][j] == 0:
                    unknown.append([i,j])
        return unknown

    # extract python list's column
    def column(self,col):
        return [row[col] for row in self.sudoku]
    
    
    def find(self,coordinate,init):
        for num in range((init+1),10):
            if self.check(coordinate,num):
                return num
        return 0

    def check(self,coordinate,num):
        if num in self.sudoku[coordinate[0]] or num in self.column(coordinate[1]):
            return 0
        else:
            cube = []
            cindex = [int(coordinate[0]/3)*3, int(coordinate[1]/3)*3]
            for row in [0,1,2]:
                cube += self.sudoku[cindex[0]+row][cindex[1]:cindex[1]+3]
            if num in cube:
                return 0
        return 1
                
            
    def solve(self):
        vol = len(self.unknown)
        index = 0
        while(index < vol and index >=0):
            coordinate = self.unknown[index]
            r = self.find(coordinate,self.sudoku[coordinate[0]][coordinate[1]])
            if r != 0:
                self.sudoku[coordinate[0]][coordinate[1]] = r
                index += 1
            else:
                index -= 1
                self.sudoku[coordinate[0]][coordinate[1]] = 0 # !important
        return self.sudoku if index > 0 else "ERROR! No solution."
