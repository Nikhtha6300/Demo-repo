"""
Team Members:
- Shabbir Ahmed Hasan (22BTRCL139)
- Chilaka Nikhitha (22BTRCL042)
- Harshitha P (22BTRCL064)
- Amrit Sutradhar (22BTRCL014) : Leader

Typehinting, formatting, merging and finalization of this code
have been performed by Amrit Sutradhar.
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


"""
First we are solving the previous problem statements mentioned in Day1.
Then we continue with the problem statements mentioned in Day2.
This is done because we are required to have the solutions of Day1 for processing in Day2.
"""

PATH_TO_SAVE_FOLDER = "Health-Care/Clean-Data/"
PATH_TO_DATA_FOLDER = "Health-Care/Data/"

### Start of Day1

# Variables
relevant_census = [
    "State name", "District name", "Population", "Male", "Female",
    "Literate", "Male_Literate", "Female_Literate", "Rural_Households",
    "Urban_Households", "Households", "Age_Group_0_29", "Age_Group_30_49",
    "Age_Group_50", "Age not stated"
]
column_name_mapping_census = {
    "State name": "State/UT",
    "District name": "District",
    "Male_Literate": "Literate_Male",
    "Female_Literate": "Literate_Female",
    "Rural_Households": "Households_Rural",
    "Urban_Households": "Households_Urban",
    "Age_Group_0_29": "Young_and_Adult",
    "Age_Group_30_49": "Middle_Aged",
    "Age_Group_50": "Senior_Citizen",
    "Age not stated": "Age_Not_Stated"
}
telangana_districts = [
    "Adilabad", "Nizamabad", "Karimnagar", "Medak", "Hyderabad",
    "Rangareddy", "Mahbubnagar", "Nalgonda", "Warangal", "Khammam"
]
laddakh_districts = ["Leh(Ladakh)", "Kargil"]

# Functions
def rename_and_update(row: pd.Series) -> pd.Series:
    """
        Combined Problem Statement 3 and Problem Statement 4
        together into one single function
    """
    if row["District"] in telangana_districts:             # Problem Statement 4
        row["State/UT"] = "Telangana"
    elif row["District"] in laddakh_districts:
        row["State/UT"] = "Laddakh"
    if row["State/UT"] not in ["Laddakh", "Telangana"]:    # Problem Statement 3
        formatted_words = []
        for word in row["State/UT"].split():
            if word.lower() == "and":
                formatted_words.append(word.lower())
            else:
                formatted_words.append(word.capitalize())
        row["State/UT"] = " ".join(formatted_words)
    return row

# Filtering
census_data = pd.read_csv(f"{PATH_TO_DATA_FOLDER}census_2011.csv")

filtered_census = census_data[relevant_census]
filtered_census = filtered_census.rename(columns=column_name_mapping_census)
filtered_census = filtered_census.apply(rename_and_update, axis=1)


### End of Day 1
# ----------------
### Start of Day 2


### Problem Statement 5: Finding percentage of missing data (by Amrit Sutradhar)
missing_pre_update = (filtered_census.isnull().sum()/len(filtered_census))*100
missing_pre_update = missing_pre_update.reset_index()
missing_pre_update.columns = ["Column", "Missing_Pre_Update"]

# Adding new calculated columns
filtered_census["Population"] = filtered_census["Male"] + filtered_census["Female"]
filtered_census["Literate"] = filtered_census["Literate_Male"] + filtered_census["Literate_Female"]
filtered_census["Households"] = filtered_census["Households_Rural"] + filtered_census["Households_Urban"]

filtered_census["Young_and_Adult"].fillna(filtered_census["Young_and_Adult"].mean(), inplace=True)
filtered_census["Middle_Aged"].fillna(filtered_census["Middle_Aged"].mean(), inplace=True)
filtered_census["Senior_Citizen"].fillna(filtered_census["Senior_Citizen"].mean(), inplace=True)

filtered_census.drop(["Age_Not_Stated", "Households_Rural", "Households_Urban"], axis=1, inplace=True)

missing_post_update = (filtered_census.isnull().sum()/len(filtered_census))*100
missing_post_update = missing_post_update.reset_index()
missing_post_update.columns = ["Column", "Missing_Post_Update"]

missing_result = pd.merge(missing_pre_update, missing_post_update, on="Column", suffixes=("_Before", "_After"))
missing_result["Missing_Pre_Update"] = missing_result["Missing_Pre_Update"].astype(float)
missing_result["Missing_Post_Update"] = missing_result["Missing_Post_Update"].astype(float)

sns.set(style="whitegrid")
fig, axis = plt.subplots(figsize=(10, 6))
sns.barplot(x="Column", y="Missing_Pre_Update", data=missing_result, alpha=0.5, label="Before")
sns.barplot(x="Column", y="Missing_Post_Update", data=missing_result, alpha=0.5, label="After")
axis.set_title("Percentage of Missing Data Before and After Data Filling")
axis.set_ylabel("Percentage of Missing Data")
axis.legend()
plt.xticks(rotation=45)
plt.show()


### Problem Statement 6: Saving the data (by Shabbir Ahmed Hasan)
filtered_census.to_csv(f"{PATH_TO_SAVE_FOLDER}census.csv", index=False)


### Problem Statement 7: Processing (Filtering and Merging) relevant housing and census data (by Harshitha P and Amrit Sutradhar)
## Individual work of Harshitha P starts here:
housing_data = pd.read_csv(f"{PATH_TO_DATA_FOLDER}housing.csv")
relevant_housing = [
    "District Name", "Rural/Urban", "Total Number of households",
    "Total Number of Livable", "Total Number of Dilapidated", "Latrine_premise"
]

filtered_housing = housing_data[relevant_housing]
census_data.rename(columns={"District name": "District Name"}, inplace=True)

merged_data = pd.merge(housing_data, census_data, on="District Name") # Merge both data on common District Name

# Calculate absolute values for Total Number of Dilapidated and Latrine_premise for rural areas
merged_data["Absolute Dilapidated Rural"] = merged_data["Total Number of households"] * (merged_data["Total Number of Dilapidated"] / 100)
merged_data["Absolute Latrine_premise Rural"] = merged_data["Total Number of households"] * (merged_data["Latrine_premise"] / 100)

# Calculate absolute values for Total Number of Dilapidated and Latrine_premise for urban areas
merged_data["Absolute Dilapidated Urban"] = merged_data["Total Number of households"] * ((100 - merged_data["Total Number of Livable"]) / 100)
merged_data["Absolute Latrine_premise Urban"] = merged_data["Total Number of households"] * ((100 - merged_data["Latrine_premise"]) / 100)

## Individual work of Harshitha P ends here.
## Combined work of Harshitha P and Amrit Sutradhar starts here:
column_name_mapping_housing = {
    "District Name": "District",
    "Rural/Urban": "Households_Rural_Urban",
    "Total Number of households": "Households_Total",
    "Total Number of Livable": "Households_Livable",
    "Total Number of Dilapidated": "Households_Dilapidated",
    "Latrine_premise": "Households_Toilet_Premise"
}
filtered_housing = filtered_housing.rename(columns=column_name_mapping_housing)
# Using pivot_table to separate Rural, Urban and Total from Rural/Urban column
pivoted_housing = filtered_housing.pivot_table(index="District", columns="Households_Rural_Urban", values=["Households_Total", "Households_Livable", "Households_Dilapidated", "Households_Toilet_Premise"], aggfunc="first")

updated_columns = {
    "District": pivoted_housing.index,
    "Households_Rural": pivoted_housing["Households_Total"]["Rural"].values,
    "Households_Rural_Livable": pivoted_housing["Households_Livable"]["Rural"].values,
    "Households_Rural_Dilapidated": pivoted_housing["Households_Dilapidated"]["Rural"].values,
    "Households_Rural_Toilet_Premise": pivoted_housing["Households_Toilet_Premise"]["Rural"].values,
    "Households_Urban": pivoted_housing["Households_Total"]["Urban"].values,
    "Households_Urban_Livable": pivoted_housing["Households_Livable"]["Urban"].values,
    "Households_Urban_Dilapidated": pivoted_housing["Households_Dilapidated"]["Urban"].values,
    "Households_Urban_Toilet_Premise": pivoted_housing["Households_Toilet_Premise"]["Urban"].values,
    "Households_Total": pivoted_housing["Households_Total"]["Total"].values,
    "Households_Total_Livable": pivoted_housing["Households_Livable"]["Total"].values,
    "Households_Total_Dilapidated": pivoted_housing["Households_Dilapidated"]["Total"].values,
    "Households_Total_Toilet_Premise": pivoted_housing["Households_Toilet_Premise"]["Total"].values,
}
updated_filtered_housing = pd.DataFrame(updated_columns)
required_housing_columns = [
    "District", "Households_Rural", "Households_Rural_Livable",
    "Households_Rural_Dilapidated", "Households_Rural_Toilet_Premise",
    "Households_Urban", "Households_Urban_Livable", "Households_Urban_Dilapidated",
    "Households_Urban_Toilet_Premise"
]
required_filtered_housing = updated_filtered_housing[required_housing_columns]

required_filtered_housing.to_csv(f"{PATH_TO_SAVE_FOLDER}housing.csv", index=False)
## Combined work of Harshitha P and Amrit Sutradhar ends here.


### Problem Statement 8: Visualizing filtered data (by Chilaka Nikhitha)
plt.figure(figsize=(10, 6))
plt.plot(updated_filtered_housing["District"].values, updated_filtered_housing["Households_Total_Livable"].values, color="skyblue")
plt.title("Number of Households for 100 people by District")
plt.xlabel("District")
frame = plt.gca()
frame.get_xaxis().set_visible(False)    # Disable showing of District names
plt.ylabel("Households per 100 people")
plt.xticks(rotation=45)
plt.show()

# Visualize Percentage of households that have toilet(s) in premise
plt.figure(figsize=(10, 6))
plt.plot(updated_filtered_housing["District"].values, updated_filtered_housing["Households_Total_Toilet_Premise"].values, color="lightgreen")
plt.title("Percentage of Households with Toilet(s) by District")
plt.xlabel("District")
frame = plt.gca()
frame.get_xaxis().set_visible(False)    # Disable showing of District names
plt.ylabel("Percentage of Households with Toilet(s)")
plt.xticks(rotation=45)
plt.show()

# Calculate Urban to Rural population ratio
updated_filtered_housing["Urban_to_Rural_Ratio"] = updated_filtered_housing["Households_Urban_Livable"] / updated_filtered_housing["Households_Rural_Livable"]

# Visualize Urban to Rural population ratio
plt.figure(figsize=(10, 6))
plt.plot(updated_filtered_housing["District"].values, updated_filtered_housing["Urban_to_Rural_Ratio"].values, color="orange")
plt.title("Urban to Rural Population Ratio by District")
plt.xlabel("District")
frame = plt.gca()
frame.get_xaxis().set_visible(False)    # Disable showing of District names
plt.ylabel("Urban to Rural Population Ratio")
plt.xticks(rotation=45)
plt.show()


### Problem Statement 9: Calculating inconsistency in datasets (by Shabbir Ahmed Hasan)
try:
    merged_data["Households_Rural_Diff"] = (merged_data["Rural_Households"] - merged_data["Total Number of households"]) / merged_data["Rural_Households"] * 100
    merged_data["Households_Urban_Diff"] = (merged_data["Urban_Households"] - merged_data["Total Number of households"]) / merged_data["Urban_Households"] * 100

    major_difference_districts = merged_data[(abs(merged_data["Households_Rural_Diff"]) > 10) | (abs(merged_data["Households_Urban_Diff"]) > 10)]
    major_difference_district_names = major_difference_districts["District Name"]

    print("\nDistricts with major differences in household counts:")
    print(major_difference_district_names)
except KeyError:
    pass
print("the names of the districts where a major difference is found in the data:")
print(housing_data["District Name"].head())
