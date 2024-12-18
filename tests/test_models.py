"""Tests for statistics functions within the Model layer."""

import pandas as pd

import pytest

def test_max_mag_integers():
    """Test that max_mag function works for integers"""
    from lcanalyzer.models import max_mag

    test_df = pd.DataFrame(data=[[1, 5, 3], 
                                       [7, 8, 9], 
                                       [3, 4, 1]], columns=list("abc"))
    test_colname = "a"
    test_output = 7

    assert max_mag(test_df, test_colname) == test_output

def test_max_mag_zeros():
    """Test that max_mag function works for zeros"""
    from lcanalyzer.models import max_mag

    test_df = pd.DataFrame(data=[[0, 0, 0], 
                                       [0, 0, 0], 
                                       [0, 0, 0]], columns=list("abc"))
    test_colname = "b"
    test_output = 0

    assert max_mag(test_df, test_colname) == test_output

def test_min_mag_negatives():
    """Test that min_mag function works for negatives"""
    from lcanalyzer.models import min_mag

    test_df = pd.DataFrame(data=[[-7, -7, -3], [-4, -3, -1], [-1, -5, -3]], columns=list("abc"))
    test_colname = "b"
    test_output = -7

    assert min_mag(test_df, test_colname) == test_output

def test_mean_mag_integers():
    """Test that mean_mag function works for negatives"""
    from lcanalyzer.models import mean_mag

    test_df = pd.DataFrame(data=[[-7, -7, -3], [-4, -3, -1], [-1, -5, -3]], columns=list("abc"))
    test_colname = "a"
    test_output = -4.

    assert mean_mag(test_df, test_colname) == test_output

### Get maximum values for all bands
def calc_stat(lc, bands, mag_col):
    import lcanalyzer.models as models
    # Define an empty dictionary where we will store the results
    stat = {}
    # For each band get the maximum value and store it in the dictionary
    for b in bands:
        stat[b + "_max"] = models.max_mag(lc[b], mag_col)
    return stat

def test_calc_stat():
    # Mock light curve data as a dictionary of DataFrames
    lc = {
        'band1': pd.DataFrame({'mag': [10, 12, 14, 11]}),
        'band2': pd.DataFrame({'mag': [20, 19, 17, 18]}),
        'band3': pd.DataFrame({'mag': [30, 29, 28, 31]}),
    }

    # List of bands to test
    bands = ['band1', 'band2', 'band3']
    
    # Column name for magnitudes
    mag_col = 'mag'

    # Expected output
    expected_output = {
        'band1_max': 14,
        'band2_max': 20,
        'band3_max': 31,
    }

    # Calculate the actual output using the function
    actual_output = calc_stat(lc, bands, mag_col)
    
    # Assert that the actual output matches the expected output
    assert actual_output == expected_output, f"Expected {expected_output}, but got {actual_output}"


@pytest.mark.parametrize(
    "test_df, test_colname, expected",
    [
        (pd.DataFrame(data=[[1, 5, 3],
                            [7, 8, 9],
                            [3, 4, 1]],
                      columns=list("abc")),
         "a",
         7),
        (pd.DataFrame(data=[[0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0]],
                      columns=list("abc")),
         "b",
         0),
    ])
def test_max_mag(test_df, test_colname, expected):
    """Test max function works for array of zeroes and positive integers."""
    from lcanalyzer.models import max_mag
    assert max_mag(test_df,test_colname) == expected

# Parametrization for mean_mag function testing
@pytest.mark.parametrize(
    "test_df, test_colname, expected",
    [
        (pd.DataFrame(data=[[1, 5, 3], 
                            [7, 8, 9], 
                            [3, 4, 1]], 
                      columns=list("abc")),
        "a",
        pytest.approx(3.66,0.01)),
        (pd.DataFrame(data=[[0, 0, 0], 
                            [0, 0, 0], 
                            [0, 0, 0]], 
                      columns=list("abc")),
        "b",
        0),
    ])
