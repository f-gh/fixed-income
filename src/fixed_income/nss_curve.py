# Implementing Nelson-Siegel curve fitting
# One lambda parameter which is fixed for data 

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import least_squares

maturities = np.array([0.0833, 0.125, 0.1666, 0.25, 0.3333, 0.5, 1, 2, 3, 5, 7, 10, 20, 30])
rates = np.array([0.0406, 0.041, 0.0413, 0.0417, 0.0426, 0.0427, 0.0444, 0.0478, 0.0491, 0.0501, 0.0512, 0.0524, 0.0564, 0.0561])



def nelson_siegel(t: NDArray[np.float64],
    b_0: float,
    b_1: float,
    b_2: float,
    lmbda: float) -> NDArray[np.float64]:
    """
    Calculating yields using the Nelson-Siegell model.
    t: Maturities in years (sorted from shortest to longest)
    b_0: long-term yield level
    b_1: slope component
    b2_2: curvature component
    lmbda: decay parameter
    """
    rate_t = b_0 + b_1 * ((1 - np.exp(-1 * lmbda * t)) / (lmbda * t)) + b_2 * ((1 - np.exp(-1 * lmbda * t)) / (lmbda * t) - np.exp(-1 * lmbda * t))
    return rate_t 

    
def residuals(
    params: NDArray[np.float64],
    maturities: NDArray[np.float64],
    rates: NDArray[np.float64]) -> NDArray[np.float64]:
    LMBDA = 0.1
    b_0, b_1, b_2 = params
    return nelson_siegel(maturities, b_0, b_1, b_2, LMBDA) - rates

initial_guess = [0.04, 0.01, 0.01]

res = least_squares(
    residuals,
    initial_guess,
    args=(maturities, rates)
)






