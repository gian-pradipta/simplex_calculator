from Matrix import Matrix
from tabulate import tabulate
from fractions import Fraction
class SimplexTableu :
    def __init__(self, matrix : Matrix, headers : list, basis : list, decision_vars:list=[]):
        self.data = matrix
        self.headers = headers
        self.basis = basis
        self.decision_vars = decision_vars

    def write_table(self, data=[], headers=[], tambahan1=[], tambahan2=[]):
        tambahan2 = self.basis
        tambahan1 = [1] + [0]*(len(self.basis)-1)
        data = self.data.return_matrix()
        headers = self.headers
        for i in range(len(data)) :
            if len(tambahan1) != 0:
                data[i].insert(0, tambahan1[i])
            if len(tambahan2) != 0:
                data[i].insert(0, tambahan2[i])
        
        table = tabulate(data, headers, tablefmt="grid")
        print(table)

    def get_result(self):
        kamus = dict()
        kamus[self.basis[0]] = self.data.return_matrix()[0][-1]
        for i in self.decision_vars:
            kamus[i] = 0
        
        for i, var in enumerate(self.basis):
            if var in kamus:
                kamus[var] = self.data.return_matrix()[i][-1]
        return kamus
    

    def tukar_basis(self, list_basis =[], entering=0, leaving=0):
        list_basis = self.basis
        leaving_ind = list_basis.index(leaving)
        list_basis[leaving_ind] = entering

    def find_column_pivot (self, matrix : Matrix=[], minimize = False) :
        matrix = self.data
        top_row = matrix.container[0][:-1]
        if minimize:
            top_row = list(map(lambda a: a*-1, top_row))
        min_num = min(top_row)
        if float(min_num) < 0:
            return matrix.container[0][:-1].index(min_num)
        else :
            return None
    def find_row_pivot (self, matrix : Matrix = []) :
        column = []
        matrix = self.data
        for row in matrix.container:
            column.append(row[-1])
        
        column_pivot = self.find_column_pivot(matrix)
        if column_pivot == None:
            return None
        min_nums = []
        for i in range(len(matrix.container)):
            if float(matrix.container[i][column_pivot]) > 0:
                min_nums.append((column[i]/matrix.container[i][column_pivot], i))
        
        min_num = sorted(min_nums)[0][-1]
        return min_num

    def do_iteration(self, m=[], basis=[], headers=[]) :
        m = self.data
        basis = self.basis
        headers = self.headers
        iterasi = 1
        print("Tabel Awal")
        self.write_table(m.return_matrix(), headers, tambahan2=basis, tambahan1= [1, 0, 0, 0])
        while True:
            row = self.find_row_pivot(m)
            column = self.find_column_pivot(m)
            if column != None or row != None:
                self.tukar_basis(basis, headers[2:len(headers)-1][column], basis[row])
                
                m.gaussian_jordan(row, column)
                print(f"iterasi-{iterasi}")
                self.write_table(m.return_matrix(), headers, tambahan2=basis, tambahan1= [1, 0, 0, 0])
                iterasi += 1 
            else :
                break

def main() :
    basis = ["z", "s1", "s2", "s3"]
    headers = ['basis', "z", 'x', 'x2','s1', 's1','s3', 'solution']
    M = 100
    m = Matrix([
        
# x+ 2y + S1  = 20
# 3x + 5y + S2  = 31
# 4x + 6y + S3  = 24
    #   [x  ,y  ,s1 , s2, s3, sol]
        [-1, -2, 0, 0,0, 0],
        [1, 2, 1, 0,0, 20],
        [3, 5, 0, 1,0, 31],
        [4, 6, 0, 0,1, 24]

    ])

    a : SimplexTableu = SimplexTableu(m, headers, basis)
    a.do_iteration()
    
if __name__ == "__main__":
    main()

