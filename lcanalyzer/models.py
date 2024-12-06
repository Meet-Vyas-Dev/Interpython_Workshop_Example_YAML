"""Module containing models representing lightcurves.

The Model layer is responsible for the 'business logic' part of the software.

The lightcurves are saved in a table (2D array) where each row corresponds to a single observation. 
Depending on the dataset (LSST or Kepler), a table can contain observations of a single or several objects, 
in a single or different bands.
"""

import pandas as pd
import numpy as np
from astropy.timeseries import LombScargle

def load_dataset(filename):
    """Load a table from CSV file.
    
    :param filename: The name of the .csv file to load
    :returns: pd.DataFrame with the data from the file.
    """
    return pd.read_csv(filename)


def mean_mag(data,mag_col):
    """Calculate the mean magnitude of a lightcurve"""
    return data[mag_col].mean()


def max_mag(data,mag_col):
    """Calculate the max magnitude of a lightcurve"""
    return data[mag_col].max()


def min_mag(data,mag_col):
    """Calculate the min magnitude of a lightcurve
    :param data: pd.DataFrame with observed magnitudes for a single source.
    :param mag_col: a string with the name of the column for calculating the min value.
    :returns: The min value of the column.
    """
    return data[mag_col].min()

def normalize_lc(df,mag_col):
    # Normalize a light curve
    if any(df[mag_col].abs() > 90):
        raise ValueError(mag_col+' contains values with abs() larger than 90!')
    min = min_mag(df,mag_col)
    max = max_mag((df-min),mag_col)
    lc = (df[mag_col]-min)/max
    lc = lc.fillna(0)
    return lc