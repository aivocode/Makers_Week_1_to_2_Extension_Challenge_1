import os
import csv

# == INSTRUCTIONS ==
#
# Below, you'll find lots of incomplete functions.
#
# Your job: Implement each function so that it does its job effectively.
#
# Tips:
# * Use the material, Python Docs and Google as much as you want
#
# * A warning: the data you are using may not contain quite what you expect;
#   cleaning data (or changing your program) might be necessary to cope with
#   "imperfect" data

# == EXERCISES ==

# Purpose: return a boolean, False if the file doesn't exist, True if it does
# Example:
#   Call:    does_file_exist("nonsense")
#   Returns: False
#   Call:    does_file_exist("AirQuality.csv")
#   Returns: True
# Notes:
# * Use the already imported "os" module to check whether a given filename exists
def does_file_exist(filename):
    return os. path. exists(filename)

# Purpose: get the contents of a given file and return them; if the file cannot be
# found, return a nice error message instead
# Example:
#   Call: get_file_contents("AirQuality.csv")
#   Returns:
#     Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);[...]
#     10/03/2004;18.00.00;2,6;1360;150;11,9;1046;166;1056;113;1692;1268;[...]
#     [...]
#   Call: get_file_contents("nonsense")
#   Returns: "This file cannot be found!"
# Notes:
# * Learn how to open file as read-only
# * Learn how to close files you have opened
# * Use readlines() to read the contents
# * Use should use does_file_exist()
def get_file_contents(filename):
    if does_file_exist(filename):
        contents = open(filename, "r")
        lines = contents.readlines()
        contents.close()
        return lines
    return "This file cannot be found!"

# Purpose: fetch Christmas Day (25th December) air quality data rows, and if
# boolean argument "include_header_row" is True, return the first header row
# from the filename as well (if it is False, omit that row)
# Example:
#   Call: christmas_day_air_quality("AirQuality.csv", True)
#   Returns:
#     Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);[...]
#     25/12/2004;00.00.00;5,9;1505;-200;15,6;1168;567;525;169;1447;[...]
#     [...]
#   Call: christmas_day_air_quality("AirQuality.csv", False)
#   Returns:
#     25/12/2004;00.00.00;5,9;1505;-200;15,6;1168;567;525;169;1447;[...]
#     [...]
# Notes:
# * should use get_file_contents() - N.B. as should any subsequent
# functions you write, using anything previously built if and where necessary
def christmas_day_air_quality(filename, include_header_row=None):
    lines = get_file_contents(filename)
    if include_header_row == True or include_header_row == None:
        x = []
        for i in lines:
            if i[:5] == "25/12":
                x.append(i)
        x.insert(0, lines[0])
        return x
    if include_header_row == False:
        x = []
        for i in lines:
            if i[:5] == "25/12":
                x.append(i)
        return x

# Purpose: fetch Christmas Day average of "PT08.S1(CO)" values to 2 decimal places
# Example:
#   Call: christmas_day_average_air_quality("AirQuality.csv")
#   Returns: 1439.21
# Data sample:
# Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);NOx(GT);PT08.S3(NOx);NO2(GT);PT08.S4(NO2);PT08.S5(O3);T;RH;AH;;
# 10/03/2004;18.00.00;2,6;1360;150;11,9;1046;166;1056;113;1692;1268;13,6;48,9;0,7578;;
def christmas_day_average_air_quality(filename):
    christmas_lines = christmas_day_air_quality(filename, False)
    sum = 0
    for i in christmas_lines:
        x = i.split(";")
        sum += int(x[3])
    return round(sum / len(christmas_lines), 2)


# Purpose: scrape all the data and calculate average values for each of the 12 months
#          for the "PT08.S1(CO)" values, returning a dictionary of keys as integer
#          representations of months and values as the averages (to 2 decimal places)
# Example:
#   Call: get_averages_for_month("AirQuality.csv")
#   Returns: {1: 1003.47, [...], 12: 948.71}
# Notes:
# * Data from months across multiple years should all be averaged together
def get_averages_for_month(filename):
    lines = get_file_contents(filename)

    #remove header
    lines.pop(0)

    #remove rubbish lines
    while ";;;;;;;;;;;;;;;;\n" in lines:
        lines.remove(";;;;;;;;;;;;;;;;\n")

    #fancy way of making dictionary
    my_dict = dict.fromkeys([i for i in range(1, 13)], [])

    #concatenate lst with month converted from str that was split from each line
    for line in lines:
        split_line = line.split(";")        
        my_dict[int(split_line[0][3:5])] = my_dict[int(split_line[0][3:5])]+[int(split_line[3])]

    #round up based on sum of lst elemenents divided lst len    
    for key in my_dict:
        my_dict[key] = round(sum(my_dict[key]) / len(my_dict[key]), 2)

    return my_dict

# Purpose: write only the rows relating to March (any year) to a new file, in the same
# location as the original, including the header row of labels
# Example
#   Call: create_march_data("AirQuality.csv")
#   Returns: nothing, but writes header + March data to file called
#            "AirQualityMarch.csv" in same directory as "AirQuality.csv"

def create_march_data(filename):
    lines = get_file_contents(filename)
    sorted_lines = []
    sorted_lines.append(lines[0][:-1])
    
    #add lines with march month in it to lst
    for line in lines:
        if line[3:5] == "03":
            sorted_lines.append(line[:-1])

    #create and populate file            
    with open("AirQualityMarch.csv", "w") as f:
        writer = csv.writer(f, delimiter=";")
        for line in sorted_lines:
            split_line = line.split(";")
            writer.writerow(split_line)
    
# Purpose: write monthly responses files to a new directory called "monthly_responses",
# in the same location as AirQuality.csv, each using the name format "mm-yyyy.csv",
# including the header row of labels in each one.
# Example
#   Call: create_monthly_responses("AirQuality.csv")
#   Returns: nothing, but files such as monthly_responses/05-2004.csv exist containing
#            data matching responses from that month and year
def create_monthly_responses(filename):
    lines = get_file_contents(filename)
    while ";;;;;;;;;;;;;;;;\n" in lines:
        lines.remove(";;;;;;;;;;;;;;;;\n")
    mega_sorted_dict = {}

    #find mm-yyyy to add to dict as keys:
    for line in lines[1:]:
        if not line[3:10] in mega_sorted_dict:
            mega_sorted_dict.update({line[3:10].replace("/", "-"): []})

    #append list of lines to each dict key
    for line in lines[1:]:
        date_old = line[3:10]
        for i in list(mega_sorted_dict.keys()):
            if i.replace("-", "/") == date_old:
                mega_sorted_dict[i].append(line[:-1])

    #add header to beginning of each lst for each key
    for key in mega_sorted_dict:
        mega_sorted_dict[key].insert(0,lines[0][:-1])

    #create dir
    if not os.path.isdir("monthly_responses"):
        os.makedirs("monthly_responses")

    #create and populate files for each mm-yyyy
    for i in mega_sorted_dict.keys():
        with open("monthly_responses/"+str(i)+".csv", "w") as f:
            print(i)
            writer = csv.writer(f, delimiter=";")
            for lst in mega_sorted_dict[i]:
                split_line = lst.split(";")
                writer.writerow(split_line)