#!/usr/bin/env python3

'''
question_2_script.py
  Author(s): Amirhossein Nafissi (1319709), Arya Rahimian Emam (1315123), Felix Nguyen (1316719)
  Earlier contributors(s): Deborah Stacey, Andrew Hamilton-Wright

  Project: Milestone II
  Date of Last Update: March 8, 2025.

  Functional Summary
      question_2_script.py takes in a CSV (comma separated version) file 
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
    if len(argv) != 2:
        print("Not enough arguments")

        # we exit with a zero when everything goes well, so we choose
        # a non-zero value for exit in case of an error
        sys.exit(1)

    #getting command line arguments
    namedata_filename = sys.argv[1]

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

    # variables:
    read_first_line = False
    
    list_of_education_levels = [] # to hold education levels (only one occurance)
    list_of_education_levels_value = [] # same as above but represented by a value, will be kept parrarel to the first
    
    list_of_occupations = [] # to hold occupations (only one occurance)
    count = 0

    # getting occurancies of each field:
    for row_data_fields in file_reader:
    
        if not read_first_line: #skip reading the header
            read_first_line = True
            continue
        
        national_Occupational_Classification = row_data_fields[3]
        job_vacancy_characteristics = row_data_fields[4]
        status = row_data_fields[13]
        
        if job_vacancy_characteristics not in list_of_education_levels:
            
            #add to list and assign it a value
            list_of_education_levels.append(job_vacancy_characteristics)
            list_of_education_levels_value.append(count)

            # #print it
            # print(f"\"{job_vacancy_characteristics}\",{count}")
            
            # count += 1
        
        if national_Occupational_Classification not in list_of_occupations:
            list_of_occupations.append(national_Occupational_Classification)
    
    # making a 2D array containing the occurancies of each job per occupation.
    # it contains a list for every job, each indexed from 0 to # of different education levels
    # in the for loop after this one, whenever a education level was seen for that job occupation, the specific index 
    # representing the education level will be incremented by one, counting the occurancy. The index with the highest
    # occurancy will be the average education level for that specific occupation. 
    
    education_occurancies_per_occupation = []
    
    for i in list_of_occupations:
        education_occurancies_per_occupation.append([0] * len(list_of_education_levels_value)) # this syntax was inspired by this link: https://sparkbyexamples.com/python/create-a-list-of-zeros-in-python/#:~:text=You%20can%20use%20'%20*%20'%20multiplication,zeros()%20functions.
    
    
    print("#############################")
    for i in education_occurancies_per_occupation:
        for j in i:
            print(j, end = " ")
        print()
    
    # read the file:
    
    #
    # THE FOR LOOP BELOW IS NOT EXECUTING!!!!!!!!!!!!!!!!!!!!
    #
    
    file_reader = csv.reader(namedata_fh)
    
    read_first_line = False # set it back to false
    
    for row_data_fields in file_reader:
        
        if not read_first_line: #skip reading the header
            read_first_line = True
            continue
        
        national_Occupational_Classification = row_data_fields[3] # the occupation
        job_vacancy_characteristics = row_data_fields[4] # the education level
        status = row_data_fields[13]
        
        print("Index job: ", list_of_occupations.index(national_Occupational_Classification))
        print("Index education: ", list_of_education_levels.index(job_vacancy_characteristics))
        
        education_occurancies_per_occupation[list_of_occupations.index(national_Occupational_Classification)][list_of_education_levels.index(job_vacancy_characteristics)] += 1
        
    
    #printing
    print("#############################")
    for i in education_occurancies_per_occupation:
        for j in i:
            print(j, end = " ")
        print()
            
                

        # #reading the header
        # if not read_first_line:
        #     REF_DATE = row_data_fields[0]
        #     GEO = row_data_fields[1]
        #     National_Occupational_Classification = row_data_fields[3]
        #     job_vacancy_characteristics = row_data_fields[4]
        #     statistics = row_data_fields[5]
        #     VALUE = row_data_fields[12]

        #     print(f"{REF_DATE},{GEO},{National_Occupational_Classification},{job_vacancy_characteristics},{statistics},{VALUE}")

        #     read_first_line = True
        
        # #reading the rest of the data
        # if read_first_line:
        #     REF_DATE = row_data_fields[0]
        #     GEO = row_data_fields[1]
        #     National_Occupational_Classification = row_data_fields[3]
        #     job_vacancy_characteristics = row_data_fields[4]
        #     statistics = row_data_fields[5]
        #     VALUE = row_data_fields[12]

        #     #checking if VALUE is empty
        #     if VALUE == '':
        #         VALUE = '0'
            
        #     #printing filtered data
        #     if GEO == region_Name:
        #         if National_Occupational_Classification == "Software engineers and designers [2173]":
        #             if job_vacancy_characteristics == "Bachelor's degree":
        #                 if statistics == "Job vacancies":
                        
        #                     print(f"{REF_DATE},{GEO},{National_Occupational_Classification},{job_vacancy_characteristics},{statistics},{VALUE}")

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
