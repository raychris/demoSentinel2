# WELCOME
This package demonstrates the ability to perform the following tasks:

1. Inspect the metadata of the provided Sentinel 2 data using any python library and provide the output print out
2. Clip to the extent of the image covered by the provided region and add a metadata tag called “region” that should have the value “test roi”.
3. Calculate the Min, Max, Mean, Median and Standard Deviation of the spectral index
4. Add the spectral index outputs as bands to the original image and label them appropriately
5. Using PostgreSQL, create a database called zonal_statistics_db then in python, create a table called test_roi_tbl and columns should be image_date, min, max, mean, median, std_dev . Update the values of the Question 4 c. above to the table and print out the values to make sure they were saved correctly. 

# GETTING STARTED
This package is designed to run on a linux operating system.  It was tested on RHEL 8.