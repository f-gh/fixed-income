import numpy as np
import pandas as pd
from numpy.typing import NDArray

from fixed_income.nss_curve import fit_ns, fit_nss


# This helper function selects the best lambda or lambda and mu and their betas based on 3 error criteria
def select_best_fits(search_result):
    search_result = {
        key: value for key, value in search_result.items() if value["success"]
    }

    if not search_result:
        raise ValueError("No successful optimization results.")

    criteria = ["RMSE", "MAE", "Max error"]

    best_fits = {}

    for criterion in criteria:
        best_key, best_result = min(
            search_result.items(),
            key=lambda item: item[1][criterion],
        )

        best_fits[criterion] = {
            "parameters": best_key,
            "result_vector": best_result["betas"],
            "criterion_value": best_result[criterion],
        }

    rows = []

    for criterion, result in best_fits.items():
        params = result["parameters"]

        if isinstance(params, tuple):
            lmbda, mu = params
        else:
            lmbda, mu = params, np.nan

        row = {
            "Criterion": criterion,
            "Lambda": lmbda,
            "Mu": mu,
            "Criterion Value": result["criterion_value"],
        }

        for i, beta in enumerate(result["result_vector"]):
            row[f"Beta{i}"] = beta
        rows.append(row)

    return pd.DataFrame(rows).set_index("Criterion").round(4)


# Line search for finding best lambda for ns model based on 3 criteria:
# RMSE: Root Mean Square Error
# MAE: Mean Absolute Error
# Maximum residual
# Mean of residuals


def ns_linesearch(
    maturities: NDArray[np.float64],
    rates: NDArray[np.float64],
    lambda_values: NDArray[np.float64] | None = None,
):

    if lambda_values is None:
        lambda_values = np.round(np.arange(0.05, 1.05, 0.05), 2)

    search_result = {}
    for lmbda in lambda_values:
        result = fit_ns(
            maturities,
            rates,
            lmbda=lmbda,
        )
        search_result[lmbda] = {
            "betas": result.x,
            "RMSE": np.sqrt(np.mean(result.fun**2)),
            "MAE": np.mean(np.abs(result.fun)),
            "Max error": np.max(np.abs(result.fun)),
            "success": result.success,
        }
    return select_best_fits(search_result)


# Grid search for finding best lambda and mu for nss model based on 3 criteria:
# RMSE: Root Mean Square Error
# MAE: Mean Absolute Error
# Maximum residual
# Mean of residuals


def nss_gridsearch(
    maturities: NDArray[np.float64],
    rates: NDArray[np.float64],
    lambda_values: NDArray[np.float64],
    mu_values: NDArray[np.float64] | None = None,
):

    if lambda_values is None:
        lambda_values = np.round(np.arange(0.05, 1.05, 0.05), 2)
    if mu_values is None:
        mu_values = np.round(np.arange(0.05, 1.05, 0.05), 2)

    search_result = {}
    for lmbda in lambda_values:
        for mu in mu_values:
            result = fit_nss(
                maturities,
                rates,
                lmbda=lmbda,
                mu=mu,
            )
            search_result[lmbda, mu] = {
                "betas": result.x,
                "RMSE": np.sqrt(np.mean(result.fun**2)),
                "MAE": np.mean(np.abs(result.fun)),
                "Max error": np.max(np.abs(result.fun)),
                "success": result.success,
            }
    return select_best_fits(search_result)
