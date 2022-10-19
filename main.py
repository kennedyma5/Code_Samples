# Task: Output the following information for each school in Virginia as a csv.
# School_Name
# School_District
# School_Address
# School_Phone_Number
# Principal_FName
# Principal_LName
# Grades
# School_Type
# Super_Phone_Number
# Super_FName
# Super_LName

import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://www.va-doeapp.com/PublicSchoolsByDivisions.aspx?w=true"


def get_school_data(url):
    # Takes in the website url for school and district data.
    # Returns two lists, one contianing information for each school and the
    # other containing information for each district.

    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')

    school_data = []
    district_data = []
    removed_text = ["Principal", "Grades", "Type", "ELEMENTARY", "MIDDLE", "HIGH", "Website",
                    "COMBINED", "GOVERNORS", "SPECIAL EDUCATION", "ALTERNATIVE", "PRESCHOOL",
                    "CHARTER"]
    website_data = soup.find_all('td')

    for element in website_data:
        sub_data = []
        if "Public Schools" in element.get_text():
            for sub_element in element:
                try:
                    text = sub_element.get_text()
                    text = text.strip()
                    if len(text) > 1:
                        sub_data.append(text)
                except:
                    continue
            district_data.append(" ".join(sub_data))
            school_data.append(" ".join(sub_data))
        elif "Superintendent:" in element.get_text():
            for sub_element in element:
                try:
                    text = sub_element.get_text()
                    text = text.strip()
                    if len(text) > 1:
                        sub_data.append(text)
                except:
                    continue
            if len(sub_data) > 1:
                district_data.append(" ".join(sub_data))
        else:
            if element.get_text()[:5] != "Stree" and element.get_text()[:5] != "Maili":
                for sub_element in element:
                    try:
                        text = sub_element.get_text()
                        text = text.strip()
                        for item in removed_text:
                            text = text.replace(item, "")
                        if len(text) > 1:
                            sub_data.append(text)
                    except:
                        continue
            if len(sub_data) > 0:
                school_data.append(" ".join(sub_data))
    return (school_data, district_data)


def clean_school_df(original_df):
    columns = ['School_Name', 'School_District', "School_Address", "School_Phone_Number",
               'Principal_FName', 'Principal_LName', 'Grades', 'School_Type']

    clean_df = pd.DataFrame(columns=[columns])

    School_Name = School_District = School_Address = School_Phone_Number = \
        Principal_FName = Principal_LName = Grades = School_Type = "NaN"

    for index, row in original_df.iterrows():
        text = original_df.at[index, 'column']

        data = row["column"].split()
        if len(data) > 6:
            School_Phone_Number = data[-1]
            split_index = data.index("address:")
            School_Address = " ".join(data[(split_index + 1):-1])
            School_Name = " ".join(data[:(split_index - 1)])
        elif len(data) == 1 and "-" in text:
            Grades = text
        elif len(data) == 1 and "PK" in text:
            Grades = text
        elif len(data) > 1 and "Public" in text:
            School_District = text
        elif len(data) > 1:
            name = []
            for item in data:
                if "." not in item and len(item) > 1:
                    name.append(item)
            Principal_FName = " ".join(name[0:-1])
            Principal_LName = name[-1]
        else:
            School_Type = text
            entry = [School_Name, School_District, School_Address, School_Phone_Number,
                     Principal_FName, Principal_LName, Grades, School_Type]
            clean_df.loc[len(clean_df)] = entry
    return clean_df


def clean_district_df(original_df):
    columns = ['School_District', "Super_Phone_Number", 'Super_FName', 'Super_LName']

    clean_df = pd.DataFrame(columns=[columns])

    School_District = Super_Phone_Number = Super_FName = Super_LName = "NaN"

    for index, row in original_df.iterrows():
        text = original_df.at[index, 'column']

        data = row["column"].split()
        if len(data) > 1 and "Public" in text:
            School_District = text
        else:
            phone_split_index = data.index("Phone:")
            Super_Phone_Number = data[(phone_split_index + 1)]

            raw_name = data[1:(phone_split_index)]
            name = []
            for item in raw_name:
                if "." not in item and len(item) > 1:
                    name.append(item)
            Super_FName = " ".join(name[0:-1])
            Super_LName = name[-1]

            entry = [School_District, Super_Phone_Number, Super_FName, Super_LName]
            clean_df.loc[len(clean_df)] = entry
    return clean_df


school_data, district_data = get_school_data(url)

school_df = clean_school_df(pd.DataFrame(school_data, columns=["column"]))
district_df = clean_district_df(pd.DataFrame(district_data, columns=["column"]))

clean_df = school_df.merge(district_df, how='left')
clean_df.to_csv('VA_School_Data.csv')