def test_mean_mag(test_df, test_colname, expected):
    """Test mean function works for array of zeroes and positive integers."""
    from lcanalyzer.models import mean_mag
    assert mean_mag(test_df, test_colname) == expected


# Parametrization for min_mag function testing
@pytest.mark.parametrize(
    "test_df, test_colname, expected",
    [
        (pd.DataFrame(data=[[1, 5, 3], 
                            [7, 8, 9], 
                            [3, 4, 1]], 
                      columns=list("abc")),
        "a",
        1),
        (pd.DataFrame(data=[[0, 0, 0], 
                            [0, 0, 0], 
                            [0, 0, 0]], 
                      columns=list("abc")),
        "b",
        0),
        (pd.DataFrame(data=[[-7, -7, -3], 
                            [-4, -3, -1], 
                            [-1, -5, -3]], 
                      columns=list("abc")),
        "b",
        -7),
    ])
def test_min_mag(test_df, test_colname, expected):
    """Test mean function works for array of zeroes and positive integers."""
    from lcanalyzer.models import min_mag
    assert min_mag(test_df, test_colname) == expected

# Parametrization for normalize_lc function testing with ValueError
@pytest.mark.parametrize(
    "test_input_df, test_input_colname, expected, expected_raises",
    [
        (pd.DataFrame(data=[[8, 9, 1], 
                            [1, 4, 1], 
                            [1, 2, 4], 
                            [1, 4, 1]], 
                      columns=list("abc")),
        "b",
        pd.Series(data=[1,0.285,0,0.285]),
        None),
        (pd.DataFrame(data=[[1, 1, 1], 
                            [1, 1, 1], 
                            [1, 1, 1], 
                            [1, 1, 1]], 
                      columns=list("abc")),
        "b",
        pd.Series(data=[0.,0.,0.,0.]),
        None),
        (pd.DataFrame(data=[[0, 0, 0], 
                            [0, 0, 0], 
                            [0, 0, 0], 
                            [0, 0, 0]], 
                      columns=list("abc")),
        "b",
        pd.Series(data=[0.,0.,0.,0.]),
        None),
        (pd.DataFrame(data=[[8, 9, 1], 
                            [1, -99.9, 1], 
                            [1, 2, 4], 
                            [1, 4, 1]], 
                      columns=list("abc")),
        "b",
        pd.Series(data=[1,0.285,0,0.285]),
        ValueError),
    ])
def test_normalize_lc(test_input_df, test_input_colname, expected,expected_raises):
    """Test how normalize_lc function works for arrays of positive integers."""
    from lcanalyzer.models import normalize_lc
    import pandas.testing as pdt
    if expected_raises is not None:
        with pytest.raises(expected_raises):
            pdt.assert_series_equal(normalize_lc(test_input_df,test_input_colname),expected,check_exact=False,atol=0.01,check_names=False)
    else:
        pdt.assert_series_equal(normalize_lc(test_input_df,test_input_colname),expected,check_exact=False,atol=0.01,check_names=False)


# # Function to test mean_mag
# def test_mean_mag(test_df, test_colname, expected):
#     """Test mean function works for various inputs."""
#     from lcanalyzer.models import mean_mag
#     assert mean_mag(test_df, test_colname) == expected

# # Parameterized test cases for mean_mag
# @pytest.mark.parametrize(
#     "test_df, test_colname, expected, expected_raises",
#     [
#         (pd.DataFrame(data=[[8, 9, 1], 
#                             [1, 4, 1], 
#                             [1, 2, 4], 
#                             [1, 4, 1]], 
#                       columns=list("abc")),
#         "b",
#         pd.Series(data=[1,0.285,0,0.285]),
#         None),
#         (pd.DataFrame(data=[[1, 1, 1], 
#                             [1, 1, 1], 
#                             [1, 1, 1], 
#                             [1, 1, 1]], 
#                       columns=list("abc")),
#         "b",
#         pd.Series(data=[0.,0.,0.,0.]),
#         None),
#         (pd.DataFrame(data=[[0, 0, 0], 
#                             [0, 0, 0], 
#                             [0, 0, 0], 
#                             [0, 0, 0]], 
#                       columns=list("abc")),
#         "b",
#         pd.Series(data=[0.,0.,0.,0.]),
#         None),
#         (pd.DataFrame(data=[[8, 9, 1], 
#                             [1, -99.9, 1], 
#                             [1, 2, 4], 
#                             [1, 4, 1]], 
#                       columns=list("abc")),
#         "b",
#         pd.Series(data=[1,0.285,0,0.285]),
#         ValueError),
#     ])


