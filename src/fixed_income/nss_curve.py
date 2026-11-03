import numpy as np
from numpy.typing import NDArray
from scipy.optimize import least_squares

# Implementing Nelson-Siegel and  Nelson-Siegel_Svensson curve fitting
# Lambda and Mu decay parameters are fixed for the data
LMBDA = 0.2  # lambda = 0.1 -> tau = 10 years
MU = 0.1  # lambda = 0.01 -> tau = 100 years

maturities = np.array(
    [0.0833, 0.125, 0.1666, 0.25, 0.3333, 0.5, 1, 2, 3, 5, 7, 10, 20, 30]
)
rates = np.array(
    [
        0.0406,
        0.041,
        0.0413,
        0.0417,
        0.0426,
        0.0427,
        0.0444,
        0.0478,
        0.0491,
        0.0501,
        0.0512,
        0.0524,
        0.0564,
        0.0561,
    ]
)


def nelson_siegel(
    t: NDArray[np.float64], b_0: float, b_1: float, b_2: float, lmbda: float
) -> NDArray[np.float64]:
    """
    Calculating yields using the Nelson-Siegel model.
    t: Maturities in years (sorted from shortest to longest)
    b_0: long-term yield level
    b_1: slope component
    b_2: curvature component
    lmbda: decay parameter
    """
    rate_t = (
        b_0
        + b_1 * ((1 - np.exp(-1 * lmbda * t)) / (lmbda * t))
        + b_2 * ((1 - np.exp(-1 * lmbda * t)) / (lmbda * t) - np.exp(-1 * lmbda * t))
    )
    return rate_t


def nelson_siegel_svensson(
    t: NDArray[np.float64],
    b_0: float,
    b_1: float,
    b_2: float,
    b_3: float,
    lmbda: float,
    mu: float,
) -> NDArray[np.float64]:
    """
    Calculating yields using the Nelson-Siegel-Svensson model.
    t: Maturities in years (sorted from shortest to longest)
    b_0: long-term yield level
    b_1: slope component
    b_2: first curvature component
    b_3: second curvature component
    lmbda: first decay parameter
    mu: second decay parameter
    """
    rate_t = (
        b_0
        + b_1 * ((1 - np.exp(-1 * lmbda * t)) / (lmbda * t))
        + b_2 * ((1 - np.exp(-1 * lmbda * t)) / (lmbda * t) - np.exp(-1 * lmbda * t))
        + b_3 * ((1 - np.exp(-1 * mu * t)) / (mu * t) - np.exp(-1 * mu * t))
    )
    return rate_t


def ns_residuals(
    params: NDArray[np.float64],
    maturities: NDArray[np.float64],
    rates: NDArray[np.float64],
) -> NDArray[np.float64]:
    b_0, b_1, b_2 = params
    return nelson_siegel(maturities, b_0, b_1, b_2, LMBDA) - rates


def nss_residuals(
    params: NDArray[np.float64],
    maturities: NDArray[np.float64],
    rates: NDArray[np.float64],
) -> NDArray[np.float64]:
    b_0, b_1, b_2, b_3 = params
    return nelson_siegel_svensson(maturities, b_0, b_1, b_2, b_3, LMBDA, MU) - rates


ns_initial_guess = [rates[-1], 0.0, 0.0]  # b_0 is close to longest obsereved yield

ns_res = least_squares(ns_residuals, ns_initial_guess, args=(maturities, rates))


nss_initial_guess = [
    rates[-1],
    0.0,
    0.0,
    0.0,
]  # b_0 is close to longest obsereved yield

nss_res = least_squares(nss_residuals, nss_initial_guess, args=(maturities, rates))


ns_rmse = np.sqrt(np.mean(ns_res.fun**2))
nss_rmse = np.sqrt(np.mean(nss_res.fun**2))

print(ns_res.x)
print(nss_res.x)
print(f"NS RMSE:  {ns_rmse * 10000:.2f} bps")
print(f"NSS RMSE: {nss_rmse * 10000:.2f} bps")
