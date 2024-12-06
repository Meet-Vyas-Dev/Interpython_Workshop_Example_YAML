import pandas as pd
import numpy as np

class Lightcurve:
    """
    A class to represent an astronomical light curve.

    Attributes:
        lc (dict): A dictionary to hold light curve data.
    """

    def __init__(self, mjds: np.ndarray = None, mags: np.ndarray = None, mag_errs: np.ndarray = None):
        """
        Initializes the Lightcurve object with optional observations.

        Parameters:
            mjds (np.ndarray): Array of Modified Julian Dates.
            mags (np.ndarray): Array of magnitudes.
            mag_errs (np.ndarray): Array of magnitude errors (optional).
        """
        self.lc = {}
        if mjds is not None and mags is not None:
            self.add_observations(mjds, mags, mag_errs)

    def add_observations(self, mjds: np.ndarray, mags: np.ndarray, mag_errs: np.ndarray = None):
        """
        Adds observations to the light curve.

        Parameters:
            mjds (np.ndarray): Array of Modified Julian Dates.
            mags (np.ndarray): Array of magnitudes.
            mag_errs (np.ndarray): Array of magnitude errors (optional).
        """
        mjds_array = self._convert_to_array(mjds)
        mags_array = self._convert_to_array(mags)
        mag_errs_array = self._convert_to_array(mag_errs) if mag_errs is not None else np.array([])

        self._compare_len([mjds_array, mags_array, mag_errs_array] if mag_errs is not None else [mjds_array, mags_array])

        self.lc = {
            "mjds": mjds_array,
            "mags": mags_array,
            "mag_errs": mag_errs_array
        }

    def _convert_to_array(self, data) -> np.ndarray:
        """
        Converts input data to a numpy array.

        Parameters:
            data: Data to convert (list, tuple, Series, int, or float).

        Returns:
            np.ndarray: The converted numpy array.
        """
        if data is None:
            return np.array([])  # Return an empty array if data is None
        return np.asarray(data)

    def _compare_len(self, arrs):
        """
        Compares the lengths of arrays to ensure they match.

        Parameters:
            arrs (list): List of arrays to compare.
        """
        if len({len(arr) for arr in arrs if len(arr) > 0}) > 1:
            raise ValueError("Input arrays must have the same length!")

    @property
    def mean_mag(self) -> float:
        """
        Calculates the mean magnitude.

        Returns:
            float: The mean of the magnitudes.
        """
        return np.mean(self.lc["mags"]) if len(self.lc["mags"]) > 0 else float('nan')

    def __len__(self) -> int:
        """
        Returns the number of observations in the light curve.

        Returns:
            int: The number of observations.
        """
        return len(self.lc.get("mjds", []))
