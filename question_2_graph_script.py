'''
question_2_graph_script.py
  Author(s): Felix Nguyen (1316719)
  Earlier contributors(s): Andrew Hamilton-Wright, Amirhossein Nafissi (1319709), Arya Rahimian Emam (1319709)

  Project: Milestone III
  Date of Last Update: March 28, 2025.

  Functional Summary
      
        1. Takes the csv file and stores industry names, index for most frequent and index for second most frequent
        2. Industry names is set to the x-axis and Index value for the y-axis
        3. Adjusted some minor fixes to make the industry names readable and the size of the graph
        4. Display the information in a visual bar chart with legend to see which bar is which

      Commandline Parameters: 3
        argv[1] - file name of the data that will be graphed
        argv[2] - file name of the output destination to store the graph
        argv[3] - the year that is of focus (will only be used to change the title)
        
        How to Run: python3 question_2_graph_script.py question_2_output_[year].csv question_2_graph_[year].png [year]

      References
        The data is taked from https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410037201&cubeTimeFrame.startMonth=01&cubeTimeFrame.startYear=2023&cubeTimeFrame.endMonth=12&cubeTimeFrame.endYear=2023&referencePeriods=20230101%2C20231201
        and https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410020401&pickMembers%5B0%5D=1.1&pickMembers%5B1%5D=2.1&pickMembers%5B2%5D=3.1&cubeTimeFrame.startYear=2019&cubeTimeFrame.endYear=2023&referencePeriods=20190101%2C20230101

        Youtube video used to help with plotting the graph: https://www.youtube.com/watch?v=zwSJeIcRFuQ and https://www.youtube.com/watch?v=1M65rAAcl5E 

'''
#required libraries
import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib
import numpy

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
# Take the occupation names and display them on the x-axis
occupation = file['Occupation'].tolist()
# the index will be display on y-axis
index = file['Most_Frequent_Index']
positions = numpy.arange(len(index))


# Second Most Frequent Index
index2 = file['Second_Most_Frequent_Index']
positions2 = numpy.arange(len(index2))
width = 0.4

# This loop is used to make the industries name readable in the graph
for i in range(len(occupation)):
    occupation[i] = occupation[i].replace(" ", "\n")



# Setting Figure Size
plt.figure(figsize=(14, 6))

# Label for x-axis, y-axis and title
plt.xlabel('Industry', fontweight='bold')
plt.ylabel('Education Level Index', fontweight='bold')
plt.title(f'How does the average educational level vary across different employment sectors in Canada for {year}?', fontweight='bold')

# Replace axis label 
plt.xticks(positions, occupation, rotation=0, ha='center', fontsize=7)

# The industry names were being cut off so add larger bottom margin
plt.subplots_adjust(bottom=0.2)

# Plot bar graph
plt.bar(positions-width/2, index, width, label='Most Frequent Education Level', color='red')
plt.bar(positions+width/2, index2, width, label='Second Most Frequent Education Level', color='blue')

# Display Legend Top Right
plt.legend()

#save the file
plt.savefig(output_file_name, bbox_inches = "tight")

# Display bar graph
# plt.show() #uncomment to display the GUI