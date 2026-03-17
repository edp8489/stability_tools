from scipy import optimize as opt
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

K_shear = {
  "shear_buckling_coefficients": {
    "hinged_boundary_condition": {
      "data": [
        {"x": 1.00, "y": 9.68},
        {"x": 1.05, "y": 9.03},
        {"x": 1.53, "y": 7.00},
        {"x": 2.00, "y": 6.43},
        {"x": 3.00, "y": 5.83},
        {"x": 4.00, "y": 5.74},
        {"x": 5.00, "y": 5.54}
      ]
    },
    "clamped_boundary_condition": {
      "data": [
        {"x": 1.00, "y": 15.00},
        {"x": 1.14, "y": 13.00},
        {"x": 1.27, "y": 12.30},
        {"x": 1.40, "y": 11.80},
        {"x": 1.60, "y": 11.30},
        {"x": 1.68, "y": 11.00},
        {"x": 1.98, "y": 10.40},
        {"x": 2.57, "y": 9.82},
        {"x": 3.00, "y": 9.75},
        {"x": 3.51, "y": 9.59},
        {"x": 4.00, "y": 9.55},
        {"x": 4.42, "y": 9.55},
        {"x": 5.00, "y": 9.59}
      ]
    }
  }
}

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
    hinged_data = json_data['shear_buckling_coefficients']['hinged_boundary_condition']['data']
    boundary_conditions['hinged']['xPts'] = np.array([point['x'] for point in hinged_data])
    boundary_conditions['hinged']['yPts'] = np.array([point['y'] for point in hinged_data])

    # Parse clamped boundary condition data
    clamped_data = json_data['shear_buckling_coefficients']['clamped_boundary_condition']['data']
    boundary_conditions['clamped']['xPts'] = np.array([point['x'] for point in clamped_data])
    boundary_conditions['clamped']['yPts'] = np.array([point['y'] for point in clamped_data])

    return boundary_conditions

def exp_decay(x, A, B, C):
    return A + B * np.exp(-C * x)

def inverse_power(x,A,B):
    return A/np.power(x,B)

if __name__ == "__main__":
    # Parse the data
    parsed_data = parse_buckling_coefficients(K_shear)

    # Access the numpy arrays
    hinged_x = parsed_data['hinged']['xPts']
    hinged_y = parsed_data['hinged']['yPts']
    clamped_x = parsed_data['clamped']['xPts']
    clamped_y = parsed_data['clamped']['yPts']

    # attempt curve fit on data
    params_c, _ = opt.curve_fit(exp_decay, clamped_x, clamped_y)
    #params_2, _ = opt.curve_fit(inverse_power, clamped_x, clamped_y)
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