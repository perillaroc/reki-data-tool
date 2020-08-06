"""
Notes
-----
Codes in this file are from GetPy, which is an inner project in NWPC.
"""
import numpy as np
import pandas as pd


def calculate_plev_stats(
        forecast_array,
        analysis_array,
        climate_array,
        domain,
):
    lat = np.arange(90, -90 - 1.5, -1.5)
    lon = np.arange(0, 360, 1.5)
    llon, llat = np.meshgrid(lon, lat)

    start_j = int((90.0 - domain[1]) / 1.5 + 1)
    end_j = int((90.0 - domain[0]) / 1.5 + 1)
    start_i = int(domain[2] / 1.5)
    end_i = int(domain[3] / 1.5)

    domain_forecast_array = forecast_array[start_j:end_j, start_i:end_i]
    domain_analysis_array = analysis_array[start_j:end_j, start_i:end_i]
    domain_climate_array = climate_array[start_j:end_j, start_i:end_i]

    lats = llat[start_j:end_j, start_i:end_i]

    return pd.DataFrame({
        "rmse": [np.sqrt(mse(domain_forecast_array, domain_analysis_array, lats))],
        "bias": [bias(domain_forecast_array, domain_analysis_array, lats)],
        "absolute_bias": [absolute_bias(domain_forecast_array, domain_analysis_array, lats)],
        "std": [std(domain_forecast_array, domain_analysis_array, lats)],
        "rmsem": [rmsem(domain_forecast_array, domain_analysis_array, lats)],
        "rmsep": [rmsep(domain_forecast_array, domain_analysis_array, lats)],
        "acc": [acc(domain_forecast_array, domain_analysis_array, domain_climate_array, lats)],
    })


def mse(forecast_array, analysis_array, lats):
    result = np.sum(
        np.power(forecast_array - analysis_array, 2) * np.cos(lats * np.pi / 180.0)
    ) / np.sum(np.cos(lats * np.pi / 180.0))
    return result


def bias(forecast_array, analysis_array, lats):
    result = np.sum(
        (forecast_array - analysis_array) * np.cos(lats * np.pi / 180.0)
    ) / np.sum(np.cos(lats * np.pi / 180.0))
    return result


def absolute_bias(forecast_array, analysis_array, lats):
    result = np.sum(
        np.abs(forecast_array - analysis_array) * np.cos(lats * np.pi / 180.0)
    ) / np.sum(np.cos(lats * np.pi / 180.0))
    return result


def std(forecast_array, analysis_array, lats):
    bias_result = bias(forecast_array, analysis_array, lats)
    result = np.sqrt(
        np.sum(
            np.power(forecast_array - analysis_array - bias_result, 2) * np.cos(lats * np.pi / 180.)
        ) / np.sum(np.cos(lats * np.pi / 180.))
    )
    return result


def rmsem(forecast_array, analysis_array, lats):
    return np.abs(bias(forecast_array, analysis_array, lats))


def rmsep(forecast_array, analysis_array, lats):
    return np.sqrt(mse(forecast_array, analysis_array, lats)) - rmsem(forecast_array, analysis_array, lats)


def acc(forecast_array, analysis_array, climate_array, lats):
    forecast_climate = bias(forecast_array, climate_array, lats)
    obs_climate = bias(analysis_array, climate_array, lats)
    acc1 = np.sum(
        (forecast_array - climate_array - forecast_climate) * (analysis_array - climate_array - obs_climate) * np.cos(lats * np.pi / 180.)
    )
    acc2 = np.sum(
        np.power(forecast_array - climate_array - forecast_climate, 2) * np.cos(lats * np.pi / 180.)
    )
    acc3 = np.sum(
        np.power(analysis_array - climate_array - obs_climate, 2) * np.cos(lats * np.pi / 180.)
    )
    result = acc1 / np.sqrt(acc2 * acc3)
    return result