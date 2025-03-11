#!/usr/bin/env python3
'''
question_1_script.py
  Author(s): Arya Rahimian Emam (1319709)
  Earlier contributors(s):

  Project: Milestone II
  Date of Last Update: March 11, 2025.

  Functional Summary
      question_1_script.py takes in a CSV (comma separated version) file 
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
        
        How to Run: python3 question_2_script.py question_2_sample_data.csv 14100328.csv > [file_output_name].csv

     References
        The data is taked from 
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
    
    if len(argv) != 3:
        
        print("Not enough arguments")
        
        sys.exit(1)

    #getting file names from command line:
    job_vacancies_file = sys.argv[1]
    earnings_file = sys.argv[2]

    
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
    job_header = next(job_reader)  # Read header row 

    # Dynamically find column indices (this idea as well as the next() function above was taken from https://chatgpt.com/)
    date_idx = job_header.index("REF_DATE")
    industry_idx = job_header.index("North American Industry Classification System (NAICS)")
    value_idx = job_header.index("VALUE")
    status_idx = job_header.index("STATUS")

    job_vacancies = {} #initialize dictionary

    for row in job_reader:
        date = row[date_idx]
        industry = row[industry_idx].strip().lower() #remove space and covert to lowercase
        vacancies = row[value_idx]
        status = row[status_idx]

        year = date.split("-")[0] #split at the dash and keep the 0th element

        if year == "2023" and status not in ["E", "F"] and vacancies.strip(): #skips empty cells
            try:
                vacancies = float(vacancies)
                if industry not in job_vacancies:
                    job_vacancies[industry] = [0, 0] #if industry is not in the dictionary yet, initialize it
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
    earnings_header = next(earnings_reader)  # Read header row

    # Dynamically find column indices 
    industry_idx = earnings_header.index("North American Industry Classification System (NAICS)")
    value_idx = earnings_header.index("VALUE")
    status_idx = earnings_header.index("STATUS")

    earnings_dict = {}

    for row in earnings_reader:
        industry = row[industry_idx].strip().lower()
        weekly_earnings = row[value_idx]
        status = row[status_idx]

        if status in ["E", "F"] or not weekly_earnings.strip():
            continue

        try:
            earnings_dict[industry] = float(weekly_earnings)
        except ValueError:
            continue

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
