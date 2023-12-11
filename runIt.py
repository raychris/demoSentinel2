'''command line interface for running this package'''

import json
import os
import geopandas as gpd
import shapely
from osgeo import gdal

from demoSentinel2.appLogging.appLogging import enableLogging
from demoSentinel2.argParsing.argParsing import getArguments
from demoSentinel2.geospatialOps.utilities import makeRasters, addNDVIBand

#turn on logging
log = enableLogging()

def main():
    '''drive the package'''
    #get the command line input

    #get the __dict__ attribute of the returned argparse.Namespace object
    commandLineArgs = vars(getArguments(argList=None))
    log.info(commandLineArgs)

    if commandLineArgs['taskNumber'] == '1':
        log.info('running task 1')
        # Inspect the metadata of the provided Sentinel 2 data using any python library and provide the output print out
        # read in the MTD_MSIL2A.xml file and write it out to the outputs dir
        with open(os.path.join(commandLineArgs['inputDataBasePath'],'S2B_MSIL2A_20221127T075159_N0400_R135_T36NXF_20221127T100500.SAFE','MTD_MSIL2A.xml'),'r') as metadata:
            theLines = metadata.readlines()
        with open(os.path.join(commandLineArgs['outputPath'],'task1.txt'),'w') as task1:
            task1.writelines(theLines)
    if commandLineArgs['taskNumber'] == '2':
        log.info('running task 2')
        # lip to the extent of the image covered by the provided region
        # add a metadata tag called “region” that should have the value “test roi”.
        # assume clip extent is wgs 84
        with open(os.path.join(commandLineArgs['inputDataBasePath'],'region_of_interest.geojson')) as clipGeom:
            x = clipGeom.read()
            sh = shapely.from_geojson(x)
            clipGeomJson = json.loads(x)
            pass
    if commandLineArgs['taskNumber'] == '3':
        log.info('running task 3')
        # Calculate the Min, Max, Mean, Median and Standard Deviation of the spectral index (just ndvi)
        # just do this on the 60m band
        pathTo60m = 'S2B_MSIL2A_20221127T075159_N0400_R135_T36NXF_20221127T100500.SAFE/GRANULE/L2A_T36NXF_A029905_20221127T080452/IMG_DATA/R60m'
        pathtoGeoTiff = makeRasters(os.path.join(commandLineArgs['inputDataBasePath'],pathTo60m),commandLineArgs['outputPath'])
        # add ndvi
        addNDVIBand(pathToGeoTiff=pathtoGeoTiff)
        # show statistics for band 4 (that's the ndvi band)
        r = gdal.Open(pathtoGeoTiff)
        ndviBand = r.GetRasterBand(4)
        stats = ndviBand.GetStatistics(True,True)
        log.info('statistics: {}'.format(stats))
if __name__ == '__main__':
    main()