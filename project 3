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


DATA_PATH = "Health-Care/Data/"
CLEAN_DATA_PATH = "Health-Care/Clean-Data/"


### Problem Statement 10: Renaming dataset column acronyms (by Chilaka Nikhitha)
hospital_data = pd.read_csv(f"{DATA_PATH}hospitals.csv")
hospital_colrename_map = {
    hospital_data.columns[0]: "State/UT",
    "PHC": "Number of Primary Health Centers",
    "CHC": "Community Health Centers",
    "SDH": "Sub-District/Divisional Hospitals",
    "DHs": "District Hospitals"
}
hospital_data.rename(columns=hospital_colrename_map, inplace=True)
print(f"10] Renamed dataset:\n{hospital_data.head()}\n")


### Problem Statement 11: Function to create data uniformity (by Shabbir Ahmed Hasan)
def normalize_names(name: str) -> str:
    chars = []
    for word in name.split():
        chars.append(word.capitalize())
    name = " ".join(chars)
    return name.replace("*", "").replace("&", "and")

hospital_data["State/UT"] = hospital_data["State/UT"].apply(normalize_names)
print(f"11] Data after normalization for uniformity:\n{hospital_data.head()}\n")

hospital_data.to_csv(f"{CLEAN_DATA_PATH}all_hospitals.csv", index=False)


### Problem Statement 12: Analyze healthcare facility disparity (by Harshitha P)
census_data = pd.read_csv(f"{CLEAN_DATA_PATH}census.csv")
merged_hc = pd.merge(hospital_data, census_data, on="State/UT")

merged_hc["Beds per 10000"] = (merged_hc["HospitalBeds"].astype(float) / merged_hc["Population"].astype(float)) * 10000
merged_hc = merged_hc.sort_values(by="Beds per 10000", ascending=True)
national_avg = merged_hc["HospitalBeds"].astype(float).sum() / merged_hc["Population"].astype(float).sum() * 10000

plt.figure(figsize=(12, 8))
plt.barh(merged_hc["State/UT"], merged_hc["Beds per 10000"], color="skyblue")
plt.axvline(national_avg, color="red", linestyle="--", label="National Average")
plt.xlabel("Beds per 10,000 People")
plt.title("Hospital Beds per 10,000 People by State/UT")
plt.legend()
plt.show()

print("12] States/UTs with the least beds per 10,000 people:")
print(merged_hc.head(3)[["State/UT", "Beds per 10000"]])
print(f"-- Highly recommended to set up new hospital beds in the aforementioned States/UTs.\n")


### Problem Statement 13: Simplifying dataset with multiple headers (by Amrit Sutradhar)
govthosp_data = pd.read_csv(f"{DATA_PATH}government_hospitals.csv", header=[0, 1])
govthosp_rename_map = {
    "Unnamed: 0_level_1": "",
    "Unnamed: 2_level_0": "Rural hospitals",
    "Unnamed: 4_level_0": "Urban hospitals",
    "Unnamed: 5_level_1": ""
}
govthosp_data = govthosp_data.rename(columns=govthosp_rename_map)
print(f"13.1] Display multi-header dataset:\n{govthosp_data.head()}\n")

govthosp_required_map = {
    "State/UT": govthosp_data["States/UTs"],
    "Rural_Government_Hospitals": govthosp_data["Rural hospitals"]["No."],
    "Rural_Government_Beds": govthosp_data["Rural hospitals"]["Beds"],
    "Urban_Government_Hospitals": govthosp_data["Urban hospitals"]["No."],
    "Urban_Government_Beds": govthosp_data["Urban hospitals"]["Beds"],
    "Last_Updated": govthosp_data["As on"]
}
required_govthosp_data = pd.DataFrame(govthosp_required_map)
print(f"13.2] Simplified multi-header dataset:\n{required_govthosp_data.head()}\n")


### Problem Statement 14: Simplifying dataset with multiple headers (by Amrit Sutradhar)
def update_date(date: str) -> str:
    if date is not np.nan:
        valid = []
        for x in date.split("."):
            valid.append(x)
        return "-".join(valid[::-1])
    return np.nan
required_govthosp_data["Last_Updated"] = required_govthosp_data["Last_Updated"].apply(update_date)
print(f"14.1] Updating date:\n{required_govthosp_data.head()}\n")

required_govthosp_data["State/UT"] = required_govthosp_data["State/UT"].apply(normalize_names)
print(f"14.2] Updating State/UT (normalizing):\n{required_govthosp_data.head()}\n")

required_govthosp_data.to_csv(f"{CLEAN_DATA_PATH}government_hospital.csv", index=False)
