#!/usr/bin/env python3
'''
question_1_preprocessing_script.py
  Author(s): Arya Rahimian Emam (1319709)
  Earlier contributors(s): Andrew Hamilton-Wright, Amirhossein Nafissi (1319709), Felix Nguyen (1316719)

  Project: Milestone III
  Date of Last Update: March 28, 2025.

  Functional Summary
      question_1_preprocessing_script.py takes in 2 CSV (comma separated version) files 
      and prints out the fields according to the command line parameters found below:

      There are expected to be two parameters:
          1. job vacancy data file to process
          2. weekly earnings data file to process
          3. the year the data is based on
    
      First, the script records job vacancy data for each industry from every month of the selected year.
      Next, it calculates the average job vacancy for each industry over the entire year.
      Then, it retrieves the weekly earnings data for each industry.
      Then, it computes a ratio between job vacancies and salary
      Finally, it prints the average job vacancy, weekly earnings and vacancy-to-salary ratio for each industry.
     
      Commandline Parameters: 3 
        argv[1] - job_vacancies.csv
        argv[2] - weekly_earnings.csv
        argv[3] - year that you want the data for
        
        How to Run: python3 question_1_preprocessing_script.py job_vacancies.csv weekly_earnings.csv [year] > question_1_output_[year].csv
        
      References
        The data is taked from https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410037201&cubeTimeFrame.startMonth=01&cubeTimeFrame.startYear=2023&cubeTimeFrame.endMonth=12&cubeTimeFrame.endYear=2023&referencePeriods=20230101%2C20231201
        and https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410020401&pickMembers%5B0%5D=1.1&pickMembers%5B1%5D=2.1&pickMembers%5B2%5D=3.1&cubeTimeFrame.startYear=2019&cubeTimeFrame.endYear=2023&referencePeriods=20190101%2C20230101
'''

#
#   Packages and modules
#

import sys
import csv

def main(argv):
    
    #
    #   Check that we have been given the right number of parameters,
    #
    
    if len(argv) != 4:
        
        print("Not enough arguments")
        
        sys.exit(1)

    #getting file names from command line:
    job_vacancies_file = sys.argv[1]
    earnings_file = sys.argv[2]

    #getting the year and error handeling:
    try:
        dummy_year = int(sys.argv[3])
    except ValueError:
        print("year inputted is not an integer")
        sys.exit(1)

    #checking if year is the correct range
    if dummy_year < 2015 or dummy_year > 2023:
        print("year inputted is not an in the range of 2015 - 2023")
        sys.exit(1)

    year_input = sys.argv[3]

    
    
    #opening files and error handeling:
    try: 
        job_fh = open(job_vacancies_file, encoding="utf-8-sig") #for first file

    except IOError as err:
        # Here we are using the python format() function.
        # The arguments passed to format() are placed into
        # the string it is called on in the order in which
        # they are given.
        print("Unable to open names file '{}' : {}".format(
                job_vacancies_file, err), file=sys.stderr)
        sys.exit(1)
    
    #for second file
    try:
        earnings_fh = open(earnings_file, encoding="utf-8-sig") 

    except IOError as err:
        # Here we are using the python format() function.
        # The arguments passed to format() are placed into
        # the string it is called on in the order in which
        # they are given.
        print("Unable to open names file '{}' : {}".format(
                job_vacancies_file, err), file=sys.stderr)
        sys.exit(1)

    # Read job vacancies data
    job_reader = csv.reader(job_fh)



    job_vacancies = {} #initialize dictionary

    for row in job_reader:
        date = row[0]
        industry = row[3].strip().lower() #remove space and covert to lowercase
        vacancies = row[11]
        status = row[12]
        field = row[4]

        year = date.split("-")[0] #split at the dash and keep the 0th element

        if year == year_input and field == "Job vacancies" and status not in ["E", "F"] and vacancies.strip(): #skips empty cells
            try:
                vacancies = float(vacancies)
                job_vacancies[industry] = [0,0]
                job_vacancies[industry][0] += vacancies #increments sum of job vacancies
                job_vacancies[industry][1] += 1 #increments month
            except ValueError:
                continue  # Skip invalid data

    # Compute average job vacancies per industry
    avg_job_vacancies = {}

    for industry in job_vacancies:
        total = job_vacancies[industry][0]  # Sum of vacancies
        count = job_vacancies[industry][1]  # Number of months
       
        if count > 0:
            avg_job_vacancies[industry] = total / count
        else:
            avg_job_vacancies[industry] = 0  # Avoid division by zero


    # Read salary data
    earnings_reader = csv.reader(earnings_fh)


    earnings_dict = {}

    for row in earnings_reader:
        year = row[0]  # Extract REF_DATE
        industry = row[5].strip().lower()
        weekly_earnings = row[12]
        status = row[13]

        

        if year == year_input and status not in ["E", "F"] and weekly_earnings.strip():
            try:
                earnings_dict[industry] = float(weekly_earnings)
            except ValueError:
                continue  # Skip invalid data   


    job_fh.close()
    earnings_fh.close()

    # Find industries present in both datasets (& operator finds # intersections between lists)
    matched_industries = avg_job_vacancies.keys() & earnings_dict.keys()

    # printing header
    print("\"Industry\",\"Avg Job Vacancies\",\"Weekly Salary\",\"Vacancy-to-Salary Ratio\"")

    for industry in matched_industries:
        avg_vacancies = avg_job_vacancies[industry]
        salary = earnings_dict[industry]
        if salary == 0:
            ratio = 0
        else:
            ratio = avg_vacancies / salary
        #print only 3 deciamls
        print(f"\"{industry}\",\"{avg_vacancies:.3f}\",\"{salary:.3f}\",\"{ratio:.3f}\"")
        
main(sys.argv)
