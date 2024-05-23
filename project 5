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


DATA_PATH = "Health-Care/Data/"
CLEAN_DATA_PATH = "Health-Care/Clean-Data/"


### Problem Statement 19: Evaluation of Ayush Hospitals across different demographics (by Harshitha P)
ayush_data=pd.read_csv(f"{DATA_PATH}AYUSHHospitals.csv", header=[0, 1])
rename_level_zero = {
    "Unnamed: 3_level_0": "Number of Hospitals",
    "Unnamed: 4_level_0": "Number of Hospitals",
    "Unnamed: 5_level_0": "Number of Hospitals",
    "Unnamed: 7_level_0": "Number of Beds",
    "Unnamed: 8_level_0": "Number of Beds",
    "Unnamed: 9_level_0": "Number of Beds",
}
rename_level_one = {"Unnamed: 1_level_1": ""}
ayush_data.rename(columns=rename_level_zero, level=0, inplace=True)
ayush_data.rename(columns=rename_level_one, level=1, inplace=True)

ayush_data.sort_index(axis=1, inplace=True)
ayush_data.drop("Srl no.", axis=1, inplace=True)
ayush_data.drop(index=ayush_data.index[0], inplace=True)
ayush_data.rename(columns={"State / UT": "State/UT"}, inplace=True)

ayush_data = pd.DataFrame({
    "State/UT": ayush_data["State/UT"],
    "Hospital_Govt": ayush_data["Number of Hospitals"]["Govt."],
    "Hospital_Local": ayush_data["Number of Hospitals"]["Local Body"],
    "Hospital_Other": ayush_data["Number of Hospitals"]["Others"],
    "Hospital_Total": ayush_data["Number of Hospitals"]["Total"],
    "Bed_Govt": ayush_data["Number of Beds"]["Govt."],
    "Bed_Local": ayush_data["Number of Beds"]["Local Body"],
    "Bed_Other": ayush_data["Number of Beds"]["Others"],
    "Bed_Total": ayush_data["Number of Beds"]["Total"],
})
ayush_data = ayush_data.drop(ayush_data.tail(5).index)
census_data = pd.read_csv(f"{CLEAN_DATA_PATH}census.csv")
aggregations = {
    "Population": "sum",
    "Male": "sum",
    "Female": "sum",
    "Literate": "sum",
    "Literate_Male": "sum",
    "Literate_Female": "sum",
    "Households": "sum",
    "Young_and_Adult": "sum",
    "Middle_Aged": "sum",
    "Senior_Citizen": "sum"
}
aggregated_census = census_data.groupby("State/UT").agg(aggregations)
merged_ayush = pd.merge(ayush_data, aggregated_census, on="State/UT", how="left")

merged_ayush["Hospital_Ratio"] = merged_ayush["Hospital_Total"].astype(float) / merged_ayush["Population"].astype(float)
# List of socio-economic strata to compare
strata = ["Population", "Literate", "Households", "Young_and_Adult", "Middle_Aged", "Senior_Citizen"]
num_plots = len(strata)
num_cols = 3
num_rows = (num_plots + num_cols - 1) // num_cols

plt.figure(figsize=(20, 20))
for i, stratum in enumerate(strata, start=1):
    plt.subplot(num_rows, num_cols, i)
    sns.barplot(x=merged_ayush.index, y=merged_ayush[stratum], color="navy")
    plt.title(stratum)
    plt.xlabel("State/UT")
    plt.ylabel("Value")
plt.tight_layout()
plt.show()

merged_ayush_melted = merged_ayush.melt(id_vars="State/UT", var_name="Stratum", value_name="Value")
fig, axs = plt.subplots(nrows=num_rows, ncols=num_cols, figsize=(20, 20))

for i, stratum in enumerate(strata):
    row = i // num_cols
    col = i % num_cols
    sns.barplot(data=merged_ayush_melted, x="State/UT", y="Value", hue="Stratum", ax=axs[row, col])
    axs[row, col].set_title(stratum)
    axs[row, col].set_xlabel("State/UT")
    axs[row, col].set_ylabel("Value")
