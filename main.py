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
import matplotlib.pyplot as plt
import seaborn as sns


DATA_PATH = "Health-Care/Data/"
CLEAN_DATA_PATH = "Health-Care/Clean-Data/"


### Problem Statement 15: State/UT for least beds based on their population (by Harshitha P)
census_data = pd.read_csv(f"{CLEAN_DATA_PATH}census.csv")
population_data = census_data.groupby(["State/UT"])["Population"].sum()

govthosp_data = pd.read_csv(f"{CLEAN_DATA_PATH}government_hospital.csv")
merged_gc = pd.merge(govthosp_data, population_data, on="State/UT")

merged_gc["Total_Beds"] = merged_gc["Rural_Government_Beds"].astype(float) + merged_gc["Urban_Government_Beds"].astype(float)
merged_gc["Beds_per_Capita"] = merged_gc["Total_Beds"].astype(float) / merged_gc["Population"].astype(float)
merged_gc = merged_gc.sort_values(by="Beds_per_Capita", ascending=True)

print("15] States/UTs with the least beds for their population:")
print(merged_gc.head(3)[["State/UT", "Beds_per_Capita"]])
print(f"-- Highly recommended to set up new government hospital beds in the aforementioned States/UTs.\n")


### Problem Statement 16: Visualize difference between expected and total hospital beds (by Chilaka Nikhitha)
hosp_data = pd.read_csv(f"{CLEAN_DATA_PATH}all_hospitals.csv")
merged_hc = pd.merge(hosp_data, population_data, on="State/UT")

merged_hc["ExpectedBeds"] = (3 * merged_hc["Population"].astype(float)) / 1000
merged_hc["DifferenceInBeds"] = (merged_hc["ExpectedBeds"].astype(float) - merged_hc["HospitalBeds"].astype(float))

national_data = {
    "State/UT": "National",
    "ExpectedBeds": merged_hc["ExpectedBeds"].sum(),
    "DifferenceInBeds": merged_hc["DifferenceInBeds"].sum()
}
merged_hc.loc[len(merged_hc)] = national_data
merged_hc = merged_hc.sort_values(by="DifferenceInBeds", ascending=True)

plt.figure(figsize=(10, 6))
plt.barh(merged_hc["State/UT"], merged_hc["DifferenceInBeds"], color="skyblue")
plt.xlabel("Difference in Beds")
plt.title("Difference between Expected and Available Hospital Beds by State/UT and National Level")
plt.grid(axis="x")
plt.show()


### Problem Statement 17: Hospitals required to meet the standards (by Shabbir Ahmed Hasan)
# reusing merged_gc : merged government hospital and population data
merged_gc["Total_Hospitals"] = merged_gc["Urban_Government_Hospitals"].astype(float) + merged_gc["Rural_Government_Hospitals"].astype(float)

merged_gc["WHO_Standards"] = (3 * merged_gc["Population"].astype(float)) / 1000
merged_gc["BedsGap"] = (merged_gc["WHO_Standards"].astype(float) - merged_gc["Total_Beds"].astype(float))

total_beds_sum = merged_gc["Total_Beds"].sum()
total_hospitals_sum = merged_gc["Total_Hospitals"].sum()
average_beds = total_beds_sum / total_hospitals_sum if total_hospitals_sum != 0 else pd.NA

merged_gc["Required_Hospitals"] = (merged_gc["BedsGap"] / average_beds).round().astype(int, errors="ignore")

plt.figure(figsize=(12, 8))
plt.bar(merged_gc["State/UT"], merged_gc["Required_Hospitals"], color="skyblue")
plt.title("Required Number of Government Hospitals to Meet WHO Standards")
plt.xlabel("State/Union Territory")
plt.ylabel("Number of Hospitals Required")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()


### Problem Statement 18: Assessment of Housing Quality and its Correlation with Demographic (by Amrit Sutradhar)
housing_data = pd.read_csv(f"{CLEAN_DATA_PATH}housing.csv")
merged_data = pd.merge(census_data, housing_data, on="District")
actionable_data = merged_data.drop(["State/UT", "District"], axis=1)
correlation_matrix = actionable_data.corr()

plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix")
plt.show()

plottable = actionable_data[["Young_and_Adult", "Middle_Aged", "Senior_Citizen",
                "Literate", "Male", "Female", "Households_Rural_Livable",
                "Households_Rural_Toilet_Premise",  "Households_Urban_Livable",
                "Households_Urban_Toilet_Premise"]]

# Multi-Axis plot
sns.pairplot(plottable, diag_kind="kde")
plt.show()

sns.scatterplot(plottable)
plt.show()
