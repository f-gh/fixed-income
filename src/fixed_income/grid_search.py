import numpy as np

from fixed_income.nss_curve import fit_ns, fit_nss

lambda_values = np.arange(0.05, 1.05, 0.05)
mu_values = np.arange(0.05, 1.05, 0.05)


def ns_linesearch(
    maturities: NDArray[np.float64],
    rates: NDArray[np.float64],
    lambda_values: NDArray[np.float64],
):
    for lmbda in lambda_values:
        result = fit_nelson_siegel_svensson(
            maturities,
            rates,
            lmbda=lmbda,
            mu=mu,
        )


def nss_gridsearch(
    maturities: NDArray[np.float64],
    rates: NDArray[np.float64],
    lambda_values: NDArray[np.float64],
    mu_values: NDArray[np.float64],
):
    for lmbda in lambda_values:
        for mu in mu_values:
            result = fit_nelson_siegel_svensson(
                maturities,
                rates,
                lmbda=lmbda,
                mu=mu,
            )
