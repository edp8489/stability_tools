from scipy import optimize as opt
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import json
from pathlib import Path

data_points = Path("assets/compression_buckling.json")

def parse_buckling_coefficients(json_data):
    """
    Parses the shear buckling coefficients JSON data into numpy vectors for each boundary condition.

    Args:
        json_data (dict): The JSON object containing shear buckling coefficients.

    Returns:
        dict: A dictionary with keys 'hinged' and 'clamped', each containing numpy arrays for x and y data.
    """
    # Initialize dictionaries to hold the numpy arrays
    boundary_conditions = {
        'hinged': {'xPts': None, 'yPts': None},
        'clamped': {'xPts': None, 'yPts': None}
    }

    # Parse hinged boundary condition data
    hinged_data = json_data['ss_edges']['data']
    boundary_conditions['hinged']['xPts'] = np.array([point['x'] for point in hinged_data])
    boundary_conditions['hinged']['yPts'] = np.array([point['y'] for point in hinged_data])

    # Parse clamped boundary condition data
    clamped_data = json_data['clamped_edges']['data']
    boundary_conditions['clamped']['xPts'] = np.array([point['x'] for point in clamped_data])
    boundary_conditions['clamped']['yPts'] = np.array([point['y'] for point in clamped_data])

    return boundary_conditions

def exp_decay(x, A, B, C):
    return A + B * np.exp(-C * x)

def inverse_power(x,A,B):
    return A/np.power(x,B)

if __name__ == "__main__":
    # Parse the data
    with open(data_points, mode='r') as f:
        json_data = json.load(f)
    parsed_data = parse_buckling_coefficients(json_data)

    # Access the numpy arrays
    hinged_x = parsed_data['hinged']['xPts']
    hinged_y = parsed_data['hinged']['yPts']
    clamped_x = parsed_data['clamped']['xPts']
    clamped_y = parsed_data['clamped']['yPts']

    # attempt curve fit on data
    params_c, _ = opt.curve_fit(exp_decay, clamped_x, clamped_y)
    params_h, _ = opt.curve_fit(exp_decay, hinged_x, hinged_y)

    # print parameters
    print("Curve fit equation:")
    print("\tA + B * e^(-C*x)")
    print("Parameters:")
    print(f"\tClamped: A = {params_c[0]:.4f}; B = {params_c[1]:.4f}; C = {params_c[2]:.4f}")
    print(f"\tHinged: A = {params_h[0]:.4f}; B = {params_h[1]:.4f}; C = {params_h[2]:.4f}")

    x_cf = np.linspace(0.5,5.5)

    plt.figure()
    plt.plot(clamped_x, clamped_y,"xk",label="Clamped")
    plt.plot(hinged_x, hinged_y,"xr",label="Hinged")
    plt.plot(x_cf, exp_decay(x_cf,*params_c),'--b',label='Clamped Curve Fit')
    plt.plot(x_cf, exp_decay(x_cf,*params_h),'--r',label='Hinged Curve Fit')
    plt.legend(loc="best")
    plt.xlabel("a/b")
    plt.ylabel("Ks")
    plt.xlim(0,6)
    plt.ylim(0,16)
    plt.grid(which="major",axis="both")


    plt.show()