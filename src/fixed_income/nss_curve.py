import numpy as np
from numpy.typing import NDArray
from scipy.optimize import least_squares

# Implementing Nelson-Siegel and  Nelson-Siegel_Svensson curve fitting
# Preset Lambda and Mu decay parameters are:
# lambda = 0.2 -> tau_1 = 5 years
# mu = 0.1 -> tau_2 = 10 years


def nelson_siegel(
    t: NDArray[np.float64],
    b_0: float,
    b_1: float,
    b_2: float,
    lmbda: float,
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
    lmbda: float,
) -> NDArray[np.float64]:
    b_0, b_1, b_2 = params
    return nelson_siegel(maturities, b_0, b_1, b_2, lmbda) - rates


def nss_residuals(
    params: NDArray[np.float64],
    maturities: NDArray[np.float64],
    rates: NDArray[np.float64],
    lmbda: float,
    mu: float,
) -> NDArray[np.float64]:
    b_0, b_1, b_2, b_3 = params
    return nelson_siegel_svensson(maturities, b_0, b_1, b_2, b_3, lmbda, mu) - rates


def fit_ns(
    maturities: NDArray[np.float64],
    rates: NDArray[np.float64],
    *,
    lmbda: float = 0.2,
):

    ns_initial_guess = [rates[-1], 0.0, 0.0]  # b_0 is close to longest obsereved yield

    return least_squares(
        ns_residuals, ns_initial_guess, args=(maturities, rates, lmbda)
    )


def fit_nss(
    maturities: NDArray[np.float64],
    rates: NDArray[np.float64],
    *,
    lmbda: float = 0.2,
    mu: float = 0.1,
):
    nss_initial_guess = [
        rates[-1],
        0.0,
        0.0,
        0.0,
    ]  # b_0 is close to longest obsereved yield

    return least_squares(
        nss_residuals, nss_initial_guess, args=(maturities, rates, lmbda, mu)
    )
