import argparse
from lcanalyzer import survey, plots

def main():
    """The MVC Controller of the LSST data table.

    The Controller is responsible for:
    - selecting the necessary models and views for the current task
    - passing data between models and views
    """
    infile = args.infile
    lsst = survey.Survey(infile)

    if args.info == 'unique':
        print(lsst.unique_objects)

    elif args.info == 'plotFirst':
        obj_id = lsst.unique_objects[0]
        band = args.band
        time_col = 'mjds'
        mag_col = 'mags'

        if args.obj_id is not None:
            obj_id = args.obj_id

        lc = lsst.get_lc(obj_id, band)
        plots.plotUnfolded(lc[time_col], lc[mag_col])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A package for inspecting LSST survey tables containing variability observations')

    parser.add_argument(
        'infile',
        help='Input CSV or PKL file containing LSST light curves')
    
    parser.add_argument(
        '--info',
        default='unique',
        choices=['unique', 'plotFirst'],
        help='Which info should be displayed?')

    parser.add_argument(
        '--band',
        type=str,
        default='g',
        help='Which band should be plotted?')

    parser.add_argument(
        '--obj_id',
        type=str,
        help='ID of the object for which to plot the light curve')

    args = parser.parse_args()
    main()
