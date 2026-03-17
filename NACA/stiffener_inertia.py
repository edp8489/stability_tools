import numpy as np
from matplotlib import pyplot as plt

def stiffener_inertia(d, h, Kshear):
    if d > h:
        Iv_dt3 = 0.0217*(np.power(np.sqrt(Ks),8/3))
        return Iv_dt3

    Iv_dt3 = 0.0217/np.power(d/(h*np.sqrt(Ks)),8/3)
    return Iv_dt3

def stiffener_inertia_nondim(x):
    Iv_dt3 = 0.0217/np.power(x,8/3)
    return Iv_dt3

def shear_buckling_coeff(a_b, bc='hinged'):
    """
    Calculate shear buckling coefficient as function of side ratio a/b:
    Curve fit equation:
        x = a/b
        Ks = A + B * e^(-C*x)
    Parameters:
        Clamped: A = 9.6166; B = 40.3234; C = 2.0744
        Hinged: A = 5.6873; B = 25.3064; C = 1.8852
    """
    if bc not in ['hinged','clamped']:
        print(f"ERROR: Invalid boundary condition '{bc}'! Must be either 'hinged' or 'clamped'.")
        return None

    if bc == 'hinged':
        A = 5.6873
        B = 25.3064
        C = 1.8852
    
    if bc == 'clamped':
        A = 9.6166
        B = 40.3234
        C = 2.0744
    
    return A + B * np.exp(-C * a_b)

if __name__ == "__main__":
    d_hks = [0.02, 0.04, 0.05, 0.11, 0.16, 0.175]
    Iv_dt3 = [700, 100, 60, 8, 3, 2]

    #x = np.linspace(0.01,0.25,)
    x = np.arange(0.01,0.26,0.005)
    y = stiffener_inertia_nondim(x)

    plt.figure()
    plt.semilogy(d_hks, Iv_dt3, ".r")
    plt.semilogy(x,y,'--b',label="d < h")
    #plt.semilogy(x,y,'--k',label="d ? h")
    plt.grid(which="both", axis="y")
    plt.grid(which="both", axis="x")
    plt.xlabel("d / (h*sqrt(Ks))")
    plt.ylabel("Iv / (dt^3)")
    plt.title("Required Stiffener Bending Inertia")
    plt.show()