# Remove unused subplots
for i in range(num_plots, num_rows * num_cols):
    fig.delaxes(axs.flatten()[i])
plt.tight_layout()
plt.show()


### Problem Statement 20: Population density analysis (by Harshitha P)
approx_area_km2 = 100
# Calculate population density (population per square kilometer)
census_data["Population Density"] = census_data["Population"] / approx_area_km2
# Identify the most densely populated districts in each state
most_densely_populated = census_data.groupby("State/UT").apply(lambda x: x.nlargest(1, "Population Density")).reset_index(drop=True)

# Visualize population density using seaborn
plt.figure(figsize=(10, 6))
sns.barplot(data=most_densely_populated, x="District", y="Population Density", hue="State/UT")
plt.xlabel("District")
plt.ylabel("Population Density (per sq. km)")
plt.title("Most Densely Populated Districts in Each State")
plt.xticks(rotation=45, ha="right")
plt.legend(title="State", loc="upper center", bbox_to_anchor=(0.5, -0.3), ncol=3, prop={"size": 7})
plt.tight_layout()
plt.show()


### Problem Statement 21: Gender Literacy gap analysis (by Shabbir Ahmed)
census_data["Literacy_Gap"] = census_data["Literate_Male"] - census_data["Literate_Female"]
mean_gap_by_state = census_data.groupby("State/UT")["Literacy_Gap"].mean().reset_index()

plt.figure(figsize=(12, 6))
sns.barplot(data=mean_gap_by_state, x="State/UT", y="Literacy_Gap", hue="State/UT", palette="viridis", dodge=False)
plt.xticks(rotation=90)
plt.title("Mean Literacy Gap between Males and Females Across States/UT")
plt.xlabel("State/UT")
plt.ylabel("Mean Literacy Gap")
plt.legend([],[], frameon=False)
plt.show()


### Problem Statement 22: Urban vs Rural healthcare accessibility (by Shabbir Ahmed)
hosp_data = pd.read_csv(f"{CLEAN_DATA_PATH}all_hospitals.csv")
govthosp_data = pd.read_csv(f"{CLEAN_DATA_PATH}government_hospital.csv")
# Remove All India data
hosp_data = hosp_data[hosp_data["State/UT"] != "All India"]
govthosp_data = govthosp_data[govthosp_data["State/UT"] != "India"]

merged_hospgovt = pd.merge(hosp_data, govthosp_data, on="State/UT", suffixes=("_hospital", "_gov_hospital"))

def categorize_area(row):
    urban_cols = ["State/UT", "Urban_Government_Hospitals", "Urban_Government_Beds"]
    rural_cols = ["State/UT", "Rural_Government_Hospitals", "Rural_Government_Beds"]
    if row["State/UT"] in ["Delhi", "Chandigarh", "Puducherry", "Dadra & Nagar Haveli", "Daman & Diu", "Lakshadweep"]:
        return pd.Series([row[col] for col in urban_cols], index=urban_cols)
    else:
        return pd.Series([row[col] for col in rural_cols], index=rural_cols)

urban_df = merged_hospgovt.apply(categorize_area, axis=1)
rural_df = merged_hospgovt.apply(categorize_area, axis=1)

plt.figure(figsize=(12, 8))
sns.scatterplot(data=urban_df, x="Urban_Government_Hospitals", y="Urban_Government_Beds", color="blue", label="Urban")
sns.scatterplot(data=rural_df, x="Rural_Government_Hospitals", y="Rural_Government_Beds", color="red", label="Rural")
plt.title("Urban vs. Rural Healthcare Accessibility")
plt.xlabel("Number of Hospitals")
plt.ylabel("Number of Beds")
plt.legend()
plt.show()


### Problem Statement 23: Ayush Hospitals distrubution analysis (by Chilaka Nikhitha)
# Plotting using previously filtered Ayush Hospitals data
plt.figure(figsize=(11, 4))

