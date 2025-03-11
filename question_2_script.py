#!/usr/bin/env python3

'''
question_2_script.py
  Author(s): Amirhossein Nafissi (1319709) #####################
  Earlier contributors(s): Deborah Stacey, Andrew Hamilton-Wright, Arya Rahimian Emam (1315123), Felix Nguyen (1316719)

  Project: Milestone II
  Date of Last Update: March 11, 2025.

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
        argv[1] - data file to load the fields process
        argv[2] - data file that contains all other data
        
        How to Run: python3 question_2_script.py question_2_loading_data.csv 14100328.csv > question_2_output.csv

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
    #
    if len(argv) != 3:
        print("Not enough arguments")

        # we exit with a zero when everything goes well, so we choose
        # a non-zero value for exit in case of an error
        sys.exit(1)

    #getting command line arguments
    load_data_filename = sys.argv[1]
    full_data_filename = sys.argv[2]
    

    #
    # Open the load data input file.  The encoding argument
    # indicates that we want to handle the BOM (if present)
    # by simply ignoring it.
    #
    try:
        load_data_fh = open(load_data_filename, encoding="utf-8-sig")

    except IOError as err:
        # Here we are using the python format() function.
        # The arguments passed to format() are placed into
        # the string it is called on in the order in which
        # they are given.
        print("Unable to open names file '{}' : {}".format(
                load_data_filename, err), file=sys.stderr)
        sys.exit(1)
        
    #
    # Open the full data input file
    #
    try:
        full_data_fh = open(full_data_filename, encoding="utf-8-sig")

    except IOError as err:
        # Here we are using the python format() function.
        # The arguments passed to format() are placed into
        # the string it is called on in the order in which
        # they are given.
        print("Unable to open names file '{}' : {}".format(
                full_data_filename, err), file=sys.stderr)
        sys.exit(1)


    #
    # Create a CSV (Comma Separated Value) reader based on this
    # open file handle.  We can use the reader in a loop iteration
    # in order to access each line in turn.
    #
    load_data_reader = csv.reader(load_data_fh)


    #
    # printing the header (extracting the first line)
    #

    # variables:
    read_first_line = False
    
    list_of_education_levels = [] # to hold education levels (only one occurance)
    list_of_education_levels_value = [] # same as above but represented by a value, will be kept parrarel to the first
    
    list_of_occupations = [] # to hold occupations (only one occurance)
    count = 0

    #  getting required fields from the load data:
    for row_data_fields in load_data_reader:
    
        if not read_first_line: #skip reading the header
            read_first_line = True
            continue
        
        national_Occupational_Classification = row_data_fields[3]
        job_vacancy_characteristics = row_data_fields[4]
        
        # get education level
        if job_vacancy_characteristics not in list_of_education_levels:
            
            #add to list and assign it a value
            list_of_education_levels.append(job_vacancy_characteristics)
            list_of_education_levels_value.append(count)

            # #print it if need be
            # print(f"\"{job_vacancy_characteristics}\",{count}")
            
            count += 1
        
        # get occupation
        if national_Occupational_Classification not in list_of_occupations:
            list_of_occupations.append(national_Occupational_Classification)
    
    # making a 2D array containing the occurancies of each education level per occupation.
    # it contains a list for every occupation, each indexed from 0 to # of different education levels
    # in the for loop after this one, whenever a education level was seen for that job occupation, the specific index 
    # representing the education level will be incremented by the amount of job vacancies, counting the occurancy. 
    # The index with the highest occurancy will be the average education level for that specific occupation. 
    
    education_occurancies_per_occupation = []
    
    for i in list_of_occupations:
        education_occurancies_per_occupation.append([0] * len(list_of_education_levels_value)) # this syntax was inspired by this link: https://sparkbyexamples.com/python/create-a-list-of-zeros-in-python/#:~:text=You%20can%20use%20'%20*%20'%20multiplication,zeros()%20functions.
    
    # # printing before filling if need be
    # print("PRINTING MATRIX BEFORE FILLING")
    # for i in education_occurancies_per_occupation:
    #     for j in i:
    #         print(j, end = " ")
    #     print()
    
    #
    #start reading the full data
    #
    full_data_reader = csv.reader(full_data_fh)
    
    read_first_line = False # set it back to false
    
    for row_data_fields in full_data_reader:
        
        if not read_first_line: #skip reading the header
            read_first_line = True
            continue
        
        national_Occupational_Classification = row_data_fields[3] # the occupation
        job_vacancy_characteristics = row_data_fields[4] # the education level
        status = row_data_fields[13]
        
        #getting num job vacancies and catching ValueError:
        try: 
            num_job_vacancies = int(row_data_fields[12])
        except ValueError: 
            continue #skip over this line
       
        
        # if found the data we are looking for and status is not "E" or "F", add to the correct the frequency
        if (national_Occupational_Classification in list_of_occupations) and (job_vacancy_characteristics in list_of_education_levels) and (status != "E" or status != "F"):
            index_of_job = list_of_occupations.index(national_Occupational_Classification)
            index_of_education = list_of_education_levels.index(job_vacancy_characteristics)
        
            education_occurancies_per_occupation[index_of_job][index_of_education] += int(num_job_vacancies) #incrementing that specific index
        
    
    # #printing after filling if need be
    # print("PRINTING MATRIX AFTER FILLING")
    # for i in education_occurancies_per_occupation:
    #     for j in i:
    #         print(j, end = " ")
    #     print()
    
    # printing final product:
    print("\"Occupation\",\"Most_Frequent_Education_Level\",\"Most_Frequent_Value\",\"Most_Frequent_Index\",\"Second_Most_Frequent_Education_Level\",\"Second_Most_Frequent_Value\",\"Second_Most_Frequent_Index\"")
    
    
    #variables used to find greatest occurrence 
    greatest_value = -1
    first_greatest_index = 0
    second_greatest_index = 0
    
     
    for job in list_of_occupations:
        
        index_of_job = list_of_occupations.index(job)
        
        #find education level with most occurancies. Ignore the first education level which is "Minimum level of education required, all levels"
        for i in range(1, len(education_occurancies_per_occupation[index_of_job])):
            
            if education_occurancies_per_occupation[index_of_job][i] > greatest_value:
                
                greatest_value = education_occurancies_per_occupation[index_of_job][i]
                first_greatest_index = i
        
        #find education level with the second most occurancies. Ignore the first education level which is "Minimum level of education required, all levels"
        
        greatest_value = -1 #set greatest value back to default
        
        for i in range(1, len(education_occurancies_per_occupation[index_of_job])):
            
            if i != first_greatest_index:
                
                if education_occurancies_per_occupation[index_of_job][i] > greatest_value:
                    
                    greatest_value = education_occurancies_per_occupation[index_of_job][i]
                    second_greatest_index = i
        
        #print it
        print(f"\"{job}\",\"{list_of_education_levels[first_greatest_index]}\",\"{education_occurancies_per_occupation[index_of_job][first_greatest_index]}\",\"{first_greatest_index}\",\"{list_of_education_levels[second_greatest_index]}\",\"{education_occurancies_per_occupation[index_of_job][second_greatest_index]}\",\"{second_greatest_index}\"")
        
        #set values back to default for next iteration
        greatest_value = -1
        first_greatest_index = 0
        second_greatest_index = 0    
                

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
