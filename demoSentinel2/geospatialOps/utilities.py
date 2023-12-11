'''module for making data requests'''

import os
from osgeo import gdal, osr
import numpy

from demoSentinel2.appLogging.appLogging import enableLogging

#turn on logging
log = enableLogging()

gdal.UseExceptions()

def makeRasters(pathToData,outputPath):
    '''use datasets to make a multiband raster'''
    geoTransform = None
    rowsCount = None
    columnsCount = None
    dataType = None
    srs = osr.SpatialReference()
    # all in wgs 84
    srs.ImportFromEPSG(4326)
    # make a geotiff
    driver = gdal.GetDriverByName('Gtiff')
    outPath = None
    for i,file in enumerate(os.listdir(pathToData)):
        filepath = os.path.join(pathToData,file)
        ds = gdal.Open(filepath)
        band = ds.GetRasterBand(1)
        # put b04 in outband 1, b8a in 2, scl in 3
        if 'B04' in file:
            outBand = 1
        elif 'B8A' in file:
            outBand = 2
        elif 'SCL' in file:
            outBand = 3
        elif 'jp2' in file:
            continue
        else:
            log.warning('Found an unexpected file')
            exit('Exiting')
        # first time through get details for output
        if ('B04' in file or 'B8A' in file or 'SCL' in file) and dataType is None :
            outPath = os.path.join(outputPath,file.split('_')[0]+'_'+file.split('_')[1]+'.tif')
            geoTransform = ds.GetGeoTransform()
            rowsCount = ds.RasterYSize
            columnsCount = ds.RasterXSize
            dataType = band.DataType
            outFile = driver.Create(outPath,xsize=columnsCount,ysize=rowsCount,bands=4,eType=gdal.GDT_Float32)
            outFile.SetGeoTransform(geoTransform)
            outFile.SetProjection(srs.ExportToWkt())
            outFile = None
        outFile = gdal.Open(outPath,gdal.GA_Update)
        log.info('Adding {} to {}'.format(filepath,outPath))
        outFile.GetRasterBand(outBand).WriteArray(band.ReadAsArray())
        outFile.FlushCache()
        outFile = None
        ds = None
    log.info('Finished writing {}'.format(outPath))
    return outPath

def addNDVIBand(pathToGeoTiff):
    '''Add NDVI band to Sentinel-2 geotiffs (with SCL mask to only include SCL 4-7 inclusive)
    
    Parameters
    ----------
    pathToGeoTiff : str
        path to geotiff with Sentinel-2 channels 4 and 8


    Notes
    -----
    https://custom-scripts.sentinel-hub.com/custom-scripts/sentinel-2/ndvi/
    NDVI =(b8-b4)/(b8+b4)

    
    
    '''

    inRaster = gdal.Open(pathToGeoTiff,gdal.GA_Update)
    b4 = inRaster.GetRasterBand(1).ReadAsArray()
    b8 = inRaster.GetRasterBand(2).ReadAsArray()
    scl = inRaster.GetRasterBand(3).ReadAsArray()
    ndvi = (b8-b4)/(b4+b8)
    # use scl to set ndvi elements to 10000 if scl is outside of 4-7
    # label keepers 1 and others 0
    sclMask = numpy.where((scl<4) | (scl>7),0,1)
    # indices of others
    zeroIndices = numpy.where(sclMask==0)
    # set elements of ndvi to 10000 at zeroIndices locations
    ndvi[zeroIndices] = 10000
    # add ndvi to inRaster
    inRaster.GetRasterBand(4).WriteArray(ndvi)
    inRaster.FlushCache()
    inRaster = None