# # Function to test min_mag
# def test_min_mag(test_df, test_colname, expected, expected_raises):
#     """Test min function works for various inputs."""
#     from lcanalyzer.models import min_mag
#     if expected_raises:
#         with pytest.raises(expected_raises):
#             min_mag(test_df, test_colname)
#     else:
#         pd.testing.assert_series_equal(min_mag(test_df, test_colname), expected)

# # Parameterized test cases for min_mag
# @pytest.mark.parametrize(
#     "test_df, test_colname, expected, expected_raises",
#     [
#         (pd.DataFrame(data=[[8, 9, 1], 
#                             [1, 4, 1], 
#                             [1, 2, 4], 
#                             [1, 4, 1]], 
#                       columns=list("abc")),
#         "b",
#         pd.Series(data=[2, 2, 1, 1]),
#         None),
#         (pd.DataFrame(data=[[1, 1, 1], 
#                             [1, 1, 1], 
#                             [1, 1, 1], 
#                             [1, 1, 1]], 
#                       columns=list("abc")),
#         "b",
#         pd.Series(data=[1., 1., 1., 1.]),
#         None),
#         (pd.DataFrame(data=[[0, 0, 0], 
#                             [0, 0, 0], 
#                             [0, 0, 0], 
#                             [0, 0, 0]], 
#                       columns=list("abc")),
#         "b",
#         pd.Series(data=[0., 0., 0., 0.]),
#         None),
#         (pd.DataFrame(data=[[8, 9, 1], 
#                             [1, -99.9, 1], 
#                             [1, 2, 4], 
#                             [1, 4, 1]], 
#                       columns=list("abc")),
#         "b",
#         pd.Series(data=[-99.9, 2, 1, 1]),
#         None),
#     ]
# )


# def calc_stats(lc, bands, mag_col):
#     # Calculate max, mean and min values for all bands of a light curve
#     import lcanalyzer.models as models
#     stats = {}
#     for b in bands:
#         stat = {}
#         stat["max"] = models.max_mag(lc[b], mag_col)
#         stat["mean"] = models.max_mag(lc[b], mag_col)
#         stat["min"] = models.mean_mag(lc[b], mag_col)
#         stats[b] = stat
#     return pd.DataFrame.from_records(stats)
# test_cols = list("abc")
# test_dict = {}
# test_dict["df0"] = pd.DataFrame(
#     data=[[8, 8, 0], 
#           [0, 1, 1], 
#           [2, 3, 1], 
#           [7, 9, 7]], columns=test_cols
# )
# test_dict["df1"] = pd.DataFrame(
#     data=[[3, 8, 2], 
#           [3, 8, 0], 
#           [3, 9, 8], 
#           [8, 2, 5]], columns=test_cols
# )
# test_dict["df2"] = pd.DataFrame(
#     data=[[8, 4, 3], 
#           [7, 6, 3], 
#           [4, 2, 9], 
#           [6, 4, 0]], columns=test_cols
# )

# test_output = pd.DataFrame(data=[[9,9,6],[5.25,6.75,4.],[1,2,2]],columns=['df0','df1','df2'],index=['max','mean','min'])

# import pandas.testing as pdt

# pdt.assert_frame_equal(calc_stats(test_dict, test_dict.keys(), 'b'),
#                               test_output,
#                              check_exact=False,
#                              atol=0.01)

# Parametrization for normalize_lc function testing with ValueError