import re
from SimplexTableu import SimplexTableu
from fractions import Fraction
from Matrix import Matrix
import math

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
def parse_decision_variable(tokens):
    return re.findall(r'X\d+', ",".join(tokens))
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
    decision_vars = list(set(parse_decision_variable(constraints)))
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
    a : SimplexTableu = SimplexTableu(m, headers, basis, decision_vars)
    a.do_iteration()
    # print(a.get_result())
    # for i, j in a.get_result().items():
    #     print(f"{i} = {float(Fraction(j))}")
    return a

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

def do_integer_programming(objFunc, constraints):
    stack = []
    a = do_linear_programming(objFunc, constraints)
    result = a.get_result()
    for var, value in result.items():
        if math.ceil(float(Fraction(value))) != math.floor(float(Fraction(value))):
            stack.append(Fraction(value))
    
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

