from matplotlib import pyplot as plt
import numpy as np

def plotUnfolded(mjds, mags, obj_id=None, mjd_label='Mjd (days)', mag_label='Mag', color='blue', marker='o'):
    """
    Plots an unfolded light curve for a specific object if obj_id is provided.

    Parameters:
        mjds (array-like): Array of Modified Julian Dates.
        mags (array-like): Array of magnitudes.
        obj_id (str or None): ID of the object to plot. If None, all data is plotted (default: None).
        mjd_label (str): Label for the x-axis (default: 'Mjd (days)').
        mag_label (str): Label for the y-axis (default: 'Mag').
        color (str): Color of the markers (default: 'blue').
        marker (str): Marker style (default: 'o').
    """
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.subplots_adjust(bottom=0.15)
    
    if obj_id is not None:
        # Filter data for the specified object ID
        mask = np.array([id_ == obj_id for id_ in obj_ids])
        mjds = mjds[mask]
        mags = mags[mask]
    
    ax.scatter(
        mjds,
        mags,
        color=color,
        marker=marker
    )
    ax.minorticks_on()
    ax.set_xlabel(mjd_label)
    ax.set_ylabel(mag_label)
    plt.tight_layout()
    plt.show()
