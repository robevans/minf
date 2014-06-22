from json import load
from scipy.io import savemat
from os.path import basename, splitext


def convert_to_matlab_file(output_filename, *input_files):
    """
    Converts the json file output by the video-data syncronisation tool to one usable by MATLAB,
    in the form required for the HMM+FNN gait segmenter.
    Note that the Matlab gait segmenter does not allow class 0 (on 20/06/14)
    """

    matlab_variables = {}

    try:
        for input_file in input_files:
            with open(input_file, 'r') as fin:
                file_data = load(fin)

            variable_name = splitext(basename(input_file))[0]

            duplicate_number = 0
            while variable_name in matlab_variables:
                duplicate_number += 1
                if duplicate_number == 1:
                    variable_name += '_{0}'.format(duplicate_number)
                else:
                    variable_name = variable_name[:-1] + str(duplicate_number)

            matlab_variables[variable_name] = sorted([[int(k), int(v)] for k, v in file_data['event_annotations'].items()])

    except Exception, e:
        print "Error loading data", e

    savemat(output_filename, matlab_variables)
