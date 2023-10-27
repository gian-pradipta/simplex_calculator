from equation_parser import do_linear_programming 

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