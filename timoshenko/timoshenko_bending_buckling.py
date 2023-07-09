"""
Timoshenko bending-compression buckling module
Eric Peters
May 2023
"""

import sympy as sym

# create symbols for variables we don't use in the equation
#  D = (E*h**3)/(12(1-nu**2))
#  scr = sigma_cr
#  S = scr*(h)/(D*pi**2)
S = sym.symbols('S')

def minGreaterZero(values: list):
    # Given a list of values with real + imaginary parts,
    # returns the minimum value whose real part > 0
    minK = min(sym.re(k) for k in values if sym.re(k) > 0)
    return minK

def calcAlpha(Ntop, Nbot):
    """
    Calculates alpha, the load ratio between the top and bottom 
    edges of the part.
        alpha = 0 --> pure compression
        0 < alpha < 2 --> bending + compression
        alpha = 2 --> pure bending
        alpha > 2 --> Bending + tension
    """
    alpha = 1 - (Nbot/Ntop)
    return alpha

def cMatrix(a, b, alpha):
    C1 = (1 + (a/b)**2)**2 - S*(a**2)*(1-(alpha/2))
    C2 = -1*8*alpha*S*(a**2)*(2/9)/(sym.pi**2)
    C3 = 0
    C4 = C2
    C5 = (1 + 4*(a/b)**2)**2 - S*(a**2)*(1-(alpha/2))
    C6 = -1*8*alpha*S*(a**2)*(6/25)/(sym.pi**2)
    C7 = 0
    C8 = C6
    C9 = (1 + 9*(a/b)**2)**2 - S*(a**2)*(1-(alpha/2))

    Cmatrix = sym.Matrix([[C1, C2, C3],[C4, C5, C6],[C7, C8, C9]])
    return Cmatrix

def calcBucklingCoeff(Nfree, Nbase, a, b):
    # calculate alpha
    alpha = calcAlpha(Nfree, Nbase)
    print("alpha = {:.2f}".format(alpha))
    # calculate a/b ratio
    a_b = a/b
    print("a = {}, b = {}, a/b = {}".format(a, b, a_b))
    # generate coefficient matrix for user inputs
    # buckling coefficient K is found by solving equation det(C) = 0
    detC = cMatrix(a, b, alpha).det()
    # use sympy to solve system of equations det(C) = 0, returning [3x1] vector of solutions
    k_vals = sym.solve(detC)
    # we only care about the minimum solution (that's > 0)
    k_min = minGreaterZero(k_vals)

    # print("k = {:.2f} (a/b={:.2f}, alpha={:.2f})".format(k_b, a_b, alpha))
    print("k = {:.2f}".format(k_min))

if __name__ == "__main__":
    # print usage instructions
    instructions = """TIMOSHENKO BENDING-COMPRESSION BUCKLING TOOL
USAGE: function calcBucklingCoeff(Nfree, Nbase, a, b) is provided for convenience
    Nfree = running load (or stress) at top (free edge) of plate (stiffener)
    Nbase = running load (or stress) at base (supported edge) of plate (stiffener)
    a = length of long edge of plate (parallel to loading direction)
    b = height of short edge of plate (base to free edge)
    """
    print(instructions)

    # show validation problems
    # VALIDATION PROBLEM 1
    # a/b = 1, alpha = 2 --> k = 25.6
    ab_v1 = 1
    k_v1 = sym.solve(cMatrix(1,1,2).det())
    k_v1 = minGreaterZero(k_v1)
    error_v1 = (k_v1 - 25.6)/25.6
    print("Validation Example 1\n(a/b = 1, alpha = 2)")
    print("computed k = {:.2f}".format(k_v1))
    print("expected k = 25.6")
    print("error: {:.1f}%\n".format(error_v1*100))


    # VALIDATION PROBLEM 2
    # a/b = 1.5, alpha = 1 --> k = 8.4
    ab_v2 = 1.5
    k_v2 = sym.solve(cMatrix(1.5,1,1).det())
    k_v2 = minGreaterZero(k_v2)
    error_v2 = (k_v2 - 8.4)/8.4
    print("Validation Example 2:")
    print("a/b = 1.5, alpha = 1")
    print("computed k = {:.2f}".format(k_v2))
    print("expected k = 8.4")
    print("error: {:.1f}%".format(error_v2*100))