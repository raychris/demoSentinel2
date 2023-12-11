'''Command line interface argument handling'''

import argparse
import textwrap    

def getArguments(argList):
    '''Get arguments from the command line interface and return parsed arguments'''
    description = textwrap.dedent('''\
                                       A python package that performs the following tasks
​
                                        1) Inspect the metadata of the provided Sentinel 2 data using any python library and provide the output print out
                                        2) Clip to the extent of the image covered by the provided region and add a metadata tag called “region” that should have the value “test roi”.
                                        3) Calculate the Min, Max, Mean, Median and Standard Deviation of the spectral index
                                        4) Add the spectral index outputs as bands to the original image and label them appropriately
                                        5) Using PostgreSQL, create a database called zonal_statistics_db then in python, create a table called test_roi_tbl and columns should be image_date, min, max, mean, median, std_dev . Update the values of the Question 4 c. above to the table and print out the values to make sure they were saved correctly. ''')

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    addArguments(parser, argList)
    return parser.parse_args()

def addArguments(parser, argList):
    '''Define how arguments available to the command line interface should be parsed'''
    parser.add_argument('--taskNumber',
                        help='task to run')
    parser.add_argument('--inputDataBasePath',
                        help='where to look for input data')
    parser.add_argument('--outputPath',
                        help='basepath for output')