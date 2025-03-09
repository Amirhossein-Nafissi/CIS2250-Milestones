#!/usr/bin/env python3

'''
extract_software_by_province.py
  Author(s): Amirhossein Nafissi (1319709), Arya Rahimian Emam (1315123), Felix Nguyen (1316719)
  Earlier contributors(s): Deborah Stacey, Andrew Hamilton-Wright

  Project: Project Kickoff Lab
  Date of Last Update: Feb 26, 2025.

  Functional Summary
      extract_software_by_province.py takes in a CSV (comma separated version) file 
      and prints out the fields according to the command line parameters found below:

      There are expected to be three fields:
          1. data file to process
          2. an argument indicating either the name of a province, 
            or the word “Canada” which will extract only the national data.

      First it prints the header, and then prints the fields that are the same as the command line parameters.
      The data is also filtered by only showing "Software engineers and designers [2173]" for National Occupational Classification
      and "Job vacancies" for Statistics.

     Commandline Parameters: 1
        argv[1] - data file to process
        argv[2] - an argument indicating either the name of a province, 
            or the word “Canada” which will extract only the national data.

     References
        The data is taked from https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410032805 
'''


#
#   Packages and modules
#

# The 'sys' module gives us access to system tools, including the
# command line parameters, as well as standard input, output and error
import sys

# The 'csv' module gives us access to a tool that will read CSV
# (Comma Separated Value) files and provide us access to each of
# the fields on each line in turn
import csv


#
# Define any "constants" for the file here.
# Names of constants should be in UPPER_CASE.
#


def main(argv):

    '''
    Main function in the script. Putting the body of the
    script into a function allows us to separate the local
    variables of this function from the global constants
    declared outside.
    '''

    #
    #   Check that we have been given the right number of parameters,
    #   and store the single command line argument in a variable with
    #   a better name
    #
    if len(argv) != 3:
        print("Not enough arguments")

        # we exit with a zero when everything goes well, so we choose
        # a non-zero value for exit in case of an error
        sys.exit(1)

    #getting command line arguments
    namedata_filename = sys.argv[1]
    region_Name = sys.argv[2]

    #
    # Open the name data input file.  The encoding argument
    # indicates that we want to handle the BOM (if present)
    # by simply ignoring it.
    #
    try:
        namedata_fh = open(namedata_filename, encoding="utf-8-sig")

    except IOError as err:
        # Here we are using the python format() function.
        # The arguments passed to format() are placed into
        # the string it is called on in the order in which
        # they are given.
        print("Unable to open names file '{}' : {}".format(
                namedata_filename, err), file=sys.stderr)
        sys.exit(1)


    #
    # Create a CSV (Comma Separated Value) reader based on this
    # open file handle.  We can use the reader in a loop iteration
    # in order to access each line in turn.
    #
    file_reader = csv.reader(namedata_fh)


    #
    # printing the header (extracting the first line)
    #

    read_first_line = False

    for row_data_fields in file_reader:

        #reading the header
        if not read_first_line:
            REF_DATE = row_data_fields[0]
            GEO = row_data_fields[1]
            National_Occupational_Classification = row_data_fields[3]
            job_vacancy_characteristics = row_data_fields[4]
            statistics = row_data_fields[5]
            VALUE = row_data_fields[12]

            print(f"{REF_DATE},{GEO},{National_Occupational_Classification},{job_vacancy_characteristics},{statistics},{VALUE}")

            read_first_line = True
        
        #reading the rest of the data
        if read_first_line:
            REF_DATE = row_data_fields[0]
            GEO = row_data_fields[1]
            National_Occupational_Classification = row_data_fields[3]
            job_vacancy_characteristics = row_data_fields[4]
            statistics = row_data_fields[5]
            VALUE = row_data_fields[12]

            #checking if VALUE is empty
            if VALUE == '':
                VALUE = '0'
            
            #printing filtered data
            if GEO == region_Name:
                if National_Occupational_Classification == "Software engineers and designers [2173]":
                    if job_vacancy_characteristics == "Bachelor's degree":
                        if statistics == "Job vacancies":
                        
                            print(f"{REF_DATE},{GEO},{National_Occupational_Classification},{job_vacancy_characteristics},{statistics},{VALUE}")

    #
    #   End of Function
    #

##
## Call our main function, passing the system argv as the parameter
##
main(sys.argv)


#
#   End of Script
#