plt.subplot(1, 2, 1)
sns.barplot(data=ayush_data, x="State/UT", y="Hospital_Total", palette="viridis", hue="State/UT", legend=False)
plt.title("Number of AYUSH Hospitals by State")
plt.xlabel("State")
plt.ylabel("Number of AYUSH Hospitals")
plt.xticks(rotation=90, ha="right")

plt.subplot(1, 2, 2)
sns.barplot(data=ayush_data, x="State/UT", y="Bed_Total", palette="viridis", hue="State/UT", legend=False)
plt.title("Number of AYUSH Beds by State")
plt.xlabel("State")
plt.ylabel("Number of AYUSH Beds")
plt.xticks(rotation=90, ha="right")

plt.tight_layout()
plt.show()


### Problem Statement 24: Analysis of housing conditions across districts (by Chilaka Nikhitha)
housing_data = pd.read_csv(f"{CLEAN_DATA_PATH}housing.csv")

housing_data["Livability_Score"] = ((housing_data["Households_Rural_Livable"] + housing_data["Households_Urban_Livable"]) / (housing_data["Households_Rural"] + housing_data["Households_Urban"])) * 100
housing_data["Latrine_Presence"] = housing_data["Households_Rural_Toilet_Premise"] + housing_data["Households_Urban_Toilet_Premise"]

plt.figure(figsize=(10, 6))
sns.barplot(data=housing_data, x="District", y="Livability_Score", palette="coolwarm", hue="Latrine_Presence", legend=False)
plt.title("Average Livability Score by District")
plt.xlabel("District")
plt.ylabel("Average Livability Score")
frame = plt.gca()
frame.get_xaxis().set_visible(False)    # Disable showing of District names
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(data=housing_data, x="Latrine_Presence", palette="coolwarm", hue="Latrine_Presence", legend=False)
plt.title("Presence of Latrines by District")
plt.xlabel("Latrine Availability")
plt.ylabel("Count")
frame = plt.gca()
frame.get_xaxis().set_visible(False)    # Disable showing of District names
plt.tight_layout()
plt.show()


### Problem Statement 25: Hospital beds per 1000 people and its visualization (by Amrit Sutradhar)
population_data = census_data.groupby("State/UT")["Population"].sum().reset_index()

merged_hpop = pd.merge(hosp_data, population_data, on="State/UT")
merged_hpop["Beds_Per_1000"] = (merged_hpop["HospitalBeds"].astype(float) / merged_hpop["Population"].astype(float)) * 1000

print("State/UT with under-allocation of resources:")
print(merged_hpop[["State/UT", "Beds_Per_1000"]].loc[merged_hpop["Beds_Per_1000"].astype(float) < 1.0], "\n")
print("State/UT with over-allocation of resources:")
print(merged_hpop[["State/UT", "Beds_Per_1000"]].loc[merged_hpop["Beds_Per_1000"].astype(float) > 2.0], "\n")

palette = ["red" if x > 2.0 else "yellow" if x < 1.0 else "grey" for x in merged_hpop["Beds_Per_1000"]]

sns.barplot(x=merged_hpop["State/UT"], y=merged_hpop["Beds_Per_1000"], hue=merged_hpop["State/UT"], palette=palette, legend=False)
plt.xticks(rotation=90)
plt.show()


### Problem Statement 26: Correlation between population metrics and beds per capita (by Amrit Sutradhar)
required_census = [
    "Population", "Male", "Female", "Literate", "Literate_Male", "Literate_Female",
    "Households", "Young_and_Adult", "Middle_Aged", "Senior_Citizen"
]
grouped_census = census_data.groupby("State/UT")[required_census].sum().reset_index()

merged_hc = pd.merge(hosp_data[["State/UT", "HospitalBeds"]], grouped_census, on="State/UT")
merged_hc["Beds_Per_Capita"] = merged_hc["HospitalBeds"].astype(float) / merged_hc["Population"].astype(float)

capita_correlation = merged_hc.drop("State/UT", axis=1).corr()["Beds_Per_Capita"]

sns.barplot(x=capita_correlation.index, y=capita_correlation.values)
plt.xticks(rotation=90)
plt.show()
