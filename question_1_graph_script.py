'''
Question1GraphScript.py
  Author(s): Felix Nguyen (1316719)
  Earlier contributors(s): Andrew Hamilton-Wright, Amirhossein Nafissi (1319709), Arya Rahimian Emam (1319709)

  Project: Milestone III
  Date of Last Update: March 13, 2025.

  Functional Summary
      
        1. Takes the csv file and stores industry names and the job/salary ratio
        2. Industry names is set to the x-axis and Ratio for the y-axis
        3. Adjusted some minor fixes to make the industry names readable and the size of the graph
        4. Display the information in a visual bar chart
      
      Commandline Parameters: 3
        argv[1] - file name of the data that will be graphed
        argv[2] - file name of the output destination to store the graph
        argv[3] - the year that is of focus (will only be used to change the title)
        
        How to Run: python3 question_1_graph_script.py question_1_output_(year).csv (year)_graph_question_1.png (year)

      References
        The data is taked from https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410037201&cubeTimeFrame.startMonth=01&cubeTimeFrame.startYear=2023&cubeTimeFrame.endMonth=12&cubeTimeFrame.endYear=2023&referencePeriods=20230101%2C20231201
        and https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410020401&pickMembers%5B0%5D=1.1&pickMembers%5B1%5D=2.1&pickMembers%5B2%5D=3.1&cubeTimeFrame.startYear=2019&cubeTimeFrame.endYear=2023&referencePeriods=20190101%2C20230101

        Youtube video used to help with plotting the graph: https://www.youtube.com/watch?v=zwSJeIcRFuQ 

'''



import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib

import sys

# Check that we have been given the right number of command line arguments,
if len(sys.argv) != 4:
    print("Not enough arguments")
    sys.exit(1)

#getting command line arguments:
data_file_name = sys.argv[1]
output_file_name = sys.argv[2]
year = sys.argv[3]



# Read the CSV file
file = pd.read_csv(data_file_name)

'''Data Set'''
# Take the industry names and display them on the x-axis
industries = file['Industry'].tolist()

# This loop is used to the industries name readable in the graph
for i in range(len(industries)):
    industries[i] = industries[i].replace(" ", "\n")

# Ratio values for y-axis 
ratios = file['Vacancy-to-Salary Ratio']
positions = range(len(ratios))

# Setting Figure Size
plt.figure(figsize=(14, 6))

# Labels for xaxis, yaxis and title
plt.xlabel('Industry')
plt.ylabel('Vacancy-to-Salary Ratio')
plt.title(f'Do industries with higher job vacancies offer lower salaries in {year}?')

# Replace axis label 
plt.xticks(positions, industries, rotation=0, ha='center', fontsize=7)

# The industry names were being cut off so add larger bottom margin
plt.subplots_adjust(bottom=0.2)

# Plot bar graph
plt.bar(positions, ratios)

#save the file
plt.savefig(output_file_name, bbox_inches = "tight")

# # Display bar graph
# plt.show()

