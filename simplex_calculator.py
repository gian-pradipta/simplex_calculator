import re
import subprocess
try:
    from tabulate import tabulate
except ImportError:
    subprocess.run(["pip", "install", "tabulate"], check=True, text=True)
    from tabulate import tabulate

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

    
class SimplexTableu :
    def __init__(self, matrix : Matrix, headers : list, basis : list):
        self.data = matrix
        self.headers = headers
        self.basis = basis

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

    

    def tukar_basis(self, list_basis =[], entering=0, leaving=0):
        list_basis = self.basis
        leaving_ind = list_basis.index(leaving)
        list_basis[leaving_ind] = entering

    def find_column_pivot (self, matrix : Matrix=[]) :
        matrix = self.data
        top_row = matrix.container[0][:-1]
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




# remove whitespace
def remove_all_space(equation):
    return re.sub(r'\s+', '', equation)

def give_constant_to_variable(equation:str):
    matches = re.finditer(r"(?<!\d)[XSA](\d+)", equation)
    n = 0
    for match in matches:
        start = match.start()
        end = match.end()
        matched_text = "1" + match.group()
        equation = equation[:start+n] + "1" + equation[n+start:end+n] + equation[n+end:] 
        n += 1
    return equation


def normalize_objective_function(equation:str):
    equation = equation.split("=")
    if equation[1][0] != "-":
        equation[1] = "+" + equation[1]
    equation = "=".join(equation)
    final_equation = ""
    for i in equation:
        if i == "+":
            final_equation+= "-"
        elif i == "-":
            final_equation+="+"
        else:
            final_equation+=i
    final_equation = final_equation.split("=")
    final_equation = final_equation[0] + final_equation[1]+"="+"0"
    final_equation = remove_all_space(final_equation)
    final_equation = give_constant_to_variable(final_equation)
    return final_equation

def normalize(equations :list) :
    a_sum = 1
    s_sum = 1
    basis = []
    for i, equation in enumerate(equations):
        split_result = []
        pemisah = ''
        if len(equation.split("<=")) == 2 :
            pemisah = "<="
            split_result = equation.split("<=")
            split_result[0] += f"+1S{s_sum}"
            basis.append(f"S{s_sum}")
            s_sum += 1

        elif len(equation.split(">=")) == 2 :
            pemisah = ">="
            split_result = equation.split(">=")
            split_result[0] += f"-1S{s_sum}+1A{a_sum}"
            basis.append(f"A{a_sum}")
            s_sum += 1
            a_sum += 1
        
        elif len(equation.split("=")) == 2:
            pemisah = "="
            split_result = equation.split("=")
            split_result[0] += f"+1A{a_sum}"
            basis.append(f"A{a_sum}")
            a_sum += 1

        else :
            raise NameError

        equations[i] = pemisah.join(split_result)
        equations[i] = remove_all_space(equations[i])
        equations[i] = give_constant_to_variable(equations[i])
    equations.insert(0, basis)

def parse_token(equation):
    tokens = re.findall(r'-?\d*[XSA]\d+', equation)
    return tokens
#  (?<==)\d*
# \d+(?=[XSA])
# (?<!\d)[XSA](\d+)
def parse_number_from_tokens(tokens):
    return re.findall(r'-?\d+(?=[XSA])', ",".join(tokens))
def parse_variable_from_tokens(tokens):
    return re.findall(r'[XSA]\d+', ",".join(tokens))
def custom_sort_key(item):
    char, num = item[0], item[1:]
    return char, int(num)

def get_decision_variable(r) :
    l = []
    for i in r:
        l += parse_variable_from_tokens(parse_token(i))
    l = set(l)
    l = list(l)
    # # print(r[::-1]
    # print(constraints)
    l = sorted(l,key=custom_sort_key)
    x = []
    s = []
    a = []
    for i in range(len(l)):
        if l[i][0] == "A":
            a.append(l[i])
        elif l[i][0] == "X":
            x.append(l[i])
        elif l[i][0] == "S":
            s.append(l[i])
    return x + s + a
         

