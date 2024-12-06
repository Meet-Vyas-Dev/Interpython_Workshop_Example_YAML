from lcanalyzer.lightcurve import Lightcurve
import pandas as pd
from typing import Optional

class Survey:
    """
    A class to represent a survey and handle its light curve data.
    """

    def __init__(
        self,
        filename: str,
        clean_nans: bool = True,
        id_col: str = "objectId",
        band_col: str = "band",
        time_col: str = "expMidptMJD",
        mag_col: str = "psfMag",
    ):
        """
        Initializes the Survey object by loading data from a file.

        Parameters:
            filename (str): The name of the file to load.
            clean_nans (bool): Whether to clean NaNs in the data.
            id_col (str): Column name for object IDs.
            band_col (str): Column name for bands.
            time_col (str): Column name for observation times.
            mag_col (str): Column name for magnitudes.
        """
        self.id_col = id_col
        self.band_col = band_col
        self.time_col = time_col
        self.mag_col = mag_col
        self.data = self._load_table(filename, clean_nans)
        self.unique_objects = self.data[self.id_col].unique()

    def _load_table(self, filename: str, clean_nans: bool = True) -> pd.DataFrame:
        """
        Loads data from a CSV or pickle file and optionally cleans NaNs.

        Parameters:
            filename (str): The file to load data from.
            clean_nans (bool): Whether to clean NaNs from the data.

        Returns:
            pd.DataFrame: The loaded data.
        """
        if filename.endswith(".csv"):
            df = pd.read_csv(filename)
        elif filename.endswith(".pkl"):
            df = pd.read_pickle(filename)
        else:
            raise ValueError(f"Unsupported file format: {filename}")

        if clean_nans:
            df = self._clean_table(df)

        return df

    def _clean_table(self, df: pd.DataFrame, nan_val: Optional[str] = None) -> pd.DataFrame:
        """
        Cleans NaNs from the DataFrame based on the specified value.

        Parameters:
            df (pd.DataFrame): The DataFrame to clean.
            nan_val (Optional[str]): The value to treat as NaN.

        Returns:
            pd.DataFrame: The cleaned DataFrame.
        """
        if nan_val is not None:
            filt_nan = ~(df[self.mag_col] == nan_val)
        else:
            filt_nan = ~df[self.mag_col].isna()

        return df[filt_nan]

    def get_obj_band_df(self, obj_id: str, band: str) -> pd.DataFrame:
        """
        Filters the data for a specific object and band.

        Parameters:
            obj_id (str): The ID of the object.
            band (str): The band to filter by.

        Returns:
            pd.DataFrame: The filtered DataFrame.
        """
        filt_obj_band = (self.data[self.id_col] == obj_id) & (self.data[self.band_col] == band)
        return self.data[filt_obj_band]

    def get_lc(self, obj_id: str, band: str) -> dict:
        """
        Retrieves the light curve for a specific object and band.

        Parameters:
            obj_id (str): The ID of the object.
            band (str): The band to retrieve the light curve for.

        Returns:
            dict: The light curve data.
        """
        df = self.get_obj_band_df(obj_id, band)
        lc = Lightcurve(mjds=df[self.time_col], mags=df[self.mag_col])
        return lc.lc
