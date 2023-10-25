from fractions import Fraction
import copy
class Matrix :
    def __init__(self, matrix):
        self.container = matrix
    
    def add_two_lists(self, list1, list2):
        for i in range(len(list1)):
            list1[i] += list2[i]
    def substract_two_lists(self, list1, list2):
        for i in range(len(list1)):
            list1[i] -= list2[i]

    def add_line1_with_line2(self, index1, index2):
        self.add_two_lists(self.container[index1],  self.container[index2])

    def subtract_line1_with_line2(self, index1, index2):
        self.substract_two_lists(self.container[index1],  self.container[index2])

    def apalah(self, index1, index2, angka):
        copy_of_container = copy.deepcopy(self.container)
        line2 = map(lambda a: a*angka, copy_of_container[index2],)
        self.substract_two_lists(self.container[index1],list(line2))
    def write_matrix(self):
        for row in self.container:
            line = map(lambda a: str(a), row)
            print(list(line))

    def return_matrix(self):
        result = []
        for row in self.container:
            line = map(lambda a: str(a), row)
            result.append(list(line))
        return result

    def gaussian_jordan (self, row, column):
        center = self.container[row][column]
        result = map(lambda a: Fraction(a) / Fraction(center) ,self.container[row])
        self.container[row] = list(result)

        number_of_lines = len(self.container)
        for line in range(number_of_lines):
            if line != row:
                angka = self.container[line][column]
                self.apalah(line, row, angka)

    