def make_matrix(constraints, objFunc):
    matrix = []
    decision_vars = get_decision_variable(constraints)
    constraints.insert(0, objFunc)
    for equation in constraints:
        row = []
        for i, var in enumerate(decision_vars):
            pattern = f"-?\\d+(?={var})"
            found = re.findall(pattern, equation)
            if len(found) == 0:
                row.append(0)
            else:
                row.append(int(found[0]))
        row.append(int(equation.split("=")[-1]))
        matrix.append(row)
        
    return matrix
def get_basis(headers):
    basis = ["Z"]
    s = 1
    # a = 1
    while True:
        a = f"S{s}"
        if a in headers:
            basis.append(a)
            s += 1
        else :
            break

    return basis

def do_linear_programming(objFunc, constraints):
    normalize(constraints)
    objFunc = normalize_objective_function(objFunc)
    # Headers
    basis = constraints.pop(0)

    headers = get_decision_variable(constraints)

    headers.insert(0, "Z")
    headers.insert(0, "basis")
    headers.append("Solution")
    # Basis
    basis.insert(0, "Z")
    if "A1" in basis:
        constraints.insert(0, basis)
        do_two_phase(objFunc, constraints)
        return
    matrix = make_matrix(constraints, objFunc)
    m : Matrix = Matrix(matrix)
    a : SimplexTableu = SimplexTableu(m, headers, basis)
    a.do_iteration()

def first_phase(constraints, objFunc):
    # normalize(constraints)
    
    objFunc = normalize_objective_function(objFunc)
    # print(objFunc)
    # Headers
    basis = constraints.pop(0)

    headers = get_decision_variable(constraints)
    headers.insert(0, "Z")
    headers.insert(0, "basis")
    headers.append("Solution")
    # Basis
    original_objFunc = objFunc
    objFunc = "Z="
    for i in basis:
        if i[0] == "A":
            objFunc += f"-{i}"
    objFunc = normalize_objective_function(objFunc)
    m : list = make_matrix(constraints, objFunc)
    m : Matrix = Matrix(m)
    st : SimplexTableu = SimplexTableu(m, headers, basis)
    basis = st.basis
    st.write_table()
    for i, row in enumerate(st.basis):
        if basis[i][0] == "A":
            st.data.apalah(0, i, 1)
    print("FASE 1")
    st.do_iteration()
    headers = st.headers[2:len(st.headers)]
    # print(headers)
    n = 0
    for i, var in enumerate(headers):
        if headers[i][0] == "A":
            for row in st.data.container:
                row.pop(i-n)
            # headers.pop(i)
            n +=1
    
    for var in headers:
        if var[0] == "A":
            st.headers.remove(var)
    # st.write_table()
    return st
def second_phase(st: SimplexTableu, objFunc):
    # print(",".join(parse_token(objFunc)))
    row = []
    for i, var in enumerate(st.headers[2:len(st.headers)-1]):
        pattern = f"-?\\d+(?={var})"
        found = re.findall(pattern, objFunc)
        if len(found) == 0:
            row.append(0)
        else:
            row.append(int(found[0]))
    row.append(0)
    st.data.container[0] = row
    basis = st.basis[1:]
    headers = st.headers[2:]
    # st.write_table()

    print("FASE 2")
    st.write_table()
    for i, var in enumerate(basis):
        col = headers.index(var)
        row = i+1
        st.data.apalah(0, row, st.data.container[0][col])

    st.do_iteration()

def do_two_phase(objFunc, constraints):
    st : SimplexTableu = first_phase(constraints,objFunc)
    second_phase(st, objFunc)

    
def main():
    print("ACCEPTED VARIABLE: X1, X2, X3, ..... Z")
    objFunc = input("Masukkan fungsi Objektif: ")
    n = int(input("Masukkan banyak constraint: "))
    constraints = []
    for i in range (n):
        equ = input(f"{i+1}. ")
        constraints.append(equ)

    do_linear_programming(objFunc, constraints)

if __name__ == "__main__":
    main()